#增强版爬虫，爬取完整的T250并保存到CSV文件中以便做数据分析
import requests               #引入requests库发送http请求
from bs4 import BeautifulSoup
import time
import pandas as pd

def crawl_douban_top250():
    all_movies = []
    #循环10页。每页25部电影信息
    for page in range(10):
        #计算开始页位置
        start = page * 25
        url = f'https://movie.douban.com/top250?start={start}&filter='
        print(f'正在爬取第{page+1}页电影信息...')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        #使用try-except捕获可能的异常
        try:
            response = requests.get(url,headers=headers,timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,'html.parser')
                #检查是否找到了电影列表
                movie_list = soup.find_all('div',class_='info')
                if len(movie_list) > 0:
                    #解析当前页的25部电影
                    for movie in movie_list:
                        title = movie.find('span',class_='title').text
                        rating = movie.find('span',class_='rating_num').text
                        #获取评价人数
                        spans = movie.find_all('span')
                        evaluate = "未知"
                        for span in spans:
                            if '人评价' in span.text:
                                evaluate = span.text.replace('人评价','')
                                break
                        #获取引用语（有可能不存在）
                        quote_element = movie.find('span',class_='inq')
                        quote = quote_element.text if quote_element else "无"

                        all_movies.append({
                            '电影名称':title,
                            '评分':rating,
                            '评价人数':evaluate,
                            '引用语':quote
                        }) 
                    print(f'第{page+1}页爬取完成，共{len(movie_list)}部电影')
                else:
                    print(f'第{page+1}页请求失败，状态码：',response.status_code)
                    #添加延迟，避免请求过快被封ip
                    time.sleep(3)
        except Exception as e:
            print(f'第{page+1}页抓取出错',e)
            time.sleep(3)
    return all_movies
#执行爬虫
print('开始抓取豆瓣Top250...')
movie_data = crawl_douban_top250()
#有数据才保存
if movie_data:
    #显示统计信息
    print(f'\n===抓取完成！共抓取{len(movie_data)}部电影')
    #保存到csv文件
    df = pd.DataFrame(movie_data)
    df.to_csv('douban_top250.csv',index=False,encoding='utf-8-sig')
    print('数据已保存到douban_top250.csv')
    #显示前5条数据预览
    print('\n前5部电影信息:')
    print(df.head())
else:
    print('\n===抓取失败！可能被反爬虫了===')
    print('建议过一段时间再试,或使用代理ip')

