# coding=utf-8
import os

import random

import  tempfile, zipfile, zipstream

import time

from django.shortcuts import render
from wsgiref.util import FileWrapper

from datetime import date, datetime

from .models import *
from .ZipUtilities import *

from django.http import StreamingHttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.db import connection
from django.shortcuts import render_to_response
from django.shortcuts import render

from .utils import *

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import messages

# 学生页左半部
def student_left(request):
    return render_to_response('student_left.html')


# 主页
def index(request):
    from django.contrib.messages import get_messages
    storage = get_messages(request)
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type']:
        tp = request.session['type']
        uid = request.session['id']
        if tp == 's':
            per = Student.objects.get(id=uid)
            ustr = "Student"
        elif tp == 't':
            per = Teacher.objects.get(id=uid)
            ustr = "Teacher"
        elif tp == 'e':
            per = EduAdmin.objects.get(id=uid)
            ustr = "Administrator"
        return render(request, "index.html", {'msg': storage, 'len': len(storage), 'str': ustr, 'per': per})
    return render(request, "index.html", {'msg': storage, 'len': len(storage)})


# 头部
def header(request):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type']:
        tp = request.session['type']
        uid = request.session['id']
        if tp == 's':
            per = Student.objects.get(id=uid)
            str = "Student"
            return render(request, "header.html", {'str': str, 'per': per})
        elif tp == 't':
            per = Teacher.objects.get(id=uid)
            str = "Teacher"
            return render(request, "header.html", {'str': str, 'per': per})
        elif tp == 'e':
            per = EduAdmin.objects.get(id=uid)
            str = "Administrator"
            return render(request, "header.html", {'str': str, 'per': per})
        else:
            return HttpResponseRedirect("/EducationalSystem/")
    else:
        return HttpResponseRedirect("/EducationalSystem/")


# 教师页左部
def teacher_left(request):
    # urlAll = request.path
    # s = urlAll.split('/')
    # str = s[-1]
    # print (str)
    return render_to_response('teacher_left.html')

# 添加课程，单独页面
def jiaowu_addcourse(request):
    tm = Term.objects.filter(is_over=False).order_by("-start")
    return render(request, "jiaowu_addcourse.html", {'tm': tm})

def jiaowu_rewriteCourse(request,cou_id):
    print (cou_id)
    tm = Term.objects.filter(is_over=False).order_by("-start")
    course = Course.objects.get(id=cou_id)
    return render(request, "jiaowu_rewritecourse.html",{'tm': tm, 'course':course })


# 添加学期，单独页面
def jiaowu_addsemester(request):
    return render_to_response('jiaowu_addsemester.html')

# 课程信息：教务，单独页面
def jiaowu_courseinfo(request, cou_id):
    course = Course.objects.get(id=cou_id)
    tid = course.term_id
    cou_stu = Course_Student.objects.filter(course_id=course).values("student_id")
    stu = Student.objects.filter(id__in=cou_stu).order_by("number")
    cou_tea = Course_Teacher.objects.filter(course_id=course).values("teacher_id")
    tea = Teacher.objects.filter(id__in=cou_tea)
    #stu_id = cou_stu.student_id
    #term = Term.objects.get(id=tid)
    return render(request, "jiaowu_courseinfo.html", {'course':course, 'term':tid, 'stu':stu, 'tea': tea})

# 设置当前学期，教务，跳转到原页面
def jiaowu_setcurrentsemester(request, term_id):
    try:
        Term.objects.all().update(is_current=False)
        term = Term.objects.get(id=term_id)
        term.is_current=True
        term.save()
        messages.success(request,"操作成功")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)
    except:
        messages.error(request,"操作失败")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)

# 学生课程，单独页面
def displayCourseForStudent(request):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 's':
        thisTerm = Term.objects.all()
        sid = request.session['id']
        student_course = Course_Student.objects.filter(student_id__id=sid)
        cou_id = student_course.values("course_id")
        cou = Course.objects.filter(term_id__id__in=thisTerm, id__in=cou_id)
        return render(request, "student.html", {'cou': cou})
    else:
        return HttpResponseRedirect("/EducationalSystem/")
    # if 'id' in request.GET and request.GET['id']:
    # 	if 'term_id' in request.GET and request.GET['term_id']:
    # 		stu_id = request.GET['id']
    # 		term_id = request.GET['term_id']
    # 		student_course = Course_Student.objects.filter(student_id__id=id)
    # 		course_id = student_course.course_id__id
    # 		ret_course = Course(term_id__id=term_id, id__in=course_id)

#展示课程：教师
def displayCourseForTeacher(request):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 't':
        thisTerm = Term.objects.all()
        tid = request.session['id']
        teacher_course = Course_Teacher.objects.filter(teacher_id__id=tid)
        cou_id = teacher_course.values("course_id")
        cou = Course.objects.filter(term_id__id__in=thisTerm, id__in=cou_id)
        return render(request, "teacher.html", {'cou': cou})
    else:
        return HttpResponseRedirect("/EducationalSystem/")

#登陆功能，处理函数
def login(request):
    if 'name' in request.POST and request.POST['name'] \
        and 'password' in request.POST and request.POST['password'] \
        and 'type' in request.POST and request.POST['type']:
        userName = request.POST['name']
        userPassword = request.POST['password']
        userKind = request.POST['type']

        if userKind == 't':
            tea = Teacher.objects.filter(number = userName, password = userPassword)
            if tea.count() == 1:
                print('successT')
                request.session["id"] = tea[0].id
                request.session["type"] = "t"
                return HttpResponseRedirect("/EducationalSystem/teacher/")
            else:
                messages.error(request,"密码错误、用户不存在或帐号不属于教师用户")
                return HttpResponseRedirect("/EducationalSystem/")
            # if tea:
            # 	return render_to_response('index.html')
            # else:
            # 	return render_to_response('index.html')
        elif userKind == 's':
            stu = Student.objects.filter(number = userName, password = userPassword)
            if stu.count() == 1:
                print('successS')
                request.session["id"] = stu[0].id
                request.session["type"] = "s"
                return HttpResponseRedirect("/EducationalSystem/student/")
            else:
                messages.error(request,"密码错误、用户不存在或帐号不属于学生用户")
                return HttpResponseRedirect("/EducationalSystem/")
            # 	return render_to_response('index.html')
            # else:
            # 	return render_to_response('index.html')
        elif userKind == "e":
            ea = EduAdmin.objects.filter(number = userName, password = userPassword)
            if ea.count() == 1:
                print('successE')
                request.session["id"] = ea[0].id
                request.session["type"] = "e"
                return HttpResponseRedirect("/EducationalSystem/jiaowu/")
            else:
                messages.error(request,"密码错误、用户不存在或帐号不属于教务用户")
                return HttpResponseRedirect("/EducationalSystem/")
            # if ea:
            # 	return render_to_response('index.html')
            # else:
            # 	return render_to_response('index.html')
        else:
            return HttpResponseRedirect("/EducationalSystem/")
    else:
        return HttpResponseRedirect("/EducationalSystem/")

# 注销功能，处理函数
def logout(request):
    try:
        del request.session['id']
        del request.session['type']
    except KeyError:
        pass
    return HttpResponseRedirect("/EducationalSystem/")


# 展示所有课程：教务 单独页面
def displayCourseForEA(request, t_id):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 'e':
        thisTerm = -1
        terms = Term.objects.order_by("-id")
        if not t_id:
            flag = False
            for i in terms:
                if i.is_current == True:
                    thisTerm = i
                    flag = True
                    break
            if flag == False:
                thisTerm = terms[0]
        else:
            t = Term.objects.get(id=t_id)
            thisTerm = t
        cou = Course.objects.filter(term_id__id=thisTerm.id)
        return render(request, "jiaowu.html", {'terms': terms, 'cou': cou, 't_id': t_id, 'thisTerm': thisTerm})
    else:
        return HttpResponseRedirect("/EducationalSystem/")


