import datetime

from chinese_calendar import is_holiday, is_workday, get_holiday_detail, Holiday


from ..models import User, Report, Postion, Leave, Salary


def statistic_day(start_date, end_date):
    count_day = {
        '月工作日': 0,
        '月休息日': 0,
        '月天数': 0,
        '法定节假日': 0
    }
    festival_name = ''
    for i in range((end_date-start_date).days+1):
        day = start_date + datetime.timedelta(days=i)
        count_day['月天数'] += 1
        if is_workday(day):
            count_day['月工作日'] += 1
        if is_holiday(day):
            count_day['月休息日'] += 1
        festival = get_holiday_detail(day)
        if festival[0] and festival[1]:
            if festival_name != festival[1]:
                festival_name = festival[1]
                count_day['法定节假日'] += Holiday(festival_name).days

    return count_day


def statistic_report(start_date, end_date):
    count_report = {k['name']: {'日报': {'正常': 0, '异常': 0, '未提交': 0}, '周计划': {'正常': 0, '异常': 0, '未提交': 0}}
                    for k in User.objects.values('name').distinct()}
    count_day = statistic_day(start_date, end_date)

    for name in [k for k in count_report]:
        for i in range((end_date-start_date).days+1):
            day = start_date + datetime.timedelta(days=i)
            if is_workday(day):
                data = Report.objects.filter(
                    time__year=day.year, time__month=day.month, time__day=day.day, user__name=name, type=1).order_by('time')
                if not data:
                    count_report[name]['日报']['未提交'] += 1
                    continue
                data = data[0]
                if data.time <= datetime.datetime(day.year, day.month, day.day, 20, 0):
                    count_report[name]['日报']['正常'] += 1
                else:
                    count_report[name]['日报']['异常'] += 1

        if Postion.objects.filter(user__name=name, is_manager=True):
            for i in range((end_date-start_date).days+1):
                day = start_date + datetime.timedelta(days=i)
                day_1 = day-datetime.timedelta(days=1)
                if is_workday(day) and is_holiday(day_1):
                    data = Report.objects.filter(
                        time__year=day.year, time__month=day.month, time__day=day.day, user__name=name, type=0).order_by('time')
                    if data:
                        data = data[0]
                        if data.time <= datetime.datetime(day.year, day.month, day.day, 9, 30):
                            count_report[name]['周计划']['正常'] += 1
                        else:
                            count_report[name]['周计划']['异常'] += 1
                    else:
                        status = False
                        while is_holiday(day_1):
                            data = Report.objects.filter(
                                time__year=day_1.year, time__month=day_1.month, time__day=day_1.day, user__name=name, type=0).order_by('time')
                            if data:
                                count_report[name]['周计划']['正常'] += 1
                                status = True
                                break
                            else:
                                day_1 -= datetime.timedelta(days=1)
                        if not status:
                            data = Report.objects.filter(
                                time__year=day_1.year, time__month=day_1.month, time__day=day_1.day, user__name=name, type=0).order_by('time')
                            if data:
                                count_report[name]['周计划']['正常'] += 1
                            else:
                                count_report[name]['周计划']['未提交'] += 1

    return {'汇报统计': count_report, '月信息统计': count_day}


def statistic_leave(start_date, end_date):
    def get_leave_len(leave_time):
        leave_len = 0
        if leave_time.days == 0:
            if leave_time.seconds/(60*60) == 0:
                leave_len = 0.5
            else:
                leave_len = 1
        else:
            leave_len = leave_time.days
            if leave_time.seconds/(60*60) == 0:
                leave_len += 0.5
            else:
                leave_len += 1
        return leave_len

    count_day = statistic_day(start_date, end_date)
    count_leave = {k['name']: {'非调休假': 0, '调休假': 0}
                   for k in User.objects.values('name').distinct()}
    leaves = Leave.objects.filter(
        start_time__gte=start_date, end_time__lte=end_date)

    for leave in leaves:
        leave_len = get_leave_len(leave.end_time - leave.start_time)
        if leave.leave == 9:
            count_leave[leave.user.name]['调休假'] += leave_len
        else:
            count_leave[leave.user.name]['非调休假'] += leave_len

    return {'请假统计': count_leave, '月信息统计': count_day}


