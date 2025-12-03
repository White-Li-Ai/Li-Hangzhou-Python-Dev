#BOSS直聘数据清洗和修复
import pandas as pd
import re

def clean_boss_data(input_file='boss_final_data.csv',output_file='boss_cleaned_data.csv'):
    """清洗和修复BOSS直聘数据"""
    #读取原始数据
    df = pd.read_csv(input_file,encoding='utf-8-sig')
    print(f"原始数据：{len(df)}条记录")
    #1 修复薪资编码问题
    print("修复薪资编码...")
    def fix_salary_encoding(salary):
        if not isinstance(salary,str):
            return salary
        #修复特殊编码的薪资
        encoding_map = {
            '': '1', '': '2', '': '3', '': '4', '': '5', 
            '': '6', '': '7', '': '8', '': '9', '': '10',
            '': '0', '': '-', '·': '·'
        }
        for old,new in encoding_map.items():
            salary = salary.replace(old,new)
        #清理多余字符
        salary = re.sub(r'[^\d\-kK·薪]','',salary)
        return salary
    df['薪资范围'] = df['薪资范围'].apply(fix_salary_encoding)
    #2 清理公司名称
    print("清理公司名称...")
    def clean_company_name(company):
        if not isinstance(company,str):
            return company
        #移除无关内容
        company = company.split('【')[0].split('（')[0].split('(')[0]
        company = company.strip()
        #过滤明显不是公司名的
        if len(company) < 2 or '订阅' in company or '职位名称' in company:
            return '未知公司'
        return company
    df['公司名称'] = df['公司名称'].apply(clean_company_name)
    #3 清理职位名称
    print("清理职位名称...")
    def clean_job_title(title):
        if not isinstance(title,str):
            return title
        #移除无关前缀
        title = title.replace('职位名称：','').replace('订阅【','').replace('】','')
        title = title.strip()
        #过滤过长内容（可能是公司介绍）
        if len(title) > 100:
            return '岗位描述过长'
        return title
    df['职位名称'] = df['职位名称'].apply(clean_job_title)
    #4 提取薪资数值用于分析
    print("提取薪资数值...")
    def extract_salary_numeric(salary):
        if not isinstance(salary,str) or '面议' in salary:
            return None
        #匹配15-28k格式
        match = re.search(r'(\d+)[kK]?\s*[-~～]\s*(\d+)[kK]?',salary)
        if match:
            try:
                low = int(match.group(1))
                high = int(match.group(2))
                return (low + high) / 2 #返回平均薪资
            except:
                return None
        return None
    df['平均薪资(k)'] = df['薪资范围'].apply(extract_salary_numeric)
    #5 

