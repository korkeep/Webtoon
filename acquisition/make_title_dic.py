import json
import re
from bs4 import BeautifulSoup

dic = {}

with open('incomplete.html', 'r', encoding='utf-8') as incomp:
    soup = BeautifulSoup(incomp.read(), 'html.parser')
    a_list = soup.select('#content > div.list_area.daily_all > div > div > ul > li > a')
    for a in a_list:
        t_id = re.search(r"Id=(\d+)", a['href']).group(1)
        if t_id not in dic:
            dic[t_id] = a.get_text().strip()

with open('complete.html', 'r', encoding='utf-8') as incomp:
    soup = BeautifulSoup(incomp.read(), 'html.parser')
    dt_list = soup.select('#content > div.list_area > ul > li > dl > dt')
    for dt in dt_list:
        if dt.em is not None:
            continue
        t_id = re.search(r"Id=(\d+)", dt.a['href']).group(1)

        dic[t_id] = dt.a.get_text().strip()

with open('dict.json', 'w', encoding='utf-8') as dic_file:
    json.dump(dic, dic_file, ensure_ascii=False)
with open('titleId.txt', 'w', encoding='utf-8') as id_list:
    for t in dic:
        id_list.write(t + '\n')
print(dic)
