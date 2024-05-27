from simplegmail import Gmail
from datetime import datetime, timedelta
import re
# Set the start and end dates
end_date = datetime(2024, 5, 26)  # May 20, 2023
start_date = datetime(2024, 5, 26)   # May 15, 2023

# Convert dates to Gmail API format
start_date_str = start_date.strftime('%Y/%m/%d')
end_date_str = (end_date + timedelta(days=1)).strftime('%Y/%m/%d')  # Add 1 day to end_date (before is exclusive)

# Construct the query string
query = f'after:{start_date_str} before:{end_date_str}'

gmail = Gmail()
messages = []
# Unread messages in your inbox
messages = gmail.get_messages(attachments='ignore',query=query)

# print(gmail.list_labels())

# Starred messages
# messages = gmail.get_starred_messages()

# messages = gmail.get_messages(query=query)

# ...and many more easy to use functions can be found in gmail.py!

# Print them out!
for message in messages:
    print("\n ================ \n")
    print("To: " + message.recipient)
    print("From: " + message.sender)
    print("Subject: " + message.subject)
    print("Date: " + message.date)
    print("Preview: " + message.snippet)
    
    if message.plain:
        body = message.plain# or message.html
    elif message.html:
        body = message.html
    # url_pattern = #r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

    # Remove URLs from the string
    # cleaned_text = re.sub(url_pattern, '', body)

    print("Message Body: " + body) #cleaned_text) 