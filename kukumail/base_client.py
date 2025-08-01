from typing import List, Dict, Optional, Any


class BaseClient:
    """基本クライアントクラス"""
    
    def __init__(self, session_hash: Optional[str] = None, proxy: Optional[str] = None):
        self.me = {}
        self.session_hash = session_hash
        self.cookies = {}
        self.token = None
        self.sub_token = None
        self._setup_session()

    def _setup_session(self):
        """セッション初期設定"""
        if self.session_hash:
            self.cookies = {"cookie_sessionhash": self.session_hash}
            # セッション情報を取得
            self._load_session_info()

    def _load_session_info(self):
        """セッション情報を読み込み"""
        # このメソッドは継承先で実装
        pass

    def me(self) -> Dict[str, str]:
        """現在のユーザー情報を取得"""
        return self.me

    def generate_onetime_email(self) -> str:
        """ワンタイムメールアドレス生成"""
        if self.me == {}:
            return ""
        # このメソッドは継承先で実装
        return ""

    def generate_random_email(self) -> str:
        """ランダムメールアドレス生成"""
        if self.me == {}:
            return ""
        # このメソッドは継承先で実装
        return ""

    def generate_email(self, domain: str = "nyasan.com", address: str = "") -> str:
        """カスタムメールアドレス生成"""
        if self.me == {}:
            return ""
        # このメソッドは継承先で実装
        return ""

    def get_address(self) -> List[str]:
        """メールアドレス一覧取得"""
        if self.me == {}:
            return []
        # このメソッドは継承先で実装
        return []

    def recv_email(self, mail: str) -> List[Dict[str, Any]]:
        """メール受信"""
        if self.me == {}:
            return []
        # このメソッドは継承先で実装
        return []

    def get_mail(self, num: str, key: str) -> str:
        """メール本文取得"""
        if self.me == {}:
            return ""
        # このメソッドは継承先で実装
        return "" 