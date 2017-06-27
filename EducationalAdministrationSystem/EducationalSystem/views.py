from django.shortcuts import render

from .models import *

def index(request):
	if 'name' in request.GET and request.GET['name']:
		if 'password' in request.GET and request.GET['password']:
			if 'kind' in request.GET and request.GET['kind']:
                userName = request.GET['name']
                userPassword = request.GET['password']
                userKind = request.GET['kind']

                if userKind == 't':
                    tea = Teacher.objects.filter(number = userName, password = userPassword)
                    if not tea:
                        return
                elif userKind == 's':
                    stu = Student.objects.filter(number = userName, password = userPassword)
                    if not stu:
                        return
                elif userKind == "e":
                    ea = EduAdmin.objects.filter(number = userName, password = userPassword)
                    if not ea:
                        return

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

def closeTerm(request):
    if 'id' in request.GET and request.GET['id']:
        name = request.GET['id']
        term = Term.objects.get(id = id)
        term.is_over = True
        term.save()

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

def displayCourseForEA(request):
    if 'id' in request.GET and request.GET['id']:
        course = Course.objects.get(id=id)

def setTeacher(request):