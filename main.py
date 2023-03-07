import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

# This script aims to provide all links for articles containing desired element - the game coin

app = Flask(__name__)


# @app.route("/")
# def landing():
#     return render_template('./index.html')

@app.route("/")
def landing():
    with open('templates/links.html', 'r') as f:
        links_html = f.read()

    return render_template('index.html', links_html=links_html)

base_url = 'https://www.idnes.cz/zpravy/archiv'
pages_to_check = [''] # add extra pages here move this back = ,'/2','/3','/4'
article_links = []

# This loops through multiple pages on iDNES.cz and searches for a specific element class: art-link
for page in pages_to_check:
    url = base_url + page + '?datum=&idostrova=idnes'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article_links.extend(soup.find_all('a', {'class': 'art-link'}))

# This statement saves the links to .txt file. It is necessary, so I can display the results online, but does not affect
# the rest of the code, so it can be erased and the code will still work
with open('links.txt', 'w') as f:
    for link in article_links:
        f.write(link.get('href') + '\n')

# This loops through
for i, link in enumerate(article_links):
    # print(f"Checking article {i+1}/{len(article_links)}: {link.get('href')}") # This code is correct, but not helpful
    article_page = requests.get(link.get('href'))
    article_soup = BeautifulSoup(article_page.content, 'html.parser')
    image = article_soup.find('img', {'class': 'block full mbrem'})
    if image:
        for img in article_soup.find_all('img', {'class': 'block full mbrem'}):
            print(link.get('href'))
            break

# This section creates the .html content from .txt file
with open('links.txt', 'r') as f:
    links = f.readlines()

links_html = '<ul>\n'
for link in links:
    links_html += f'<li><a href="{link.strip()}">{link.strip()}</a></li>\n'
links_html += '</ul>\n'

with open('templates/links.html', 'w') as f:
    f.write(links_html)
