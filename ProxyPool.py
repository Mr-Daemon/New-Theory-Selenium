import json
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime


def get_proxy_ip():
    database = sqlite3.connect('database.sqlite')
    cur = database.cursor()
    cur.execute('''SELECT ip_address,id
                   FROM ip_pool
                   WHERE used==FALSE
                   LIMIT 1;''')
    record = cur.fetchall()
    database.execute('''UPDATE ip_pool
                    SET used=TRUE
                    WHERE id=?''', (record[1],))
    return record[0]


BASE_URL = 'https://ip.jiangxianli.com/?page='

if __name__ == '__main__':
    connect = sqlite3.connect('database.sqlite')
    connect.execute('DELETE FROM ip_pool;')
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
                connect.execute('INSERT INTO ip_pool VALUES(?, ?, ?, ?)',
                                (proxy, False, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count))
                connect.commit()
        page += 1
