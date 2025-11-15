import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_pulte_jobs(output_file='pulte_jobs.csv'):
    # 1. 设置 Chrome 选项（无头模式 + 防检测）
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面运行
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. 自动安装 ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        # 3. 访问目标页面
        print("正在加载页面...")
        driver.get("https://pultegroup.wd1.myworkdayjobs.com/PGI")

        # 4. 显式等待职位列表加载（最长20秒）
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-automation-id='jobListing']")))
        except TimeoutException:
            print("错误：无法加载职位列表！可能原因：")
            print("- 网页结构已变化，请检查选择器")
            print("- 网络较慢，尝试增加等待时间")
            return

        # 5. 获取所有职位元素
        jobs = driver.find_elements(By.CSS_SELECTOR, "li[data-automation-id='jobListing']")
        print(f"找到 {len(jobs)} 个职位")

        # 6. 提取数据并写入CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['职位标题', '工作地点', '职位ID', '发布日期', '申请链接'])

            for job in jobs:
                try:
                    title = job.find_element(By.CSS_SELECTOR, "a.css-19uc56f").text
                    location = job.find_element(By.CSS_SELECTOR, "div.css-1d6wmgf").text
                    job_id = job.find_element(By.CSS_SELECTOR, "div.css-1d6wmgf + div").text
                    posted_date = job.find_element(By.CSS_SELECTOR, "div.css-1d6wmgf + div + div").text
                    job_url = job.find_element(By.CSS_SELECTOR, "a.css-19uc56f").get_attribute("href")
                    writer.writerow([title, location, job_id, posted_date, job_url])
                except NoSuchElementException as e:
                    print(f"跳过一条记录（缺失字段）：{e}")
                    continue

        print(f"数据已保存到 {output_file}")

    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        driver.quit()  # 确保关闭浏览器

if __name__ == "__main__":
    scrape_pulte_jobs()
