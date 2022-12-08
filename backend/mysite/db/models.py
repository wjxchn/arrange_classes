from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_type = models.IntegerField()
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    student_name = models.CharField(max_length=100)
    student_sex = models.CharField(max_length=100)
    student_major = models.CharField(max_length=100)
    student_class = models.CharField(max_length=200)

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    teacher_name = models.CharField(max_length=100)
    teacher_sex = models.CharField(max_length=100)
    teacher_profession_title = models.CharField(max_length=200)

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()

class Time(models.Model):
    semester = models.CharField(max_length=100)
    week = models.IntegerField()
    day = models.IntegerField()
    class_num = models.IntegerField()

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=100)
    classroom_capacity = models.IntegerField()
    classroom_place = models.CharField(max_length=200)

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=32)
    course_max_capacity = models.IntegerField()
    course_introduction = models.CharField(max_length=200)
    course_hour = models.IntegerField()
    course_type = models.CharField(max_length=100)
    course_score = models.FloatField()
    course_teacher = models.ManyToManyField(Teacher)
    course_time = models.ManyToManyField(Time)
    course_classroom = models.ManyToManyField(Classroom)
    course_student = models.ManyToManyField(Student)

class Course_constraint(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_continue = models.BooleanField()
    course_is_odd_week = models.BooleanField()
    course_smallest_day_number = models.IntegerField()
    course_biggest_day_number = models.IntegerField()
    max_course_room_ratio = models.FloatField()
    illegal_course_before = models.ManyToManyField(Course)

class Course_table(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_table_name = models.CharField(max_length=200)
    course_list = models.ManyToManyField(Course)


# 以下三个表在数据库中作测试用
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    age=models.IntegerField()

class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)
    email=models.EmailField()

class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    publish = models.ForeignKey(to = 'Publish',to_field= 'nid',on_delete=models.CASCADE)
    author = models.ManyToManyField(to='Author',)
