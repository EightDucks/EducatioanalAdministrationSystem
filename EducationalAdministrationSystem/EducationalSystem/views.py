# coding=utf-8
from django.shortcuts import render

from .models import *



from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.db import connection
from django.shortcuts import render_to_response
from django.shortcuts import render


from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import messages



#主页
def index(request):
	return render_to_response('index.html')

#
def jiaowu_addcourse(request):
	return render_to_response('jiaowu_addcourse.html')

def jiaowu_addsemester(request):
    return render_to_response('jiaowu_addsemester.html')

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
			if tea:
				print('successT')
				return HttpResponseRedirect("/EducationalSystem")
			return HttpResponseRedirect("/EducationalSystem/")
			# if tea:
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		elif userKind == 's':
			stu = Student.objects.filter(number = userName, password = userPassword)
			if stu:
				print('successS')
				return HttpResponseRedirect("/EducationalSystem/")
			return HttpResponseRedirect("/EducationalSystem/")
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		elif userKind == "e":
			ea = EduAdmin.objects.get(number = userName, password = userPassword)
			if ea:
				print('successE')
				request.session["id"] = ea.id
				request.session["type"] = "e"
				return HttpResponseRedirect("/EducationalSystem/jiaowu/")
			return HttpResponseRedirect("/EducationalSystem/")
			# if ea:
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		else:
			return HttpResponseRedirect("/EducationalSystem/")
	else:
		return HttpResponseRedirect("/EducationalSystem/")

