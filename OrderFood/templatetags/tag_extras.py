# coding=utf-8
from django import template

from OrderFood.models import Orderlist


register = template.Library()


@register.filter
def total_order(value, arg=None):
    result = 0
    if arg is not None:
        for order in value.filter(period=arg):
            result += total_foods(order.foods.all())
    else:
        for order in value:
            result += total_foods(order.foods.all())
    return result


@register.filter
def total_foods(foods):
    result = 0
    for food in foods:
        result += int(food.price)
    return result


@register.filter
def name(value, arg=None):
    result = ''
    assert isinstance(value, Orderlist)
    if arg is not None:
        if arg == 'food':
            foods = value.foods.all().filter(type__id=1)
            if foods.count() > 1:
                result += '套餐('
                for index, food in enumerate(foods):
                    result += food.name.encode('utf-8')
                    if (index+1) < foods.count():
                        result += ' + '
                result += ')'
            elif foods.count() == 1:
                result = foods[0].name
        if arg == 'drink':
            drinks = value.foods.all().filter(type__id=2)
            for index, drink in enumerate(drinks):
                    result += drink.name.encode('utf-8')
                    if (index+1) < drinks.count():
                        result += ' + '
    return result


# @register.filter(is_safe=False)
# def countinfo(orders):
#     """
#
#     :param orders:
#     :return:
#     """
#     result = 'nihao<br>hehe'
#     return result