# 展示个人信息
def displayUserInfo(request):
    if 'id' in request.GET and request.GET['id']:
        if 'kind' in request.GET and request.GET['kind']:
            user_id = request.GET['id']
            userKind = request.GET['kind']

            if userKind == 's':
                stu = Student.objects.get(id=user_id)
            elif userKind == 't':
                tea = Teacher.objects.get(id=user_id)
            elif userKind == 'e':
                ea = EduAdmin.objects.get(id=user_id)


# 保存学期信息，处理函数
def saveTermInfo(request):
    if 'semester_name' in request.GET and 'semester_startdate' in request.GET \
            and 'semester_enddate' in request.GET and 'semester_numofweeks' in request.GET \
            and request.GET['semester_name'] and request.GET['semester_startdate'] \
            and request.GET['semester_enddate'] and request.GET['semester_numofweeks']:
        name = request.GET['semester_name']
        start = request.GET['semester_startdate']
        end = request.GET['semester_enddate']
        week = request.GET['semester_numofweeks']

        term_tmp = Term(name=name, start=start, end=end, week=week)
        term_tmp.save()
        return HttpResponseRedirect("/EducationalSystem/jiaowu/")
    else:
        print('cnm')
        return HttpResponseRedirect("/EducationalSystem/jiaowu/")

def changeTerm(request):
    if 'term' in request.GET and request.GET['term']:
        tid = request.GET['term']
        return HttpResponseRedirect("/EducationalSystem/jiaowu/" + str(tid))
    else:
        return HttpResponseRedirect("/EducationalSystem/jiaowu/")

#关闭学期
def closeTerm(request, term_id):
    try:
        term = Term.objects.get(id=term_id)
        term.is_over = True
        term.save()
        messages.success(request, "操作成功")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)
    except:
        messages.error(request, "操作失败")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)

#解除学期
def decloseTerm(request, term_id):
    try:
        term = Term.objects.get(id=term_id)
        term.is_over = False
        term.save()
        messages.success(request, "操作成功")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)
    except:
        messages.error(request, "操作失败")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/"+term_id)



# 添加课程，处理函数
def addCourse(request):
    if 'course_name' in request.GET and 'course_point' in request.GET \
            and 'course_time' in request.GET and 'course_location' in request.GET \
            and 'selectterm' in request.GET and 'course_timelength' in request.GET \
            and request.GET['course_point'] and request.GET['course_time'] \
            and request.GET['course_name'] and request.GET['course_timelength'] \
            and request.GET['course_location'] and request.GET['selectterm'] \
            and 'course_teacherid_0' in request.GET and request.GET['course_teacherid_0']:

        strhead = "course_teacherid_"
        count = 0
        name = request.GET['course_name']
        credit = request.GET['course_point']
        time = request.GET['course_time']
        hour = request.GET['course_timelength']
        location = request.GET['course_location']
        term_id = request.GET['selectterm']

        term = Term.objects.get(id=term_id)
        Course_tmp = Course(name=name, credit=credit, time=time, location=location, term_id=term, hour=hour)
        Course_tmp.save()

        cid = Course_tmp.id
        dirname = 'course' + str(cid)
        baseDir = os.path.dirname(os.path.abspath(__name__))
        filepath = os.path.join(baseDir, 'static', 'files', dirname)
        os.makedirs(filepath)
        rspath = os.path.join(filepath, 'rs')
        hwpath = os.path.join(filepath, 'hw')
        os.makedirs(rspath)
        os.makedirs(hwpath)

        while True:
            strq = strhead + str(count)
            if strq not in request.GET:
                break
            tea_num = request.GET[strq]
            Tea = Teacher.objects.get(number=tea_num)
            if not Tea:
                return HttpResponseRedirect("/EducationalSystem/jiaowu/")
            count = count + 1
            cou_tea = Course_Teacher(course_id=Course_tmp, teacher_id=Tea)
            cou_tea.save()

        return HttpResponseRedirect("/EducationalSystem/jiaowu/")
    else:
        return HttpResponseRedirect("/EducationalSystem/jiaowu/")


def rewriteCourse(request):
    if 'course_name' in request.GET and 'course_point' in request.GET \
            and 'course_time' in request.GET and 'course_location' in request.GET \
            and 'selectterm' in request.GET and 'course_timelength' in request.GET \
            and request.GET['course_point'] and request.GET['course_time'] \
            and request.GET['course_name'] and request.GET['course_timelength'] \
            and request.GET['course_location'] and request.GET['selectterm'] \
            and 'course_teacherid_0' in request.GET and request.GET['course_teacherid_0'] \
            and 'course_id' in request.GET and request.GET['course_id']:

        strhead = "course_teacherid_"
        count = 0
        name = request.GET['course_name']
        credit = request.GET['course_point']
        time = request.GET['course_time']
        hour = request.GET['course_timelength']
        location = request.GET['course_location']
        term_id = request.GET['selectterm']
        course_id = request.GET['course_id']

        term = Term.objects.get(id=term_id)
        # Course_tmp = Course(name=name, credit=credit, time=time, location=location, term_id=term, hour=hour)
        # Course_tmp.save()
        Course.objects.filter(id=course_id).update(name=name, credit=credit, time=time, location=location, term_id=term,
                                                   hour=hour)
        cou = Course.objects.get(id=course_id)
        cou_tea_tmp = Course_Teacher.objects.filter(course_id=cou)
        cou_tea_tmp.delete()

        while True:
            strq = strhead + str(count)
            if strq not in request.GET:
                break
            tea_num = request.GET[strq]
            Tea = Teacher.objects.filter(number=tea_num)
            if Tea.count() < 1:
                messages.error(request, "工号为 "+tea_num+" 的老师不存在")
                return HttpResponseRedirect("/EducationalSystem/jiaowu_course/"+course_id)
            count = count + 1
            cou_tea = Course_Teacher(course_id=cou, teacher_id=Tea)
            cou_tea.save()
        messages.success(request, "操作成功")
        return HttpResponseRedirect("/EducationalSystem/jiaowu_course/"+course_id)
    else:
        messages.error(request, "操作失败")
        return HttpResponseRedirect("/EducationalSystem/jiaowu/")



