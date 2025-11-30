#BOSS直聘Playerwright爬虫--浏览器模拟方案
from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
import os

class BOSSPlaywrightCrawler:
    def __init__(self):
        self.jobs_data = []
    def crawl_with_real_browser(self,max_pages=2):
        """
        使用真实浏览器模拟人类行为
        """
        print("启动BOSS直聘Playwright挑战")
        print("使用真实浏览器模拟人类行为...")
        with sync_playwright() as p:
            #启动浏览器(先非无头模式便于调试)
            browser = p.chromium.launch(headless=False) #成功后改为True
            context = browser.new_context(
                viewport = {'width':1920,'height':1080},
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            try:
                #1 访问BOSS直聘主页
                print("访问BOSS直聘主页...")
                page.goto('https://www.zhipin.com',timeout=60000)
                time.sleep(3)
                #模拟人类行为：随即滚动
                self.simulate_human_behavior(page)
                #2 搜索Pyhton岗位
                print("搜索Python岗位...")
                page.fill('input[placeholder="搜索职位、公司"]','Python')
                time.sleep(2)
                #点击搜索按钮
                search_btn = page.query_selector('a.search-btn')
                if search_btn:
                    search_btn.click()
                else:
                    page.keyboard.press('Enter')
                #等待搜索结果加载
                print("等待搜索结果...")
                page.wait_for_selector('.job-list-box',timeout=15000)
                time.sleep(3)
                #3 爬取多页数据
                for page_num in range(1,max_pages + 1):
                    print(f"\n提取第{page_num}页数据...")
                    #提取当前页数据
                    page_data = self.extract_page_data(page)
                    self.jobs_data.extend(page_data)
                    print(f"第{page_num}页提取完成：{len(page_data)}个岗位")
                    #如果不是最后一页，尝试翻页
                    if page_num < max_pages:
                        if not self.go_to_next_page(page):
                            print("没有下一页，停止爬取")
                            break
                        #页间延时
                        time.sleep(random.uniform(3,6))
            except Exception as e:
                print(f"爬取过程中出错：{e}")
            finally:
                browser.close()
        return self.jobs_data
    def simulate_human_behavior(self,page):
        """模拟人类浏览行为"""
        print("模拟人类滚动行为...")
        for i in range(4):
            scroll_amount = random.randint(200,600)
            page.mouse.wheel(0,scroll_amount)
            time.sleep(random.uniform(0.5,2))
    def extract_page_data(self,page):
        """提取当前页面的岗位数据"""
        jobs_data = []
        try:
            job_cards = page.query_selector_all('.job-card-wrapper')
            print(f"找到{len(job_cards)}个岗位卡片")
            for i,card in enumerate(job_cards[:10]): #先试前10个
                try:
                    #滚动到元素可见
                    card.scroll_into_view_if_needed()
                    job_name = card.query_selector('.job-name').inner_text()
                    company = card.query_selector('.company-name').inner_text()
                    salary = card.query_selector('.salary').inner_text()
                    #尝试获取更多信息
                    try:
                        experience = card.query_selector('.job-area').inner_text()
                    except:
                        experience = "未知"
                    job_info = {
                        '职位名称':job_name,
                        '公司名称':company,
                        '薪资范围':salary,
                        '工作经验':experience,
                        '数据来源':'BOSS直聘',
                        '爬取方式':'Playwright真实浏览器',
                        '爬取时间':pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    jobs_data.append(job_info)
                    print(f"[{i + 1}]{company} - {job_name} - {salary}")
                except Exception as e:
                    print(f"页面数据提取失败：{e}")
                    continue
        except Exception as e:
            print(f"页面数据提取失败:{e}")
        return jobs_data
    def go_to_next_page(self,page):
        """翻到下一页"""
        try:
            next_btn = page.query_selector('a.next')
            if next_btn and next_btn.is_enabled():
                next_btn.click()
                page.wait_for_selector('.job-list-box',timeout=10000)
                time.sleep(3)
                return True
            return False
        except Exception as e:
            print(f"翻页失败：{e}")
            return False
    def save_results(self):
        """保存结果"""
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            filename = f'boss_playwright_jobs.csv'
            df.to_csv(filename,index=False,encoding='utf-8-sig')
            print(f"数据已保存：{filename}")
            #数据统计
            print(f"\n最终结果：")
            print(f"总岗位数：{len(df)}")
            print(f"公司数量：{df['公司名称'].nunique()}")
            print(f"薪资范围：{df['薪资范围'].unique()[:3]}...")
        else:
            print("无数据可保存")
def main():
    """主函数"""
    print("=" * 60)
    print("BOSS直聘Playwright爬虫挑战")
    print("使用真实浏览器模拟人类行为")
    print("注意：将打开浏览器窗口，勿操作")
    print("=" * 60)
    crawler = BOSSPlaywrightCrawler()
    #开始爬取
    input("按Enter键开始运行...")
    jobs_data = crawler.crawl_with_real_browser(max_pages=2)
    #保存结果
    crawler.save_results()
    if jobs_data:
        print(f"\nPlaywright挑战成功！获得{len(jobs_data)}条真实数据！")
        print("这次用真实浏览器完全模拟人类行为")
    else:
        print(f"\n虽然数据不多，但浏览器模拟技术已验证可行！")
        print("可以调整策略继续优化")
if __name__ == "__main__":
    main()


            

