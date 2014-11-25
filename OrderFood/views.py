# -*- coding: UTF-8 -*-
from datetime import datetime, date
import json
from django.core import serializers
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import TemplateDoesNotExist, RequestContext
from django.views.decorators.csrf import csrf_exempt
import itertools
from OrderFood.forms import ContactForm, OrderListForm
from OrderFood.models import Food, FoodCategory, Orderlist, Team, Department, Restaurant


def index(request):
    return render_to_response('index.html')


@csrf_exempt
def load_nav_info(request):
    restaurants = serializers.serialize("json", Restaurant.objects.all())
    teams = serializers.serialize("json", Team.objects.all())
    response_data = {'restaurants': restaurants, 'teams': teams}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def demo(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print cd
            return HttpResponseRedirect('/demo/')
        else:
            return render_to_response('demo.html', locals(), context_instance=RequestContext(request))
    else:
        form = ContactForm()
        return render_to_response('demo.html', locals(), context_instance=RequestContext(request))


def direct_to_template(request, template_name):
    try:
        return render_to_response("%s.html" % template_name)
    except TemplateDoesNotExist:
        raise Http404()


def order_food(request, restaurant_name):
    if request.method == 'POST':
        form = OrderListForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(name=form.cleaned_data['team'])
            dept = Department.objects.get(name=form.cleaned_data['dept'])
            period = form.cleaned_data['period']
            restaurant = Restaurant.objects.get(code=restaurant_name)
            comments = form.cleaned_data['comments']
            order = Orderlist.objects.create(owner=form.cleaned_data['name'], own_team=team, own_dept=dept,
                                             restaurant=restaurant, comments=comments, period=period)

            food_ids = form.cleaned_data['food_ids']
            food_arr = food_ids.split(',')
            for food_id in food_arr:
                order.foods.add(Food.objects.get(id=food_id))
            # print order
            redirect_url = "/orderdetail/" + team.name + '/today/'
            return HttpResponseRedirect(redirect_url)

    foods = Food.objects.filter(Q(isFixed=1) | Q(vaildtime_end__gte=date.today(), vaildtime_begin__lte=date.today()), restaurant__code=restaurant_name)
    categories = FoodCategory.objects.filter(restaurant__code=restaurant_name)
    if request.method == 'GET':
        form = OrderListForm()
    return render_to_response('ordermenu/orderList.html', locals(), context_instance=RequestContext(request))


def fetch_order(team, year, month, day):
    return Orderlist.objects.filter(own_team__name=team,
                                    createdTime=datetime(int(year), int(month), int(day))).order_by("-id")


def order_detail(request, team, year, month, day):
    orders = fetch_order(team, year, month, day)

    dinner_total = orders.filter(period='dinner').count()
    lunch_total = orders.filter(period='lunch').count()
    breakfast_total = orders.filter(period='breakfast').count()

    restaurants = orders.values_list('restaurant__id', 'restaurant__name')
    restaurants = set(restaurants)
    print restaurants
    period = [('dinner', u'晚餐', dinner_total), ('lunch', u'中饭', lunch_total), ('breakfast', u'早餐', breakfast_total)]

    return render_to_response('ordermenu/orderDetail.html', locals(), context_instance=RequestContext(request))


def order_today(request, team):
    _now = datetime.now()
    return order_detail(request, team, str(_now.year), str(_now.month), str(_now.day))


@csrf_exempt
def remove_order(request):
    try:
        _id = request.POST['id']
        order = Orderlist.objects.get(id=_id)
        order.delete()
    except Exception, e:
        print e
        return HttpResponse("0")
    return HttpResponse('1')


def order_count_today(request, team):
    _now = datetime.now()
    return order_count(request, team, str(_now.year), str(_now.month), str(_now.day))


def order_count(request, team, year, month, day):
    created_time = year+'-'+month+'-'+day
    count_info = Orderlist.objects.count_order(team, created_time)
    return render_to_response('ordermenu/orderCount.html', locals(), context_instance=RequestContext(request))
