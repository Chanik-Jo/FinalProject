import requests
from bs4 import BeautifulSoup
isbn="979-11-5839-179-9"
url = 'https://www.nl.go.kr/NL/contents/search.do?' \
      'srchTarget=total&pageNum=1&pageSize=10&kwd={}'.format(isbn)
print("url is \n",url)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
           '537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
response = requests.get(url,headers=headers)


if response.status_code == 200:
    #html = response.text
    html=response.content
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#sub_content > div.content_wrap > div > '
                            'div.integSearch_wrap > div.search_cont_wrap >'
                            ' div > div > div.search_right_section > div.sect'
                            'ion_cont_wrap > div:nth-child(1) > div.cont_list.lis'
                            't_type > div.row > span.txt_left.row_txt_tit > a')
    textTitle = title.get_text()
    print("book name is \n",textTitle)
else :
    print(response.status_code)
