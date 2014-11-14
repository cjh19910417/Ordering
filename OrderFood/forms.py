# -*- coding: UTF-8 -*-
from django import forms


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