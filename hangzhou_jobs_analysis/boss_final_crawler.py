#BOSS直聘-手动验证版
from playwright.sync_api import sync_playwright  #浏览器自动化
import pandas as pd   #数据处理
import time      #时间控制

class BOSSFinalCrawler:
    def __init__(self):
        self.jobs_data = []
    def crawl_with_manual_verify(self):
        """手动验证方案"""
        print("BOSS直聘爬虫-手动验证方案")
        print("需要您手动完成一次验证")
        with sync_playwright() as p:
            #启动真实浏览器（非无头）
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width':1200,'height':800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            print("第一步：访问页面并完成手动验证")
            print("浏览器窗口将打开，请手动完成BOSS直聘的验证")
            print("验证完成后，页面会显示搜索结果")
            page.goto("https://www.zhipin.com")
            time.sleep(2)
            #手动搜索Python
            page.fill('input[placeholder="搜索职位、公司"]','Python')
            page.keyboard.press('Enter')
            print("\n等待手动验证...")
            print("请完成：")
            print("滑动验证码")
            print("点击验证")
            print("任何其他验证步骤")
            input("完成验证后，按Enter键继续爬取...")
            print("\n第二步：自动爬取验证后的数据")
            print("现在应该能看到Python岗位的列表了")
            #等待搜索结果
            time.sleep(5)
            #提取数据
            self.extract_verified_data(page)
            browser.close()
        return self.jobs_data

    def extract_verified_data(self,page):
        """数据提取"""
        print("开始提取验证后的数据...")
        try:
            #直接获取页面文本内容
            page_text = page.inner_text('body')
            lines = [line.strip() for line in page_text.split('\n') if line.strip()]
            print(f"页面共有{len(lines)}行文本")
            #提取包含关键信息的行
            job_blocks = []
            current_block = []
            for line in lines:
                if any(keyword in line for keyword in ['Python','开发','工程师','AI','算法']):
                    if current_block:
                        job_blocks.append(current_block)
                    current_block = [line]
                elif current_block:
                    current_block.append(line)
            if current_block:
                job_blocks.append(current_block)
            print(f"识别到{len(job_blocks)}个岗位区块")
            #解析每个区块
            for i,block in enumerate(job_blocks[:20]): #试前20个
                job_info = self.parse_job_block(block,i+1)
                if job_info:
                    self.jobs_data.append(job_info)
        except Exception as e:
            print(f"数据提取失败：{e}")
            #备用方案：截图分析
            page.screenshot(path='boss_verified_page.png')
            print("已截图：boss_verified_page.png")
    def parse_job_block(self,block,index):
        """详细解析岗位信息"""
        try:
            #智能解析各行内容
            company = "未知公司"
            job_name = "未知职位"
            salary = "面议"
            location = "杭州"
            #智能解析逻辑
            for line in block:
                if '公司' in line or '有限' in line or '科技' in line:
                    company = line
                elif any(word in line for word in ['Python','AI','开发','工程师','算法']):
                    job_name = line
                elif('k' in line or 'K' in line) and ('-' in line or '~' in line):
                    salary = line
                elif '杭州' in line or '区' in line:
                    location = line
            job_info = {
                '序号':index,
                '公司名称':company,
                '职位名称':job_name,
                '薪资范围':salary,
                '工作地点':location,
                '数据来源':'BOSS直聘',
                '爬取方式':'BOSS直聘-手动验证版',
                '爬取时间':pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(f"[{index}]{company} - {job_name} - {salary}")
            return job_info
        except Exception as e:
            print(f"解析岗位详情失败：{e}")
            return None
    def save_final_results(self):
        """保存结果"""
        if self.jobs_data:
            df = pd.DataFrame(self.jobs_data)
            filename = f'boss_final_data.csv'
            df.to_csv(filename,index=False,encoding='utf-8-sig')
            print(f"数据已保存：{filename}")
            #数据统计
            print(f"\n数据概览：")
            print(f"总岗位数：{len(df)}")
            #显示前几条数据
            print(f"\n数据样例：")
            for i,row in df.head(5).iterrows():
                print(f"{row['公司名称'][:20]}... | {row['职位名称'][:20]}... | {row['薪资范围']}")
        else:
            print("没有提取到数据")
def main():
    print("=" * 60)
    print("BOSS直聘爬虫-手动验证版")
    print("目标绕过无限验证循环的唯一可靠方法")
    print("=" * 60)
    crawler = BOSSFinalCrawler()

    print("操作说明:")
    print("1.浏览器窗口将打开")
    print("2.手动完成BOSS直聘的所有验证")
    print("3.确保看到Python岗位搜索结果")
    print("4.回到终端按Enter继续")
    print("=" * 60)
    input("准备好后按Enter键开始...")
    data = crawler.crawl_with_manual_verify()
    #保存结果
    crawler.save_final_results()
if __name__ == "__main__":
    main()


