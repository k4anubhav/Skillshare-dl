import requests


res = requests.post(url='https://api.skillshare.com/login',
                    headers={
                        "Cookie": "__cf_bm=fa70bb249a820ae1f9de922b003317429fe0ba29-1611949839-1800-AZGit0IB3gmpu2nVCQnzR1h1qm2aOW18R67xov0n9dDsOxz+NE1dqmXherOwDmLsoUqQRn/0aY0ayqHvLEPLhSw=; path=/; expires=Fri, 29-Jan-21 20:20:39 GMT; domain=.skillshare.com; HttpOnly; Secure; SameSite=None",
                        # "Authorization": "Basic c2tpbGxzaGFyZWFuZHJvaWQ6aiNhYWVnTTgvelg0cE0=",
                        # "X-Embed-Mode": "on",
                        "User-Agent": "Skillshare/5.3.16; Android 9.1.2 Mobile",
                        "Accept": "application/vnd.skillshare.user+json;,version=0.8",
                        # "Content-Type": "application/json; charset=UTF-8",
                        # "Content-Length": "109",
                        "Host": "api.skillshare.com",
                        # "Connection": "Keep-Alive",
                        # "Accept-Encoding": "gzip"
                      }
                    ,
                    data={
                        "email": "iiitvprod@k4anubhav.cf",
                        "password": "TL6jxBYHq6ZU",
                        "appsflyer_id": "1611841823569-13253186778651765"
                    }
)

print(res)
print(res.text)
print(res.headers)