# coding:utf-8
# author:YJ沛

'''
简介
    查询集表示从数据库中获取的对象集合
    查询集可以含有零个、一个或多个过滤器
    过滤器基于所给的参数限制查询的结果
    从Sql的角度，查询集和select语句等价，过滤器像where和limit子句

接下来主要讨论如下知识点
    1，查询集
    3，字段查询：比较运算符，F对象，Q对象

查询集
    1，在管理器上调用过滤器方法会返回查询集
    2，查询集经过过滤器筛选后返回新的查询集，因此可以写成链式过滤
    3，惰性执行：创建查询集不会带来任何数据库的访问，直到调用数据时，才会访问数据库
    4，何时对查询集求值：迭代，序列化，与if合用
    5，返回查询集的方法，称为过滤器
        all()
        filter()
        exclude()
        order_by()
        values()：一个对象构成一个字典，然后构成一个列表返回
    写法：
        filter(键1=值1,键2=值2)
        等价于
        filter(键1=值1).filter(键2=值2)


返回单个值的方法
    get()：返回单个满足条件的对象
        如果未找到会引发"模型类.DoesNotExist"异常
        如果多条被返回，会引发"模型类.MultipleObjectsReturned"异常

    count()：返回当前查询的总条数
    first()：返回第一个对象
    last()：返回最后一个对象
    exists()：判断查询集中是否有数据，如果有则返回True


限制查询集
    1，查询集返回列表，可以使用下标的方式进行限制，等同于sql中的limit和offset子句
    2，注意：不支持负数索引
    3，使用下标后返回一个新的查询集，不会立即执行查询
    4，如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()引发DoesNotExist异常


查询集的缓存
    每个查询集都包含一个缓存来最小化对数据库的访问
    在新建的查询集中，缓存为空，首次对查询集求值时，会发生数据库查询，django会将查询的结果存在查询集的缓存中，并返回请求的结果，接下来对查询集求值将重用缓存的结果
    情况一：这构成了两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载
        print([e.title for e in Entry.objects.all()])
        print([e.title for e in Entry.objects.all()])

    情况二：两次循环使用同一个查询集，第二次使用缓存中的数据
        querylist=Entry.objects.all()
        print([e.title for e in querylist])
        print([e.title for e in querylist])

    何时查询集不会被缓存：当只对查询集的部分进行求值时会检查缓存，但是如果这部分不在缓存中，那么接下来查询返回的记录将不会被缓存，这意味着使用索引来限制查询集将不会填充缓存，如果这部分数据已经被缓存，则直接使用缓存中的数据


字段查询
    1，实现where子名，作为方法filter()、exclude()、get()的参数
    2，语法：属性名称__比较运算符=值
    3，表示两个下划线，左侧是属性名称，右侧是比较类型
    4，对于外键，使用“属性名_id”表示外键的原始值
    5，转义：like语句中使用了%与，匹配数据中的%与，在过滤器中直接写，
        例如：filter(title__contains="%")=>where title like '%\%%'，表示查找标题中包含%的

比较运算符
    exact：表示判等，大小写敏感；如果没有写“ 比较运算符”，表示判等
        filter(isDelete=False)

    contains：是否包含，大小写敏感
        exclude(btitle__contains='传')

    startswith、endswith：以value开头或结尾，大小写敏感
        exclude(btitle__endswith='传')

    isnull、isnotnull：是否为null
        filter(btitle__isnull=False)

    在前面加个i表示不区分大小写，如iexact、icontains、istarswith、iendswith
    in：是否包含在范围内
        filter(pk__in=[1, 2, 3, 4, 5])

    gt、gte、lt、lte：大于、大于等于、小于、小于等于
        filter(id__gt=3)

    year、month、day、week_day、hour、minute、second：对日期间类型的属性进行运算
        filter(bpub_date__year=1980)
        filter(bpub_date__gt=date(1980, 12, 31))


跨关联关系的查询：处理join查询
    1，语法：模型类名 <属性名> <比较>
    2，注：可以没有__<比较>部分，表示等于，结果同inner join
    3，可返向使用，即在关联的两个模型中都可以使用
        filter(heroinfo_ _hcontent_ _contains='八')


查询的快捷方式：pk，pk表示primary key，默认的主键是id
    filter(pk__lt=6)


聚合函数
    1，使用aggregate()函数返回聚合函数的值
    2，函数：Avg，Count，Max，Min，Sum
        from django.db.models import Max
        maxDate = list.aggregate(Max('bpub_date'))

    3，count的一般用法：
        count = list.count()


F对象
    1，可以使用模型的字段A与字段B进行比较，如果A写在了等号的左边，则B出现在等号的右边，需要通过F对象构造
        list.filter(bread__gte=F('bcommet'))

    2，django支持对F()对象使用算数运算
        list.filter(bread__gte=F('bcommet') * 2)

    3，F()对象中还可以写作“模型类__列名”进行关联查询
        list.filter(isDelete=F('heroinfo__isDelete'))

    4，对于date/time字段，可与timedelta()进行运算
        list.filter(bpub_date__lt=F('bpub_date') + timedelta(days=1))


Q对象
    1，过滤器的方法中关键字参数查询，会合并为And进行
    2，需要进行or查询，使用Q()对象
    3，Q对象(django.db.models.Q)用于封装一组关键字参数，这些关键字参数与“比较运算符”中的相同
        from django.db.models import Q
        list.filter(Q(pk_ _lt=6))

    4，Q对象可以使用&（and）、|（or）操作符组合起来
    5，当操作符应用在两个Q对象时，会产生一个新的Q对象
        list.filter(pk_ _lt=6).filter(bcommet_ _gt=10)
        list.filter(Q(pk_ _lt=6) | Q(bcommet_ _gt=10))

    6，使用~（not）操作符在Q对象前表示取反
        list.filter(~Q(pk__lt=6))

    7，可以使用&|~结合括号进行分组，构造做生意复杂的Q对象
    8，过滤器函数可以传递一个或多个Q对象作为位置参数，如果有多个Q对象，这些参数的逻辑为and
    9，过滤器函数可以混合使用Q对象和关键字参数，所有参数都将and在一起，Q对象必须位于关键字参数的前面

'''
