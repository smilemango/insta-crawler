import http.client, urllib.parse

# Host: www.instagram.com
# User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate, br
# Upgrade-Insecure-Requests: 1
# Cookie: mid=WRq09gAEAAF1Ypa2afCJ7qC1hDoy; s_network=""; csrftoken=u3kZdgBObVVM4cMBmIilGt70fjkihtVd
# Connection: keep-alive

headers = {"Host": "www.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests":"1",
            "Connection": "keep-alive"
            }

conn = http.client.HTTPSConnection("www.instagram.com")
conn.request("GET","/")
response = conn.getresponse()
data = response.read()
print(data)
conn.close()


#
#
# params = urllib.parse.urlencode({'username': 'smileman_god@naver.com', 'password': 'sm140928'})
#
#
# headers = {"Host": "www.instagram.com",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
#             "Accept": "*/*",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Accept-Encoding": "gzip, deflate, br",
#             "X-Instagram-AJAX": "1",
#             "Content-Type": "application/x-www-form-urlencoded",
#             "X-Requested-With": "XMLHttpRequest",
#             "Referer": "https://www.instagram.com/",
#             "Connection": "keep-alive",
#             "X-CSRFToken": "6VEnDTMwKiX3g0vGVvBucJLJ9vaOmfku",
#             "Cookie": "mid=WRq09gAEAAF1Ypa2afCJ7qC1hDoy; s_network=""; rur=FRC; ig_vw=1920; ig_pr=1; csrftoken=6VEnDTMwKiX3g0vGVvBucJLJ9vaOmfku"
#             }
# conn = http.client.HTTPSConnection("www.instagram.com")
# conn.request("POST", "/accounts/login/ajax/", params, headers)
# response = conn.getresponse()
# print(response.status, response.reason)
# data = response.read()
# conn.close()