#def setTeacher(request):
#czy
#展示所有资源：教师/学生
def displayAllResource(request, course_id):
    Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True, virtual_path='/')
    Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False, virtual_path='/')
    print('display resource')
    print([res.id for res in Resources], [f.id for f in Folders], course_id, '/')
    if 'id' in request.session and request.session['id'] and 'type' in request.session:
        if request.session['type'] == 's':
            sen_type = 's'
        elif request.session['type'] == 't':
            sen_type = 't'
        else:
            return HttpResponseRedirect("/EducationalSystem/")
        return render(request, 'resources.html',
                    {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': '/', 'sen_type': sen_type})
    else:
        return HttpResponseRedirect("/EducationalSystem/")


# 上传资源：教师

# mine


# 展示所有作业
def displayCourseAssignments(request):
    if 'id' in request.GET and request.GET['id']:
        cur_id = request.GET['id']
        cur_ass = Assignment.objects.GET(course_id=cur_id)


# 展示作业信息：教师
def displayAssignmentsForTeacher(request):
    if 'id' in request.GET and request.GET['id']:
        ass_id = request.GET['id']
        stu_ass = Assignment_Resource.objects.filter(team_asn_id__asn_id__id=ass_id)
        ass_info = Assignment.objects.GET(id=ass_id)


# 展示作业信息：学生
def displayAssignmentsForStudents(request):
    if 'id' in request.GET and request.GET['id'] \
            and 'id' in request.session and request.session['id']:
        ass_id = request.GET['id']
        stu_id = request.session['id']
        ass_info = Assignment.objects.GET(id=ass_id)
        stu_team = Student_Team.objects.GET(student_id=stu_id, is_approved=True, team_id__course_id=ass_info.course_id)
        ass_res = Assignment_Resource.objects.filter(team_asn_id__team_id=stu_team.id)

# def downloadResource(request):
# 	if 'fid' in request.GET and request.GET['fid']:
# 		fid = request.GET['fid']
# 		myFile = Resource.objects.GET(id = fid)
# 		fname = myFile.name
# 		fpath = myFile.path
# 		def fileIterator(fname, chunk_size = 512):
# 			with open(fname) as f:
# 				while(True):
# 					c = f.read(chunk_size)
# 					if c:
# 						yield c
# 					else:
# 						break
# 		response = StreamingHttpResponse(fileIterator(fname))
# 		response['Content-Type'] = 'application/octet-stream'
# 		response['Content-Disposition'] = 'attachment;filename = "{0}"'.format(fname)
# 		return response



#评论学生作业：教师
def setTeamAssignmentComment(request):
    if 'TA_id' in request.GET and request.GET['TA_id'] and \
                    'comment' in request.GET and request.GET['comment']:
        TA_id = request.GET['TA_id']
        comment = request.GET['comment']

        TA_tmp = Team_Assignment(id=TA_id)
        TA_tmp.comment = comment
        TA_tmp.save()


# 给作业成绩：教师
def setTeamAssignmentMark(request):
    if 'TA_id' in request.GET and request.GET['TA_id'] and \
                    'mark' in request.GET and request.GET['mark']:
        TA_id = request.GET['TA_id']
        mark = request.GET['mark']

        TA_tmp = Team_Assignment(id=TA_id)
        TA_tmp.mark = mark
        TA_tmp.save()

#给作业成绩页面：教师
def displaySetGrade(request, TA_id):
    ta = Team_Assignment.objects.get(id = TA_id)
    messages.success(request,"设置作业成绩及评论-提交成功")
    return render(request, "teacher_setgrade.html", {'ta':ta})
    #return render_to_response("teacher_setgrade.html")

#给评价与成绩：教师
def setTeamAssignmentCommentMark(request,TA_id):
    if 	'homework_grade' in request.GET and request.GET['homework_grade'] and \
        'homework_comment' in request.GET and request.GET['homework_comment']:

        comment = request.GET['homework_comment']
        mark = request.GET['homework_grade']

        TA_tmp = Team_Assignment.objects.get(id=TA_id)
        TA_tmp.comment = comment
        TA_tmp.mark = mark
        TA_tmp.is_corrected = True
        TA_tmp.save()
        messages.success(request, "批改成功")
        return HttpResponseRedirect("/EducationalSystem/teacher/Asn/" + str(TA_tmp.asn_id.id) + "/")

#展示添加作业页面，单独页面
def displayAddAsn(request, cou_id):
    cou = Course.objects.get(id=cou_id)
    return render(request, "teacher_course_homework_add.html", {'cou':cou})

#添加作业，处理函数
def addAssignment(request, cou_id):

    url = ""
    if 	'assignment_name' in request.GET and request.GET['assignment_name'] and \
        'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
        'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
        'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
        'grade_ratio' in request.GET and request.GET['grade_ratio']:

        name = request.GET['assignment_name']
        requirement = request.GET['assignment_requirement']

        starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        duetime = request.GET['assignment_duetime']
        submit_limits = request.GET['maximum_submit']
        weight = request.GET['grade_ratio']

        dt_buf = duetime.split('T')
        try:
            dt_str = dt_buf[0]+' '+dt_buf[1]+":00"
        except:
            dt_str = duetime
        print(dt_str)

        # 判断起始截止时间先后
        if float(time.mktime(time.strptime(starttime,"%Y-%m-%d %H:%M:%S"))) >= float(time.mktime(time.strptime(dt_str,"%Y-%m-%d %H:%M:%S"))):
            messages.error(request,"操作失败：起始时间在截止时间同时或之前")
        else:
            cou = Course.objects.get(id=cou_id)
            asn = Assignment(name=name, requirement=requirement, starttime=starttime, duetime=dt_str, submit_limits =submit_limits, weight=weight, course_id=cou )
            asn.save()

            tem = Team.objects.filter(course_id=cou)

            for t in tem:
                t_a = Team_Assignment(asn_id=asn, team_id=t, submit_times=0)
                t_a.save()

            dirname = "course" + str(cou_id)
            asnname = asn.id
            baseDir = os.path.dirname(os.path.abspath(__name__))
            filepath = os.path.join(baseDir, 'static', 'files', dirname, 'hw', str(asnname))
            os.makedirs(filepath)
            messages.success(request,"新增作业-设置成功")
        url = "/EducationalSystem/teacher/CouAsn/"+str(asn.course_id.id)+"/"

    return  HttpResponseRedirect(url)
    # return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示修改作业页面，单独页面
def displayModAsn(request, asn_id):
    asn = Assignment.objects.get(id=asn_id)
    cou = asn.course_id
    return render(request, "teacher_course_homework_modify.html", {'asn':asn, 'cou':cou})

#修改作业，处理函数
def modifyAssignment(request, asn_id):

    if 'assignment_name' in request.GET and request.GET['assignment_name'] and \
        'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
        'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
        'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
        'grade_ratio' in request.GET and request.GET['grade_ratio']:

        name = request.GET['assignment_name']
        requirement = request.GET['assignment_requirement']
        duetime = request.GET['assignment_duetime']
        submit_limits = request.GET['maximum_submit']
        weight = request.GET['grade_ratio']

        dt_buf = duetime.split('T')
        try:
            dt_str = dt_buf[0]+' '+dt_buf[1]+":00"
        except:
            dt_str = duetime
        print(dt_str)

        asn = Assignment.objects.get(id=asn_id)
        asn.name = name
        asn.requirement = requirement
        asn.duetime = dt_str
        asn.submit_limits = submit_limits
        asn.weight = weight

        # 判断起始截止时间先后
        if float(time.mktime(time.strptime(asn.starttime,"%Y-%m-%d %H:%M:%S"))) >= float(time.mktime(time.strptime(dt_str,"%Y-%m-%d %H:%M:%S"))):
            messages.error(request,"操作失败：起始时间在截止时间同时或之前")
        else:
            asn.save()
            messages.success(request, "修改作业-设置成功")
        return_url="/EducationalSystem/teacher/CouAsn/"+str(asn.course_id.id)
        return HttpResponseRedirect(return_url)
    else:
        messages.warning(request,"修改作业失败-请重新填写")
        return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示所有作业，单独页面
def displayHwForTea(request, cou_id):
    cou = Course.objects.get(id=cou_id)
    asn = Assignment.objects.filter(course_id=cou)
    return render(request, "teacher_course_homework.html", {'asn': asn, 'cou':cou})

def displayCourseInfo(request, course_id):
    course = Course.objects.get(id=course_id)
    term = course.term_id
    cou_tea = Course_Teacher.objects.filter(course_id=course).values("teacher_id")
    tea = Teacher.objects.filter(id__in=cou_tea)
    return render(request, 'teacher_set_course_basicinfo.html',
                  {'course_id':course.id, 'term_name':term.name,
                   'course_name':course.name, 'time':course.time,
                   'location':course.location, 'credit':course.credit,
                   'hour':course.hour, "cou":course, 'tea':tea})

#展示单个作业，单独页面
def displayHw(request, asn_id):
    asn = Assignment.objects.get(id=asn_id)
    cou = asn.course_id
    tem = Team.objects.filter(course_id=cou)
    tas = Team_Assignment.objects.filter(team_id__in = tem, asn_id = asn)
    return render(request, "teacher_course_homework_watchdetails.html", {'asn':asn, 'tem':tas, 'cou':cou, })

def setStuGrade(request, t):

    tem_asn = Team_Assignment.objects.get(id=t)
    tem = tem_asn.team_id
    stu_tem = Student_Team.objects.filter(team_id=tem)

    strq = "rate_id_"
    cn = 1
    strA = strq + str(cn)
    all = 0.0
    while strA in request.GET and request.GET[strA]:
        f = request.GET[strA]
        all = all + float(f)
        cn = cn + 1
        strA = strq + str(cn)
    if all != cn - 1:
        messages.error(request, "所给系数不符合要求")
        print("所给系数不符合要求")
        return HttpResponseRedirect('/EducationalSystem/student/Asn/' + str(tem_asn.asn_id.id) + '/')
    cn = 1
    strA = strq + str(cn)
    while strA in request.GET and request.GET[strA]:
        f = request.GET[strA]
        st = cn - 1
        stu = stu_tem[st]
        stu_gd = Student_Grade(student_id=stu.student_id, team_asn_id=tem_asn)
        gd = float(f) * float(tem_asn.mark)
        stu_gd.weight = gd
        stu_gd.save()
        cn = cn + 1
        strA = strq + str(cn)
    tem_asn.is_graded = True
    tem_asn.save()
    messages.success(request, "设置成功")
    return HttpResponseRedirect('/EducationalSystem/student/Asn/' + str(tem_asn.asn_id.id) + '/')

# 删除作业
def deleteAssignment(request, asn_id):
    TA = Team_Assignment.objects.filter(asn_id__id=asn_id)

    Assignment_Resource.objects.filter(team_asn_id__in=TA).delete()
    Student_Grade.objects.filter(team_asn_id__in=TA).delete()

    TA.delete()

    asn = Assignment.objects.get(id=asn_id)
    cou_id = asn.course_id.id
    asn.delete()
    return HttpResponseRedirect("/EducationalSystem/teacher/CouAsn/" + str(cou_id) +"/")

#从excel中添加课程学生表条目
def addCourseStudent(request, cid):
    if request.method == 'POST' :
        if "fileupload" not in request.FILES or not request.FILES["fileupload"]:
            messages.error(request, "上传失败")
            return HttpResponseRedirect("/EducationalSystem/jiaowu_course/" + str(cid) + "/")
        myFiles = request.FILES["fileupload"]


        baseDir = os.path.dirname(os.path.abspath(__name__))
        filepath = os.path.join(baseDir, 'static', 'files', myFiles.name)
        destination = open(filepath, 'wb+')


        for chunk in myFiles.chunks():
            destination.write(chunk)

        stri = myFiles.name.split('.')
        type = stri[-1]
        if type == "xlsx":
            num, recs = readFromXLSX(filepath)
        else:
            messages.error(request, "上传失败")
            return HttpResponseRedirect("/EducationalSystem/jiaowu_course/" + str(cid) + "/")

        for i in range(num):
            #c_id = recs[i][0].value
            stu_id = recs[i][0].value
            #stu_name = recs[i][2].value
            cur_stu = Course_Student.objects.filter(course_id__id = cid, student_id__number = stu_id)
            if cur_stu:
                continue
            else:
                cou = Course.objects.get(id=cid)
                stu = Student.objects.filter(number=stu_id)
                if stu:
                    stu1 = Student.objects.get(number=stu_id)
                    cour_stu = Course_Student(course_id=cou, student_id=stu1)
                    cour_stu.save()
                else:
                    continue
        messages.success(request,"上传成功")
        return HttpResponseRedirect("/EducationalSystem/jiaowu_course/" + str(cid) +"/")
    else:
        return HttpResponseRedirect("/EducationalSystem/jiaowu_course/" + str(cid) +"/")

def setCourseInfo(request, course_id):
    print('team_uplimit' in request.GET, 'team_downlimit' in request.GET,
          'other_limit' in request.GET, 'description' in request.GET)
    if 'team_uplimit' in request.GET and request.GET['team_uplimit'] and \
        'team_downlimit' in request.GET and request.GET['team_downlimit'] and \
        'other_limit' in request.GET and 'description' in request.GET:
        team_uplimit = request.GET['team_uplimit']
        team_downlimit = request.GET['team_downlimit']
        other_limit = request.GET['other_limit']
        description = request.GET['description']

        course = Course.objects.get(id=course_id)
        course.team_uplimit = team_uplimit
        course.team_downlimit = team_downlimit
        course.other_limit = other_limit
        course.description = description
        course.save()
        return_url="/EducationalSystem/teacher/course/"+course_id
        return HttpResponseRedirect(return_url)
        #return HttpResponseRedirect("/EducationalSystem/jiaowu/")

    else:
        return HttpResponseRedirect("/EducationalSystem/teacher/")

def uploadResource(request):
    # print('updateResource')
    # #file_obj = request.POST.get('file')
    # file_obj = request.FILES.get('file')
    # print(file_obj)
    # path = request.POST.get('path')
    # print(path)
    # f = open(os.path.join('C:\\Users\\Administrator\\Desktop\\', file_obj.name), 'wb+')
    # for chunk in file_obj.chunks():
    # 	f.write(chunk)
    # f.close()
    # return HttpResponse('ok')
    if request.method == 'POST':
        myFiles = request.FILES.getlist("file", None)
        print(myFiles)
        course_id = request.POST.get('courseid')
        virpath = request.POST.get('path')
        cou = Course.objects.get(id=course_id)
        if not myFiles:
            dstatus = ("No file to upload")
            return
        ret_str = ''
        for f in myFiles:
            baseDir = os.path.dirname(os.path.abspath(__name__))
            filepath = os.path.join(baseDir, 'static', 'files', 'course'+str(course_id), 'rs')
            for name in virpath.split('/'):
                filepath = os.path.join(filepath, name)
            filepath = os.path.join(filepath, f.name)
            print(filepath)
            destination = open(filepath, 'wb+')
            res = Resource(name=f.name, path=filepath, course_id=cou, virtual_path=virpath, is_dir=False)
            res.save()
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            ret_str = ret_str + '<li class="myfile"><input type="text" class="changename" name="1" value="' + \
                res.name + '"/><input class="checkbox" name="' + str(res.id) + '" type="checkbox" value="" /></li>' + '\n'
            print(ret_str)

        print('ready to return')
        return HttpResponse(ret_str)
    # file_obj = request.FILES.get('file')
    # if file_obj:  # 处理附件上传到方法
    # 	request_set = {}
    # 	print('file--obj', file_obj)
    # 	# user_home_dir = "upload/%s" % (request.user.userprofile.id)
    # 	accessory_dir = settings.accessory_dir
    # 	if not os.path.isdir(accessory_dir):
    # 		os.mkdir(accessory_dir)
    # 	upload_file = "%s/%s" % (accessory_dir, file_obj.name)
    # 	recv_size = 0
    # 	with open(upload_file, 'wb') as new_file:
    # 		for chunk in file_obj.chunks():
    # 			new_file.write(chunk)
    # 	order_id = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 	cache.set(order_id, upload_file)
    # 	return HttpResponse(order_id)

def downloadResource(request, down):
    utilities = ZipUtilities()
    # if 'down' in request.GET and request.GET['down']:
    # unsplitted = request.GET['down']
    unsplitted = down
    splitted = unsplitted.split(',')
    num = len(splitted) - 1
    resource_id = splitted[0:num]
    for r_id in resource_id:
        res = Resource.objects.get(id=int(r_id))
        tmp_dl_path = res.path
        print('')
        utilities.toZip(tmp_dl_path, res.name)
    # utilities.close()
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("download.zip")
    print('download success')
    # dlResource(response)
    return response

# def dlResource(response):
# 	return response

    # team_asn = Team_Assignment.objects.get(team_id=tid, asn_id__id=asn_id)
    # asn_res = Assignment_Resource.objects.filter(team_asn_id=team_asn)
    # utilities = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
    # for a_r in asn_res:
    # 	tmp_dl_path = a_r.path
    # 	utilities.write(tmp_dl_path, arcname=os.path.basename(tmp_dl_path))
    # # utilities.close()
    # response = StreamingHttpResponse(utilities, content_type='application/zip')
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")#需要更改文件名
    # return response

def deleteResource(request):
    print('del' in request.GET)

    if 'del' in request.GET and request.GET['del'] and \
        'path' in request.GET and request.GET['path']:

        unsplitted = request.GET['del']
        splitted = unsplitted.split(',')
        num = len(splitted) - 1
        course_id = int(splitted[num])
        virpath = request.GET['path']

        for i in range(num):
            res_id = int(splitted[i])
            res = Resource.objects.get(id=res_id)
            is_dir = res.is_dir
            path = res.path
            if is_dir:
                resources = Resource.objects.filter(path__startswith=path, is_dir=False).order_by('is_dir')
                folders = Resource.objects.filter(path__startswith=path, is_dir=True).order_by('-path')
                for resource in resources:
                    os.remove(resource.path)
                    resource.delete()
                for folder in folders:
                    print(folder.id, folder.name, folder.path)
                    os.rmdir(folder.path)
                    folder.delete()


                #resources.delete()
                #os.removedirs(path)
            else:
                res.delete()
                os.remove(path)

        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True)
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False)

        if 'type' in request.session and request.session['type'] == 's':
            sen_type = 's'
        elif 'type' in request.session and request.session['type'] == 't':
            sen_type = 't'
        else:
            sen_type = 'err'

        return render(request, 'resources.html',
                      {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': virpath, 'sen_type': sen_type})
    else:
        course_id = 0
        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True)
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False)
        virpath = '/'
        if 'type' in request.session and request.session['type'] == 's':
            sen_type = 's'
        elif 'type' in request.session and request.session['type'] == 't':
            sen_type = 't'
        else:
            sen_type = 'err'
        return render(request, 'resources.html',
                      {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': virpath, 'sen_type': sen_type})


def uploadHomework(request,asn_id):
    if request.method == 'POST' and 'id' in request.session and request.session['id']:

        sid = request.session['id']
        asne = Assignment.objects.get(id=asn_id)
        stu = Student_Team.objects.get(student_id__id=sid, team_id__course_id=asne.course_id)
        stu_team =stu.team_id

        strA = "assignment_attachment_"
        i = 0

        while True:
            newStr = strA + str(i)
            if newStr in request.FILES:
                file_obj = request.FILES[newStr]

                asn = Assignment.objects.get(id=asn_id)
                cou = asn.course_id
                couDir = "course" + str(cou.id)
                baseDir = os.path.dirname(os.path.abspath(__name__))
                filepath = os.path.join(baseDir, 'static', 'files', couDir, 'hw', str(asn_id), file_obj.name)

                destination = open(filepath, 'wb+')
                # asn_res = Assignment_Resource(team_asn_id = teamAsn.id, path = destination, is_corrected = False)
                # asn_res.save()
                t_a = Team_Assignment.objects.get(asn_id=asn, team_id=stu_team)
                t_a.submit_times = t_a.submit_times + 1
                if t_a.submit_times > asn.submit_limits:
                    messages.error(request, "提交次数超过上限")
                    return HttpResponseRedirect("/EducationalSystem/student/Asn/" + asn_id +"/")

                t_a.save()
                asn_res = Assignment_Resource(team_asn_id=t_a, path=filepath)
                asn_res.save()
                for chunk in file_obj.chunks():
                    destination.write(chunk)
                destination.close()
                i = i + 1
            else:
                break
        messages.success(request, "提交成功")
        return HttpResponseRedirect("/EducationalSystem/student/Asn/" + asn_id +"/")
    messages.error(request, "无文件提交")
    return HttpResponseRedirect("/EducationalSystem/student/Asn/" + asn_id +"/")


# def downloadHomework(request, asn_id, tid):
# 		# file_obj = request.FILES.getlist(asdfh)
# 		team_asn = Team_Assignment.objects.get(team_id = tid, asn_id = asn_id)
# 		asn_res =  Assignment_Resource.objects.filter(team_asn_id = team_asn)
#
# 		asn_res_path = asn_res.path
# 		#asn_res_id = asn_res.team_asn_id
#
# 		def fileIterator(fpath, chunk_size = 1024):
# 			with open(fpath) as f:
# 				while(True):
# 					print('yes')
# 					c = f.read(chunk_size)
# 					if c:
# 						yield c
# 					else:
# 						break
#
#
# 		aresponse = StreamingHttpResponse(fileIterator(asn_res_path))
# 		aresponse['Content-Type'] = 'application/octet-stream'
# 		aresponse['Content-Disposition'] = 'attachment;filename = "{0}"'.format(asn_res_path)
# 		return aresponse


def downloadHomework(request, asn_id, tid):
    team_asn = Team_Assignment.objects.get(team_id=tid, asn_id__id=asn_id)
    asn_res = Assignment_Resource.objects.filter(team_asn_id=team_asn)
    utilities = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
    for a_r in asn_res:
        tmp_dl_path = a_r.path
        utilities.write(tmp_dl_path, arcname=os.path.basename(tmp_dl_path))
    # utilities.close()
    response = StreamingHttpResponse(utilities, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("download.zip")#需要更改文件名
    return response

def downloadAllHomework(request, asn_id):
    team_asn = Team_Assignment.objects.filter(asn_id__id = asn_id)
    asn_res = Assignment_Resource.objects.filter(team_asn_id__in=team_asn)
    utilities = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
    for a_r in asn_res:
        tmp_dl_path = a_r.path
        utilities.write(tmp_dl_path, arcname=os.path.basename(tmp_dl_path))
    # utilities.close()
    response = StreamingHttpResponse(utilities, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("download.zip")  # 需要更改文件名
    return response

# def downloadHomework(request, asn_id, tid):
# 	team_asn = Team_Assignment.objects.get(team_id=tid, asn_id=asn_id)
# 	asn_res = Assignment_Resource.objects.filter(team_asn_id=team_asn)
# 	utilities = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
# 	for a_r in asn_res:
# 		tmp_dl_path = a_r.path
# 		utilities.write(tmp_dl_path, arcname=os.path.basename(tmp_dl_path))
# 	# utilities.close()
# 	response = StreamingHttpResponse(utilities, content_type='application/zip')
# 	response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")#需要更改文件名
# 	return response

#展示学生课程信息页面，单独页面
def displayCouForStu(request, cou_id):
    cou = Course.objects.get(id=cou_id)
    term = cou.term_id
    cou_tea = Course_Teacher.objects.filter(course_id_id=cou_id).values("teacher_id")
    tea = Teacher.objects.filter(id__in=cou_tea)
    return render(request, "student_course_basicinfo.html", {'cou':cou, 'term':term, 'tea':tea})

#展示学生所有作业页面，单独页面
def displayHwForStu(request, cou_id):
    cou = Course.objects.get(id=cou_id)
    asn = Assignment.objects.filter(course_id=cou)
    return render(request, "student_course_homework.html", {'cou':cou, 'asn':asn})

#展示学生某一作业，单独页面
def displayStuHw(request, asn_id):
    if 'id' in request.session and request.session['id'] and \
        'type' in request.session and request.session['type'] == 's':

        stu_id = request.session['id']
        stu = Student.objects.get(id=stu_id)
        asn = Assignment.objects.get(id=asn_id)
        cou = asn.course_id
        tem = Team.objects.filter(course_id=cou, manager_id=stu)
        stu_tem = Student_Team.objects.get(team_id__course_id=cou, student_id=stu)
        hisTem = stu_tem.team_id
        if not tem:
            #not manager

            tem_asn = Team_Assignment.objects.get(team_id=hisTem, asn_id=asn)
            asn_res = Assignment_Resource.objects.filter(team_asn_id=tem_asn)
            #stu_gd = Student_Grade.objects.get(team_asn_id=tem_asn, student_id=stu)

            #grade = stu_gd.weight * tem_asn
            names = []
            grade = 0
            if tem_asn.is_graded == True:
                stu_gd = Student_Grade.objects.get(team_asn_id=tem_asn, student_id=stu)
                grade = stu_gd.weight
            else:
                grade = 0
            for a_r in asn_res:
                filename = a_r.path.split('/')
                name = filename[-1]
                names.append((a_r.path,name))
            return render(request, "student_course_homework_watchdetails.html", {'cou': cou, 'asn': asn, "asn_res":asn_res, "tem_asn":tem_asn, "names":names, "grade":grade})
        else:
            tem_asn = Team_Assignment.objects.get(team_id__in=tem, asn_id=asn)
            s_t = Student_Team.objects.filter(team_id=hisTem)
            asn_res = Assignment_Resource.objects.filter(team_asn_id=tem_asn)
            names = []
            if tem_asn.is_graded == True:
                stu_gd = Student_Grade.objects.get(team_asn_id=tem_asn, student_id=stu)
                grade = stu_gd.weight
            else:
                grade = 0
            for a_r in asn_res:
                filename = a_r.path.split('/')
                name = filename[-1]
                names.append((a_r.path,name))

            # 判断是否已到DDL
            if float(time.mktime(time.localtime())) >= float(time.mktime(time.strptime(asn.duetime,"%Y-%m-%d %H:%M:%S"))):
                ddl_status = 1
            else:
                ddl_status = 0
            return render(request, "student_course_homework_watchdetails_manager.html", {'cou':cou, 'asn':asn, "asn_res":asn_res, "tem_asn":tem_asn, "stu_tem":s_t, "names":names, "grade":grade, 'ddl_status':ddl_status})

    return HttpResponseRedirect('/EducationalSystem/')


def doubleclick(request):
    print(request.GET['id'])
    print(request.GET['name'])
    print(request.GET['path'])

    if 'id' in request.GET and request.GET['id'] and \
        'name' in request.GET and request.GET['name'] and \
        'path' in request.GET and request.GET['path']:

        print(111)

        course_id = Resource.objects.get(id=int(request.GET['id'])).course_id.id
        print(course_id)
        folder_name = request.GET['name']
        virpath = request.GET['path']
        virpath = virpath + folder_name + '/'

        print(course_id, folder_name, virpath)
        #Folders = Resource.objects.filter(course_id__id=course_id, path_isnull=True, virtual_path=virpath)
        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True, virtual_path=virpath)
        print('Folder done.')
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False, virtual_path=virpath)

        print('ready to render '+virpath)
        print([res.id for res in Resources], [f.id for f in Folders], course_id, virpath)
        #return render(request, 'resources.html',
        #			  {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': virpath})

        ############

        ret_str = fileSystemResponse(Resources, Folders)
        print(ret_str)
        ############

        return HttpResponse(ret_str)
    else:
        course_id = 0
        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True)
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False)
        virpath = '/'
        ret_str = fileSystemResponse(Resources, Folders)
        return HttpResponse(ret_str)
        #return render(request, 'resources.html',
        #			  {'resources': Resources, 'folders':Folders, 'course_id': course_id, 'virpath': virpath})

