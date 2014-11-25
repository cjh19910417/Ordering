# -*- coding: UTF-8 -*-
from django import forms
from OrderFood.models import Team, Department, Orderlist


__author__ = 'chenjianhua'


class ContactForm(forms.Form):
    subject = forms.CharField(required=True, label='主题', help_text='填写一个主题信息', max_length='20', min_length='5')
    email = forms.EmailField(required=True, help_text='Example@qq.com')
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


class OrderListForm(forms.Form):
    name = forms.CharField(required=True, label='名字', max_length=30, min_length=2)
    dept = forms.ModelChoiceField(required=True, queryset=Department.objects.all(), label='部门')
    team = forms.ModelChoiceField(required=True, queryset=Team.objects.all(), label='项目组')
    food_ids = forms.CharField(widget=forms.HiddenInput)
    comments = forms.CharField(required=False, label='备注', max_length=100, help_text='如:加饭!')
    period = forms.CharField( widget=forms.Select(choices=(('dinner', u'晚餐'),('lunch', u'中饭'),('breakfast', u'早餐'),)),
                             label='时段', required=True)