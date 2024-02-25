from django.shortcuts import render 
from django.http import HttpResponse
from .utils import send_reset_password_email_task

def index(request):
    send_reset_password_email_task()
    return HttpResponse('Done')