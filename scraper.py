import config
import requests
from bs4 import BeautifulSoup

loginurl = ('https://carleton.reclaimhosting.com:2087/login/?login_only=1')
secureurl = ('https://carleton.reclaimhosting.com:2087/cpsess1745090637/?login=1&post_login=59666413072871')

payload = {
    'user': config.username,
    'pass': config.password,
}

with requests.session() as s:
    s.post(loginurl, data=payload)
    r = s.get(secureurl)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify())


# r = requests.post(loginurl, data = payload)
#
# print(r.text)
