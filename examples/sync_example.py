from kukumail import SyncClient, Config, Logger

def main():
    # ログ設定
    logger = Logger(level="INFO", log_file="sync_example.log")
    logger.info("同期版使用例開始")
    
    # 設定読み込み
    config = Config()
    
    # 同期クライアント作成
    client = SyncClient(
        session_hash=config.get("session_hash"),
        proxy=config.get("proxy")
    )
    
    try:
        # アカウント登録（セッションがない場合）
        if client.me() == {}:
            logger.info("アカウント登録を開始")
            result = client.register()
            logger.log_session_created(result["username"])
            print(f"登録成功: {result}")
            
            # セッション情報を保存
            config.update_session(
                result["session_hash"],
                result["username"],
                result["password"]
            )
        else:
            print("既存のセッションを使用")
        
        # ランダムメールアドレス生成
        logger.info("ランダムメールアドレス生成")
        email = client.generate_random_email()
        if email:
            logger.log_email_generated(email)
            print(f"生成されたメールアドレス: {email}")
        
        # カスタムメールアドレス生成
        logger.info("カスタムメールアドレス生成")
        custom_email = client.generate_email("nyasan.com", "testuser")
        if custom_email:
            logger.log_email_generated(custom_email)
            print(f"カスタムメールアドレス: {custom_email}")
        
        # メールアドレス一覧取得
        logger.info("メールアドレス一覧取得")
        addresses = client.get_address()
        print(f"メールアドレス一覧 ({len(addresses)}件):")
        for i, addr in enumerate(addresses, 1):
            print(f"{i}. {addr}")
        
        # 利用可能なドメイン一覧取得
        logger.info("利用可能なドメイン一覧取得")
        domains = client.get_domains()
        print(f"利用可能なドメイン ({len(domains)}件):")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        # メール受信（最初のメールアドレスで）
        if addresses:
            logger.info("メール受信開始")
            emails = client.recv_email(addresses[0])
            if emails:
                logger.log_email_received(addresses[0], len(emails))
                print(f"受信メール ({len(emails)}件):")
                for i, mail in enumerate(emails, 1):
                    print(f"{i}. 件名: {mail['subject']}")
                    print(f"   送信者: {mail['from']}")
                    print(f"   本文: {mail['body'][:100]}...")
                    print()
            else:
                print("受信メールがありません")
        
        # メールアドレス削除（テスト用）
        if addresses:
            logger.info("メールアドレス削除テスト")
            success = client.delete_email(addresses[0])
            logger.log_email_deleted(addresses[0], success)
            print(f"削除結果: {'成功' if success else '失敗'}")
        
    except Exception as e:
        logger.log_error("メイン処理", e)
        print(f"エラーが発生しました: {e}")
    
    finally:
        # セッション終了
        client.close()
        logger.info("同期版使用例終了")

if __name__ == "__main__":
    main() 