#BOSS直聘Playwright爬虫（隐身）-真实完整数据提取版
from playwright.sync_api import sync_playwright  #浏览器自动化
import pandas as pd   #数据处理
import time      #时间控制
import random   #随机数生成

class BOSSStealthCrawler:
    def __init__(self):
        self.jobs_data = []
    def crawl_with_stealth(self):
        """使用隐身模式绕过检测"""
        print("启动BOSS直聘隐身爬虫...")
        with sync_playwright() as p:
            #高级隐身配置
            browser = p.chromium.launch(
                headless= False, #先观察效果
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows', 
                    '--disable-renderer-backgrounding'
                ]
            )
            #创建隐身上下文
            context = browser.new_context(
                viewport={'width':1920,'height':1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                bypass_csp=True,
                ignore_https_errors=True
            )
            #隐藏自动化特征
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            page = context.new_page()
            try:
                print("尝试直接访问搜索页面...")
                #直接访问搜索URL（绕过首页）
                search_url = "https://www.zhipin.com/web/geek/job?query=Python&city=101210100"
                page.goto(search_url,timeout=30000,wait_until='networkidle')
                print("页面加载成功，检查是否被拦截...")
                #检查是否在安全验证页面
                if 'security-check' in page.url:
                    print("触发安全验证，尝试手动处理...")
                    input("请手动完成验证后按Enter键继续...")
                else:
                    print("成功绕过安全检测！")
                    #等待页面完全加载
                    time.sleep(5)
                #模拟人类滚动
                self.similate_human_behavior(page)
                #详细提取数据
                jobs = self.extract_detailed_jobs(page)
                self.jobs_data.extend(jobs)
            except Exception as e:
                print(f"爬取失败：{e}")
                print("尝试备用方案...")
                self.try_backup_plan(page)
            finally:
                browser.close()
        return self.jobs_data 
    def similate_human_behavior(self,page):
        """模拟人类浏览行为"""
        print("模拟人类滚动行为...")
        for i in range(4):
            scroll_amount = random.randint(200,600)
            page.mouse.wheel(0,scroll_amount)
            time.sleep(random.uniform(0.5,2))
    def extract_detailed_jobs(self,page):
        """详细提取岗位数据"""
        jobs = []
        try:
            #使用多种选择器尝试定位岗位卡片
            selectors = [
                '.job-card-wrapper',
                '[class*="job-card"]',
                '.job-list li',
                '.job-item'
            ]
            job_elements = []
            for selector in selectors:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"使用选择器'{selector}'找到{len(elements)}个元素")
                    job_elements = elements
                    break
            if not job_elements:
                print("未找到岗位卡片元素")
                return jobs
            print(f"开始提取{len(job_elements)}个岗位的详细信息...")
            for i,element in enumerate(job_elements[:10]): #先试前10个
                try:
                    #滚动到元素可见
                    element.scroll_into_view_if_needed()
                    time.sleep(0.5)
                    #提取详细信息
                    job_info = self.extract_single_job(element,i+1)
                    if job_info:
                        jobs.append(job_info)
                except Exception as e:
                    print(f"提取第{i+1}个岗位失败：{e}")
                    continue
        except Exception as e:
            print(f"数据提取失败：{e}")
        return jobs
    def extract_single_job(self,element,index):
        """提取单个岗位的详细信息"""
        try:
            #提取职位名称
            job_name_element = element.query_selector('.job-name,[class*="job-name"],.job-title')
            job_name = job_name_element.inner_text() if job_name_element else "未知职位"
            #提取公司名称
            company_element = element.query_selector('.company-name,[class*="company"],.brand')
            company = company_element.inner_text() if company_element else "未知公司"
            #提取薪资
            salary_element = element.query_selector('.salary,[class*="salary"],.pay')
            salary = salary_element.inner_text() if salary_element else "面议"
            #提取经验要求
            exp_element = element.query_selector('.job-area,.info,.demand,.req')
            experience = exp_element.inner_text() if exp_element else "经验不限"
            #提取福利标签
            welfare_element = element.query_selector_all('.tag,.welfare,.benefit')
            welfare = ','.join([tag.inner_text() for tag in welfare_element]) if welfare_element else "福利面议"
            #构建完整信息
            job_info = {
                '职位名称':job_name,
                '公司名称':company,
                '薪资范围':salary,
                '工作经验':experience,
                '福利待遇':welfare,
                '数据来源':'BOSS直聘',
                '爬取方式':'Playwright隐身浏览器',
                '爬取时间':pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(f"[{index}]{company} - {job_name} - {salary}")
            return job_info
        except Exception as e:
            print(f"解析岗位详情失败：{e}")
            return None
    def try_backup_plan(self,page):
        """备用方案：尝试其他URL"""
        backup_urls = [
            "https://www.zhipin.com/job_detail/?query=Python&city=101210100",
            "https://www.zhipin.com/web/geek/job?query=Python"
        ]
        for url in backup_urls:
            try:
                print(f"尝试备用URL：{url}")
                page.goto(url,timeout=15000)
                time.sleep(5)
                if 'security-check' not in page.url:
                    print("备用URL成功！")
                    #提取数据
                    jobs = self.extract_detailed_jobs(page)
                    self.jobs_data.extend(jobs)
                    break
            except Exception as e:
                print(f"备用URL失败：{e}")
                continue
    def save_results(self):
        """保存结果"""
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            filename = f'boss_stealth_jobs_{pd.Timestamp.now().strftime("%Y%m%d_%H%M")}.csv'
            df.to_csv(filename,index=False,encoding='utf-8-sig')
            print(f"数据已保存：{filename}")
            #数据统计
            print(f"\n数据概览：")
            print(f"总岗位数：{len(df)}")
            print(f"公司数量：{df['公司名称'].nunique()}")
            print(f"薪资示例：{df['薪资范围'].iloc[0] if len(df) > 0 else '无'}")
        else:
            print("无数据可保存")
def main():
    print("=" * 60)
    print("BOSS直聘Playerwright爬虫（隐身）-真实完整数据提取版")
    print("目标绕过安全检测，获取完整岗位信息")
    print("注意：可能需要手动完成验证")
    print("=" * 60)
    crawler = BOSSStealthCrawler()
    input("按Enter键开始隐身爬虫...")
    data = crawler.crawl_with_stealth()
    #保存结果
    crawler.save_results()
    if data:
        print(f"\n隐身模式成功！获得{len(data)}条完整数据！")
        print("这次我们提取了完整的岗位信息！")
    else:
        print(f"\n虽然数据不多，但对反爬机制的理解加深。")
        print("建议换个时间段试试")
if __name__ == "__main__":
    main()