def returnSuperiorMenu(request):
    print('returnSuperiorMenu')
    if 'id' in request.GET and request.GET['id'] and \
        'path' in request.GET and request.GET['path']:

        course_id = request.GET['id']
        virpath = request.GET['path']

        if virpath == '/':
            return HttpResponse('root')

        splitted = virpath.split('/')
        num = len(splitted)

        new_virpath = ''

        for i in range(num-2):
            new_virpath = new_virpath + splitted[i] + '/'

        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True, virtual_path=new_virpath)
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False, virtual_path=new_virpath)

        print([f.id for f in Folders], [res.id for res in Resources])

        ret_str = fileSystemResponse(Resources, Folders)

        return HttpResponse(ret_str)

    else:
        course_id = 0
        Folders = Resource.objects.filter(course_id__id=course_id, is_dir=True)
        Resources = Resource.objects.filter(course_id__id=course_id, is_dir=False)
        virpath = '/'

        ret_str = fileSystemResponse(Resources, Folders)
        return HttpResponse(ret_str)

def returnVirpath(request):

    print('id' in request.GET, 'name' in request.GET, 'path' in request.GET, 'flag' in request.GET)
    # print(request.GET['id'], request.GET['name'], request.GET['path'], request.GET['flag'])

    if 'flag' in request.GET and request.GET['flag']:

        if request.GET['flag']=='1':
            if 'id' in request.GET and request.GET['id'] and \
                'name' in request.GET and request.GET['name'] and \
                'path' in request.GET and request.GET['path']:
                folder_name = request.GET['name']
                virpath = request.GET['path']
                virpath = virpath + folder_name + '/'

                return HttpResponse(virpath)

        elif request.GET['flag']=='2':
            if 'id' in request.GET and request.GET['id'] and \
                'path' in request.GET and request.GET['path']:

                virpath = request.GET['path']
                if virpath=='/':
                    return HttpResponse('/')
                splitted = virpath.split('/')
                num = len(splitted)
                new_virpath = ''
                for i in range(num - 2):
                    new_virpath = new_virpath + splitted[i] + '/'
                return HttpResponse(new_virpath)

