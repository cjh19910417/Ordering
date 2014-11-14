from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import TemplateDoesNotExist, RequestContext
from OrderFood.forms import ContactForm


def hello(request):
    return HttpResponse("Hello world")


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