# !pip install torch
import torch

# !pip install transformers
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, LlamaTokenizer, LlamaForCausalLM
from huggingface_hub import login

# !pip install langchain
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# !pip install langchain-huggingface
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

# !pip install langgraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
## langraph is useful for storing the conversation



login(token = "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")

class LLMHandler:
    def __init__(self, model_id = "meta-llama/Llama-3.2-3B-Instruct") -> None:
        
                
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        # Set pad_token to eos_token
        # tokenizer.pad_token = tokenizer.eos_token

        # Define the model
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        tokenizer.add_special_tokens({'pad_token': '<pad>'})
        model.resize_token_embeddings(len(tokenizer))
        model.config.pad_token_id = tokenizer.pad_token_id


        # Load the model
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=256,
        )
        # Reference: https://huggingface.co/blog/langchain
        llm = HuggingFacePipeline(pipeline=pipe)

        # reference : https://api.python.langchain.com/en/latest/_modules/langchain_community/chat_models/huggingface.html#ChatHuggingFace
        self.llm = ChatHuggingFace(llm=llm, model_id=model_id, tokenizer=tokenizer)
        
        # Reference: https://python.langchain.com/docs/tutorials/chatbot/
        # Define a new graph
        self.workflow = StateGraph(state_schema=MessagesState)

        # Define the (single) node in the graph
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)

        # Add 
        # Inmemory storage: reference: https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.MemorySaver
        self.memory = MemorySaver()
        
        # For persistent memory check 

        # Compile the graph
        self.app = self.workflow.compile(checkpointer=self.memory)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                # SystemMessage(content = "You are a Sales Assistant. Only provide responses when the Human asks questions or says something. Do not simulate Human inputs or assume details not provided by the user."),
                SystemMessage(content= "You are Jarvis from Iron man. You will responses accordingly.",),
                MessagesPlaceholder(variable_name="messages"),
                # HumanMessage(variable_name="messages")
            ]
        )

    def updade_prompt(self, prompt):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                # SystemMessage(content = "You are a Sales Assistant. Only provide responses when the Human asks questions or says something. Do not simulate Human inputs or assume details not provided by the user."),
                SystemMessage(content= prompt+". Limit your responses to 100 words.",),
                MessagesPlaceholder(variable_name="messages"),
                # HumanMessage(variable_name="messages")
            ]
        )
    # Define the function that calls the model
    def call_model(self,state: MessagesState):
        """
        A function that calls the LLM model and formats the output properly.

        Args:
            state (MessagesState): The current state of the conversation.

        Returns:
            dict: A dictionary with a single key "messages" containing the response as a list of messages.
        """
        chain = self.prompt | self.llm
        # print("\nstate : ", state)
        # response = chain.invoke(state["messages"])
        # print("state messages", state["messages"][-1])
        response = chain.invoke(state)
        # print("response : ", response)
        filtered_response = self.extract_last_assistant_message(response.content)
        response = AIMessage(content=filtered_response)

        return {"messages": response}


    def get_response(self, message="hi", rag_context = "", session_id="random123", max_new_tokens=256):
        config = {"configurable": {"thread_id": session_id}}
        # message += " \nSales Assistant: "
        input_message = []
        if rag_context != "":
            input_message.append(SystemMessage(content = "Additional context: " + rag_context))

        input_message.append(HumanMessage(content = message))

        output = self.app.invoke({"messages": input_message}, config)

        # return "Human: " + output["messages"][-1].content.split("Human:")[1]
        # print(output)
        return output["messages"][-1].content

    def get_all_messages(self, session_id="random123"):
        """
        Retrieve all stored messages from the workflow's memory.

        Args:
            session_id (str): The unique session ID for the conversation.

        Returns:
            list: A list of all messages in the session.
        """
        # Fetch the current state from memory
        try:
            state = self.memory.get({"configurable": {"thread_id": session_id}})
            print("state : ", state) 
            if state and "messages" in state:
                return state["messages"]  # Return all stored messages
            else:
                return []  # If no messages found, return empty list
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
            
    def extract_last_assistant_message(self, conversation):
        # Split by the assistant marker
        assistant_start = conversation.rfind("<|start_header_id|>assistant<|end_header_id|>") + len("<|start_header_id|>assistant<|end_header_id|>\n\n")
        if assistant_start == -1:
            return None  # No assistant message found
        
        # Extract until the next marker or end of text
        assistant_end = conversation.find("<|eot_id|>", assistant_start)
        if assistant_end == -1:
            assistant_message = conversation[assistant_start:]  # Extract until the end of text
        else:
            assistant_message = conversation[assistant_start:assistant_end]

        return assistant_message.strip()



if __name__ == "__main__":
    
    # # Test the llama
    # messages = [
    #     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    #     {"role": "user", "content": "Who are you?"},
    # ]
    # outputs = pipe(
    #     messages,
    #     max_new_tokens=256,
    # )


    # print(outputs[0]["generated_text"][-1])

    llm = LLMHandler()
    while True:
        message = input(">: ")
        if message == "exit":
            break

        print("\n Assistant: " + llm.get_response(message=message))

    print("All messages: " + str(llm.get_all_messages()))