def createFolder(request):
    if 'courseid' in request.GET and request.GET['courseid'] and \
        'path' in request.GET and request.GET['path'] and \
        'foldername' in request.GET and request.GET['foldername']:

        course_id = request.GET['courseid']
        folder_name = request.GET['foldername']
        virpath = request.GET['path']

        print('virpath=' + virpath)
        baseDir = os.path.dirname(os.path.abspath(__name__))
        filepath = os.path.join(baseDir, 'static', 'files', 'course'+str(course_id), 'rs')
        for name in virpath.split('/'):
            filepath = os.path.join(filepath, name)
        print('baseDir=' + baseDir, 'filepath=' + filepath)
        os.makedirs(os.path.join(filepath, folder_name))

        print(folder_name, virpath+folder_name+'/', course_id)

        res = Resource(name=folder_name, path=os.path.join(filepath, folder_name), virtual_path=virpath, course_id_id=course_id, is_dir=True)
        res.save()
        ret_str = '<li class="myfolder"><input type="text" class="changename" name="1" value="' + \
                res.name + '"/><input class="checkbox" name="' + str(res.id) + '" type="checkbox" value="" /></li>'
        return HttpResponse(ret_str)

def displayInfo(request):
    if "id" in request.session and request.session["id"] and "type" in request.session and request.session["type"]:
        user_id = request.session["id"]
        user_type = request.session["type"]
        if user_type == "s":
            stu = Student.objects.get(id=user_id)
            return render(request, "student_profile.html", {"stu":stu})
        elif user_type == "t":
            tea = Teacher.objects.get(id=user_id)
            return render(request, "teacher_and_admin_profile.html", {"user":tea,"type":"t"})
        elif user_type == "e":
            ea = EduAdmin.objects.get(id=user_id)
            return render(request, "teacher_and_admin_profile.html", {"user":ea,"type":"e"})

