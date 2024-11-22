import httpx
import time
import re
import json
import urllib

class Client:
    def __init__(self,proxy):
        self.session=httpx.Client(proxy=proxy)
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

    def register(self):
        r = self.session.get("https://m.kuku.lu/index.php")
        self.cookies = r.cookies.get_dict()
        self.sub_token = re.search("csrf_subtoken_check=(\w+)",r.text).group(1)
        self.token=self.cookies["cookie_csrf_token"]
        self.session.get("https://m.kuku.lu/index.php?action=agreeEULA&nopost=1&by_system=1&csrf_token_check={}&_={}".format(self.token, round(time.time()*1000)),cookies=self.cookies)
        return {"token":self.token,"sub_token":self.sub_token,"cookies":self.cookies}

    def login(self,username,password):
        r = self.session.get("https://m.kuku.lu/index.php")
        self.cookies = r.cookies.get_dict()
        self.sub_token = re.search("csrf_subtoken_check=(\w+)",r.text).group(1)
        self.token=self.cookies["cookie_csrf_token"]
        r=self.session.post("https://m.kuku.lu/smphone.app.index.php",cookies=self.cookies,data={"action":"checkLogin","confirmcode":"","nopost":"1","csrf_token_check":self.token,"csrf_subtoken_check":self.sub_token,"number":username,"password":password,"syncconfirm":"no"})
        self.cookies = r.cookies.get_dict()
        return {"token":self.token,"sub_token":self.sub_token,"cookies":r.cookies.get_dict()}

    def me(self):
        r=self.session.get("https://m.kuku.lu/smphone.app.index.php?pagemode_login=1&noindex=1",cookies=self.cookies).text
        return {"username":r.split('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">')[1].split("<")[0],"password":r.split('<span id="area_passwordview_copy">')[1].split("<")[0]}

    def generate_onetime_email(self):
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByOnetime&nopost=1&by_system=1&csrf_token_check="+self.token+"&csrf_subtoken_check="+self.sub_token+"&recaptcha_token=&_={round(time.time()*1000)}").text
        return str(email.split(":")[1]).split(",")[0]

    def generate_random_email(self):
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1&csrf_token_check="+self.token+"&csrf_subtoken_check="+self.sub_token+"&recaptcha_token=&_={round(time.time()*1000)}").text
        return str(email.split(":")[1]).split(",")[0]

    def generate_email(self,domain="nyasan.com",address=""):
        email=self.session.post("https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t="+str(int(time.time()))+"&csrf_token_check="+self. token+"&csrf_subtoken_check="+self.sub_token+"&newdomain="+domain+"&newuser="+address+"&recaptcha_token=&_="+str(int(+time.time()*1000)),cookies=self.cookies).text
        return str(email.split(":")[1])

    def get_address(self):
        r=self.session.get("https://m.kuku.lu/index._addrlist.php",cookies=self.cookies).text
        return re.findall(r'openMailAddrData\("([\w@\.]+)"\)', r)

    def recv_email(self,mail):
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
        params = {
            "num": num,
            "key": key,
            "noscroll": 1
        }
        response = self.session.post("https://m.kuku.lu/smphone.app.recv.view.php",cookies=self.cookies, params=params)
        return response.text
