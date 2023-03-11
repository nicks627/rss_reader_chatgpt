import feedparser
import requests
import pandas as pd
import openai
from bs4 import BeautifulSoup

openai_key = "API_KEY"
openai.api_key = openai_key

system_settings = '''以下のサイトを次の項目で説明してください。
-タイトル-見どころ-詳しい内容
'''

def completion(new_message_text:str, settings_text:str = '', past_messages:list = []):
    if len(past_messages) == 0 and len(settings_text) != 0:
        system = {"role": "system", "content": settings_text}
        past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages
    )
    response_message_text = result.choices[0].message.content
    return response_message_text


dic = {'はてなブックマークテクノ':"http://b.hatena.ne.jp/hotentry/it.rss", 'GIGAZINE':"http://feed.rssad.jp/rss/gigazine/rss_2.0", 'ギズモード':"http://feed.rssad.jp/rss/gigazine/rss_2.0", 'TechCrunch':"http://jp.techcrunch.com/feed/", 'CNET Japan':"http://feed.japan.cnet.com/rss/index.rdf", 'ITmedia':"http://rss.itmedia.co.jp/rss/1.0/topstory.xml", 'ガジェット':"http://getnews.jp/feed", 'ZDNet':"http://feed.japan.zdnet.com/rss/index.rdf"}
# feed = feedparser.parse('https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml')
for n in dic.keys():
    print(n)

site = input("上のサイトから気になるサイトを選んでコピーしてください:")

feed = feedparser.parse(dic[site])

# if len(feed.entries) == 0:
#     print()
for entry in feed.entries:
    print('タイトル:', entry.title)
    print('URL:', entry.link)


url = input("上の気になるサイトのURLをコピーしてください。")

html=requests.get(url).text
soup=BeautifulSoup(html,"html.parser")
for script in soup(["script", "style"]):
    script.decompose()

text=soup.get_text()
#print(text)
lines= [line.strip() for line in text.splitlines()]
text="\n".join(line for line in lines if line)

summary = completion(text)