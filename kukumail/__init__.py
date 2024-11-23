import httpx
import time
import re
import json
import urllib

class Client:
    def __init__(self,session_hash=None,proxy:str=None):
        self.session=httpx.Client(proxy=proxy,follow_redirects=True)
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.me={}
        self.session_hash=session_hash
        if not self.session_hash == None:
            self.cookies={"cookie_sessionhash":self.session_hash}
            r = self.session.get("https://m.kuku.lu/index.php",cookies=self.cookies)
            self.me={"username":r.text.split('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">')[1].split("<")[0],"password":r.text.split('<span id="area_passwordview_copy">')[1].split("<")[0]}
            self.sub_token = re.search("csrf_subtoken_check=(\w+)",r.text).group(1)
            self.cookies["cookie_csrf_token"]=r.cookies["cookie_csrf_token"]
            self.token=r.cookies["cookie_csrf_token"]
        else:
            self.cookies={}
            self.token=None
            self.sub_token=None

    def register(self):
        r = self.session.get("https://m.kuku.lu/index.php")
        self.me={"username":r.text.split('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">')[1].split("<")[0],"password":r.text.split('<span id="area_passwordview_copy">')[1].split("<")[0]}
        self.cookies = r.cookies
        self.token=self.cookies["cookie_csrf_token"]
        self.session_hash=self.cookies["cookie_sessionhash"]
        self.sub_token = re.search("csrf_subtoken_check=(\w+)",r.text).group(1)
        self.session.get("https://m.kuku.lu/index.php?action=agreeEULA&nopost=1&by_system=1&csrf_token_check={}&_={}".format(self.token, round(time.time()*1000)),cookies=self.cookies)
        return {"session_hash":self.session_hash,"username":self.me["username"],"password":self.me["password"]}

    def me(self):
        return self.me

    def generate_onetime_email(self):
        if self.me=={}:return ""
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByOnetime&nopost=1&by_system=1&csrf_token_check="+self.token+"&csrf_subtoken_check="+self.sub_token+"&recaptcha_token=&_={round(time.time()*1000)}").text
        return str(email.split(":")[1]).split(",")[0]

    def generate_random_email(self):
        if self.me=={}:return ""
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1&csrf_token_check="+self.token+"&csrf_subtoken_check="+self.sub_token+"&recaptcha_token=&_={round(time.time()*1000)}").text
        return str(email.split(":")[1]).split(",")[0]

    def generate_email(self,domain="nyasan.com",address=""):
        if self.me=={}:return ""
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t="+str(int(time.time()))+"&csrf_token_check="+self. token+"&csrf_subtoken_check="+self.sub_token+"&newdomain="+domain+"&newuser="+address+"&recaptcha_token=&_="+str(int(+time.time()*1000)),cookies=self.cookies).text
        return str(email.split(":")[1])

    def get_address(self):
        if self.me=={}:return []
        r=self.session.get("https://m.kuku.lu/index._addrlist.php",cookies=self.cookies).text
        return re.findall(r'openMailAddrData\("([\w@\.]+)"\)', r)

    def recv_email(self,mail):
        if self.me=={}:return []
        while len(re.findall("openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=%\.;\-]+)'", self.session.get(f"https://m.kuku.lu/recv._ajax.php?&nopost=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&_={round(time.time()*1000)}&q={mail}",cookies=self.cookies).text)) == 0:time.sleep(1)
        r=self.session.get(f"https://m.kuku.lu/recv._ajax.php?&&nopost=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&_={round(time.time()*1000)}&q={mail}",cookies=self.cookies)
        results = []
        mails = re.findall("openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=%\.;\-]+)'", r.text)
        subjects = re.findall('<span style=\"overflow-wrap: break-word;word-break: break-all;\">(.*)<\/span>|<span class=\"font_gray\" style=\"\">(.+)</span>',r.text)
        for i in range(len(mails)):
            mail = mails[i]
            num = mail[0]
            id = mail[1]
            a = urllib.parse.unquote(mail[2]).split(";")
            frommail = a[0].split("=")[1]
            to = a[2].split("=")[1]
            subject = subjects[i][0]
            results.append({"number":num,"id":id,"from":frommail,"to":to,"subject":subject,"body":self.get_mail(num,id)})
        return results

    def get_mail(self, num: str, key: str):
        if self.me=={}:return ""
        params = {
            "num": num,
            "key": key,
            "noscroll": 1
        }
        response = self.session.post("https://m.kuku.lu/smphone.app.recv.view.php",cookies=self.cookies, params=params)
        return response.text
