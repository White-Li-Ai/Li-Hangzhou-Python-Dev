#真实挑战BOSS直聘爬虫尝试版
import requests
import pandas as pd
import time
import random
import json
from datetime import datetime

class BOSSChallengeCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.set_realistic_headers()
        self.jobs_data = []
    def set_realistic_headers(self):
        """设置更真实的请求头"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.zhipin.com/web/geek/job?query=Python&city=101210100',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
        })
    def crawl_with_real_strategy(self,city_code='101210100',keyword='Python',max_pages=3):
        """
        使用真实爬取策略
        """
        print(f"开始进行真实BOSS直聘数据爬取...")
        print(f"目标：{keyword}岗位 in 杭州")
        success_pages = 0
        for page in range(1,max_pages + 1):
            print(f"\n尝试第{page}页...")
            try:
                #真实的延时策略
                delay = random.uniform(8,15)
                print(f"等待{delay:.1f}秒模拟人类行为...")
                time.sleep(delay)
                #使用BOSS直聘的Geek接口
                url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
                params = {
                    'scene':'1',
                    'query':keyword,
                    'city':city_code,
                    'page':page,
                    'pageSize':'30'
                }
                print(f"请求URL:{url}")
                print(f"参数：{params}")
                response = self.session.get(url,timeout=15)
                print(f"响应状态：{response.status_code}")
                if response.status_code == 200:
                    raw_data = response.text
                    print(f"原始响应长度：{len(raw_data)}字符")
                    #尝试解析JSON
                    try:
                        data = response.json()
                        print(f"JSON解析：{data.get('code','无code字段')}")
                        if data.get('code') == 0:
                            jobs = data.get('zpData',{}).get('jobList',[])
                            print(f"成功解析到{len(jobs)}个岗位")
                            for job in jobs:
                                job_info = self.parse_job_detail(job)
                                if job_info:
                                    self.jobs_data.append(job_info)
                                    print(f"{job_info['公司名称']} - {job_info['职位名称']}")
                            success_pages += 1
                            print(f"第{page}页爬取成功！")
                        else:
                            error_msg = data.get('message','未知错误')
                            print(f"API错误：{error_msg}")
                            self.analyze_block_reason(response)
                            break
                    except json.JSONDecodeError as e:
                        print(f"JSON解析失败:{e}")
                        self.analyze_html_response(raw_data)
                        break
                elif response.status_code == 403:
                    print("访问被拒绝(403) - 可能出发了反爬虫")
                    self.analyze_block_reason(response)
                    break
                else:
                    print(f"HTTP错误：{response.status_code}")
                    break
            except requests.exceptions.Timeout:
                print("请求超时")
            except requests.exceptions.ConnectionError:
                print("连接错误")
            except Exception as e:
                print(f"未知错误：{e}")
                break
        print(f"\n{'='*50}")
        print(f"挑战结果统计：")
        print(f"成功页数：{success_pages}/{max_pages}")
        print(f"获取岗位：{len(self.jobs_data)}个")
        print(f"成功率:{(success_pages/max_pages)*100:.1f}%")
        return self.jobs_data
    def parse_job_detail(self,job):
        """详细解析岗位信息"""
        try:
            #提取薪资（处理13k-26k格式）
            salary = job.get('salaryDesc','面议')
            if salary != '面议':
                try:
                    low,high = map(lambda x:int(x.replace('k','')),salary.split('-'))
                    avg_salary = (low + high) / 2
                except:
                    avg_salary = 0
            else:
                avg_salary = 0
            return{
                '职位名称':job.get('jobName',''),
                '公司名称':job.get('brandName',''),
                '薪资范围':salary,
                '平均薪资':avg_salary,
                '工作经验':job.get('jobExperience',''),
                '学历要求':job.get('jobDegree',''),
                '公司地点':f"{job.get('cityName','')}{job.get('areaDistrict','')}",
                '技能标签':','.join(job.get('skills',[])),
                '福利待遇':','.join(job.get('welfareList',[])),
                '行业领域':job.get('brandIndustry',''),
                '公司规模':job.get('brandScaleName',''),
                '数据来源':'BOSS直聘',
                '爬取时间':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"解析失败：{e}")
            return None
    def analyze_block_reason(self,response):
        """分析被封锁原因"""
        print(f"\n反爬虫分析：")
        print(f"响应头:{dict(response.headers)}")
        print(f"响应内容前500字符:{response.text[:500]}")
        if '验证码' in response.text:
            print("检测到验证码挑战")
        if 'access denied' in response.text.lower():
            print("访问被明确拒绝")
        if 'robot' in response.text.lower():
            print("被识别为机器人")
    def analyze_html_response(self,html_content):
        """分析HTML响应内容"""
        if len(html_content) < 1000:
            print(f"简短响应：{html_content}")
        else:
            print(f"响应类型：HTML页面(长度:{len(html_content)})")
            if '<title>' in html_content:
                title_start = html_content.find('<title>') + 7
                title_end = html_content.find('<title>')
                if title_end > title_start:
                    print(f"页面标题：{html_content[title_start:title_end]}")
    def save_results(self):
        """保存结果"""
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            filename = f'boss_real_jobs_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
            df.to_csv(filename,index=False,encoding='utf-8-sig')
            print(f"数据已保存：{filename}")
            #数据洞察
            print(f"\n数据洞察:")
            print(f"公司数量：{df['公司名称'].nunique()}")
            print(f"最高薪资:{df[df['平均薪资']>0]['平均薪资'].max() if len(df[df['平均薪资']>0])>0 else 0}k")
            print(f"热门技能:{','.join(df['技能标签'].str.split(',').explode().value_counts().head(3).index.tolist())}")
        else:
            print("无数据可保存")
def main():
    """主函数"""
    print("BOSS直聘真实爬虫挑战")
    print("注意：这是一个真实爬虫，可能会遇到各种的反爬措施")
    print("如果失败，将分析每次失败的原因\n")
    crawler = BOSSChallengeCrawler()
    #开始挑战
    input("按Enter键开始挑战...")
    jobs_data = crawler.crawl_with_real_strategy(
        city_code='101210100', #杭州
        keyword='Python',
        max_pages=3
    )
    #保存结果
    crawler.save_results()
    #挑战总结
    if jobs_data:
        print(f"\n挑战成功！获得{len(jobs_data)}条真实数据")
        print("这些真实数据将为项目增加巨大价值.")
    else:
        print(f"\n 没拿到数据，但尝试很有价值！")
        print("分析了反爬机制，是成为爬虫专家的必经之路")
if __name__ == "__main__":
    main()


