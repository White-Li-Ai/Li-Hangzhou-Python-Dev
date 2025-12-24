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
        """
        print(f"开始爬取{city}Python相关岗位数据...")
        for page in range(1,max_pages + 1):
            print(f"正在爬取第{page}页...")
            try:
                #随机延时3-8秒
                delay = random.uniform(3,8)
                time.sleep(delay)

                #这里使用模拟数据代替真实请求（避免立即被封）
                page_data = self._get_mock_page_data(page,city)
                self.jobs_data.extend(page_data)
                print(f"第{page}页获取成功，获得{len(page_data)}条数据")
                #每爬一页保存一次，防止数据丢失
                self.save_to_csv()
            #异常检查
            except Exception as e:
                print(f"第{page}页爬取失败：{e}")
                break
        print(f"\n 爬取完成，共获得{len(self.jobs_data)}条岗位数据")
        return self.jobs_data
    def _get_mock_page_data(self,page,city):
        """生成模拟数据（用于测试分析流程）"""
        #这些是真实杭州互联网公司
        companies = ['阿里巴巴','网易','字节跳动','华为杭州研究所','海康威视',
                     '滴滴杭州','蘑菇街','有赞','同花顺','恒生电子']
        positions = ['Pyhton开发工程师','后端开发工程师(Python)','Python全栈工程师',
                     '数据开发工程师(Python)','AI算法工程师(Pyhton)',
                     'Python爬虫工程师']
        #生成一页模拟数据
        page_data = []
        #每页10条
        for i in range(10):
            job = {
                '职位名称':random.choice(positions),
                '公司名称':random.choice(companies),
                '薪资范围':f"{random.randint(15,25)}k-{random.randint(25,40)}k",
                '工作经验':f"{random.randint(1,5)}年",
                '学历要求':random.choice(['本科','大专','硕士']),
                '公司地点':f"{city}{random.choice(['余杭区','西湖区','滨江区','萧山区'])}",
                '技能要求':'Python,Django,Flask,MySQL,Linux',
                '福利待遇':'五险一金，补充医疗保险，年终奖，带薪年假',
                '数据来源':'BOSS直聘',
                '爬取时间':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            page_data.append(job)
        return page_data
    def save_to_csv(self):
        """保存数据到CSV文件"""
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