def chat_index(request,cou_id):
    if 'type' in request.session and request.session['type'] == 's':
        sen_type = 's'
    elif 'type' in request.session and request.session['type'] == 't':
        sen_type = 't'
    cou = Course.objects.get(id=cou_id)
    chats = list(Chat.objects.filter(courseid_id=cou_id))[-4:]
    last_chat = list(Chat.objects.all())[-1:]
    return render(request, 'chat.html', {'chats': chats, 'cou': cou, 'sen_type':sen_type, 'last_chat':last_chat})


def chat(request):
    if request.method == 'POST':
        #print("get post")
        post_type = request.POST.get('post_type')
        cou_id = request.POST.get('cou_id_holder')
        if post_type == 'send_chat':
            #print("enter sendchat")
            if 'id' in request.session and request.session['id'] \
                    and 'type' in request.session and request.session['type'] == 's':
                sid = request.session['id']
                name = Student.objects.get(id=sid).name
                sender_type = "学生"
            elif 'id' in request.session and request.session['id'] \
                    and 'type' in request.session and request.session['type'] == 't':
                sender_type = "老师"
                tid = request.session['id']
                name = Teacher.objects.get(id=tid).name
            new_chat = Chat.objects.create(content=request.POST.get('content'),sender=name,courseid_id=cou_id,type=sender_type)
            new_chat.save()
            #chats = list(Chat.objects.filter(id=cou_id))
            return HttpResponse()
        elif post_type == 'get_chat':
            cou_id = int(request.POST.get('cou_id_holder'))
            #print("enter getchat")
            #print(cou_id)
            #chats = list(Chat.objects.filter(courseid_id = cou_id))[-4:]
            last_chat_id = int(request.POST.get('last_chat_id'))
            print(last_chat_id)
            chats = Chat.objects.filter(id__gt=last_chat_id,courseid_id=cou_id)
            return render(request, 'chat_list.html',{'chats': chats})

