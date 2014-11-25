# coding=utf-8
from django.db import models, connections, connection

# Create your models here.


class Department(models.Model):
    """
        部门
    """
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    """
        团队
    """
    name = models.CharField(max_length=30)
    dept = models.ForeignKey(Department, null=True)

    def __unicode__(self):
        return self.name


class FoodType(models.Model):
    """
        食物类型
    """
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    """
        联系方式
    """
    telNo1 = models.CharField(max_length=11, blank=True, null=True)
    telNo2 = models.CharField(max_length=11, blank=True, null=True)
    telNo3 = models.CharField(max_length=11, blank=True, null=True)
    telNo4 = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.address


class Restaurant(models.Model):
    """
        饭馆
    """
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30)
    contact_info = models.ForeignKey(Contact, null=True)

    def __unicode__(self):
        return self.name


class FoodCategory(models.Model):
    """
        食物细类
    """

    name = models.CharField(max_length=30)
    type = models.ForeignKey(FoodType, null=True)
    restaurant = models.ForeignKey(Restaurant)

    def __unicode__(self):
        return self.name


class Taste(models.Model):
    """
        口味
    """
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Food(models.Model):
    """
        食物
    """
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField()
    type = models.ForeignKey(FoodType)
    category = models.ForeignKey(FoodCategory, null=True)
    taste = models.ForeignKey(Taste, null=True)
    vaildtime_begin = models.DateTimeField(blank=True, null=True)
    vaildtime_end = models.DateTimeField(blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant)
    isFixed = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s %s元' % (self.name, self.price)


def dictfetchall(cursor):

    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class OrderManager(models.Manager):
    def count_order(self, team, created_time):
        try:
            cursor = connection.cursor()
            cursor.execute("""select f.food_id,food.name,food.type_id,count(1) as total
                                 from OrderFood_orderlist o,OrderFood_team t,OrderFood_orderlist_foods f,OrderFood_food food
                                  where t.id = o.own_team_id and
                                  o.id = f.orderlist_id and
                                  f.food_id = food.id and
                                   t.name = %s and
                                    o.createdTime = %s
                                     group by f.food_id
                                     order by type_id asc,total desc """, [team, created_time])
        except Exception, e:
            print e
        return dictfetchall(cursor)


class Orderlist(models.Model):
    """
        订单
    """
    #order_id = models.CharField(max_length=50)
    owner = models.CharField(max_length=30)
    foods = models.ManyToManyField(Food)
    createdTime = models.DateField(auto_now=True)
    own_team = models.ForeignKey(Team)
    own_dept = models.ForeignKey(Department, null=True)
    comments = models.CharField(max_length=100, verbose_name='备注', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, null=True)
    period = models.CharField(max_length=10, null=True)
    objects = OrderManager()

    def __unicode__(self):
        return '%s-%s-%s' % (self.owner, self.own_team, self.comments,)