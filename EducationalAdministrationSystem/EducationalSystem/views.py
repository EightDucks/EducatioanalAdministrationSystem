# coding=utf-8
import os

import xlrd		#pip3 install xlrd
import xlwt		#pip3 install xlwt
import random

import  tempfile, zipfile, zipstream

import time

from django.shortcuts import render
from wsgiref.util import FileWrapper

from datetime import date, datetime

from .models import *

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
	return render_to_response('index.html')


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


# 添加学期，单独页面
def jiaowu_addsemester(request):
	return render_to_response('jiaowu_addsemester.html')

# 课程信息：教务，单独页面
def jiaowu_courseinfo(request, cou_id):
	course = Course.objects.get(id=cou_id)
	tid = course.term_id
	cou_stu = Course_Student.objects.filter(course_id=course).values("student_id")
	stu = Student.objects.filter(id__in=cou_stu).order_by("number")
	#stu_id = cou_stu.student_id
	#term = Term.objects.get(id=tid)
	return render(request, "jiaowu_courseinfo.html", {'course':course, 'term':tid, 'stu':stu})

# 学生课程，单独页面
def displayCourseForStudent(request):
	if 'id' in request.session and request.session['id'] \
			and 'type' in request.session and request.session['type'] == 's':
		thisTerm = Term.objects.all()
		sid = request.session['id']
		student_course = Course_Student.objects.filter(student_id__id=sid)
		cou_id = student_course.values("course_id")
		cou = Course.objects.filter(term_id__id__in=thisTerm, id__in=cou_id)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
		elif len(cou) < 6:
			cou1 = cou[0:3]
			cou2 = cou[3:len(cou)]
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
		else:
			cou1 = cou[0:3]
			cou2 = cou[3:6]
			return render(request, "student.html", {'cou1': cou1, 'cou2': cou2})
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
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
		elif len(cou) < 6:
			cou1 = cou[0:3]
			cou2 = cou[3:len(cou)]
		else:
			cou1 = cou[0:3]
			cou2 = cou[3:6]
		return render(request, "teacher.html", {'cou1': cou1, 'cou2': cou2})
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
			tea = Teacher.objects.get(number = userName, password = userPassword)
			if tea:
				print('successT')
				request.session["id"] = tea.id
				request.session["type"] = "t"
				return HttpResponseRedirect("/EducationalSystem/teacher/")
			return HttpResponseRedirect("/EducationalSystem/")
			# if tea:
			# 	return render_to_response('index.html')
			# else:
			# 	return render_to_response('index.html')
		elif userKind == 's':
			stu = Student.objects.get(number = userName, password = userPassword)
			if stu:
				print('successS')
				request.session["id"] = stu.id
				request.session["type"] = "s"
				return HttpResponseRedirect("/EducationalSystem/student/")
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
			thisTerm = terms[0].id
		else:
			t = Term.objects.get(id=t_id)
			thisTerm = t.id
		cou = Course.objects.filter(term_id__id=thisTerm)
		if len(cou) < 3:
			cou1 = cou[0:len(cou)]
			cou2 = None
		elif len(cou) < 6:
			cou1 = cou[0:3]
			cou2 = cou[3:len(cou)]
		else:
			cou1 = cou[0:3]
			cou2 = cou[3:6]
		return render(request, "jiaowu.html", {'terms': terms, 'cou1': cou1, 'cou2': cou2, 't_id': t_id})
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
def closeTerm(request):
	if 'id' in request.GET and request.GET['id']:
		name = request.GET['id']
		term = Term.objects.get(id=id)
		term.is_over = True
		term.save()


