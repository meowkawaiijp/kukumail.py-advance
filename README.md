# kukumail.py-advance

## 新機能

### 1. 非同期対応 (Async Implementation)
- `AsyncClient`クラスで非同期処理をサポート
- 複数のメールアドレスを同時に管理可能
- 並行処理による高速化

### 2. 高度なメール管理機能
- メールアドレスの削除機能 (`delete_email`)
- 利用可能なドメイン一覧取得 (`get_domains`)
- メールフィルタリング機能

### 3. セキュリティ強化
- セッション管理の改善
- プロキシローテーション対応
- レート制限対応

### 4. 使いやすさの向上
- CLI インターフェース
- 設定ファイル対応 (`Config`クラス)
- ログ機能 (`Logger`クラス)

## 基本的な使用方法

### 同期版
```python
import kukumail

# 同期クライアント
c = kukumail.SyncClient(session_hash="", proxy="https://localhost:8080")

# アカウント登録
if c.me() == {}:
    print(c.register())

# メールアドレス生成
email = c.generate_random_email()
print(email)

# メール受信
print(c.recv_email(email))

# メールアドレス一覧
print(c.get_address())

# メールアドレス削除
c.delete_email(email)

# 利用可能なドメイン一覧
print(c.get_domains())
```

### 非同期版
```python
import asyncio
import kukumail

async def main():
    # 非同期クライアント
    c = kukumail.AsyncClient(session_hash="", proxy="https://localhost:8080")
    
    # アカウント登録
    if c.me() == {}:
        result = await c.register()
        print(result)
    
    # メールアドレス生成
    email = await c.generate_random_email()
    print(email)
    
    # メール受信
    emails = await c.recv_email(email)
    print(emails)
    
    # セッション終了
    await c.close()

# 実行
asyncio.run(main())
```

### CLI使用例
```bash
# アカウント登録
python -m kukumail.cli --register

# メールアドレス生成
python -m kukumail.cli --generate

# 非同期でメールアドレス生成
python -m kukumail.cli --async-mode --generate

# メールアドレス一覧表示
python -m kukumail.cli --list

# メール受信
python -m kukumail.cli --receive "example@nyasan.com"

# カスタムメールアドレス生成
python -m kukumail.cli --generate --domain "nyasan.com" --address "test"
```

## 設定ファイル

`kukumail_config.json`ファイルで設定を管理できます。

```json
{
  "session_hash": null,
  "proxy": null,
  "auto_save_session": true,
  "log_level": "INFO",
  "timeout": 30,
  "retry_count": 3,
  "domains": ["nyasan.com", "kuku.lu"],
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

## ログ機能

```python
from kukumail import Logger

logger = Logger(level="INFO", log_file="kukumail.log")
logger.info("メールアドレス生成開始")
logger.log_email_generated("test@nyasan.com")
```

## インストール

```bash
pip install -r requirements.txt
```