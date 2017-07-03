from openpyxl import Workbook
from openpyxl import workbook
from openpyxl import load_workbook
from openpyxl import worksheet

def readFromXLSX(path):
    wb = load_workbook(path)
    ws = wb.active

    ws_rows = tuple(ws.rows)
    rows_len = len(ws_rows)

    return rows_len-1, ws_rows[1:rows_len]

def writeAssignment(form, asn_name):
    wb = Workbook()
    ws = wb.active

    row_num = len(form)

    ws['A1'] = '团队ID'
    ws['B1'] = '团队名称'
    ws['C1'] = '作业提交情况'
    ws['D1'] = '作业分数'

    for i in range(row_num):
        ws['A'+str(i+2)] = form[i][0]
        ws['B'+str(i+2)] = form[i][1]
        ws['C'+str(i+2)] = form[i][2]
        ws['D'+str(i+2)] = form[i][3]

    save_path = '作业' + asn_name +'报表.xlsx'
    wb.save(save_path)

    return save_path

def writeAllAssignment(form, course_name):
    wb = Workbook()
    ws = wb.active

    row_num = len(form)
    now = 0

    for i in range(row_num):
        if form[i][2]=='':
            if i>0:
                ws = wb.create_sheet()
                now = 0
            ws.title = form[i][1]

        ws['A'+str(now+1)] = form[i][0]
        ws['B'+str(now+1)] = form[i][1]
        ws['C'+str(now+1)] = form[i][2]
        ws['D'+str(now+1)] = form[i][3]

        now = now + 1

    save_path = '课程' + course_name +'作业报表.xlsx'
    wb.save(save_path)

    return save_path

def writeTeam(form, course_name):
    wb = Workbook()
    ws = wb.active

    row_num = len(form)

    ws['A1'] = '团队ID'
    ws['B1'] = '团队名称'
    ws['C1'] = '学生学号'
    ws['D1'] = '学生姓名'
    ws['E1'] = '担任角色'

    for i in range(row_num):
        ws['A'+str(i+2)] = form[i][0]
        ws['B'+str(i+2)] = form[i][1]
        ws['C'+str(i+2)] = form[i][2]
        ws['D'+str(i+2)] = form[i][3]
        ws['E'+str(i+2)] = form[i][4]

    save_path = '课程' + course_name +'团队报表.xlsx'
    return save_path

def fileSystemResponse(Resources, Folders):
    R1 = '<li class="myfile"><input type="text" class="changename" name="1" value="'
    R2 = '"/><input class="checkbox" name="'
    R3 = '" type="checkbox" value="" /></li>'
    R_str = []
    for res in Resources:
        R_str.append(R1 + res.name + R2 + str(res.id) + R3 + '\n')

    F1 = '<li class="myfolder"><input type="text" class="changename" name="1" value="'
    F2 = '"/><input class="checkbox" name="'
    F3 = '" type="checkbox" value="" /></li>'
    F_str = []
    for f in Folders:
        F_str.append(F1 + f.name + F2 + str(f.id) + F3 + '\n')

    ret_str = ''
    for res in R_str:
        ret_str = ret_str + res
    for f in F_str:
        ret_str = ret_str + f

    return ret_str

def deleteResource(path):
    for res_path in path:
        print(res_path)


if __name__ == '__main__':
    form1 = [[1, 'storm', '已提交', 100],
             [2, 'aaa', '未提交', 0]]
    xlsx1 = writeAssignment(form1, '测试')
    print(xlsx1)

    form2 = [[1, 'storm', '', ''],
             ['作业ID', '作业名称', '作业提交情况', '作业分数'],
             [1, '分析', '已提交', 98],
             [2, '开发', '已提交', 99],
             [3, '测试', '已提交', 100],
             [2, 'aaa', '', ''],
             ['作业ID', '作业名称', '作业提交情况', '作业分数'],
             [1, '分析', '未提交', 0],
             [2, '开发', '未提交', 0],
             [3, '测试', '未提交', 0]]
    xlsx2 = writeAllAssignment(form2, '软工过程')
    print(xlsx2)