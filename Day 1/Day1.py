import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

urls = [
    'https://www.bbc.com/news',
    'https://www.cnn.com/',
    'https://www.nytimes.com/',
    'https://www.theguardian.com/international',
    'https://www.reuters.com/news/world'
]

articles = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles += soup.find_all('article')

data = []
for article in articles:
    article_url = article.find('a')['href']
    if not article_url.startswith('http'):
        article_url = f'https://{urlparse(url).netloc}{article_url}'

    title = article.find('h3')
    if title:
        title = title.text.strip()

    date = article.find('time')
    if date:
        try:
            date = datetime.strptime(date['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            date = None

    author = article.find('span', class_='c-byline__name')
    if author:
        author = author.text.strip()

    content = ''
    content_url = article_url
    content_response = requests.get(content_url)
    content_soup = BeautifulSoup(content_response.content, 'html.parser')
    paragraphs = content_soup.find_all('p')
    for paragraph in paragraphs:
        content += paragraph.text

    data.append({
        'title': title,
        'date': date,
        'author': author,
        'content': content,
        'url': article_url
    })

df = pd.DataFrame(data)
print(df.head())