#ABOUT TEAM
def displayMyTeam(request, cid):
    if "id" in request.session and request.session["id"] and \
        "type" in request.session and request.session["type"] == "s":
        stu_id = request.session["id"]
        cou = Course.objects.get(id=cid)
        stu_tem = Student_Team.objects.filter(team_id__course_id__id=cid, student_id=stu_id)
        if stu_tem.count() < 1:
            tem = Team.objects.filter(manager_id__id=stu_id, course_id=cou)
            if tem.count() < 1:
                return render(request, "student_course_myteam_noteam.html", {"cou":cou})
            else:
                stus = None
                sts = "审核未通过"
                return render(request, "student_course_myteam_manager.html", {"tem": tem[0], "stus": stus, "status": sts, "cou": cou})
        tem = stu_tem[0].team_id


        #is_manager = Team.object.fliter(id=tem, manager_id=stu_id)
        sts = ""
        if tem.manager_id.id != stu_id:
            stu_dt = Student_Team.objects.get(team_id=tem, student_id__id=stu_id)
            if stu_dt.is_approved == False:
                sts = "申请中"
            else:
                sts = "申请通过"
            stus = Student_Team.objects.filter(team_id=tem, is_approved=True)
            return render(request, "student_course_myteam.html", {"tem":tem, "stus":stus, "status":sts, "cou":cou})
            # is not a manager
        else:
            # is a manager
            if tem.status == 0:
                sts = "组建中"
            elif tem.status == 1:
                sts = "审核中"
            elif tem.status == 2:
                sts = "审核通过"
            elif tem.status == 3:
                sts = "审核未通过"
            stus = Student_Team.objects.filter(team_id=tem)
            return render(request, "student_course_myteam_manager.html", {"tem":tem, "stus":stus, "status":sts, "cou":cou})
    return HttpResponseRedirect('/EducationalSystem/')

def displayTeamDt(request, tem_id):
    if "id" in request.session and request.session["id"] and \
        "type" in request.session and request.session["type"] == "s":
        stu_id = request.session["id"]
        tem = Team.objects.get(id=tem_id)
        cou = tem.course_id
        stu_team = Student_Team.objects.filter(team_id__course_id=cou, student_id__id=stu_id)
        psSts = False
        if stu_team.count() < 1:
            psSts = True
        else:
            psSts = False

        sts = ""

        if tem.status == 0:
            sts = "组建中"
        elif tem.status == 1:
            sts = "审核中"
        elif tem.status == 2:
            sts = "审核通过"
        elif tem.status == 3:
            sts = "审核未通过"
        stus = Student_Team.objects.filter(team_id=tem)
        return render(request, "student_course_teamdetails.html", {"tem":tem, "stus":stus, "status":sts, "cou":cou, "psSts":psSts})
    return HttpResponseRedirect("/EducationalSystem/")

def teamApply(request, tem_id):
    if "id" in request.session and request.session["id"] and \
        "type" in request.session and request.session["type"] == "s":
        stu_id = request.session["id"]
        tem = Team.objects.get(id=tem_id)
        cou = tem.course_id.id
        stu = Student.objects.get(id=stu_id)
        stu_tem = Student_Team(team_id=tem, student_id=stu, is_approved=False)
        stu_tem.save()
        return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou) +"/")
    return HttpResponseRedirect("/EducationalSystem/")

def displayAllTeam(request, cou_id):
    if "id" in request.session and request.session["id"] and \
        "type" in request.session and request.session["type"] == "s":
        tem = Team.objects.filter(course_id__id=cou_id, status__lt=3)
        cou = Course.objects.get(id=cou_id)
        stu_id = request.session["id"]
        Stu_team = Student_Team.objects.filter(team_id__course_id__id=cou_id, student_id__id=stu_id)
        psSts = False
        if Stu_team.count() < 1:
            psSts = True
        else:
            psSts = False
        # if tem.status == 0:
        # 	sts = "组建中"
        # elif tem.status == 1:
        # 	sts = "未审核"
        # elif tem.status == 2:
        # 	sts = "审核通过"
        # elif tem.status == 3:
        # 	sts = "审核未通过"
    return render(request, "student_course_teamlist.html", {"tem":tem, "cou":cou, "psSts":psSts})

def acceptApply(request, st_id):
    st = Student_Team.objects.get(id=st_id)
    st.is_approved = True
    st.save()
    cou = st.team_id.course_id.id
    return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou) + "/")

def refuseApply(request, st_id):
    st = Student_Team.objects.get(id=st_id)
    cou = st.team_id.course_id.id
    st.delete()
    return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou) + "/")

def submitApply(request, tem_id):
    tem = Team.objects.get(id=tem_id)
    cou = tem.course_id
    stu_tem = Student_Team.objects.filter(team_id=tem)
    if cou.team_downlimit is not None:
        if len(stu_tem) < cou.team_downlimit:
            messages.error(request, "人数不足")
            return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou.id) + "/")#不允许审核
    for member in stu_tem:
        if member.is_approved == 0:
            messages.error(request, "存在未通过申请的学生， 不允许审核")
            return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou.id) + "/")
    tem.status = 1
    tem.save()
    return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou.id) + "/")#允许审核

def displayTeamListForTeacher(request, cou_id):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 't':
        # 判断老师是否教这门课
        # cou_id 代表课程id
        have_course = Course_Teacher.objects.filter(teacher_id=request.session['id'],course_id=cou_id)
        if have_course.count() < 1:
            return HttpResponseRedirect("/EducationalSystem/teacher")
        else:
            # 所有该门课程团队的display
            team_list = Team.objects.filter(course_id=cou_id)
            cou = Course.objects.get(id=cou_id)
            return render(request, "teacher_course_teamlist.html", {'cou':cou, 'team_list':team_list})
    else:
        # 禁止访问
        return HttpResponseRedirect("/EducationalSystem/")

# 查看团队详情页面，单独页面
def disPlayTeamInfoForTeacher(request, team_id):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 't':
        # 判断老师是否教这门课
        # cou_id 代表课程id
        try:
            team=Team.objects.get(id=team_id)
        except:
            return HttpResponseRedirect("/EducationalSystem/")
        cou_id=team.course_id.id
        have_course = Course_Teacher.objects.filter(teacher_id=request.session['id'],course_id=cou_id)
        if have_course.count() < 1:
            return HttpResponseRedirect("/EducationalSystem/teacher")
        else:
            # 该队伍的信息，team
            # 未加入任何团队或已解散团队的学生的信息
            # 已解散团队Student_team表已删除
            # 上该课的学生_课程
            cs_have_course = Course_Student.objects.filter(course_id=cou_id)
            # 有团队的学生_团队
            ts = Student_Team.objects.all()
            ts_have_team = []
            for i in ts:
                if i.team_id.course_id.id == cou_id:
                    ts_have_team.append(i)
            # 无团队的学生-查找
            student_have_course = []
            for st in cs_have_course:
                student_have_course.append(st.student_id)
            student_have_team = []
            for st in ts_have_team:
                student_have_team.append(st.student_id)
            # 无团队的学生
            student_have_no_team=list(set(student_have_course).difference(set(student_have_team)))
            # 团队学生列表
            ts_member=Student_Team.objects.filter(team_id=team_id)
            student_teammember = []
            for st in ts_member:
                student_teammember.append(st.student_id)
            uplimit = team.course_id.team_uplimit
            team_member_cnt=ts_member.count()
            return render(request, "teacher_course_team_teaminfo.html", {'cou':team.course_id, 'team':team, 'student_have_no_team':student_have_no_team, 'teammember': student_teammember, 'uplimit':uplimit, 'cnt':team_member_cnt})
    else:
        # 禁止访问
        return HttpResponseRedirect("/EducationalSystem/")

#
# 0: 未提交团队申请
# 1：已提交团队申请未审核
# 2：已提交团队申请，并通过申请
# 3：已提交团队申请，未通过审核
#

# 教师批准团队申请
# 返回原页面 teacher_course_team_teaminfo
def approveTeam(request, team_id):
    team = Team.objects.get(id=team_id)
    team.status = 2
    team.save()
    #alert
    messages.success(request,"团队批准成功")
    direct="/EducationalSystem/teacher/teamDt/"+team_id
    return HttpResponseRedirect(direct)

