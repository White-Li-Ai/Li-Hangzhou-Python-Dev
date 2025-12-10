#增强版爬虫，爬取完整的T250并保存到CSV文件中以便做数据分析
import requests               #引入requests库发送http请求
from bs4 import BeautifulSoup  #引入html xml数据提取库做页面解析
import time                   #导入time模块，用于爬虫延迟（防止被封ip）和时间截获取等时间相关操作
import pandas as pd            #导入pandas库并重命名为pd，做数据分析和处理的核心库（将爬取的数据保存为csv文件）

def crawl_douban_top250():    #爬取豆瓣电影T250的主函数，功能：遍历10页，爬取所有250电影信息并返回列表 返回值：包含所有电影信息的字典列表
    all_movies = []               #初始化空列表，用于存储所有爬取到的电影信息
    #循环10页。每页25部电影信息，T250共十页
    for page in range(10):    #range(10)生成0-9对应是个页码
        #计算开始页位置：豆瓣使用start参数控制分页，每页25条
        start = page * 25        #第0页start=0 第1页start=25以此类推
        #构造目标URL使用F-string格式化，插入start参数
        url = f'https://movie.douban.com/top250?start={start}&filter='
        #打印爬取进度展示
        print(f'正在爬取第{page+1}页电影信息...')
        #设置请求头，模拟浏览器访问，避免被识别为爬虫
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        #使用try-except捕获可能的异常（网络错误、超时、解析错误等）
        try:
            #发送HTTP GET请求到目标URL headers传递请求头伪装浏览器 timeout=10设置10秒超时，防止长时间等待
            response = requests.get(url,headers=headers,timeout=10)
            #检查HTTP响应状态码是否为200（成功）
            if response.status_code == 200:
                #使用BeautifulSoup解析html响应内容，‘html.parser’是python内置的html解析器
                soup = BeautifulSoup(response.text,'html.parser')
                #检查是否找到了电影列表，查找多有class属性为‘info’的div元素 每个class=‘info’的div都对应一部电影的信息
                movie_list = soup.find_all('div',class_='info')
                #判断时候成功找到电影列表（正常情况下应该有25个）
                if len(movie_list) > 0:
                    #解析当前页的25部电影，遍历每个div电影信息
                    for movie in movie_list:
                        #提取电影中文主标题：查找class=‘tilte’的span标签，获取其文本
                        title = movie.find('span',class_='title').text
                        #提取评分：查找class=‘rating_num’的span标签
                        rating = movie.find('span',class_='rating_num').text
                        #获取评价人数（因为是html结构需要特殊处理）获取该电影区域的所有span标签
                        spans = movie.find_all('span')
                        evaluate = "未知" #默认值，防止找不到时出错
                        #便利所有span标签，查找包含‘人评价’文本
                        for span in spans:
                            if '人评价' in span.text: #判断是否包含关键字
                                evaluate = span.text.replace('人评价','')#去除 人评价 文字 
                                break #找到后立即跳出循环 提高效率
                        #获取引用语（经典台词、短评 有可能不存在）
                        #查找class=inq的span标签
                        quote_element = movie.find('span',class_='inq')
                        #使用三元表达式 如果找到就取文本，否则设为无
                        quote = quote_element.text if quote_element else "无"
                        #将当前电影信息以字典形式添加到总列表
                        all_movies.append({
                            '电影名称':title,
                            '评分':rating,
                            '评价人数':evaluate,
                            '引用语':quote
                        }) 
                    #打印当前页爬取完成信息
                    print(f'第{page+1}页爬取完成，共{len(movie_list)}部电影')
                else:
                    #如果找到了页面但没找到电影列表，可能时页面结构发生了变化，状态码不是200如404 503等
                    print(f'第{page+1}页请求失败，状态码：',response.status_code)
                    #添加延迟，避免请求过快被封ip
                    time.sleep(3) #暂停三秒
        except Exception as e: #捕获所有异常 网络超时、连接错误、解析错误等
            print(f'第{page+1}页抓取出错',e)#打印错误信息
            time.sleep(3)#避免频繁请求 出错后也暂停3秒
    #循环结束，返回包含所有信息的列表
    return all_movies
#执行爬虫程序的流程开始
print('开始抓取豆瓣Top250...')
#调用爬虫函数crawl_douban_top250（），该函数会遍历10页，爬取所有电影信息
#函数返回一个包含250部电影信息的列表，每个元素时一个字典
movie_data = crawl_douban_top250()
#有数据才保存 检查爬虫是否成功获取到数据即列表不为空
if movie_data:
    #显示统计信息 使用f-string格式化输出{len...}会被替换为实际数量
    print(f'\n===抓取完成！共抓取{len(movie_data)}部电影')
    #将电影数据列表转换为panadas dataframe，便于数据分析 
    #dartaframe时pandas的核心数据结构，类似于excel表格
    df = pd.DataFrame(movie_data)
    #将dataframe保存为csv文件，参数说明：douban_...是保存文件名 index=false是不保存dataframe的索引列(0,1,2...) utf-8-sig是使用bom的utf-8编码，确保打开时中文部乱码
    df.to_csv('douban_top250.csv',index=False,encoding='utf-8-sig')
    #提示保存成功
    print('数据已保存到douban_top250.csv')
    #显示前5条数据预览，快速了解数据格式和内容
    print('\n前5部电影信息:')
    #df.head（）返回dataframe的前5行，默认显示所有列
    print(df.head())
else:
    #如果爬虫返回空列表，movie_data为空，说明爬取失败
    print('\n===抓取失败！可能被反爬虫了===')
    #给出排查建议
    print('建议过一段时间再试,或使用代理ip')

