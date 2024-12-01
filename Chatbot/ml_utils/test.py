import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq, AutoTokenizer
from transformers.image_utils import load_image


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def extract_last_assistant_message(conversation):
    # Split by the assistant marker
    assistant_start = conversation.rfind("Assistant:") + len("Assistant:")
    if assistant_start == -1:
        return None  # No assistant message found
    
    # Extract until the next marker or end of text
    assistant_end = conversation.find("<end_of_utterance>", assistant_start)
    if assistant_end == -1:
        assistant_message = conversation[assistant_start:]  # Extract until the end of text
    else:
        assistant_message = conversation[assistant_start:assistant_end]

    return assistant_message.strip()


# Load images
image1 = load_image("https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg")
image2 = load_image("https://huggingface.co/spaces/merve/chameleon-7b/resolve/main/bee.jpg")

# Initialize processor and model
# processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolVLM-Instruct", )

model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-Instruct",
    torch_dtype=torch.bfloat16,
    _attn_implementation="eager" # "flash_attention_2" if DEVICE == "cuda" else "eager",
).to(DEVICE)

# # Create input messages
messages = [
    
        {"role": "system", "content": [{"type": "text",
        "text" :"You are a Sales Assistant. Only provide responses when the Human asks questions or says something. Do not simulate Human inputs or assume details not provided by the user.",
        }]},
        {
        "role": "user",
        "content": [
            # {"type": "image"},
            {"type": "text", "text": "hi, who are you? Can I have some products to see?"},
        ]
    },
    {
        "role": "assistant",
        "content": [
            # {"type": "image"},
            {"type": "text", "text": "hi, I am a Sales Assistant. Can I help you find something?"}],
    },
    {
        "role": "user",
        "content": [
            # {"type": "image"},
            {"type": "text", "text": "I want to see a product."}
        ]
    }
]

# # Prepare inputs
# prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
# prompt = """ <|im_start|>User: hi<end_of_utterance>
# User: hi<end_of_utterance>
# User: hi<end_of_utterance>""" 
# inputs = processor(text=tokenize_input, images=[], return_tensors="pt")
inputs = inputs.to(DEVICE)
print("inputs: ", inputs)

# Generate outputs
generated_ids = model.generate(inputs, max_new_tokens=500)
# generated_texts = processor.batch_decode(
#     generated_ids,
#     skip_special_tokens=True,
# )

pre_output = tokenizer.decode(generated_ids[0])
print("pere output: ", pre_output)

ass = extract_last_assistant_message(pre_output)
print("assistant: ", ass)

"""
Assistant: The first image shows a green statue of the Statue of Liberty standing on a stone pedestal in front of a body of water. 
The statue is holding a torch in its right hand and a tablet in its left hand. The water is calm and there are no boats or other objects visible. 
The sky is clear and there are no clouds. The second image shows a bee on a pink flower. 
The bee is black and yellow and is collecting pollen from the flower. The flower is surrounded by green leaves.
"""
