import pandas as pd
from datetime import datetime, timedelta
import re
import traceback

from llama_ollama_handler import get_response
from simplegmail import Gmail


gmail = Gmail()

labels = gmail.list_labels()

status2label = {
    'rejected' : 'Jobs/Rejected',
    'applied' : 'Jobs/Applied',
    'promotional' : 'promotional',
    'need action' : 'need attention',
    'personal' : 'personal',
    'not sure' : 'not sure',
    'job opportunities' : 'job opportunities',
}

status2labelids = {} 
for status,label_name in status2label.items():
    for label in labels:
        if label.name==label_name:
            status2labelids[status] = label.id

print(status2labelids)

def organize_email(message):
    if message.html:
        body = message.html
        # print("Message Body: " + message.html)
    else:
        body = message.snippet
    # print("body : ",body)
    resp = get_response(body,message.subject)
    # print("\n resp :",resp)
    try:
        matches = re.findall(r'\(\|(.*?)\|\)', resp)
        # print(matches[0].split("--"))
        status,jt,cn,reason = matches[0].split("--")[:4]
        status = status.lower()
        if status not in status2label.keys():
            return (False, resp, 'not sure')
        # new_row = [cn, jt, status,message.date,message.sender,message.subject,reason]
        # df.loc[len(df)] = new_row
        return (True, resp,status)
    except Exception as e:
        traceback.print_exc()
        return (False,resp,'not sure')

if __name__ == "__main__":

    # Set the start and end dates
    end_date = datetime(2024, 5, 1)  # May 20, 2023
    start_date = datetime(2024, 4, 1)   # May 15, 2023

    # Convert dates to Gmail API format
    start_date_str = start_date.strftime('%Y/%m/%d')
    end_date_str = (end_date + timedelta(days=1)).strftime('%Y/%m/%d')  # Add 1 day to end_date (before is exclusive)

    # Construct the query string
    query = f'after:{start_date_str} before:{end_date_str}'

    data = {'Job Title': [],
            'Name (Company/Person)': [], 
            'status': [],
            'date' : [],
            'from email': [],
            "subject" : [],
            'reason' : []}
    df = pd.DataFrame(data)
    filename = end_date.strftime('%Y-%m-%d')
    filename += "-"+start_date.strftime('%Y-%m-%d')
    df.to_csv(f"{filename}_email_data.csv",index=False)
    # Unread messages in your inbox
    messages = gmail.get_messages(attachments='ignore',query=query)


    for message in messages:
        print("\n ================ \n")
        print("To: " + message.recipient)
        print("From: " + message.sender)
        print("Subject: " + message.subject)
        print("Date: " + message.date)
        print("Preview: " + message.snippet)

        try:
            cnt = 0
            # try:
            flag = False
            status_cnt_dict = {}
            max_status_cnt = 0
            max_status = "not sure"
            max_status_cnt_limit = 3
            while cnt<10:
                cnt+=1
                flag, resp, status = organize_email(message)
                if flag:
                    status_cnt_dict[status] = status_cnt_dict.get(status,0)+1
                    if status_cnt_dict[status] > max_status_cnt:
                        max_status_cnt = status_cnt_dict[status] 
                    # if status_cnt_dict[status]>max_status_cnt and not status=="not sure":
                        max_status = status
                        # break
                    if max_status_cnt > max_status_cnt_limit:
                        break

            if not flag:
                df.loc[len(df)] = ['','','',message.date,message.sender,message.subject,resp]
            else:
                # add it to csv
                matches = re.findall(r'\(\|(.*?)\|\)', resp)
                # print(matches[0].split("--"))
                status,jt,cn,reason = matches[0].split("--")[:4]
                new_row = [jt, cn, status,message.date,message.sender,message.subject,reason]
                df.loc[len(df)] = new_row
            print(max_status, resp)
        
            gmail.add_label_to_email(msg_id=message.id, label_id=status2labelids[max_status])
        except Exception as e:
            df.loc[len(df)] = ['','','',message.date,message.sender,message.subject,message.snippet]
            gmail.add_label_to_email(msg_id=message.id, label_id=status2labelids['not sure'])
    df['date'] = pd.to_datetime(df['date'])
    # query = query.replace("\\","-")
    df.to_csv(f"{filename}_email_data.csv",index=False)
    print(df)