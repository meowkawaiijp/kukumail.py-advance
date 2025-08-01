import argparse
import asyncio
from .async_client import AsyncClient
from .sync_client import SyncClient
from .config import Config
from .logger import Logger


class CLI:
    """コマンドラインインターフェース"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger(
            level=self.config.get("log_level", "INFO"),
            log_file="kukumail.log"
        )
        self.client = None
    
    def setup_client(self, async_mode: bool = False):
        """クライアントをセットアップ"""
        session_info = self.config.get_session_info()
        
        if async_mode:
            self.client = AsyncClient(
                session_hash=session_info.get("session_hash"),
                proxy=self.config.get("proxy")
            )
        else:
            self.client = SyncClient(
                session_hash=session_info.get("session_hash"),
                proxy=self.config.get("proxy")
            )
    
    async def register_async(self):
        """非同期でアカウント登録"""
        if not self.client:
            self.setup_client(async_mode=True)
        
        try:
            result = await self.client.register()
            self.config.update_session(
                result["session_hash"],
                result["username"],
                result["password"]
            )
            self.logger.log_session_created(result["username"])
            print(f"登録成功: {result}")
            return result
        except Exception as e:
            self.logger.log_error("アカウント登録", e)
            print(f"登録エラー: {e}")
            return None
    
    def register_sync(self):
        """同期でアカウント登録"""
        if not self.client:
            self.setup_client(async_mode=False)
        
        try:
            result = self.client.register()
            self.config.update_session(
                result["session_hash"],
                result["username"],
                result["password"]
            )
            self.logger.log_session_created(result["username"])
            print(f"登録成功: {result}")
            return result
        except Exception as e:
            self.logger.log_error("アカウント登録", e)
            print(f"登録エラー: {e}")
            return None
    
    async def generate_email_async(self, domain: str = "", address: str = ""):
        """非同期でメールアドレス生成"""
        if not self.client:
            self.setup_client(async_mode=True)
        
        try:
            if domain and address:
                email = await self.client.generate_email(domain, address)
            else:
                email = await self.client.generate_random_email()
            
            if email:
                self.logger.log_email_generated(email)
                print(f"メールアドレス生成: {email}")
                return email
            else:
                print("メールアドレス生成に失敗しました")
                return None
        except Exception as e:
            self.logger.log_error("メールアドレス生成", e)
            print(f"生成エラー: {e}")
            return None
    
    def generate_email_sync(self, domain: str = "", address: str = ""):
        """同期でメールアドレス生成"""
        if not self.client:
            self.setup_client(async_mode=False)
        
        try:
            if domain and address:
                email = self.client.generate_email(domain, address)
            else:
                email = self.client.generate_random_email()
            
            if email:
                self.logger.log_email_generated(email)
                print(f"メールアドレス生成: {email}")
                return email
            else:
                print("メールアドレス生成に失敗しました")
                return None
        except Exception as e:
            self.logger.log_error("メールアドレス生成", e)
            print(f"生成エラー: {e}")
            return None
    
    async def list_emails_async(self):
        """非同期でメールアドレス一覧表示"""
        if not self.client:
            self.setup_client(async_mode=True)
        
        try:
            emails = await self.client.get_address()
            if emails:
                print("メールアドレス一覧:")
                for i, email in enumerate(emails, 1):
                    print(f"{i}. {email}")
            else:
                print("メールアドレスがありません")
            return emails
        except Exception as e:
            self.logger.log_error("メールアドレス一覧取得", e)
            print(f"取得エラー: {e}")
            return []
    
    def list_emails_sync(self):
        """同期でメールアドレス一覧表示"""
        if not self.client:
            self.setup_client(async_mode=False)
        
        try:
            emails = self.client.get_address()
            if emails:
                print("メールアドレス一覧:")
                for i, email in enumerate(emails, 1):
                    print(f"{i}. {email}")
            else:
                print("メールアドレスがありません")
            return emails
        except Exception as e:
            self.logger.log_error("メールアドレス一覧取得", e)
            print(f"取得エラー: {e}")
            return []
    
    async def receive_email_async(self, email: str):
        """非同期でメール受信"""
        if not self.client:
            self.setup_client(async_mode=True)
        
        try:
            emails = await self.client.recv_email(email)
            if emails:
                self.logger.log_email_received(email, len(emails))
                print(f"受信メール ({len(emails)}件):")
                for i, mail in enumerate(emails, 1):
                    print(f"{i}. 件名: {mail['subject']}")
                    print(f"   送信者: {mail['from']}")
                    print(f"   本文: {mail['body'][:100]}...")
                    print()
            else:
                print("受信メールがありません")
            return emails
        except Exception as e:
            self.logger.log_error("メール受信", e)
            print(f"受信エラー: {e}")
            return []
    
    def receive_email_sync(self, email: str):
        """同期でメール受信"""
        if not self.client:
            self.setup_client(async_mode=False)
        
        try:
            emails = self.client.recv_email(email)
            if emails:
                self.logger.log_email_received(email, len(emails))
                print(f"受信メール ({len(emails)}件):")
                for i, mail in enumerate(emails, 1):
                    print(f"{i}. 件名: {mail['subject']}")
                    print(f"   送信者: {mail['from']}")
                    print(f"   本文: {mail['body'][:100]}...")
                    print()
            else:
                print("受信メールがありません")
            return emails
        except Exception as e:
            self.logger.log_error("メール受信", e)
            print(f"受信エラー: {e}")
            return []
    
    def run(self):
        """CLIを実行"""
        parser = argparse.ArgumentParser(description="kukumail.py-advance CLI")
        parser.add_argument("--async-mode", action="store_true", help="非同期モードを使用")
        parser.add_argument("--register", action="store_true", help="アカウント登録")
        parser.add_argument("--generate", action="store_true", help="メールアドレス生成")
        parser.add_argument("--domain", type=str, help="ドメイン指定")
        parser.add_argument("--address", type=str, help="アドレス指定")
        parser.add_argument("--list", action="store_true", help="メールアドレス一覧表示")
        parser.add_argument("--receive", type=str, help="メール受信（メールアドレス指定）")
        parser.add_argument("--delete", type=str, help="メールアドレス削除")
        
        args = parser.parse_args()
        
        if args.async_mode:
            asyncio.run(self._run_async(args))
        else:
            self._run_sync(args)
    
    async def _run_async(self, args):
        """非同期実行"""
        if args.register:
            await self.register_async()
        elif args.generate:
            await self.generate_email_async(args.domain, args.address)
        elif args.list:
            await self.list_emails_async()
        elif args.receive:
            await self.receive_email_async(args.receive)
        else:
            print("コマンドを指定してください")
    
    def _run_sync(self, args):
        """同期実行"""
        if args.register:
            self.register_sync()
        elif args.generate:
            self.generate_email_sync(args.domain, args.address)
        elif args.list:
            self.list_emails_sync()
        elif args.receive:
            self.receive_email_sync(args.receive)
        else:
            print("コマンドを指定してください")


def main():
    """メイン関数"""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main() 