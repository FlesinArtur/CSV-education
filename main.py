import csv
import requests
from bs4 import BeautifulSoup
import os.path

website = "https://anitube.in.ua/?do=random_anime"
fieldnames = ["title", "url", "information", "description"]


def get_anime_html():
    connect_anime = requests.get(website)
    anime_html = connect_anime.content.decode('utf-8')
    return anime_html


def get_anime_info(anime_html):
    soup = BeautifulSoup(anime_html, 'html.parser')
    anime_url = soup.find("link", rel="canonical").get('href').strip()
    anime_title = soup.find("title").text.replace("аніме українською онлайн", "").strip()
    anime_description = soup.find("div", class_="story_c_text").find(class_="my-text").text.strip()
    anime_information = soup.find("div", class_="story_c_text").find_parent()
    anime_information.find("div", class_="story_c_text").decompose()
    anime_information = anime_information.text.strip("\n").replace("\n\n", "\n")
    return {
        "url": anime_url,
        "title": anime_title,
        "information": anime_information,
        "description": anime_description
    }


def write_anime_info(info):
    print(f'Назва:\n{info["title"]}')
    print(f'Посилання:\n{info["url"]}')
    print(f'Інформація:\n{info["information"]}')
    print(f'Опис:\n{info["description"]}')
    with open("anime_data.csv", 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "url", "information", "description"])
        writer.writerow([info["title"], info["url"], info["information"], info["description"]])


def add_anime_info(info):
    with open("anime_data.csv", 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({
            'title': info['title'],
            'url': info['url'],
            'information': info['information'],
            'description': info['description']
        })


def main():
    html = get_anime_html()
    info = get_anime_info(html)

    if os.path.isfile("anime_data.csv"):
        add_anime_info(info)
    else:
        write_anime_info(info)


if __name__ == '__main__':
    main()