def statistic_salary(start_date, end_date):
    # 1. 获取用户列表
    # 2. 计算工资 薪资，绩效薪资，绩效系数，管理岗薪资，提成，社保基数，社保，公积金，个税，税前后调整
    # 3. 判断是否为管理岗位,或者不判断,直接写入相应值就ok
    # 工资 = 月薪÷21.75×月计薪天数×（出勤天数比例）
    # 计薪天数, 出勤天数 请假文件
    count_day = statistic_day(start_date, end_date)
    count_leave = statistic_leave(start_date, end_date)
    count_report = statistic_report(start_date, end_date)

    def get_department(name):
        postion = Postion.objects.filter(user__name=name)
        if postion:
            return postion[0].postion_level.department.name
        else:
            return ''

    def get_basic_salary(name):
        try:
            postion = Postion.objects.filter(user__name=name)
            salary = Salary.objects.filter(user__name=name)
            if postion[0].is_probation:
                return salary[0].probation_salary
            if postion[0].is_formal:
                return salary[0].formal_salary
        except:
            return 0

    def get_management_salary(name):
        try:
            salary = Salary.objects.filter(user__name=name)
            return salary[0].management_salary
        except:
            return 0

    def get_performance_salary(name):
        try:
            salary = Salary.objects.filter(user__name=name)
            return salary[0].performance_salary, salary[0].performance_salary_coefficient
        except:
            return 0, 0

    def get_subsidy(name):
        try:
            salary = Salary.objects.filter(user__name=name)
            return salary[0].subsidy
        except:
            return 0

    def get_commission(name):
        try:
            salary = Salary.objects.filter(user__name=name)
            return salary[0].commission
        except:
            return 0

    def get_social(name):
        social = {
            '社保基数': 0,
            '公积金基数': 0,
            '社保': 0,
            '公积金': 0,
            '个税': 0,
            '税前工资调整': 0,
            '税后工资调整': 0
        }
        try:
            salary = Salary.objects.filter(user__name=name).first()
            social['社保基数'] = salary.social_radix
            social['公积金基数'] = salary.fund_radix
            social['社保'] = round(salary.social_radix*(0.08+0.02+0.004), 2)
            social['公积金'] = round(salary.fund_radix*0.05, 2)
            social['个税'] = salary.tax
            social['税前工资调整'] = salary.modification_before_tax
            social['税后工资调整'] = salary.modification_after_tax
        except:
            pass
        return social

    count_salary = {k['name']: {
        '部门': get_department(k['name']),
        '基本工资': {
            '出勤基本工资': get_basic_salary(k['name']),
            '岗位工资': get_management_salary(k['name']),
            '绩效部分': get_performance_salary(k['name'])[0],
            '绩效系数': get_performance_salary(k['name'])[1],
        },
        '其他补贴': get_subsidy(k['name']),
        '扣发工资': {
            '事假/缺勤/病假天数': count_leave['请假统计'][k['name']]['非调休假'],
            '扣除': 0
        },
        '提成': get_commission(k['name']),
        '社保基数': get_social(k['name'])['社保基数'],
        '实际工资': 0,
        '公积金(5%)': get_social(k['name'])['公积金'],
        '社保': get_social(k['name'])['社保'],
        '个税': get_social(k['name'])['个税'],
        '税前工资调整': get_social(k['name'])['税前工资调整'],
        '税后工资调整': get_social(k['name'])['税后工资调整'],
        '应发工资': 0,
        '实发工资': 0,
        '备注': ''
    }
        for k in User.objects.values('name').distinct()}

    # 计算
    for u in count_salary:
        count_salary[u]['实际工资'] = round(count_salary[u]['基本工资']['出勤基本工资'] *
                                        (1-count_salary[u]['扣发工资']['事假/缺勤/病假天数']/21.75) +
                                        count_salary[u]['提成'] +
                                        count_salary[u]['基本工资']['岗位工资'] +
                                        count_salary[u]['其他补贴'] +
                                        count_salary[u]['基本工资']['绩效部分'] *
                                        count_salary[u]['基本工资']['绩效系数'], 2)

        count_salary[u]['应发工资'] = round((
            count_salary[u]['实际工资'] -
            count_salary[u]['公积金(5%)'] -
            count_salary[u]['社保'] -
            count_salary[u]['个税']), 2)

        count_salary[u]['扣发工资']['扣除'] = round(count_salary[u]['基本工资']['出勤基本工资'] *
                                              (count_salary[u]['扣发工资']['事假/缺勤/病假天数']/21.75), 2)

        count_salary[u]['实发工资'] = count_salary[u]['应发工资']
    return count_salary
