import streamlit as st
import feedparser
import openai
import os

st.title("株ニュース要約Webアプリ")

# OpenAI APIキーはStreamlit Cloudの環境変数で設定済み
api_key = st.secrets["OPENAI_API_KEY"]

keyword = st.text_input("調べたい銘柄名を入力", "トヨタ自動車")

def get_yahoo_news(keyword):
    url = f"https://news.yahoo.co.jp/rss/search?p={keyword}&ei=UTF-8"
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries[:3]:  # 最新3件
        news_list.append(entry.title + "\n" + entry.link)
    return "\n\n".join(news_list)

def summarize_news(news_text, api_key):
    client = openai.OpenAI(api_key=api_key)
    prompt = f"次の株ニュースを初心者にも分かるように3行で要約してください。\n\n{news_text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは優秀な日本語の要約AIです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

if st.button("ニュース取得＆要約"):
    news = get_yahoo_news(keyword)
    if news and api_key:
        summary = summarize_news(news, api_key)
        st.subheader("要約結果")
        st.write(summary)
        st.subheader("元ニュース一覧")
        st.write(news)
    else:
        st.warning("APIキーと銘柄名を入力してください。")
