import requests
from bs4 import BeautifulSoup

# 1 设置目标URL
url = 'https://movie.douban.com/top250'
# 2 发送网络请求，获取网页内容
# 设置一个模拟浏览器的请求头部，防止被网站拒绝
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url,headers=headers)
# 3 检查请求是否成功
if response.status_code == 200:
    print('请求成功.')
# 4 解析网页内容
    soup = BeautifulSoup(response.text,'html.parser')
# 5 查找所有电影条目
    movie_list = soup.find_all('div',class_='info')
# 6 遍历每个条目，提取电影标题和评分
    for movie in movie_list:
        title = movie.find('span',class_='title').text
        rating = movie.find('span',class_='rating_num').text
        print(f'电影：{title}|评分：{rating}')
else:
    print('请求失败，状态码：',response.status_code)

