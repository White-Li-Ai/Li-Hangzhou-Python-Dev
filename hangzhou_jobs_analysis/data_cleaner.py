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
    #5  过滤无效数据
    print("过滤无效数据...")
    initial_count = len(df)
    #移除公司名称成为"未知公司"的记录
    df = df[df['公司名称'] != '未知公司']
    #移除职位名称异常的记录
    df = df[~df['公司名称'].isin(['岗位描述过长','订阅【Python】求职快人一步'])]
    #移除薪资为"面议"的记录（用于薪资分析时）
    df_with_salary = df[df['平均薪资(k)'].notna()].copy()
    print(f"数据清洗完成：")
    print(f"原始记录：{initial_count}条")
    print(f"有效记录：{len(df)}条")
    print(f"有薪资记录：{len(df_with_salary)}条")
    #6 保存清洗后的数据
    df.to_csv(output_file,index=False,encoding='utf-8-sig')
    df_with_salary.to_csv('boss_salary_analysis.csv',index=False,encoding='utf-8-sig')
    print(f"已保存：")
    print(f"- {output_file}(完整清洗数据)")
    print(f"- boss_salary_analysis.csv(薪资分析专用)")
    #7 数据洞察
    print(f"\n清洗后数据洞察：")
    print(f"公司数据：{df['公司名称'].nunique()}")
    if len(df_with_salary) > 0:
        print(f"平均薪资：{df_with_salary['平均薪资(k)'].mean():.1f}k")
        print(f"最高薪资：{df_with_salary['平均薪资(k)'].max():.1f}k")
        print(f"最低薪资：{df_with_salary['平均薪资(k)'].min():.1f}k")
    print(f"\n热门公司：")
    company_counts = df['公司名称'].value_counts().head(5)
    for company,count in company_counts.items():
        print(f"{company}:{count}个岗位")
    return df
def create_visualization(df):
    """创建数据可视化"""
    try:
        from pyecharts.charts import Bar
        from pyecharts import options as opts
        if len(df) > 0:
            #按公司统计岗位数量
            company_stats = df['公司名称'].value_counts().head(10)
            bar = (
                Bar()
                .add_xaxis(company_stats.index.tolist())
                .add_yaxis("岗位数量",company_stats.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="杭州Pyhton岗位公司公布",pos_left="center"),
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                )
            )
            bar.render("company_distribution.html")
            print("可视化图表已生成：company_distribution.html")
    except Exception as e:
        print(f"可视化创建失败：{e}")

if __name__ == "__main__":
    print("=" * 60)
    print("BOSS直聘数据清洗和修复工具")
    print("=" * 60)
    #清洗数据
    cleaned_df = clean_boss_data()
    #创建可视化
    create_visualization(cleaned_df)
    print("\n数据清洗完成，稍后进行数据分析！")