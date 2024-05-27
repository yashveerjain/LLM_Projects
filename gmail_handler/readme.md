# Working with Gmail
* use the simplegmail folder present in here, it took reference from simplegmail package python
* go through the google workspace api for handling the gmail api access

# Working with ollama
* install ollama from  this website:
    -  https://ollama.com/
* download model:
    - open command prompt:
        ```
        ollama run llama3
        ```
* python package for ollama
    - https://github.com/ollama/ollama-python

* running ollama
    - open command prompt and run the following command:
    ```
    setx OLLAMA_HOST 127.0.0.1:11435
    ollama serve
    ```
    - in anaconda prompt:
    ```
    python llama_ollama_handler.py
    ```

# Running the Code
> python get_recent_email_data.py