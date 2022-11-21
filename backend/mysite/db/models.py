from django.db import models

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=32)
    course_max_capacity = models.IntegerField()
    course_introduction = models.CharField(max_length=200)
    course_hour = models.IntegerField()
    course_type = models.CharField(max_length=100)
    course_score = models.FloatField()

class Time(models.Model):
    semester = models.CharField(max_length=100)
    week = models.IntegerField()
    day = models.IntegerField()
    class_num = models.IntegerField()

class Course_constraint(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_continue = models.BooleanField()
    class_is_odd_week = models.BooleanField()
    class_smallest_day_number = models.IntegerField()
    class_biggest_day_number = models.IntegerField()

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=100)
    classroom_capacity = models.IntegerField()
    classroom_place = models.CharField(max_length=200)

class Course_table(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_table_name = models.CharField(max_length=200)

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_type = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    student_sex = models.CharField(max_length=100)
    student_major = models.CharField(max_length=100)
    student_class = models.CharField(max_length=200)

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=100)
    teacher_sex = models.CharField(max_length=100)
    teacher_profession_title = models.CharField(max_length=200)

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)

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
