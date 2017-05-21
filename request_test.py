import requests
s = requests.Session()


# 1. Access FirstPage
# - Get 'csrftoken'(important)

headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

r = s.get('http://www.instagram.com',headers=headers)

print("HEADER==> " , r.headers)
print("*"*50)
print(r.cookies)


#2. Login
headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-CSRFToken": r.cookies['csrftoken'],
    "X-Instagram-AJAX": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
}
data = {
    "username":"smileman_god@naver.com",
    "password":"zaq1235"
}

r = s.post("https://www.instagram.com/accounts/login/ajax/",headers=headers, data=data ,cookies = r.cookies)

print(r.status_code)
print("HEADER ===> ", r.headers)
print("*"*50)
print(r.text)
print("*"*50)



#3. Request User Page
# query_id -> function id
# id -> 사용자의 unique id
# 17845312237175864
# https://www.instagram.com/graphql/query/?query_id=17845312237175864&id=1408289748

# GET 방식으로 요청함
# Request Header
# Host: www.instagram.com
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0
# Accept: */*
# Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
# Accept-Encoding: gzip, deflate, br
# Referer: https://www.instagram.com/jongsuk0206/
# X-Requested-With: XMLHttpRequest
# Cookie: csrftoken=ApIx0yUv0cFCirAaJii1zew8TFNfumxg; mid=WR238QAEAAFU70-yHlvVY_5Mk2Rz; ds_user_id=5470068000; sessionid=IGSC4d4e2b7b6137db271677bdf87f70c12d3c774c1447064bcef476c13de862281e%3AiCVSwz0UoYBgp0q6Y6xYdPoty49y3t4n%3A%7B%22_auth_user_id%22%3A5470068000%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%225470068000%3AAxUAmzDOScRbtOmpR9Y7IO31MbW92Civ%3A71026bfd5e3ccd44530f18e50901d99a582a4aa2250f0d476a74980ee679ff85%22%2C%22_platform%22%3A4%2C%22last_refreshed%22%3A1495288424.3225357533%2C%22asns%22%3A%7B%22time%22%3A1495288426%2C%22211.218.50.5%22%3A4766%7D%7D; s_network=""; rur=ATN; ig_vw=1440; ig_pr=1
# Connection: keep-alive
# Cache-Control: max-age=0

headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "*/*",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/jongsuk0206/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "csrftoken=ApIx0yUv0cFCirAaJii1zew8TFNfumxg; mid=WR238QAEAAFU70-yHlvVY_5Mk2Rz; ds_user_id=5470068000; sessionid=IGSC4d4e2b7b6137db271677bdf87f70c12d3c774c1447064bcef476c13de862281e%3AiCVSwz0UoYBgp0q6Y6xYdPoty49y3t4n%3A%7B%22_auth_user_id%22%3A5470068000%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%225470068000%3AAxUAmzDOScRbtOmpR9Y7IO31MbW92Civ%3A71026bfd5e3ccd44530f18e50901d99a582a4aa2250f0d476a74980ee679ff85%22%2C%22_platform%22%3A4%2C%22last_refreshed%22%3A1495288424.3225357533%2C%22asns%22%3A%7B%22time%22%3A1495288426%2C%22211.218.50.5%22%3A4766%7D%7D; s_network=""; rur=ATN; ig_vw=1440; ig_pr=1",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "X-CSRFToken": r.cookies['csrftoken']
}

# Content-Type: application/json
# Vary: Cookie, Accept-Language, Accept-Encoding
# Cache-Control: private, no-cache, no-store, must-revalidate
# Pragma: no-cache
# Expires: Sat, 01 Jan 2000 00:00:00 GMT
# Content-Language: ko
# Content-Length: 4659
# Content-Encoding: gzip
# Date: Sat, 20 May 2017 14:28:33 GMT
# Strict-Transport-Security: max-age=86400
# Set-Cookie: csrftoken=ApIx0yUv0cFCirAaJii1zew8TFNfumxg; expires=Sat, 19-May-2018 14:28:33 GMT; Max-Age=31449600; Path=/; Secure
# rur=ATN; Path=/
# ds_user_id=5470068000; expires=Fri, 18-Aug-2017 14:28:33 GMT; Max-Age=7776000; Path=/
# X-Firefox-Spdy: h2

function_url = "https://www.instagram.com/graphql/query/?query_id=17845312237175864&id=1408289748"
r = s.get(function_url,headers = headers, cookies=r.cookies)
print(r.status_code)
print("HEADER ===> ", r.headers)
print("*"*50)
print(r.text)
print("*"*50)
