import requests
s = requests.Session()
r = s.get('http://www.instagram.com')

print(r.text)

s.post