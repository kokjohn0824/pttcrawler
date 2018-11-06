import time
from datetime import datetime
import requests
import time
import sys
import threading
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


Board = ''
payload = {
    'from': '/bbs/' + Board + '/index.html',
    'yes': 'yes'
}
# print(dict(payload))


def getPageNumber(content):
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5: endIndex]
    return pageNumber


# def User_input(Board, ParsingPage):
#     Board = input(str('請輸入版名'))
#     ParsingPage = input(str('請輸入要抓取的頁數'))
#     return Board, ParsingPage


def execution():
    Board = input(str('請輸入版名'))
    ParsingPage = input(str('請輸入要抓取的頁數'))
    print("start parsing [" + Board + "]...")
    start_time = time.time()
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    res = rs.get('https://www.ptt.cc/bbs/' + Board + '/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    ALLpageURL = soup.select('.btn.wide')[1]['href']
    # print(ALLpageURL)
    Allpage = int(getPageNumber(ALLpageURL)) + 1
    print('Total pages:', Allpage)
    URLlist = []
    fileName = 'PttData-' + Board + '-' + datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
    for index in range(Allpage, Allpage - int(ParsingPage), -1):
        url = 'https://www.ptt.cc/bbs/' + Board + '/index' + str(index) + '.html'
        res = rs.get(url, verify=False)
        # print("正在獲取"+str(url)+'...')
        soup = BeautifulSoup(res.text, 'html.parser')
        UrlPer = []
        for entry in soup.select('.r-ent'):
            atag = entry.select('.title')[0].find('a')
            if atag is not None:
                URL = atag['href']
                UrlPer.append('https://www.ptt.cc' + URL)
                # print(list(UrlPer))
        for URL in reversed(UrlPer):
            URLlist.append(URL)
        # print(list(URLlist))

    strNext = u"\n\n\n\n*************** 下一篇 ***************\n\n\n\n\n";
    content = ''

    for URL in URLlist:
        res = rs.get(URL, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.select('.bbs-screen.bbs-content')[0].text
        content += (data + strNext)
        time.sleep(0.05)
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(content)
    print(u'====================END====================')
    print(u'execution time:' + str(time.time() - start_time) + 's')


# python pttCrawer.py
def main():
    try:
        Board = str(sys.argv[1])
        """↑在python終端機內輸入的板名"""
        ParsingPage = int(sys.argv[2])
        """↑在python終端機內輸入要抓取的頁數"""
    except IndexError:
        print("前置變量錯誤，請在下方重新輸入要搜索的板名及抓取頁數")
    execution()
    print(time.monotonic())



if __name__ == '__main__':
    main()

