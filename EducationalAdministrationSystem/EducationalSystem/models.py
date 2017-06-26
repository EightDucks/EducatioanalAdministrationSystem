from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    dept = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, null=True)

class EduAdmin(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, null=True)

class Term(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    week = models.IntegerField()
    is_over = models.BooleanField(default=False)

class Course(models.Model):
    name = models.CharField(max_length=50)
    credit = models.IntegerField()
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    team_uplimit = models.IntegerField()
    team_downlimit = models.IntegerField()
    term_id = models.ForeignKey(Term)

class Course_Teacher(models.Model):
    course_id = models.ForeignKey(Course)
    teacher_id = models.ForeignKey(Teacher)

class Course_Student(models.Model):
    course_id = models.ForeignKey(Course)
    student_id = models.ForeignKey(Student)
    grade = models.IntegerField(null=True)

class Resource(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course)
    virtual_path = models.CharField(max_length=100)

class Assignment(models.Model):
    name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course)
    requirement = models.TextField(null=True)
    starttime = models.DateTimeField()
    duetime = models.DateTimeField()
    submit_limits = models.IntegerField(null=True)
    weight = models.FloatField()

class Team(models.Model):
    name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course)
    is_approved = models.BooleanField(default=False)
    reason = models.TextField(null=True)
    manager_id = models.ForeignKey(Student)

class Team_Assignment(models.Model):
    team_id = models.ForeignKey(Team)
    asn_id = models.ForeignKey(Assignment)
    mark = models.FloatField(null=True)
    comment = models.TextField(null=True)
    submit_times = models.IntegerField(default=0)

class Assignment_Resource(models.Model):
    team_asn_id = models.ForeignKey(Team_Assignment)
    path = models.CharField(max_length=100)
    is_corrected = models.BooleanField(default=False)

class Student_Team(models.Model):
    team_id = models.ForeignKey(Team)
    student_id = models.ForeignKey(Student)
    is_approved = models.BooleanField(default=False)

class Student_Grade(models.Model):
    student_id = models.ForeignKey(Student)
    team_asn_id = models.ForeignKey(Team_Assignment)
    weight = models.FloatField(null=True)