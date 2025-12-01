#BOSS直聘Playwright爬虫（隐身）优化数据提取-增强版
from playwright.sync_api import sync_playwright  #浏览器自动化
import pandas as pd   #数据处理
import time      #时间控制
import random   #随机数生成

class BOSSEnhancedCrawler:
    def __init__(self):
        self.jobs_data = []
    def crawl_enhanced(self):
        """使用隐身模式绕过检测"""
        print("启动BOSS直聘隐身爬虫...")
        with sync_playwright() as p:
            #高级隐身配置
            browser = p.chromium.launch(
                headless= False, #先观察效果  
            )
            #创建隐身上下文
            context = browser.new_context(
                viewport={'width':1920,'height':1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            #隐藏自动化特征
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            page = context.new_page()
            try:
                print("尝试直接访问搜索页面...")
                #直接访问搜索URL（绕过首页）
                success_url = "https://www.zhipin.com/job_detail/?query=Python&city=101210100"
                print(f"访问已验证成功的URL：{success_url}")
                page.goto(success_url,timeout=30000)
                time.sleep(5)
                #模拟人类滚动
                self.similate_human_behavior(page)
                #详细提取数据
                jobs = self.extract_enhanced_jobs(page)
                self.jobs_data.extend(jobs)
            except Exception as e:
                print(f"爬取失败：{e}")
            finally:
                browser.close()
        return self.jobs_data 
    def extract_enhanced_jobs(self,page):
        """增强数据提取-专门优化薪资提取"""
        jobs = []
        try:
            #使用多种选择器尝试
            selectors = [
                '.job-list li',
                '.job-card-wrapper',
                '.job-item'
            ]
            job_elements = []
            for selector in selectors:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"找到{len(elements)}个岗位元素")
                    job_elements = elements
                    break
            for i,element in enumerate(job_elements[:15]): #试前15个
                try:
                    #滚动到元素可见
                    element.scroll_into_view_if_needed()
                    time.sleep(0.3)
                    #获取元素的完整HTML和文本，用于调试
                    full_html = element.inner_html()
                    full_text = element.inner_text()
                    #增强版数据提取
                    job_info = self.extract_detailed_info(element,full_text,i+1)
                    if job_info:
                        jobs.append(job_info)
                except Exception as e:
                    print(f"提取第{i+1}个岗位失败：{e}")
                    continue
        except Exception as e:
            print(f"数据提取失败：{e}")
        return jobs
    def extract_detailed_info(self,element,full_next,index):
        """详细解析岗位信息"""
        try:
            lines = [line.strip() for line in full_next.split('\n') if line.strip()]
            #调试输出完整文本
            print(f"岗位{index}完整文本:{lines}")
            #智能解析各行内容
            company = "未知公司"
            job_name = "未知职位"
            salary = "面议"
            location = "杭州"
            industry = "未知行业"
            #智能解析逻辑
            for i,line in enumerate(lines):
                if '.' in line and '融资' in line:
                    company = lines[i-1] if i > 0 else line.split('.')[0]
                    industry = line
                elif 'k' in line and ('-' in line or '~' in line):
                    salary = line
                elif '杭州' in line:
                    location = line
                elif any(keyword in line for keyword in ['Python','AI','开发','工程师','算法']):
                    job_name = line
            #如果还没找到公司名，取第一行
            if company == "未知公司" and lines:
                company = lines[0]
            job_info = {
                '序号':index,
                '公司名称':company,
                '职位名称':job_name,
                '薪资范围':salary,
                '工作地点':location,
                '行业信息':industry,
                '完整文本':'|'.join(lines),#用于调试
                '数据来源':'BOSS直聘',
                '爬取方式':'Playwright增强版',
                '爬取时间':pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(f"[{index}]{company} - {job_name} - {salary}")
            return job_info
        except Exception as e:
            print(f"解析岗位详情失败：{e}")
            return None
    def similate_human_behavior(self,page):
        """模拟人类浏览行为"""
        print("模拟人类滚动行为...")
        for i in range(3):
            scroll_amount = random.randint(300,600)
            page.mouse.wheel(0,scroll_amount)
            time.sleep(random.uniform(1,2))
    # def try_backup_plan(self,page):
    #     """备用方案：尝试其他URL"""
    #     backup_urls = [
    #         "https://www.zhipin.com/job_detail/?query=Python&city=101210100",
    #         "https://www.zhipin.com/web/geek/job?query=Python"
    #     ]
    #     for url in backup_urls:
    #         try:
    #             print(f"尝试备用URL：{url}")
    #             page.goto(url,timeout=15000)
    #             time.sleep(5)
    #             if 'security-check' not in page.url:
    #                 print("备用URL成功！")
    #                 #提取数据
    #                 jobs = self.extract_detailed_jobs(page)
    #                 self.jobs_data.extend(jobs)
    #                 break
    #         except Exception as e:
    #             print(f"备用URL失败：{e}")
    #             continue
    def save_enhanced_results(self):
        """保存结果"""
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            filename = f'boss_enhanced_jobs.csv'
            df.to_csv(filename,index=False,encoding='utf-8-sig')
            print(f"数据已保存：{filename}")
            #数据统计
            print(f"\n增强版数据概览：")
            print(f"总岗位数：{len(df)}")
            print(f"公司数量：{df['公司名称'].nunique()}")
            print(f"薪资分布：{df['薪资范围'].value_counts().to_dict()}")
            #显示前几条数据
            print(f"\n数据样例：")
            for i,row in df.head(3).iterrows():
                print(f"{row['公司名称']} | {row['职位名称']} | {row['薪资范围']}")
def main():
    print("=" * 60)
    print("BOSS直聘Playwright爬虫（隐身）优化数据提取-增强版")
    print("目标优化数据提取，特别是薪资信息")
    print("=" * 60)
    crawler = BOSSEnhancedCrawler()
    input("按Enter键开始增强版爬虫...")
    data = crawler.crawl_enhanced()
    #保存结果
    crawler.save_enhanced_results()
    if data:
        print(f"\n增强版成功！获得{len(data)}条优化数据！")
        print("这次提取了更完整的数据信息！")
    else:
        print(f"\n继续优化.")
if __name__ == "__main__":
    main()


