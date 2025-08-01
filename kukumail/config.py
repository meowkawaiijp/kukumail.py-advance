import json
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """設定管理クラス"""
    
    def __init__(self, config_file: str = "kukumail_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込み"""
        default_config = {
            "session_hash": None,
            "proxy": None,
            "auto_save_session": True,
            "log_level": "INFO",
            "timeout": 30,
            "retry_count": 3,
            "domains": ["nyasan.com", "kuku.lu"],
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception:
                pass
        
        return default_config
    
    def save_config(self):
        """設定を保存"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"設定保存エラー: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """設定値を設定"""
        self.config[key] = value
        if self.config.get("auto_save_session"):
            self.save_config()
    
    def update_session(self, session_hash: str, username: str, password: str):
        """セッション情報を更新"""
        self.set("session_hash", session_hash)
        self.set("username", username)
        self.set("password", password)
    
    def get_session_info(self) -> Dict[str, Optional[str]]:
        """セッション情報を取得"""
        return {
            "session_hash": self.get("session_hash"),
            "username": self.get("username"),
            "password": self.get("password")
        }
    
    def clear_session(self):
        """セッション情報をクリア"""
        self.set("session_hash", None)
        self.set("username", None)
        self.set("password", None) 