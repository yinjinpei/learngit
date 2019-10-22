from django.db import models

# Create your models here.

class BookInfo(models.Model):
    '''
    图书表结构设计：
        表名：BookInfo
        图书名称：btitle
        图书发布时间：bpub_date
    '''
    btitle=models.CharField(max_length=20)
    bpub_date=models.DateTimeField()

class HeroInfo(models.Model):
    '''
    英雄表结构设计：
        表名：HeroInfo
        英雄姓名：hname
        英雄性别：hgender
        英雄简介：hcontent
        所属图书：hbook
    '''
    hname=models.CharField(max_length=10)
    hgender=models.BooleanField()
    hcontent=models.CharField(max_length=1000)
    hbook=models.ForeignKey(BookInfo,on_delete=models.CASCADE,)

