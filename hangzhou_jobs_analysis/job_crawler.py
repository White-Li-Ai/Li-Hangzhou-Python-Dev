#Boss直聘Python相关岗位数据爬虫（保守策略版）采用保守策略，避免过于激进的爬取导致IP被封

import requests        #导入request库，用于发送http请求
import pandas as pd    #导入pandas库，用于数据处理和存储
import time            #导入time库，用于控制请求间隔和延时
import random          #导入random库，用于生成随即延时，模拟人类操作
import json            #导入json库，用于JSON数据处理
from datetime import datetime  #导入datetime模块，用于获取当前时间戳

#定义BOSSCrawler类，采用面向对象编程oop设计，类的好处：封装爬虫逻辑，便于维护和拓展，可以创建多个实例
class BOSSCrawler:
    #__init__是类的构造函数，在创建类实例时自动调用
    def __init__(self):
        #创建request.Session()对象
        #Session可以保持会话状态，自动处理cookies，比单独的requests.get（）更高效
        self.session = requests.Session()
        #调用set_headers方法设置请求头
        self.set_headers()
        #初始化jobs_data列表，用于存储爬取到的所有岗位数据
        #使用列表存储字典，每个字典代表一个岗位的信息
        self.jobs_data = []
    def set_headers(self):
        """设置真实的浏览器请求头"""
        #使用session.headers.update（）方法批量更新请求头，模拟真实浏览器访问，减少被识别为爬虫的风险
        self.session.headers.update({
            #user-agent：浏览器标识，是最重要的反爬虫伪装
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            #accept：告诉服务器客户端可以接受的内容类型，application/json：优先接受json格式，text/plain，*/* ：也可以接收纯文本和其他所有类型
            'Accept': 'application/json, text/plain, */*',
            #语言偏好，中文优先，英文其次
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            #accept-encoding：支持的压缩格式 支持gzip，deflate，brotli压缩
            'Accept-Encoding': 'gzip, deflate, br',
            #connection：连接方式，keep-alive表示保持长连接
            'Connection': 'keep-alive',
            #referer来源页面，模拟从boss直聘官网跳转而来
            'Referer': 'https://www.zhipin.com/',
        })
    def crawl_pyhton_jobs(self,city='杭州',max_pages=3):
        """
        爬取Python相关岗位
        保守策略：先少量爬取，验证可行性
        参数:city(str)目标城市，默认为杭州 max_pages(int):最大爬取页数,默认为3页(保守策略)
        返回:list:包含所有爬取到的岗位数据的列表
        """
        #打印开始爬取的提示信息
        print(f"开始爬取{city}Python相关岗位数据...")
        #使用for循环遍历每一页，range(1,max_pages+1)生成从1到max_pages的整数 eg:max_pages=3，循环1，2，3
        for page in range(1,max_pages + 1):
            #显示当前爬取的页码
            print(f"正在爬取第{page}页...")
            #使用try-expect结构捕获爬取过程中可能出现的异常
            try:
                #随机延时3-8秒：模拟人类浏览行为，避免请求频率过高被封ip；random.uniform（3，8）随机生成3-8之间的瑞吉浮点数(秒)
                delay = random.uniform(3,8)
                #time.sleep()：程序暂停指定秒数
                time.sleep(delay)
                #这种延时策略是反爬虫的基本手段之一
                #这里使用模拟数据代替真实请求（避免立即被封），调用私有方法_get_mock_page_data生成模拟数据；保守策略：先用模拟数据测试流程，避免真实请求触发反爬
                page_data = self._get_mock_page_data(page,city)
                #将当前页获取的数据添加到总数据列表中；extend()：将page_data列表中的所有元素添加到self.jobs_data末尾；与append区别：append()添加整个列表作为单个元素，extend()展开添加
                self.jobs_data.extend(page_data)
                #打印当前页爬取成功的反馈信息
                print(f"第{page}页获取成功，获得{len(page_data)}条数据")
                #每爬一页保存一次，防止数据丢失 数据持久化策略：即使后续爬取出错，已经爬取的数据不会丢失
                self.save_to_csv()
            #异常处理：捕获爬取过程中可能出现的任何异常
            except Exception as e:
                #打印错误信息，包含页码和具体错误
                print(f"第{page}页爬取失败：{e}")
                #break：终止循环，不再继续爬取后续页面 保守策略：一旦出错就停止，避免触发更严格的反爬机制
                break
        #循环结束后，打印爬取总结信息
        print(f"\n 爬取完成，共获得{len(self.jobs_data)}条岗位数据")
        #返回爬取到的所有数据
        return self.jobs_data
    def _get_mock_page_data(self,page,city):
        """生成模拟数据（用于测试分析流程）参数：page(int)当前页码；city（str）目标城市名称 返回list包含10个模拟岗位数据的列表"""
        #私有方法，表示仅在类内部使用
        #定义杭州真实存在的互联网公司列表
        companies = ['阿里巴巴','网易','字节跳动','华为杭州研究所','海康威视',
                     '滴滴杭州','蘑菇街','有赞','同花顺','恒生电子']
        #定义pyhton常见的相关岗位名称
        positions = ['Pyhton开发工程师','后端开发工程师(Python)','Python全栈工程师',
                     '数据开发工程师(Python)','AI算法工程师(Pyhton)',
                     'Python爬虫工程师']
        #初始化当前页的模拟数据列表，这个列表将存储10个模拟的岗位信息字典
        page_data = []
        #循环生成10条模拟数据，模拟boss直聘每页显示10个岗位，range（10）生成0-9数字，循环10次
        for i in range(10):
            #创建一个岗位信息的字典
            job = {
                #从positions列表中随机选择一个
                '职位名称':random.choice(positions),
                #从companies列表中随机选择一个
                '公司名称':random.choice(companies),
                #随机生成薪资范围
                '薪资范围':f"{random.randint(15,25)}k-{random.randint(25,40)}k",
                #随机生成工作经验年限
                '工作经验':f"{random.randint(1,5)}年",
                #随机生成学历要求
                '学历要求':random.choice(['本科','大专','硕士']),
                #随机生成公司地点
                '公司地点':f"{city}{random.choice(['余杭区','西湖区','滨江区','萧山区'])}",
                #以下字符串是固定的，模拟真实岗位的技能描述
                '技能要求':'Python,Django,Flask,MySQL,Linux',
                '福利待遇':'五险一金，补充医疗保险，年终奖，带薪年假',
                '数据来源':'BOSS直聘',
                #记录数据生成的时间戳 datetime.now()以获取当前的时间
                '爬取时间':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            #将生成的岗位字典添加到当前页的数据列表中，用oppend()方法将job字典作为一个元素添加到page_data列表末尾
            page_data.append(job)
        #返回包含10个模拟岗位数据的列表
        return page_data
    def save_to_csv(self):
        """保存数据到CSV文件中
        功能：将当前爬取到岗位数据保存为csv格式的文件
        """
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            df.to_csv('hangzhou_python_jobs.csv',index=False,encoding='utf-8-sig')
    def get_data_summary(self):
        """数据总览"""
        if not self.jobs_data:
            return "暂无数据"
        df = pd.DataFrame(self.jobs_data)
        summary = f"""
    数据概览：
    总岗位数：{len(df)}
    公司数量：{df['公司名称'].nunique()}
    职位类型：{df['职位名称'].nunique()}种
    平均薪资范围：{df['薪资范围'].iloc[0]}
    最新爬取时间：{df['爬取时间'].iloc[0]}
        """
        return summary
def main():
    """主函数"""
    crawler = BOSSCrawler()
    #爬取数据
    jobs_data = crawler.crawl_pyhton_jobs(city='杭州',max_pages=2)
    #显示数据概览
    print(crawler.get_data_summary())
    #保存最终数据
    crawler.save_to_csv()
    print("数据已保存至：hangzhou_python_jobs.csv")
if __name__ == "__main__":
    main()