# 添加课程，处理函数
def addCourse(request):
	if 'course_name' in request.GET and 'course_point' in request.GET \
			and 'course_time' in request.GET and 'course_location' in request.GET \
			and 'selectterm' in request.GET and 'course_timelength' in request.GET \
			and request.GET['course_point'] and request.GET['course_time'] \
			and request.GET['course_name'] and request.GET['course_timelength'] \
			and request.GET['course_location'] and request.GET['selectterm'] \
			and 'course_teacherid' in request.GET and request.GET['course_teacherid']:

		name = request.GET['course_name']
		credit = request.GET['course_point']
		time = request.GET['course_time']
		hour = request.GET['course_timelength']
		location = request.GET['course_location']
		term_id = request.GET['selectterm']
		tea_num = request.GET['course_teacherid']
		Tea = Teacher.objects.get(number=tea_num)
		if not Tea:
			return HttpResponseRedirect("/EducationalSystem/jiaowu/")
		term = Term.objects.get(id=term_id)
		Course_tmp = Course(name=name, credit=credit, time=time, location=location, term_id=term, hour=hour)
		Course_tmp.save()
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")
	else:
		return HttpResponseRedirect("/EducationalSystem/jiaowu/")

#def setTeacher(request):
#czy
#展示所有资源：教师/学生
def displayAllResource(request, course_id):
	Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True, virtual_path='/')
	Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False, virtual_path='/')
	print('display resource')
	print([res.id for res in Resources], [f.id for f in Folders], course_id, '/')
	return render(request, 'resources.html',
				  {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': '/'})


# 上传资源：教师
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

def downloadResource(request):
	if 'fid' in request.GET and request.GET['fid']:
		fid = request.GET['fid']
		myFile = Resource.objects.GET(id = fid)
		fname = myFile.name
		fpath = myFile.path
		def fileIterator(fname, chunk_size = 512):
			with open(fname) as f:
				while(True):
					c = f.read(chunk_size)
					if c:
						yield c
					else:
						break
		response = StreamingHttpResponse(fileIterator(fname))
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename = "{0}"'.format(fname)
		return response



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
		TA_tmp.save()
		return HttpResponseRedirect("/EducationalSystem/teacher/Asn/" + str(TA_tmp.asn_id.id) + "/")

#展示添加作业页面，单独页面
def displayAddAsn(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	return render(request, "teacher_course_homework_add.html", {'cou':cou})

#添加作业，处理函数
def addAssignment(request, cou_id):

	if 	'assignment_name' in request.GET and request.GET['assignment_name'] and \
		'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
		'assignment_starttime' in request.GET and request.GET['assignment_starttime'] and \
		'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
		'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
		'grade_ratio' in request.GET and request.GET['grade_ratio']:

		name = request.GET['assignment_name']
		requirement = request.GET['assignment_requirement']
		starttime = request.GET['assignment_starttime']
		duetime = request.GET['assignment_duetime']
		submit_limits = request.GET['maximum_submit']
		weight = request.GET['grade_ratio']
		cou = Course.objects.get(id=cou_id)
		asn = Assignment(name=name, requirement=requirement, starttime=starttime, duetime=duetime, submit_limits =submit_limits, weight=weight, course_id=cou )
		asn.save()

	return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示修改作业页面，单独页面
def displayModAsn(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	cou = asn.course_id
	return render(request, "teacher_course_homework_modify.html", {'asn':asn, 'cou':cou})

#修改作业，处理函数
def modifyAssignment(request, asn_id):

	if 'assignment_name' in request.GET and request.GET['assignment_name'] and \
		'assignment_requirement' in request.GET and request.GET['assignment_requirement'] and \
		'assignment_starttime' in request.GET and request.GET['assignment_starttime'] and \
		'assignment_duetime' in request.GET and request.GET['assignment_duetime'] and \
		'maximum_submit' in request.GET and request.GET['maximum_submit'] and \
		'grade_ratio' in request.GET and request.GET['grade_ratio']:

		name = request.GET['assignment_name']
		requirement = request.GET['assignment_requirement']
		starttime = request.GET['assignment_starttime']
		duetime = request.GET['assignment_duetime']
		submit_limits = request.GET['maximum_submit']
		weight = request.GET['grade_ratio']

		asn = Assignment.objects.get(id=asn_id)
		asn.name = name
		asn.requirement = requirement
		asn.starttime = starttime
		asn.duetime = duetime
		asn.submit_limits = submit_limits
		asn.weight = weight
		asn.save()
		return_url="/EducationalSystem/teacher/CouAsn/"+str(asn.course_id.id)
		return HttpResponseRedirect(return_url)
	else:
		return HttpResponseRedirect("/EducationalSystem/teacher/")


#展示所有作业，单独页面
def displayHwForTea(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	asn = Assignment.objects.filter(course_id=cou)
	return render(request, "teacher_course_homework.html", {'asn': asn, 'cou':cou})

def displayCourseInfo(request, course_id):
	course = Course.objects.get(id=course_id)
	term = course.term_id
	return render(request, 'teacher_set_course_basicinfo.html',
				  {'course_id':course.id, 'term_name':term.name,
				   'course_name':course.name, 'time':course.time,
				   'location':course.location, 'credit':course.credit,
				   'hour':course.hour, "cou":course})

#展示单个作业，单独页面
def displayHw(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	cou = asn.course_id
	tem = Team.objects.filter(course_id=cou)
	tas = Team_Assignment.objects.filter(team_id__in = tem, asn_id = asn)
	return render(request, "teacher_course_homework_watchdetails.html", {'asn':asn, 'tem':tas, 'cou':cou, })

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
		print('cnm')
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
			return

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
		return HttpResponseRedirect("/EductionalSystem/jiaowu_course/" + str(cid) +"/")
	else:
		print("hhh")
		return HttpResponseRedirect("/EductionalSystem/jiaowu_course/" + str(cid) +"/")

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

def uploadResource(request, cou_id):
	if request.method == 'POST' :
		myFiles = request.FILES.getlist("fileupload", None)
		cou = Course.objects.get(id=cou_id)
		if not myFiles:
			dstatus = ("No file to upload")
		for f in myFiles:
			baseDir = os.path.dirname(os.path.abspath(__name__))
			filepath = os.path.join(baseDir, 'static', 'files', f.name)
			destination = open(filepath, 'wb+')
			res = Resource(name=f.name, path=filepath, course_id=cou, virtual_path="")
			res.save()
			for chunk in f.chunks():
				destination.write(chunk)
			destination.close()
		return HttpResponse("/EducationalSystem/resource/" + str(cou_id))

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
			Resource.objects.get(id=int(splitted[i])).delete()

		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True)
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False)

		return render(request, 'resources.html',
					  {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': virpath})
	else:
		course_id = 0
		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True)
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False)
		virpath = '/'
		return render(request, 'resources.html',
					  {'resources': Resources, 'folders': Folders, 'course_id': course_id, 'virpath': virpath})


def uploadHomework(request,asn_id):
	if request.method == 'POST' and 'id' in request.session and request.session['id']:

		sid = request.session['id']

		# teamAsn = Team_Assignment.objects.get(team_id = stu_team.id, asn_id = asn_id)
		# if not teamAsn:
		# 	teamAsn.submit_times = 1
		# 	teamAsn.save()
		# else:
		# 	teamAsn.submit_times = teamAsn.submit_times + 1
		# 	teamAsn.save()


		strA = "assignment_attachment_"
		i = 0

		while True:
			newStr = strA + str(i)
			if newStr in request.FILES:
				file_obj = request.FILES[newStr]

				baseDir = os.path.dirname(os.path.abspath(__name__))
				filepath = os.path.join(baseDir, 'static', 'files', file_obj.name)

				destination = open(filepath, 'wb+')
				# asn_res = Assignment_Resource(team_asn_id = teamAsn.id, path = destination, is_corrected = False)
				# asn_res.save()
				t_a = Team_Assignment.objects.get(id=1)
				asn_res = Assignment_Resource(team_asn_id=t_a, path=filepath)
				asn_res.save()
				for chunk in file_obj.chunks():
					destination.write(chunk)

				destination.close()
				i = i + 1
			else:
				break

		return HttpResponseRedirect("/EducationalSystem/student/")
	return HttpResponseRedirect("/EducationalSystem/student/")

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
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")#需要更改文件名
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
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")  # 需要更改文件名
	return response

def downloadHomework(request, asn_id, tid):
	team_asn = Team_Assignment.objects.get(team_id=tid, asn_id=asn_id)
	asn_res = Assignment_Resource.objects.filter(team_asn_id=team_asn)
	utilities = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
	for a_r in asn_res:
		tmp_dl_path = a_r.path
		utilities.write(tmp_dl_path, arcname=os.path.basename(tmp_dl_path))
	# utilities.close()
	response = StreamingHttpResponse(utilities, content_type='application/zip')
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format("下载.zip")#需要更改文件名
	return response

#展示学生课程信息页面，单独页面
def displayCouForStu(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	term = cou.term_id
	return render(request, "student_course_basicinfo.html", {'cou':cou, 'term':term})

#展示学生所有作业页面，单独页面
def displayHwForStu(request, cou_id):
	cou = Course.objects.get(id=cou_id)
	asn = Assignment.objects.filter(course_id=cou)
	return render(request, "student_course_homework.html", {'cou':cou, 'asn':asn})

#展示学生某一作业，单独页面
def displayStuHw(request, asn_id):
	asn = Assignment.objects.get(id=asn_id)
	cou = asn.course_id
	return render(request, "student_course_homework_watchdetails.html", {'cou':cou, 'asn':asn})

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
		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True, virtual_path=virpath)
		print('Folder done.')
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False, virtual_path=virpath)

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
		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True)
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False)
		virpath = '/'
		ret_str = fileSystemResponse(Resources, Folders)
		return HttpResponse(ret_str)
		#return render(request, 'resources.html',
		#			  {'resources': Resources, 'folders':Folders, 'course_id': course_id, 'virpath': virpath})

def returnSuperiorMenu(request):
	if 'courseid' in request.GET and request.GET['courseid'] and \
		'path' in request.GET and request.GET['path']:

		course_id = request.GET['courseid']
		virpath = request.GET['path']

		splitted = virpath.split('/')
		num = len(splitted)

		new_virpath = ''

		for i in range(num-2):
			new_virpath = new_virpath + splitted[i] + '/'

		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True, virtual_path=new_virpath)
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False, virtual_path=new_virpath)

		ret_str = fileSystemResponse(Folders, Resources)

		return HttpResponse(ret_str)

	else:
		course_id = 0
		Folders = Resource.objects.filter(course_id__id=course_id, path__isnull=True)
		Resources = Resource.objects.filter(course_id__id=course_id, path__isnull=False)
		virpath = '/'

		ret_str = fileSystemResponse(Resources, Folders)
		return HttpResponse(ret_str)

def returnVirpath(request):
	if 'id' in request.GET and request.GET['id'] and \
		'name' in request.GET and request.GET['name'] and \
		'path' in request.GET and request.GET['path'] and \
		'flag' in request.GET and request.GET['flag']:

		if request.GET['flag']=='1':
			folder_name = request.GET['name']
			virpath = request.GET['path']
			virpath = virpath + folder_name + '/'

			return HttpResponse(virpath)

		elif request.GET['flag']=='2':
			virpath = request.GET['path']
			splitted = virpath.split('/')
			num = len(splitted)
			new_virpath = ''
			for i in range(num - 2):
				new_virpath = new_virpath + splitted[i] + '/'
			return HttpResponse(new_virpath)

def createFolder(request):
	if __name__ == '__main__':
		if 'course_id' in request.GET and request.GET['course_id'] and \
			'path' in request.GET and request.GET['path'] and \
			'folder_name' in request.GET and request.GET['folder_name']:

			course_id = request.GET['course_id']
			folder_name = request.GET['folder_name']
			virpath = request.GET['path']

			res = Resource(name=folder_name, path='new', virtual_path=virpath+folder_name+'/', course_id__id=course_id)
			res.save()
			return HttpResponse(str(res.id))
