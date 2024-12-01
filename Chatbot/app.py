import streamlit as st
# from transformers import pipeline
from ml_utils.vlm_handler import VLMHandler
from PIL import Image
import io
import base64  # Import base64 module

# Streamlit page configuration
st.set_page_config(page_title="Chatbot with Image Upload", layout="wide")

@st.cache_resource
def get_vlm_handler():
    return VLMHandler()

vlm = get_vlm_handler()

# Helper function to convert image to base64 string for embedding
def img_to_base64(uploaded_image):
    img = Image.open(uploaded_image)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Add custom CSS for styling the UI (Instagram-style chat)
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column-reverse;
            justify-content: flex-start;
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            background-color: #f7f7f7;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .message-bubble {
            margin: 5px 0;
            padding: 10px;
            border-radius: 20px;
            max-width: 70%;
        }
        .user-message {
            background-color: #e1ffc7;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #f1f0f0;
            align-self: flex-start;
        }
        .user-text, .bot-text {
            font-size: 14px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .chat-box {
            position: absolute;
            bottom: 10px;
            width: 100%;
        }
        .chat-image {
            max-width: 200px;
            max-height: 200px;
            object-fit: cover;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("Chatbot with Image Upload")

# Create a container for the chat messages (using session_state for persistence)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.image_uploaded = False  # Track if an image is uploaded

# if not st.session_state.image_uploaded:
# Image upload section
st.header("Upload an Image")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if not st.session_state.image_uploaded and uploaded_image is not None:
    
    print("Uploaded the image!!")
    # Store image flag in session state to indicate that an image has been uploaded
    st.session_state.image_uploaded = True
    st.session_state.image = uploaded_image

    # Display the image as part of the chat history
    image = Image.open(uploaded_image)
    # Show the uploaded image in the chat with a smaller resolution
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="PNG", width=150)

# Chat interface
st.header("Chat with the Bot")

# User input for text
user_input = st.text_input("Type your message:")

if user_input:
    image = []
    # If an image was uploaded, make sure to only show the image for the most recent message
    if st.session_state.image_uploaded:
        print("Reading the image!!")
        st.session_state.chat_history.append({"role": "user_image", "image": st.session_state.image})
        image = [Image.open(st.session_state.image)]
        st.session_state.image_uploaded = False
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Get chatbot response
    # response = "test"
    print("Sending the message with image!!")
    response = vlm.get_response(message=user_input,images=image)
    print("Received the response!! : ", response)
    bot_message = response

    if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1].get("role") != "bot":
        st.session_state.chat_history.append({"role": "bot", "text": bot_message})

# Limit the number of messages shown (e.g., last 5 messages)
num_messages_to_show = 5
messages_to_display = st.session_state.chat_history[-num_messages_to_show:]

# Display chat history in a scrollable box
with st.container():
    chat_container = st.empty()
    with chat_container.container():
        for msg in messages_to_display:
            if "text" in msg:
                if msg["role"] == "user":
                    st.markdown(f'<div class="message-bubble user-message"><div class="user-text">{msg["text"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="message-bubble bot-message"><div class="bot-text">{msg["text"]}</div></div>', unsafe_allow_html=True)
            elif "image" in msg:
                # Display the image uploaded by user in the chat
                st.markdown(f'<div class="message-bubble user-message"><img src="data:image/png;base64,{img_to_base64(msg["image"])}" class="chat-image"/></div>', unsafe_allow_html=True)


# Optional: Display some instructions or help
st.sidebar.markdown("""
## Instructions
1. Upload an image to display.
2. Type your message in the text input box to interact with the chatbot.
3. The chatbot will generate a response to your input, which will appear in the conversation.
4. Upload a new image by clicking the 'Upload New Image' button.
""")