# 展示所有课程：教务 单独页面
def displayCourseForEA(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type'] == 'e':
		ea_id = request.session['id']
		ea = EduAdmin.objects.get(id=ea_id)
		terms = Term.objects.order_by("-id")
		thisTerm = terms[0].id
		cou = Course.objects.filter(term_id__id = thisTerm)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
		elif len(cou) < 6:
			cou1 = cou[0:4]
			cou2 = cou[3:len(cou)]
		else:
			cou1 = cou[0:4]
			cou2 = cou[3:7]
		return render(request, "jiaowu.html", {'ea':ea, 'terms':terms, 'cou1':cou1, 'cou2':cou2})
	else:
		return HttpResponseRedirect("/EducationalSystem/")

#展示个人信息
def displayUserInfo(request):
	if 'id' in request.GET and request.GET['id']:
		if 'kind' in request.GET and request.GET['kind']:
			user_id = request.GET['id']
			userKind = request.GET['kind']

			if userKind == 's':
				stu = Student.objects.get(id = user_id)
			elif userKind == 't':
				tea = Teacher.objects.get(id = user_id)
			elif userKind == 'e':
				ea = EduAdmin.objects.get(id = user_id)

#保存学期信息
def saveTermInfo(request):
	if 'name' in request.GET and 'start' in request.GET \
		and 'end' in request.GET and 'week' in request.GET \
		and request.GET['name'] and request.GET['start'] \
		and request.GET['end'] and request.GET['week']:

		name = request.GET['name']
		start = request.GET['start']
		end = request.GET['end']
		week = request.GET['week']

		term_tmp = Term(name=name, start=start, end=end, week=week)
		term_tmp.save()

#关闭学期
def closeTerm(request):
	if 'id' in request.GET and request.GET['id']:
		name = request.GET['id']
		term = Term.objects.get(id = id)
		term.is_over = True
		term.save()

#添加课程
def addCourse(request):
	if 'name' in request.GET and 'credit' in request.GET \
		and 'time' in request.GET and 'location' in request.GET \
		and 'team_uplimit' in request.GET and 'team_downlimit' in request.GET \
		and 'term_id' in request and request.GET['name'] \
		and request.GET['credit'] and request.GET['time'] \
		and request.GET['location'] and request.GET['team_uplimit'] \
		and request.GET['team_downlimit'] and request.GET['term_id']:

		name = request.GET['name']
		credit = request.GET['credit']
		time = request.GET['time']
		location = request.GET['location']
		team_uplimit = request.GET['team_uplimit']
		team_downlimit = request.GET['team_downlimit']
		term_id = request.GET['term_id']

		Course_tmp = Course(name=name, credit=credit, time=time, location=location, team_uplimit=team_uplimit, team_downlimit=team_downlimit, term_id=term_id)
		Course_tmp.save()

# def setTeacher(request):

#czy
#展示课程：学生
def displayCourseForStudent(request):
	if 'id' in request.GET and request.GET['id']:
		if 'term_id' in request.GET and request.GET['term_id']:
			stu_id = request.GET['id']
			term_id = request.GET['term_id']
			student_course = Course_Student.objects.filter(student_id__id=id)
			course_id = student_course.course_id__id
			ret_course = Course(term_id__id=term_id, id__in=course_id)

#展示所有资源：教师/学生
def displayAllResource(request):
	if 'course_id' in request.GET and request.GET['course_id'] and \
		'virtual_path' in request.GET and request.GET['virtual_path']:
		course_id = request.GET['course_id']
		virtual_path = request.GET['virtual_path']
		res = Resource.objects.filter(course_id__id=course_id, virtual_path=virtual_path)

#上传资源：教师
def addResource(request):
	if 'name' in request.GET and request.GET['name'] and \
		'path' in request.GET and request.GET['path'] and \
		'virtual_path' in request.GET and request.GET['virtual_path'] and \
		'course_id' in request.GET and request.GET['course_id']:

		course_id = request.GET['course_id']
		name = request.GET['name']
		path = request.GET['path']
		virtual_path = request.GET['virtual_path']

		Resource_tmp = Resource(name=name, path=path, virtual_path=virtual_path, course_id=course_id)
		Resource_tmp.save()

#mine
#展示学期信息
def displayTermInfo(request):
	if 'term_id' in request.GET and request.GET['term_id']:
		term_id = request.GET['term_id']
		term = Term.objects.GET(id=term_id)

#展示课程：学生
def displayCourseForTeacher(request):
	if 'id' in request.session and request.session['id']:
		tea_id = request.session['id']
		tea_course = Course_Teacher.objects.filter(teacher_id = tea_id, course_id__term_id__is_over = False)
		course = Course.objects.filter(id__in = tea_course.course_id)

#展示课程信息
def displayCourseInfo(request):
	if 'id' in request.GET and request.GET['id']:
		cou_id = request.GET['id']
		course = Course.objects.get(id=cou_id)

#展示所有作业
def displayCourseAssignments(request):
	if 'id' in request.GET and request.GET['id']:
		cur_id = request.GET['id']
		cur_ass = Assignment.objects.GET(course_id=cur_id)

#展示作业信息：教师
def displayAssignmentsForTeacher(request):
	if 'id' in request.GET and request.GET['id']:
		ass_id = request.GET['id']
		stu_ass = Assignment_Resource.objects.filter(team_asn_id__asn_id__id=ass_id)
		ass_info = Assignment.objects.GET(id = ass_id)

#展示作业信息：学生
def displayAssignmentsForStudents(request):
	if 'id' in request.GET and request.GET['id']\
		and 'id' in request.session and request.session['id']:
		ass_id = request.GET['id']
		stu_id = request.session['id']
		ass_info = Assignment.objects.GET(id = ass_id)
		stu_team = Student_Team.objects.GET(student_id=stu_id, is_approved = True, team_id__course_id=ass_info.course_id)
		ass_res = Assignment_Resource.objects.filter(team_asn_id__team_id = stu_team.id)

#评论学生作业：教师
def setTeamAssignmentComment(request):
	if 'TA_id' in request.GET and request.GET['TA_id'] and \
		'comment' in request.GET and request.GET['comment']:
		TA_id = request.GET['TA_id']
		comment = request.GET['comment']

		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.comment = comment
		TA_tmp.save()

#给作业成绩：教师
def setTeamAssignmentMark(request):
	if 'TA_id' in request.GET and request.GET['TA_id'] and \
		'mark' in request.GET and request.GET['mark']:
		TA_id = request.GET['TA_id']
		mark = request.GET['mark']

		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.mark = mark
		TA_tmp.save()

#给评价与成绩：教师
def setTeamAssignmentCommentMark(request):
	if 'TA_id' in request.GET and request.GET['TA_id'] and \
		'comment' in request.GET and request.GET['comment'] and \
		'mark' in request.GET and request.GET['mark']:
		TA_id = request.GET['TA_id']
		comment = request.GET['comment']
		mark = request.GET['mark']

		TA_tmp = Team_Assignment(id=TA_id)
		TA_tmp.comment = comment
		TA_tmp.mark = mark
		TA_tmp.save()

#修改作业
def modifyAssignment(request):
	if 'asn_id' in request.GET and request.GET['asn_id'] and \
		'name' in request.GET and request.GET['name'] and \
		'requirement' in request.GET and \
		'starttime' in request.GET and request.GET['starttime'] and \
		'duetime' in request.GET and request.GET['duetime'] and \
		'submit_limits' in request.GET and request.GET['submit_limits'] and \
		'weight' in request.GET and request.GET['weight']:

		asn_id = request.GET['asn_id']
		name = request.GET['name']
		requirement = request.GET['requirement']
		starttime = request.GET['starttime']
		duetime = request.GET['duetime']
		submit_limits = request.GET['submit_limits']
		weight = request.GET['weight']

		asn = Assignment.objects.GET(id=asn_id)
		asn.name = name
		asn.requirement = requirement
		asn.starttime = starttime
		asn.duetime = duetime
		asn.submit_limits = submit_limits
		asn.weight = weight
		asn.save()

#删除作业
def deleteAssignment(request):
	if 'asn_id' in request.GET and request.GET['asn_id']:
		asn_id = request.GET['asn_id']

		TA = Team_Assignment.objects.filter(asn_id__id=asn_id)

		Assignment_Resource.objects.filter(team_asn_id__in=TA.id).delete()
		Student_Grade.objects.filter(team_asn_id__in=TA.id).delete()

		TA.delete()

		Assignment.objects.get(id=asn_id).delete()

