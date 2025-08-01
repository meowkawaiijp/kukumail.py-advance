import asyncio
from kukumail import AsyncClient, Config, Logger

async def main():
    # ログ設定
    logger = Logger(level="INFO", log_file="async_example.log")
    logger.info("非同期版使用例開始")
    
    # 設定読み込み
    config = Config()
    
    # 非同期クライアント作成
    client = AsyncClient(
        session_hash=config.get("session_hash"),
        proxy=config.get("proxy")
    )
    
    try:
        # アカウント登録（セッションがない場合）
        if client.me() == {}:
            logger.info("アカウント登録を開始")
            result = await client.register()
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
        
        # 複数のメールアドレスを並行生成
        logger.info("複数メールアドレス並行生成")
        tasks = []
        for i in range(3):
            task = client.generate_random_email()
            tasks.append(task)
        
        emails = await asyncio.gather(*tasks, return_exceptions=True)
        for i, email in enumerate(emails, 1):
            if isinstance(email, Exception):
                logger.log_error(f"メールアドレス生成{i}", email)
                print(f"メールアドレス{i}生成失敗: {email}")
            elif email:
                logger.log_email_generated(email)
                print(f"メールアドレス{i}: {email}")
        
        # カスタムメールアドレス生成
        logger.info("カスタムメールアドレス生成")
        custom_email = await client.generate_email("nyasan.com", "asyncuser")
        if custom_email:
            logger.log_email_generated(custom_email)
            print(f"カスタムメールアドレス: {custom_email}")
        
        # メールアドレス一覧取得
        logger.info("メールアドレス一覧取得")
        addresses = await client.get_address()
        print(f"メールアドレス一覧 ({len(addresses)}件):")
        for i, addr in enumerate(addresses, 1):
            print(f"{i}. {addr}")
        
        # 利用可能なドメイン一覧取得
        logger.info("利用可能なドメイン一覧取得")
        domains = await client.get_domains()
        print(f"利用可能なドメイン ({len(domains)}件):")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        # 複数のメールアドレスで並行受信
        if addresses:
            logger.info("複数メールアドレス並行受信")
            receive_tasks = []
            for email in addresses[:3]:  # 最初の3つでテスト
                task = client.recv_email(email)
                receive_tasks.append(task)
            
            results = await asyncio.gather(*receive_tasks, return_exceptions=True)
            for i, result in enumerate(results, 1):
                if isinstance(result, Exception):
                    logger.log_error(f"メール受信{i}", result)
                    print(f"メール受信{i}失敗: {result}")
                elif result:
                    logger.log_email_received(addresses[i-1], len(result))
                    print(f"メールアドレス{i}受信 ({len(result)}件):")
                    for j, mail in enumerate(result, 1):
                        print(f"  {j}. 件名: {mail['subject']}")
                        print(f"     送信者: {mail['from']}")
                        print(f"     本文: {mail['body'][:50]}...")
                    print()
        
        # メールアドレス削除（テスト用）
        if addresses:
            logger.info("メールアドレス削除テスト")
            success = await client.delete_email(addresses[0])
            logger.log_email_deleted(addresses[0], success)
            print(f"削除結果: {'成功' if success else '失敗'}")
        
    except Exception as e:
        logger.log_error("メイン処理", e)
        print(f"エラーが発生しました: {e}")
    
    finally:
        # セッション終了
        await client.close()
        logger.info("非同期版使用例終了")

if __name__ == "__main__":
    asyncio.run(main()) 