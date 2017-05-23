import requests
import json
import traceback
import re


class CrawlerException(Exception):
    def __init__(self, object):
        self._object = object

    def getObject(self):
        return self._object


class InstaCrawler:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = requests.session()
        self._is_logged_in = False

        headers = {
            "Host": "www.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        r = self._session.get('http://www.instagram.com', headers=headers)
        self._last_cookies = r.cookies

    def login(self):
        headers = {
            "Host": "www.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-CSRFToken": self._last_cookies['csrftoken'],
            "X-Instagram-AJAX": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/",
        }
        data = {
            "username": self._username,
            "password": self._password
        }

        r = self._session.post("https://www.instagram.com/accounts/login/ajax/", headers=headers, data=data,
                               cookies=self._last_cookies)
        self._last_cookies = r.cookies

        result = json.loads(r.text)

        # login failure
        # {"authenticated": false, "user": true, "status": "ok"}
        if result['authenticated'] == True:
            self._is_logged_in = True
            return True
        else:
            return False

    def is_logged_in(self):
        return self._is_logged_in

    def get_followed_by_id(self, id, after=None):
        if self._is_logged_in == False:
            return None

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
            "X-CSRFToken": self._last_cookies['csrftoken']
        }

        url = "https://www.instagram.com/graphql/query/?query_id=17851374694183129&id=%s&first=20" % id

        if after != None:
            url = url + "&after" + after

        r = self._session.get(url, headers=headers, cookies=self._last_cookies)
        self._last_cookies = r.cookies

        result = json.loads(r.text)
        return result

    def get_follows_by_id(self, id, after=None):
        if self._is_logged_in == False:
            return None

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
            "X-CSRFToken": self._last_cookies['csrftoken']
        }

        url = "https://www.instagram.com/graphql/query/?query_id=17874545323001329&id=%s&first=20" % id

        if after != None:
            url = url + "&after=" + after

        r = self._session.get(url, headers=headers, cookies=self._last_cookies)
        self._last_cookies = r.cookies

        try:
            result = json.loads(r.text)
        except:
            traceback.print_exc()
            raise CrawlerException(r.text)
        return result

    def get_id_by_username(self, username):

        url = "https://www.instagram.com/" + username
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
            "X-CSRFToken": self._last_cookies['csrftoken']
        }
        r = self._session.get(url, headers=headers, cookies=self._last_cookies)
        self._last_cookies = r.cookies

        m = re.findall('"id": "([0-9]{9,10})"', r.text)
        if len(m) > 1:
            return m[1]
        else:
            return None
