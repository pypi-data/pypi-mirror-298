import time
import httpx

def scrap():
    url = 'https://api.bilibili.com/x/web-interface/popular'
    params = {
        'pn': 1,
        'ps': 10
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    proxies = {
        'http://': None, 'https://': None
    }
    r = httpx.get(url=url, headers=headers, params=params, proxies=proxies, timeout=10)
    r.raise_for_status()
    return r.json()

def parse(json_dict):
    bilibili_res = []
    data = json_dict.get('data').get('list')

    for item in data:
        bilibili_res.append({
            'title': item.get('title'),
            'description': item.get('desc'),
            'publish_datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item.get('pubdate'))),
            'publish_location': item.get('pub_location'),
            'url': item.get('short_link_v2')
        })

    return bilibili_res

if __name__ == '__main__':
    from itertools import groupby, count

    with open('location.txt', 'r', encoding='utf-8') as f:
        locations = f.read().split('\n')
        print(locations)
        d = {}
        for location in locations:
            d[location] = d.get(location, 0) + 1
        a = sorted(d.items(), key=lambda x: -x[1])
        for k, v in a:
            if k == 'None':
                continue
            print(k, v)
