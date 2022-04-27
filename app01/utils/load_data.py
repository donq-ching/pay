import pandas as pd

from rest_framework.response import Response
from django.http import JsonResponse

from ..models import Leave, User, Report




def get_leave_code(leave):
    leave_choice = ((0, '事假'), (1, '年休假'), (2, '婚假'), (3, '产假'), (4, '哺乳假'),
                    (5, '陪产假'), (6, '丧假'), (7, '工伤假'), (8, '病假'), (9, '调休假'))
    for el in leave_choice:
        if el[1] == leave:
            return el[0]


def load_leave_data(request):
    '''
    @function 函数

    @details 上传请假数据

    @Args 参数
        request: 含请求头和请求体
            step: 当前操作是哪一步{0:代表只将数据输出查看, 1:代表写入数据库}
            path: 上传文件地址

    @Returns 返回
        根据stpe的值返回
        0: 返回解析后的json数据
        1: 返回上传数据库后的消息
    '''
    step = int(request.POST.get('step'))
    df = pd.read_excel(request.FILES.get('data'))

    df = df[df['当前审批状态'] == '已通过']
    df = pd.DataFrame(data=df, columns=['审批编号', '申请人', '请假类型', '开始时间', '结束时间'])
    df_list = df.values.tolist()

    if step != 1:
        return JsonResponse(df_list, safe=False, json_dumps_params={'ensure_ascii': False})
        # return Response(df_list)

    # 返回内容：
    # 2. 重复list
    # 3. 用户不存在list
    ret = {'message': '上传失败', '重复': [], '用户不存在': []}
    for el in df_list:
        if Leave.objects.filter(leave_id=el[0]):
            ret['重复'].append(el)
            continue

        user = User.objects.filter(name=el[1])
        if not user:
            ret['用户不存在'].append(el)
            continue
        user = user[0]
        el[3] = str(el[3]).replace('上午', '08:30')
        el[3] = str(el[3]).replace('下午', '17:30')
        el[3] = str(el[3]).replace('/', '-')
        el[4] = str(el[4]).replace('上午', '08:30')
        el[4] = str(el[4]).replace('下午', '17:30')
        el[4] = str(el[4]).replace('/', '-')
        leave = Leave()
        leave.leave_id = el[0]
        leave.user = user
        leave.leave = get_leave_code(el[2])
        leave.start_time = el[3]
        leave.end_time = el[4]
        leave.save()
        ret['message'] = '部分上传成功'

    # return Response(ret)
    return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})


def load_report_data(request):
    
    '''
    @function 函数
    
    @details 上传日报和周计划数据
    
    @Args 参数
        request: 含请求头和请求体
            report_type: 上传文件类型 0为周计划、1为日报
            step: 当前操作是哪一步{0:代表只将数据输出查看, 1:代表写入数据库}
            path: 上传文件地址

    @Returns 返回
        根据stpe的值返回
        0: 返回解析后的json数据
        1: 返回上传数据库后的消息
    '''
    report_type = int(request.POST.get('report_type'))
    step = int(request.POST.get('step'))
    df = pd.read_excel(request.FILES.get('data'))

    if report_type == 0:
        df = pd.DataFrame(data=df, columns=['提交时间', '申请人'])
    elif report_type == 1:
        df = pd.DataFrame(data=df, columns=['汇报时间', '汇报人'])
    df = df.dropna(axis=0)
    df_list = df.values.tolist()
    if step != 1:
        return JsonResponse(df_list, safe=False, json_dumps_params={'ensure_ascii': False})
        # return Response(df_list)

    ret = {'message':'上传失败', '用户不存在': []}
    for el in df_list:
        user = User.objects.filter(name=el[1])
        if not user:
            ret['用户不存在'].append(el)
            continue
        user = user[0]
        el[0] = str(el[0]).replace('/', '-')
        report = Report()
        report.user = user
        report.type = report_type
        report.time = el[0]
        report.save()
        ret['message'] = '部分上传成功'

    return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})
    # return Response(ret)