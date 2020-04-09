import json
import requests
from bs4 import BeautifulSoup


def get_proxy_ip():
    with open('ip_pool.json', 'r') as file:
        dictionary = json.load(file)
        for wrapper in dictionary:
            if not wrapper['used']:
                target = wrapper['ip']
                wrapper['used'] = True
                break
    with open('ip_pool.json', 'w') as file:
        json.dump(dictionary, file, sort_keys=True, indent=4)
    return target


BASE_URL = 'https://ip.jiangxianli.com/?page='

if __name__ == '__main__':
    with open('ip_pool.json', 'w') as f:
        proxy_array = list()
        count = 0
        page = 1
        while page < 15 and count < 100:
            soup = BeautifulSoup(requests.get(BASE_URL + str(page)).content)
            print('current page: ' + str(page))
            print('current count: ' + str(count))
            for tr in soup.find_all('tr')[1:]:
                if tr.contents[5].text == '中国':
                    print(tr.text)
                    proxy = tr.contents[0].text + ':' + tr.contents[1].text
                    count += 1
                    proxy_array.append({'ip': proxy, 'used': False})
            page += 1
        json.dump(proxy_array, f, sort_keys=True, indent=4)
