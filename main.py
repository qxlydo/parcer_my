import time
import requests
import json
from bs4 import BeautifulSoup


def generate_url(page_num):
    return f"https://hololist.net/top/page/{page_num}/"

def parse_vtubers(url):
    # отправляем запрос с заголовками по нужному адресу
    req = requests.get(url)
    # считываем текст HTML-документа
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')

    # Найти все элементы с классом "col-12 col-sm-6 col-lg-4"
    vtuber_cards = soup.find_all('div', class_='col-12 col-sm-6 col-lg-4')

    vtubers = []
    for vtuber_card in vtuber_cards:
        # Извлечение имени
        name = vtuber_card.find('span', itemprop='name').text.strip()
        subscribers = vtuber_card.find('div', itemprop='subscribers').text.strip()
        vtubers.append({'name': name, 'subscribers': subscribers})

    return vtubers

def main():
    vtubers = []
    page_num = 1
    while True:
        url = generate_url(page_num)
        print(f"Parsing page: {page_num}")
        page_vtubers = parse_vtubers(url)
        vtubers.extend(page_vtubers)

        # где 68 конечная страница
        page_num += 1
        if page_num == 68:
            break
        time.sleep(.1)  # Добавляем задержку, чтобы не перегружать сервер
        
    data = {}
    data["vtuname"] = []
    
    # Вывод результатов
    for i, vtuber in enumerate(vtubers, start=1):
        print(f"{i}. Name: {vtuber['name']}, Subscribers: {vtuber['subscribers']}")
        print("-----")
        
        data["vtuname"].append({'name': vtuber["name"], 'sub': vtuber["subscribers"]})
        
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        
        

if __name__ == "__main__":
    main()
