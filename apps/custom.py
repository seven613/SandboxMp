# -*- coding: utf-8 -*- 
"""
项目: sandboxMP
作者: 张强
创建时间: 2020-03-06 09:38
IDE: PyCharm
介绍:
"""
import json

from django.views.generic import CreateView, UpdateView
from django.shortcuts import HttpResponse
from django.shortcuts import Http404

from system.mixin import LoginRequiredMixin


class SandboxEditViewMixin:

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class SandboxGetObjectMixin:
    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()
        if 'id' in self.request.GET and self.request.GET['id']:
            queryset = queryset.filter(id=int(self.request.GET['id']))
        elif 'id' in self.request.POST and self.request.POST['id']:
            queryset = queryset.filter(id=int(self.request.POST['id']))
        else:
            raise AttributeError("Generic detail view %s must be called with id." % self.__class__.__name__)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query" % {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class SandboxCreateView(LoginRequiredMixin, SandboxEditViewMixin, CreateView):
    pass


class SandboxUpdateView(LoginRequiredMixin, SandboxEditViewMixin, SandboxGetObjectMixin, UpdateView):

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

# class SimpleInfoCreateView(LoginRequiredMixin, CreateView):
#
#     def post(self, request, *args, **kwargs):
#         res = dict(result=False)
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             res['result'] = True
#         return HttpResponse(json.dumps(res), content_type='application/json')
#
#
# class SandboxUpdateview(LoginRequiredMixin, UpdateView):
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         res = dict(resutl=False)
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             res['result'] = True
#         return HttpResponse(json.dumps(res), content_type='application/json')
