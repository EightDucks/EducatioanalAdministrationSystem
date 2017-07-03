# coding=utf-8

# new view
# 教师团队列表页面，单独页面
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
            ts_have_team = Student_Team.objects.filter(course_id=cou_id)
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
            ts_member=Student_Team.objects.filter(course_id=cou_id, team_id=team_id)
            student_teammember = []
            for st in ts_member:
                student_teammember.append(st.student_id)
            return render(request, "teacher_course_team_teaminfo.html", {'cou':team.course_id, 'team':team, 'student_have_no_team':student_have_no_team, 'teammember': student_teammember})
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
		team.save()
    	team.reason = request.GET['refuse_reason']
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
		team_members = Student_Team.objects.fliter(team_id=team_id)
		team = Team.objects.get(id=team_id)
		if (len(team_members) >= team.course_id.team_uplimit):
			# 团队成员人数大于等于上限
            msg="操作失败：该团队成员已达到设定上限"
            messages.error(request,msg)
			direct="/EducationalSystem/teacher/teamDt/"+team_id
        	return HttpResponseRedirect(direct)
		else:
			new_team_member = Student_Team(team_id=team_id, student_id=student_id, is_approved=True)
			new_team_member.save()
            msg="学生 "+student_id.name+" 已成功加入该团队"
            messages.success(request, msg)
			direct="/EducationalSystem/teacher/teamDt/"+team_id
        	return HttpResponseRedirect(direct)

# new url
    url(r'teacher/courseTeam/(\d+)/$', views.displayTeamListForTeacher, name='displayTeamListForTeacher'),
    url(r'teacher/teamDt/(\d+)/$', views.disPlayTeamInfoForTeacher, name='disPlayTeamInfoForTeacher'),
    url(r'teacher/teamDt/(\d+)/approve/$', views.approveTeam, name='approveTeam'),
    url(r'teacher/teamDt/(\d+)/reject/$', views.disapproveTeam, name='disapproveTeam'),
    url(r'teacher/teamDt/(\d+)/addStu/(\d+)$', views.add_team_member, name='add_team_member'),
