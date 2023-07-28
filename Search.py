import requests, re

num = -1
urlsList = []
print("Please input cookie to scan")
auth_cookie = input()

def get_private_messages(auth_cookie, page):
    url = f'https://privatemessages.roblox.com/v1/messages?pageNumber={page}&pageSize=20&messageTab=Inbox'
    headers = {'Cookie': f'.ROBLOSECURITY={auth_cookie}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['collection']
    else:
        print(f"Error: Unable to fetch messages. Status Code: {response.status_code}")
        return None

def get_total_messages_because_im_retarded(auth_cookie, page):
    url = f'https://privatemessages.roblox.com/v1/messages?pageNumber={page}&pageSize=20&messageTab=Inbox'
    headers = {'Cookie': f'.ROBLOSECURITY={auth_cookie}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["totalPages"]
    else:
        print(f"Error: Unable to fetch messages. Status Code: {response.status_code}")
        return None
def find_messages_with_keyword(messages, keyword):
    keyword_messages = []
    for message in messages:
        if keyword.lower() in message['subject'].lower() or keyword.lower() in message['body'].lower():
            keyword_messages.append(message)
    return keyword_messages
    

def find_urls_in_body(messages):
    urls = []
    pattern = r"https://www\.roblox\.com/modcreditagreement/[a-fA-F0-9-]+"

    for message in messages:
        if 'body' in message and isinstance(message['body'], str):
            urls.extend(re.findall(pattern, message['body']))

    return urls

total_pages = get_total_messages_because_im_retarded(auth_cookie, 1)

while not num+1 == total_pages:
    keyword = 'credit'
    num+=1
    messages = get_private_messages(auth_cookie, num)
    urls = find_urls_in_body(messages)
    if messages is not None:
        keyword_messages = find_messages_with_keyword(messages, keyword)
        if keyword_messages:
            for message in keyword_messages:
                urlFind = find_urls_in_body(messages)
                if not urlFind == []:
                    if not urlFind in urlsList:
                        urlsList.append(urlFind)
                        print("Added URL to list. Will print all URLS once complete.")
                    else:
                        print("Duplicate URL found for some fucking reason. Skipping...")
        else:
            print(f"No robux refund credit message found on page {num+1}/{total_pages}")
            
print("ALL URLS:")
for url in urlsList:
    print(url)
input("Press Enter to close")

#Made by Foox :3