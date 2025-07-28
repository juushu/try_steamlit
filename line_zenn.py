from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, TextMessage
from linebot.v3.messaging.models import PushMessageRequest, BroadcastRequest
from linebot.v3.exceptions import InvalidSignatureError
import feedparser
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "hMW0c2kwwPh0rFRdetEtdVhkugSam1LsjaKEG3iqfEigGj1SgLM9lTJSeayj/GicaTOwC+yfh3/g+Ae0P8JnpsKaQIyH01Q5aFPp35AkEuxkKL1nTTQyvaYVB1PXjY6wMH8L8PY5dftohmAB7PUIlAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "711f833217d44b87a8492ab183f6a362"

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(ApiClient(configuration))

def fetch_zenn_news():
    feed = feedparser.parse("https://zenn.dev/feed")
    messages = []
    for entry in feed.entries:
        keywords = []
        if "生成AI" in entry.title:
            keywords.append("生成AI")
        if "AI" in entry.title:
            keywords.append("AI")
        if keywords:
            # タイトル・リンク・キーワードのみ
            messages.append(f"タイトル: {entry.title}\nリンク: {entry.link}\nキーワード: {', '.join(keywords)}")
    return "\n\n".join(messages) if messages else "本日は生成AI関連の新着記事はありません。"

@app.route("/callback", methods=["POST"])
def callback():
    # v3ではWebhookHandlerは使わず、署名検証を自前で実装
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    # ここで署名検証を実装（省略）
    # イベント処理も自前で実装（省略）
    return "OK"

def push_news():
    news = fetch_zenn_news()
    messaging_api.broadcast(
        BroadcastRequest(
            messages=[TextMessage(text=news)],
            notificationDisabled=False
        )
    )
if __name__ == "__main__":
    push_news()