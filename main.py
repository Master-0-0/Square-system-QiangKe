import requests
from bs4 import BeautifulSoup as BS
import re

def checkhtml(table_html):
    print(len(table_html))
    # 从页面内容中提取表格内容
    table_pattern = re.compile('<table.*?id="DataGrid2".*?>(.*?)</table>', re.S)
    cell_pattern = re.compile('<td.*?>(.*?)</td>', re.S)
    # print(table_html)
    table_match = table_pattern.search(table_html)
    if table_match:
        table_text = table_match.group(1)
        rows = table_text.split('</tr>')
        table_data = []
        for row in rows:
            cells = cell_pattern.findall(row)
            table_data.append(cells)

        # 打印表格
        for row in table_data:
            row_text = [re.sub('<[^>]+>', '', cell) for cell in row]  # 使用正则表达式去掉HTML标签
            print('| ' + ' | '.join(row_text) + ' |')  # 打印去掉HTML标签后的表格
    return 0

def htmltext(text):
    soup = BS(text, 'html.parser')
    table_html = str(soup.find("table", id="DataGrid2"))
    return table_html


def check():
    url = "http://jiaowu.hncst.edu.cn/xf_xsqxxxk.aspx?xh={0}".format(number)
    header = {
        "Referer": "http://jiaowu.hncst.edu.cn/xs_main.aspx?xh={0}".format(number),
        "Cookie": "ASP.NET_SessionId={0}".format(cookie),
    }
    for x in range(1, 100):
        response = requests.get(url, headers=header)
        if len(response.text) > 5000:
            table_html = htmltext(response.text)
            checkhtml(table_html)
            break

def run():
    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "需要自己填写",
        "__VIEWSTATEGENERATOR": "03DFB912",
        "ddl_kcxz": "",
        "ddl_ywyl": "有".encode('gb2312'),
        "ddl_kcgs": "",
        "ddl_xqbs": "1",
        "ddl_sksj": "",
        "TextBox1": "",
        "kcmcGrid:_ctl2:xk": "on",
        "kcmcGrid:_ctl2:jcnr": "|||",
        "dpkcmcGrid:txtChoosePage": "1",
        "dpkcmcGrid:txtPageSize": "15",
        "Button1": "++%CC%E1%BD%BB++"
    }
    url = "http://jiaowu.hncst.edu.cn/xf_xsqxxxk.aspx?xh={0}".format(number)
    header = {
        "Referer": "http://jiaowu.hncst.edu.cn/xs_main.aspx?xh={0}".format(number),
        "Cookie": "ASP.NET_SessionId={0}".format(cookie),
    }
    for x in range(1, 1000):
        try:
            response = requests.post(url, headers=header, data=data)
            print(len(response.text))
            table_html = htmltext(response.text)
            if "return confirm(" in table_html:
                print("----------------------抢课成功-----------------------")
                checkhtml(table_html)
                break
        except requests.exceptions.ConnectionError as e:
            print("远程主机强迫关闭了一个现有的连接")
            continue

number = input("请输入学号：")
cookie = input("请输入Cookie：")
while 1:
    code = input("抢课【2】，验证抢到的课【1】 退出输入其他数字:")
    if str.isdigit(code):
        if code == '1':
            check()
        elif code == '2':
            run()
        else:          
            exit()
    else:
        print("输入的不是数字")
