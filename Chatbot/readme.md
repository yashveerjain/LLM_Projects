# Chatbot

All chatbot implementations are present here!

**Note** In this directory create `.env` file and add huggingface api key, like this:
``` 
HUGGINGFACE_API_TOKEN=<your huggingface api key>
```


## RAG based Chatbot

This used rag to retreive context and then locally run LLAMA3.2-instruct 3b for response, this model has shown better results than other models for text generation tasks. It utilizes fastapi for frontend.


## VLM based Chatbot

This used VLM to retreive context and then locally run SmolVLM huggingface for response, this model has shown better results than other models for VLM related tasks.

![](assets/working-vid-gif.gif)

### more details on how to use this feature, please refer to the [readme](docs/vlm_chatbot_readme.md) file.
