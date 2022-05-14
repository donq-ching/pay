import pandas as pd

from django.http import HttpResponse

from ..models import User, Postion, Salary, Position_Level


def load_to_sqlite(request, path = 'app01/utils/data/人员信息表.xlsx'):
    def get_degree(degree):
        degree_choice = ((0, '高中'), (1, '专科'), (2, '本科'), (3, '硕士'), (4, '博士'))
        for degree_ in degree_choice:
            if degree_[1] == degree:
                return degree_[0]
        return 0
    
    def is_tf(tf):
        # if '否' in tf:
        #     return False
        if '是' in tf:
            return True
        return False

    df = pd.read_excel(path)
    user = pd.DataFrame(df, columns=[
                        '姓名', '学历', '毕业学校', '专业', '毕业时间', '身份证号', '电话', '开户行', '银行账户', '邮箱'])
    user_dict = user.to_dict(orient='records')
    postion = pd.DataFrame(
        df, columns=['姓名', '是否实习', '是否直管', '是否劳务', '入职日期', '试用期至', '离职时间', '岗位等级', '公司'])
    postion_dict = postion.to_dict(orient='records')
    salary = pd.DataFrame(
        df, columns=['姓名', '试用期薪资', '转正后薪资', '其中绩效工资', '管理岗薪资', '公积金基数', '社保基数', '个税抵扣'])
    salary_dict = salary.to_dict(orient='records')

    for u in user_dict:
        user = User(name=u['姓名'],
                    degree=get_degree(u['学历']),
                    college=u['毕业学校'],
                    mojor=u['专业'],
                    grad_date=u['毕业时间'],
                    card_id=u['身份证号'],
                    phone=u['电话'],
                    bank=u['开户行'],
                    bank_id=u['银行账户'],
                    email=u['邮箱'],
                    )
        try:
            user.save()
        except Exception as e:
            print(e)

    for p in postion_dict:
        user = User.objects.filter(name=p['姓名']).first()
        level = Position_Level.objects.filter(level=p['岗位等级']).first()
        postion = Postion(user=user,
                          is_probation=is_tf(p['是否实习']),
                          is_direct=is_tf(p['是否直管']),
                          is_labor=is_tf(p['是否劳务']),
                          entry_date=p['入职日期'],
                          probation_end_date=p['试用期至'],
                        #   quit_date=p['离职时间'],
                          postion_level=level,
                          company=p['公司'],
                          )
        try:
            postion.save()
        except Exception as e:
            print(e)

    for s in salary_dict:
        user = User.objects.filter(name=s['姓名']).first()
        salary = Salary(user=user,
                        probation_salary=s['试用期薪资'],
                        formal_salary=s['转正后薪资'],
                        performance_salary=s['其中绩效工资'],
                        management_salary=s['管理岗薪资'],
                        fund_radix=s['公积金基数'],
                        social_radix=s['社保基数'],
                        tax=s['个税抵扣'],
                        )
        try:
            salary.save()
        except Exception as e:
            print(e)
    
    return HttpResponse('上传成功')