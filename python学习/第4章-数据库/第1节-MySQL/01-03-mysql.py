#-*- coding:utf-8 -*-
#author:YJ沛


'''
  1，E-R关系模型
2，关系包括：一对一，一对多，多对多
3，三范式：
1NF：列不可拆分
2NF：唯一标识
3NF：引用主键
4，字段类型，主要几种：
数字：int, decimal
字符串：char, varchar, text
日期：datetime
布尔：bit
5，约束：
主键：primary key
非空：not null
唯一：unique
默认：default
外键：foreign key
6，重要数据做 逻辑删除

创建数据库：
crate database python3 charset=utf8;
use python3	使用python3数据库
创建表：
mysql> create table if not exists students(
    -> id int auto_increment primary key not null,
    -> name varchar(10) not null，
    -> gender bit default 1,
    -> birthday datetime);

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8

插入数据：
全列插入：insert into 表名 values(...)
缺省插入：insert into 表名（列1,...） values(值1,...)
同时插入多条数据：insert into 表名 values(...),（...）,...
全列插入：insert into 表名（列1,...） values(值1,...),(值1,...),...
更新表数据:
update 表名 set 字段=新值,… where 条件;
备份数据库：
mysqldump -uroot -p 数据库名 > ~/bak_20190811.sql
例：mysqldump -uroot -p python3 > ~/bak_20190811.sql
恢复数据库：
mysql -uroot -p 数据库名 < ~/bak_20190811.sql
例：mysql -uroot -p python3 < ~/bak_20190811.sql
查询：
查看当前使用的数据库名：select database();
查询表所有数据：select * from 表名;
去重查询：select distinct name from 表名;

条件查询：
select * from 表名 where 条件;

比较运算符：
等于：=
大于：>
大于等于：>=
小于：<
小于等于：<=
不等于：!=  、<>
例：select * from students where id>3;

逻辑运算符：
与：and
或：or
否：not
例:select * from students where isDelete=0 and id>3;
模糊查询：
like
表示任意多个任意字符：%
表示任意一个任意字符：_
例：select * from students where name like '殷%';
select * from students where name like '殷%' or name like '王%';

范围查询：
表示在一个非连续的范围内：in
表示在一个连续的范围内：between ... and ...

例：select * from students where id in(1,3,5);
select * from students where id between 3 and 8;
select * from students where id between 3 and 8 and gender=1;

空判断查询：
is null：
例：select * from students where birthday is null;

非空判断查询：
is not null：
例：select * from students where birthday is not null;

优先级：
1，小括号>not>比较运算符>逻辑运算符
2，and比or先运算，如果同时出现并希望先算or，需要结合()使用

聚合：
5个聚合函数
count(*)：表示计算总行数
max(例)：求此列的最大值
min(例)：求此列的最小值
sum(例)：求此列的总和
avg(例)：求此列的平均值

例：select count(*) from students where isDelete=0;
select max(id) from students;
select min(id) from students;
select sum(id) from students;
select avg(id) from students where isDelete=0 and gender=0;

子查询：
例1：查询ID所有中最小的，且把这个人的信息查出来
select * from students where id=(select min(id) from students);
例2：查询ID平均值，且把这个人的信息查出来
select * from students where id=(select avg(id) from students);

分组查询：
select 列1,列2,聚合... from 表名 group by 列1,列2,列3,...
例：select gender as 性别,count(*) from students group by gender;

分组后筛选查询：
select 列1,列2,聚合... from 表名 group by 列1,列2,列3,...having 条件
例：select gender as 性别,count(*) from students group by gender having count(*)>2;
select gender as 性别,count(*) as rs from students group by gender having  rs>2;
select gender as 性别,count(*) from students group by gender having gender=0;

排序：
select * from 表名 order by 列1 asc|desc, 列2 asc|desc,...
从小到大排序(默认)：asc
从大到小排序：desc
例：select * from students order by id desc;
select * from students where gender=0 and isDelete=0 order by id desc;

分页/获取部分数据 ：
limit start,count
start：从start开始
count：共获取count条数据

select * from 表名 limit start,count
例：select * from students limit 2,3;
select * from students where gender=0 limit 2,3;

外键约束：
其他表数据

创建外键约束:
mysql> create table scores(
    -> id int auto_increment primary key not null,
    -> score decimal(4,1),
    -> stuid int,
    -> subid int,
    -> foreign key(stuid) references students(id),	#这里是把students中id设置为stuid外键约束
    -> foreign key(subid) references subjects(id));    #这里是把subjects中id设置为subid外键约束
、
外键的级联操作：
在删除students表的数据时，如果这个id值在scores中已存在，则会抛异常
推荐使用逻辑删除，还可以解决这个问题。
可以创建表时指定级联操作，也可以在创建表后再修改外键的级联操作

级联操作的类型包括：
restrict（限制）：默认值，抛异常
cascade（级联）：如果主表的记录删掉，则从表中相关联的记录都将被删除
set null：将外键设置为空
no action：什么都不做

连接查询（多表查询）：
内连接查询 :
匹配得上的才显示出来 ：inner join ... on ...

查询的所有学生所有成绩
select students.name,subjects.title,scores.score from scores
inner join students on scores.stuid=students.id
inner join subjects on scores.subid=subjects.id
order by name;

或	select students.name,subjects.title,scores.score from students
inner join scores on scores.stuid=students.id
inner join subjects on scores.subid=subjects.id
order by name;

查询的所有学生python3成绩
select students.name,subjects.title,scores.score from scores
inner join students on scores.stuid=students.id
inner join subjects on scores.subid=subjects.id
where title='python3'
order by name;

或	select students.name as '姓名',subjects.title as '科目',scores.score as '成绩' from students
inner join scores on scores.stuid=students.id
inner join subjects on scores.subid=subjects.id
where title='pythonn3'
order by name;

左连接查询 :
以左表为主 ：left join ... on ...
以students为主
select * from students
left join scores on scores.stuid=students.id;

以scores为主
select * from scores
left join students on scores.stuid=students.id
left join subjects on scores.subid=subjects.id;

右连接查询 :
以右表为主 ：right join ... on ...
以scores为主
select * from students
right join scores on scores.stuid=students.id

以students为主
select * from scores
right join students on scores.stuid=students.id;

完整的select语句：
select distinct 列*
from 表1 inner|left|right join 表2 on 表1与表2的关系
where ...
group by ... having ...
order by ... asc|desc
limit start,count;

自关联：
外键约束是自己表中的
例：pid外键约束为自己表中的id
create table areas(
aid int auto_increment primary key not null,
atitle varchar(20),
pid int,
foreign key(pid) references areas(aid));

视图：
语法：create view 视图表名 as select * from 表 .....
实际是把select语句进行封装
例：
create view v_1 as
select stu.*,sco.score,sub.title from scores as sco
inner join students as stu on sco.stuid=stu.id
inner join subjects as sub on sco.subid=sub.id;

修改视图，例：
alter view v_1 as
select stu.*,sco.score,sub.title from scores as sco
inner join students as stu on sco.stuid=stu.id
inner join subjects as sub on sco.subid=sub.id
where stu.isDelete=0;

事务：
当一个业务逻辑需要多个sql完成时，如果其中某条sql语句出错，则希望整个操作都退回
使用事务可以完成退回的功能，保证业务逻辑的正确性

事务四大特性(简称ACID)
原子性(Atomicity)：事务中的全部操作在数据库中是不可分割的，要么全部完成，要么均不执行
一致性(Consistency)：几个并行执行的事务，其执行结果必须与按某一顺序串行执行的结果相一致
隔离性(Isolation)：事务的执行不受其他事务的干扰，事务执行的中间结果对其他事务必须是透明的
持久性(Durability)：对于任意已提交事务，系统必须保证该事务对数据库的改变不被丢失，即使数据库出现故障
要求：表的类型必须是innodb或bdb类型，才可以对此表使用事务

查看表的创建语句
show create table students;
修改表的类型
alter table '表名' engine=innodb;
事务语句
开启begin;
提交commit;
回滚rollback;
例：
select * from students;
begin;
update students set birthday='1992-3-2' where name='王书亚';
commint;
select * from students;

select * from students;
begin;
update students set birthday='1992-10-2' where id=3;
rollback;
select * from students;

索引：
查看索引
show index from table_name;
例：show index from areas;

创建索引
create index indexName on talble_name(name(length));
例：create index atitle_index on areas(atitle(20));

删除索引：
drop index [indexName] on table_name;
例：drop index atitle_index on areas;

实例比较效果：
1,开启运行时间监测：
set profiling=1;
2,执行查询语句：
select * from students where birthday>'1992-8-2';
3,查看执行时间：
show profiles;
4,为表的birthday列创建索引：
create index birthday_index on students(birthday);
5,执行查询语句：
select * from students where birthday>'1992-8-2';
6,查看执行时间：
show profiles;
7,删除索引：
drop index birthday_index on students;
8,关闭时间监测：
set profiling=0;
'''