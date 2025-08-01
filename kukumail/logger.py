import logging
import sys
from typing import Optional


class Logger:
    """ログ管理クラス"""
    
    def __init__(self, name: str = "kukumail", level: str = "INFO", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 既存のハンドラーをクリア
        self.logger.handlers.clear()
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # ファイルハンドラー（指定された場合）
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """デバッグログ"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報ログ"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告ログ"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """エラーログ"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """重大エラーログ"""
        self.logger.critical(message)
    
    def log_email_generated(self, email: str):
        """メールアドレス生成ログ"""
        self.info(f"メールアドレス生成: {email}")
    
    def log_email_deleted(self, email: str, success: bool):
        """メールアドレス削除ログ"""
        status = "成功" if success else "失敗"
        self.info(f"メールアドレス削除: {email} - {status}")
    
    def log_email_received(self, email: str, count: int):
        """メール受信ログ"""
        self.info(f"メール受信: {email} - {count}件")
    
    def log_session_created(self, username: str):
        """セッション作成ログ"""
        self.info(f"セッション作成: {username}")
    
    def log_error(self, operation: str, error: Exception):
        """エラーログ"""
        self.error(f"{operation} エラー: {str(error)}") 