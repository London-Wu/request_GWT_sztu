#爬公文通1.0

import requests
from bs4 import BeautifulSoup
import os

class Arctical():
    def __init__(self, ):
# 获取公文通文章，并存储标题及链接
urls=[] #链接
name=[] #标题
url = "http://nbw.sztu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1029"
req = requests.get(url)
main_soup=BeautifulSoup(req.text,'html.parser')
needy_soup=main_soup.find_all(class_="pull-left width04 txt-elise text-left",style="width:54%;")
for child in needy_soup:
    a_name=child.a.string
    a_url=child.a["href"]
    name.append(a_name)
    urls.append(a_url)


print('深圳技术大学公文通：')
for i in range(len(urls)):
    print(f"{i}. {name[i]}")
input_number=int(input("请输入要查询的文章编号:"))
chosen_url = f"http://nbw.sztu.edu.cn/{urls[input_number]}"
os.system(f"start {chosen_url}")