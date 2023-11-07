from quart import Quart, websocket, send_from_directory, abort
from urllib.parse import parse_qs
import asyncio

app = Quart(__name__)

@app.websocket('/ws')
async def ws():
    query_params = parse_qs(websocket.query_string.decode())
    token = query_params.get("token", [None])[0]
    print(f"token: {token}")

    if token:
        abort(401)

    # クライアントに接続確立時のメッセージを送信
    await websocket.send("Connection established")
    print("Connection established")

    # クライアントからのメッセージを待ち受け、エコーとして返す
    while True:
        try:
            message = await websocket.receive()
            await websocket.send(f"Echo: {message}")
        except:
            # WebSocket接続が閉じられた場合やエラーが発生した場合の処理
            print("Connection closed")
            break

@app.route('/')
async def index():
    # 静的ファイルへのパスを適切に設定してください
    return await send_from_directory('static', 'index.html')

@app.route('/<path:path>')
async def static_file(path):
    # 静的ファイルへのパスを適切に設定してください
    return await send_from_directory('static', path)

if __name__ == "__main__":
    # コマンドラインで直接スクリプトを実行する場合、
    # 以下のコードは不要で、代わりに以下のコマンドを使用してサーバーを起動します。
    # $ hypercorn filename:app -k asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    config.worker_class = "asyncio"
    app.run(port=8000, use_reloader=False)