# 教师不通过团队申请
# 返回原页面
def disapproveTeam(request, team_id):
    if 'id' in request.session and request.session['id'] \
            and 'type' in request.session and request.session['type'] == 't' \
            and 'refuse_reason' in request.GET:
        team = Team.objects.get(id=team_id)
        team.status = 3
        team.reason = request.GET['refuse_reason']
        team.save()
        #给各位发站内信？？？
        Student_Team.objects.filter(team_id=team).delete()
        messages.success(request,"拒绝申请成功")
        direct="/EducationalSystem/teacher/teamDt/"+team_id
        return HttpResponseRedirect(direct)
    else:
        messages.error(request,"操作失败")
        direct="/EducationalSystem/teacher/teamDt/"+team_id
        return HttpResponseRedirect(direct)

# 新增团队成员
def add_team_member(request, team_id, student_id):
    stu = Student_Team.objects.filter(student_id=student_id)
    if (len(stu) > 0):
        # 说明该学生已有团队，包括未审核团队
        msg="操作失败：学生 "+student_id.name+" 已有团队"
        messages.error(request,msg)
        direct="/EducationalSystem/teacher/teamDt/"+team_id
        return HttpResponseRedirect(direct)
    else:
        team_members = Student_Team.objects.filter(team_id=team_id)
        team = Team.objects.get(id=team_id)
        student = Student.objects.get(id=student_id)
        if (len(team_members) >= team.course_id.team_uplimit):
            # 团队成员人数大于等于上限
            msg="操作失败：该团队成员已达到设定上限"
            messages.error(request,msg)
            direct="/EducationalSystem/teacher/teamDt/"+team_id
            return HttpResponseRedirect(direct)
        else:
            new_team_member = Student_Team(team_id=team, student_id=student, is_approved=True)
            new_team_member.save()
            msg="学生 "+student.name+" 已成功加入该团队"
            messages.success(request, msg)
            print(msg)
            direct="/EducationalSystem/teacher/teamDt/"+team_id
            return HttpResponseRedirect(direct)

def applyCreateTeam(request, cou_id):
    if 'team_name' in request.GET and request.GET['team_name'] and \
        'description' in request.GET and request.GET['description']and \
        'id' in request.session and request.session['id']:
        nm = request.GET['team_name']
        dis = request.GET['description']
        sid = request.session['id']
        stu = Student.objects.get(id = sid)
        cid = Course.objects.get(id = cou_id)
        tm = Team(name = nm, course_id = cid, status = 0, manager_id = stu, discription = dis)
        tm_chek = Team.objects.filter(name = nm, course_id = cou_id, status = 0 or 1 or 2)
        if not tm_chek:
            tm.save()
            st = Student_Team(team_id=tm, student_id=stu, is_approved=True)
            st.save()
            cou = tm.course_id.id
            return HttpResponseRedirect("/EducationalSystem/student/team/" + str(cou) +"/")

def applyTeam(request, cou_id):
    if 'id' in request.session and request.session['id'] \
        and 'type' in request.session and request.session['type'] == 's':
        stu_id = request.session["id"]
        stu_team = Student_Team.objects.filter(student_id=stu_id, team_id__course_id__id=cou_id)
        sts = False
        if not stu_team:
            sts = True
        else:
            sts = False
        cou = Course.objects.get(id = cou_id)
        return render(request, "apply_team.html", {'cou' : cou, 'sts':sts})
    return HttpResponseRedirect("/EducationalSystem/")

def teacherUpldAsn(request,asn_id):
    if request.method == 'POST':
        asn = Assignment.objects.get(id=asn_id)
        cou = asn.course_id
        couDir = "course" + str(cou.id)
        myFiles = request.FILES.getlist("assignment_attachment_",None)
        print(myFiles)
        print('hello')
        if not myFiles:
            return
        for f in myFiles:
            baseDir = os.path.dirname(os.path.abspath(__name__))
            filepath = os.path.join(baseDir, 'static', 'files', couDir, 'hw', str(asn_id), f.name)
            print(filepath)
            destination = open(filepath, 'wb+')
            asn_res = Assignment_Resource.objects.get(path=filepath)
            asn_res.is_corrected = True
            asn_res.save()
            print(asn_res.is_corrected)
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
        return HttpResponseRedirect("/EducationalSystem/teacher/upldAsn/" + str(asn.id) + "/")
    return HttpResponseRedirect("/EducationalSystem/teacher/Asn/" + str(asn_id) + "/")

def exportAssignment(request, asn_id):
    Team_asns = Team_Assignment.objects.filter(asn_id__id=asn_id)

    Teams = []
    for team_asn in Team_asns:
        row = []
        row.append(str(team_asn.team_id.id))
        row.append(team_asn.team_id.name)
        if team_asn.submit_times == 0:
            row.append('未提交')
            row.append('0')
        else:
            row.append('已提交')
            row.append(str(team_asn.mark))
        Teams.append(row)

    xlsx = writeAssignment(Teams, asn_id)
    baseDir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(baseDir, xlsx)

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(xlsx)
    content = open(filepath, 'rb').read()
    response.write(content)

    return response

def exportAllAssignment(request, course_id):
    Teams = Team.objects.filter(course_id__id=course_id)
    cou = Course.objects.get(id=course_id)
    form = []
    for team in Teams:
        team_id = team.id
        team_name = team.name
        TAs = Team_Assignment.objects.filter(team_id__id=team_id).order_by('asn_id__id')
        rows = []
        rows.append([str(team_id), team_name, '', ''])
        rows.append(['作业ID', '作业名称', '作业提交情况', '作业分数'])
        for ta in TAs:
            row = []
            row.append(str(ta.asn_id.id))
            row.append(ta.asn_id.name)
            if ta.submit_times == 0:
                row.append('未提交')
                row.append(0)
            else:
                row.append('已提交')
                row.append(ta.mark)
            rows.append(row)
        form.append(rows)

    xlsx = writeAllAssignment(form, course_id)
    baseDir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(baseDir, xlsx)

    # def file_iterator(file_name, chunk_size=262144):
    #     f = open(file_name, "rb")
    #     while True:
    #         c = f.read(chunk_size)
    #         if c:
    #             yield c
    #         else:
    #             break
    #     f.close()
    #
    # response = HttpResponse(file_iterator(xlsx))
    # response['Content-Type'] = 'application/vnd.ms-excel'
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(xlsx)


    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(xlsx)
    content = open(filepath, 'rb').read()
    response.write(content)

    return response


def exportTeams(request, course_id):
    Teams = Team.objects.filter(course_id__id=course_id, status=2)
    form = []
    for team in Teams:
        STs = Student_Team.objects.filter(team_id__id=team.id)
        rows = []
        for st in STs:
            student = Student.objects.get(id=st.student_id.id)
            row = []
            row.append(str(team.id))
            row.append(team.name)
            row.append(str(student.id))
            row.append(student.name)
            if (student.id==team.manager_id.id):
                row.append('组长')
            else:
                row.append('组员')
            rows.append(row)
        form.append(rows)

    xlsx = writeTeam(form, course_id)
    print(xlsx)

    baseDir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(baseDir, xlsx)

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(xlsx)
    content = open(filepath, 'rb').read()
    response.write(content)

    return response

def exportGrade(request, course_id):
    asn_list = Assignment.objects.filter(course_id__id=course_id)
    TA_list = Team_Assignment.objects.filter(asn_id__id__in=asn_list)
    SGs = Student_Grade.objects.filter(team_asn_id__id__in=TA_list).order_by('student_id__id')

    num = len(SGs)
    num_list = [0]
    for i in range(num-1):
        if SGs[i].student_id__id!=SGs[i+1].student_id__id:
            num_list.append(i+1)

    form = []
    for i in range(len(num_list)-1):
        stu_id = SGs[num_list[i]].student_id__id
        stu_name = Student.objects.get(id=stu_id).name
        grade = 0
        for sg in SGs[num_list[i]:num_list[i+1]]:
            grade = grade + sg.weight
        form.append([stu_id, stu_name, grade])

    xlsx = writeGrade(form, course_id)
    print(xlsx)

    baseDir = os.path.dirname(os.path.abspath(__name__))
    filepath = os.path.join(baseDir, xlsx)

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(xlsx)
    content = open(filepath, 'rb').read()
    response.write(content)

    return response

def downloadOwnHw(request, path):
    everypath = path.split('/')
    filename = everypath[-1]
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    content = open(path, 'rb').read()
    response.write(content)
    return response
