import pandas as pd
import sqlite3

if __name__=='__main__':
    conn = sqlite3.connect('db.sqlite3')

    df = pd.read_excel('app01/utils/data/人员信息表.xlsx')
    # User表
    user = pd.DataFrame(df, columns=[
                        '姓名', '学历', '毕业学校', '专业', '毕业时间', '身份证号', '电话', '开户行', '银行账户', '邮箱'])
    user.rename(columns={'姓名': 'name',
                        '学历': 'degree',
                        '毕业学校': 'college',
                        '专业': 'mojor',
                        '毕业时间': 'grad_date',
                        '身份证号': 'card_id',
                        '电话': 'phone',
                        '开户行': 'bank',
                        '银行账户': 'bank_id',
                        '邮箱': 'email'}, inplace=True)
    # Postion
    postion = pd.DataFrame(
        df, columns=['姓名', '是否实习', '是否直管', '是否劳务', '入职日期', '试用期至', '离职时间', '岗位等级', '公司'])
    postion.rename(columns={'姓名': 'name',
                            '是否实习': 'is_probation',
                            '是否直管': 'is_direct',
                            '是否劳务': 'is_labor',
                            '入职日期': 'entry_date',
                            '试用期至': 'probation_end_date',
                            '离职时间': 'quit_date',
                            '岗位等级': 'postion_level_id',
                            '公司': 'company',
                            }, inplace=True)
    postion['is_manager'] = 0
    # Salary
    salary = pd.DataFrame(
        df, columns=['姓名', '试用期薪资', '转正后薪资', '其中绩效工资', '管理岗薪资', '公积金基数', '社保基数', '个税抵扣'])
    salary.rename(columns={'姓名': 'name',
                        '试用期薪资': 'probation_salary',
                        '转正后薪资': 'formal_salary',
                        '其中绩效工资': 'performance_salary',
                        '管理岗薪资': 'management_salary',
                        '公积金基数': 'fund_radix',
                        '社保基数': 'social_radix',
                        '个税抵扣': 'tax'
                        }, inplace=True)
    salary['commission'] = 0
    salary['social'] = 0
    salary['fund'] = 0
    salary['tax'] = 0
    salary['modification_before_tax'] = 0
    salary['modification_after_tax'] = 0
    salary['performance_salary_coefficient'] = 1
    salary['subsidy'] = 0

    # 写入
    try:
        user.to_sql('user', conn, if_exists='append', index=False)
    except:
        print('User 重复')

    u = pd.read_sql_query('select * from user', conn)
    u = pd.DataFrame(u, columns=['id', 'name'])

    try:
        postion = pd.merge(u, postion, how='inner', on='name')
        postion.rename(columns={'id': 'user_id'}, inplace=True)
        del postion['name']
        postion.to_sql('postion', conn, if_exists='append', index=False)
    except:
        print('Postion 重复')

    try:
        salary = pd.merge(u, salary, how='inner', on='name')
        salary.rename(columns={'id': 'user_id'}, inplace=True)
        del salary['name']
        salary.to_sql('salary', conn, if_exists='append', index=False)
    except:
        print('Salary 重复')
    
    conn.close()