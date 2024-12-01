import os

# !pip install torch
import torch

# !pip install transformers
from transformers import AutoProcessor, AutoModelForVision2Seq, AutoTokenizer
from huggingface_hub import login

# !pip install langchain
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# !pip install langchain-huggingface
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

# !pip install langgraph
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory

# !pip install python-dotenv
from dotenv import load_dotenv

load_dotenv()

login(token = os.environ["HUGGINGFACE_API_TOKEN"])

class VLMHandler:
    def __init__(self, prompt= None,  model_id = "HuggingFaceTB/SmolVLM-Instruct", DEVICE = "cuda", max_new_tokens = 500) -> None:
        

        # Initialize processor and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            _attn_implementation="eager" # "flash_attention_2" if DEVICE == "cuda" else "eager",
        ).to(DEVICE)

        self.DEVICE = DEVICE
        self.max_new_tokens = max_new_tokens

        if prompt != None:
            self._update_prompt(prompt)
        else:
            self.prompt = SystemMessage(content=[{"type": "text", "text": "You are a personal assistant. Help the user with tasks like answering questions, scheduling, reminders, and analyzing images. Be polite, concise, and efficient."}])

        # Monitor first call to the chat bot
        self.start_flag = False

        self.memory = SQLChatMessageHistory(
            session_id='foo', connection_string='sqlite:///memory.db'
        )

        self.memory.add_message(self.prompt)

    def _update_prompt(self, prompt):
        ## Call when initialize the chatbot class
        self.prompt = SystemMessage(content=[{"type": "text", "text": prompt+". Limit your responses to 100 words."}])
        
    # Define the function that calls the model
    def call_model(self, messages, images):
        """
        A function that calls the LLM model and formats the output properly.

        Args:
            messages (list): A list of messages.
            images (list): A list of images (PIL Images) to be processed by the chatbot.

        Returns:
            dict: A dictionary with a single key "messages" containing the response as a list of messages.
        """


        if len(images) == 0:
            inputs = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
            inputs = inputs.to(self.DEVICE)
            generated_ids = self.model.generate(inputs, max_new_tokens=self.max_new_tokens)
            generated_text = self.tokenizer.decode(generated_ids[0])

        else:
            prompt = self.processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = self.processor(text=prompt, images=images, return_tensors="pt")
            inputs = inputs.to(self.DEVICE)
            # Generate outputs

            generated_ids = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens)
            generated_text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True,
            )[0]

        # Generate outputs
        generated_text = self.extract_last_assistant_message(generated_text)
        return generated_text 

    def get_response(self, message="hi", images = [], rag_context = "", session_id="random123", max_new_tokens=256):
        """
        Gets a response from the chatbot given a user's message and context.

        Args:
            message (str): The user's message.
            images (list): A list of images (PIL Images) to be processed by the chatbot.
            rag_context (str): The context from the RAG model.
            session_id (str): The unique session ID for the conversation.
            max_new_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The response from the chatbot.
        """
        config = {"configurable": {"thread_id": session_id}}
        # message += " \nSales Assistant: "
        input_message = []
        if rag_context != "":
            input_message.append(SystemMessage(content = {"text": "Additional context: " + rag_context}))

        # if images != []:
        #     messages = [{"type": "image"}] * len(images)
        #     messages.append({"type": "text", "text": message})
        # else:
        messages = [{"type": "text", "text": message}]
        
        if (images != []):
            print("shape : ", images[0].size)
        
        input_message.append(HumanMessage(content = messages))

        self.memory.add_messages(input_message)

        messages = self.get_all_messages()

        if len(images) > 0:
            messages[len(messages)-1].content = [{"type" : "image"}]*len(images) + messages[len(messages)-1].content

        # print("Input messages : ", messages)
        temp_messages = self._get_recent_messages(messages)
        # print("temp_messages : ", temp_messages)

        output_messages = []
        for message in messages:
            output_messages.append(self._to_chatml_format(message))

        output = self.call_model(output_messages, images)
        # print("output : ", output)
        output_message = AIMessage(content=[{ "type": "text", "text": output}])

        self.memory.add_message(output_message)

        return output_message.content[0]["text"]

    def get_all_messages(self):
        """
        Retrieve all stored messages from the workflow's memory.

        Args:
            session_id (str): The unique session ID for the conversation.

        Returns:
            list: A list of all messages in the session.
        """
        # Fetch the current state from memory
        try:
            state = self.memory.get_messages()
            return state
            # if state:
            #     return state  # Return all stored messages
            # else:
            # return []  # If no messages found, return empty list
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
            

    def _to_chatml_format(self, message: BaseMessage) -> dict:
        """Convert LangChain message to ChatML format."""

        if isinstance(message, SystemMessage):
            role = "system"
        elif isinstance(message, AIMessage):
            role = "assistant"
        elif isinstance(message, HumanMessage):
            role = "user"
        else:
            raise ValueError(f"Unknown message type: {type(message)}")

        return {"role": role, "content": message.content}


    def _get_recent_messages(self, messages):        
        """
        Trims and formats the list of messages to keep the most recent ones based on token count.

        This function processes the given list of messages, trimming it to retain only the most
        recent messages that fit within the specified maximum token count. The trimming strategy
        starts and ends with specified message types, and ensures inclusion of system messages
        if present in the original history. The trimmed messages are then converted to a specific
        format and returned.

        Args:
            messages (list): A list of messages to be processed.

        Returns:
            list: A list of formatted messages after trimming based on token count.
        """
        message_trim = trim_messages(
            messages,
            # Keep the last <= n_count tokens of the messages.
            strategy="last",
            # Remember to adjust based on your model
            # or else pass a custom token_encoder
            token_counter=len, #ChatOpenAI(model="gpt-4o"),
            # Most chat models expect that chat history starts with either:
            # (1) a HumanMessage or
            # (2) a SystemMessage followed by a HumanMessage
            # Remember to adjust based on the desired conversation
            # length
            max_tokens=200,
            # Most chat models expect that chat history starts with either:
            # (1) a HumanMessage or
            # (2) a SystemMessage followed by a HumanMessage
            start_on="human",
            # Most chat models expect that chat history ends with either:
            # (1) a HumanMessage or
            # (2) a ToolMessage
            end_on=("human", "tool"),
            # Usually, we want to keep the SystemMessage
            # if it's present in the original history.
            # The SystemMessage has special instructions for the model.
            include_system=True,
            # allow_partial=False,
        )

        output_messages = []
        for message in message_trim:
            output_messages.append(self._to_chatml_format(message))
        
        return output_messages


    def extract_last_assistant_message(self, conversation):
        # Split by the assistant marker
        """
        Extract the last assistant message from the conversation.

        Args:
            conversation (str): The conversation to extract from.

        Returns:
            str: The last assistant message, or None if none was found.
        """
        assistant_start = conversation.rfind("Assistant: ") + len("Assistant: ")
        if assistant_start == -1:
            return None  # No assistant message found
        
        # Extract until the next marker or end of text
        assistant_end = conversation.find("<end_of_utterance>", assistant_start)
        if assistant_end == -1:
            assistant_message = conversation[assistant_start:]  # Extract until the end of text
        else:
            assistant_message = conversation[assistant_start:assistant_end]

        return assistant_message.strip()
    
    def clear_memory(self):
        self.memory.clear()

if __name__ == "__main__":
    

    vlm = VLMHandler()
    while True:
        message = input(">: ")
        if message == "exit":
            break

        print("\n Assistant: " + vlm.get_response(message=message))

    print("All messages: " + str(vlm.get_all_messages()))