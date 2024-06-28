# Gmail Organizer and Automatic Labeling
This project aims to automatically organize and label your Gmail emails. It leverages the Gmail API and the Ollama chatbot for additional functionality.

## Features
- Automatic labeling of emails based on the email status (rejected, need action, applied, promotional, personal, job opportunities)
- Creation of a CSV file with email details for organizing and prioritizing mails
- Supported labels:
  - Jobs
  - Jobs/Rejected
  - Jobs/Applied
  - Promotional
  - Need Attention
  - Personal
  - Not Sure
  - Job Opportunities

## Getting Started
### Prerequisites
- Install the Ollama chatbot from [https://ollama.com/](https://ollama.com/)
- Download the Ollama model by running the following command in the terminal:
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
### Working with Gmail

To work with Gmail, you need to follow these steps:

1. **Install the `simplegmail` package**: This package is a simple wrapper around the Gmail API. You can find it in the `simplegmail` folder of this repository.

2. **Enable the Gmail API**: Visit the [Google Workspace API Console](https://console.developers.google.com/apis/library/gmail.googleapis.com) and enable the Gmail API for your project.

3. **Create credentials**: Follow the instructions in the [Gmail API Quickstart guide](https://developers.google.com/gmail/api/quickstart/python) to create credentials for your application. Make sure to download the credentials file and store it securely

## Running the code
**Run the code**: Once you have the credentials file, you can run the code using the following command:

> pip install -r requirements.txt
> python get_recent_email_data.py --client_secret_file path/to/client_secret.json --creds path/to/token.json

**Note :** Give path to client_secret.json and token.json

