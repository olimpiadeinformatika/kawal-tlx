import requests
from bs4 import BeautifulSoup
from sqlitedict import SqliteDict


with SqliteDict('./db.sqlite', autocommit=True) as d:
    url = 'https://training.ia-toki.org/submissions/programming/all/?pageIndex={page}&orderDir=asc'
    page = d.get('page', 0)
    while True:
        html = requests.get(url.format(page=page)).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        if len(rows)>0:
            for row in rows:
                cols = [ele.text.strip() for ele in row.find_all('td')]
                score = int(cols[6])
                key = '{}|{}|{}'.format(cols[1], cols[2], cols[3])
                if score > d.get(key, -1):
                    d[key] = score
            d['page'] = page
            print(page)
            page = page+1
        else:
            break

