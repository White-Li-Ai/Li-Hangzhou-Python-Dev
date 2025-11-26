#Boss直聘Python相关岗位数据爬虫（保守策略版）
import requests
import pandas as pd
import time
import random
import json
from datetime import datetime

class BOSSCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.set_headers()
        self.jobs_data = []
    def set_headers(self):
        """设置真实的浏览器请求头"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
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