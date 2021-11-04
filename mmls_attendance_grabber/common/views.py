from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.utils.decorators import classonlymethod
import asyncio

from background_task.models import Task

# Create your views here.

class IndexView(generic.View):
    template_name = 'common/index.html'

    def get(self, request):
        return render(request, self.template_name)