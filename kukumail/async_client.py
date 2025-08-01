import httpx
import asyncio
import time
import re
import urllib.parse
from typing import List, Dict, Optional, Any
from .base_client import BaseClient


class AsyncClient(BaseClient):
    """非同期版のkukumailクライアント"""
    
    def __init__(self, session_hash: Optional[str] = None, proxy: Optional[str] = None):
        super().__init__(session_hash, proxy)
        self.session = httpx.AsyncClient(proxy=proxy, follow_redirects=True)
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self._setup_session()

    async def register(self) -> Dict[str, str]:
        """非同期でアカウント登録"""
        r = await self.session.get("https://m.kuku.lu/index.php")
        self.me = {
            "username": r.text.split('<div id="area_numberview" style="white-space:wrap;word-break:break-all;">')[1].split("<")[0],
            "password": r.text.split('<span id="area_passwordview_copy">')[1].split("<")[0]
        }
        self.cookies = r.cookies
        self.token = self.cookies["cookie_csrf_token"]
        self.session_hash = self.cookies["cookie_sessionhash"]
        self.sub_token = re.search("csrf_subtoken_check=(\w+)", r.text).group(1)
        
        await self.session.get(
            f"https://m.kuku.lu/index.php?action=agreeEULA&nopost=1&by_system=1&csrf_token_check={self.token}&_={round(time.time()*1000)}",
            cookies=self.cookies
        )
        
        return {
            "session_hash": self.session_hash,
            "username": self.me["username"],
            "password": self.me["password"]
        }

    async def generate_random_email(self) -> str:
        """非同期でランダムメールアドレス生成"""
        if self.me == {}:
            return ""
        
        email = await self.session.post(
            f"https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&recaptcha_token=&_={round(time.time()*1000)}"
        )
        return str(email.text.split(":")[1]).split(",")[0]

    async def generate_email(self, domain: str = "nyasan.com", address: str = "") -> str:
        """非同期でカスタムメールアドレス生成"""
        if self.me == {}:
            return ""
        
        email = await self.session.post(
            f"https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t={int(time.time())}&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&newdomain={domain}&newuser={address}&recaptcha_token=&_={int(time.time()*1000)}",
            cookies=self.cookies
        )
        return str(email.text.split(":")[1])

    async def get_address(self) -> List[str]:
        """非同期でメールアドレス一覧取得"""
        if self.me == {}:
            return []
        
        r = await self.session.get("https://m.kuku.lu/index._addrlist.php", cookies=self.cookies)
        return re.findall(r'openMailAddrData\("([\w@\.]+)"\)', r.text)

    async def delete_email(self, email: str) -> bool:
        """メールアドレス削除"""
        if self.me == {}:
            return False
        
        try:
            response = await self.session.post(
                f"https://m.kuku.lu/index.php?action=delMailAddr&nopost=1&by_system=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&mail={email}&_={round(time.time()*1000)}",
                cookies=self.cookies
            )
            return "success" in response.text.lower()
        except Exception:
            return False

    async def get_domains(self) -> List[str]:
        """利用可能なドメイン一覧取得"""
        try:
            response = await self.session.get("https://m.kuku.lu/index.php", cookies=self.cookies)
            # ドメイン一覧を抽出するロジックを実装
            domains = re.findall(r'<option value="([^"]+)">', response.text)
            return domains
        except Exception:
            return []

    async def recv_email(self, mail: str) -> List[Dict[str, Any]]:
        """非同期でメール受信"""
        if self.me == {}:
            return []
        
        # メールが届くまで待機
        while len(re.findall(
            "openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=%\.;\-]+)'",
            (await self.session.get(
                f"https://m.kuku.lu/recv._ajax.php?&nopost=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&_={round(time.time()*1000)}&q={mail}",
                cookies=self.cookies
            )).text
        )) == 0:
            await asyncio.sleep(1)
        
        r = await self.session.get(
            f"https://m.kuku.lu/recv._ajax.php?&&nopost=1&csrf_token_check={self.token}&csrf_subtoken_check={self.sub_token}&_={round(time.time()*1000)}&q={mail}",
            cookies=self.cookies
        )
        
        results = []
        mails = re.findall("openMailData\('(\d+)',\s*'(\w+)',\s*'([\w=%\.;\-]+)'", r.text)
        subjects = re.findall('<span style=\"overflow-wrap: break-word;word-break: break-all;\">(.*)<\/span>|<span class=\"font_gray\" style=\"\">(.+)</span>', r.text)
        
        for i in range(len(mails)):
            mail_data = mails[i]
            num = mail_data[0]
            id = mail_data[1]
            a = urllib.parse.unquote(mail_data[2]).split(";")
            frommail = a[0].split("=")[1]
            to = a[2].split("=")[1]
            subject = subjects[i][0] if subjects[i][0] else subjects[i][1]
            
            results.append({
                "number": num,
                "id": id,
                "from": frommail,
                "to": to,
                "subject": subject,
                "body": await self.get_mail(num, id)
            })
        
        return results

    async def get_mail(self, num: str, key: str) -> str:
        """非同期でメール本文取得"""
        if self.me == {}:
            return ""
        
        params = {
            "num": num,
            "key": key,
            "noscroll": 1
        }
        response = await self.session.post(
            "https://m.kuku.lu/smphone.app.recv.view.php",
            cookies=self.cookies,
            params=params
        )
        return response.text

    async def close(self):
        """セッション終了"""
        await self.session.aclose() 