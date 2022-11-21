from django.db import models

class Course(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=32)
    class_max_capacity = models.IntegerField()
    class_introduction = models.CharField(max_length=200)
    class_hour = models.IntegerField()
    class_type = models.CharField(max_length=100)
    class_score = models.FloatField()

class Time(models.Model):
    nid = models.AutoField(primary_key=True)
    semester = models.CharField(max_length=100)
    week = models.IntegerField()
    day = models.IntegerField()
    class_num = models.IntegerField()



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
