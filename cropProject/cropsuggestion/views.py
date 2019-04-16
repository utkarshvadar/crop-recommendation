from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
import pandas as pd
import os
from . import modelapi
BASE = os.path.dirname(os.path.abspath(__file__))

from . import forms

def test(request):
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    return Response(df.to_dict())


class apitest(APIView):
    def get(self,request):
        df = pd.read_csv(os.path.join(BASE, 'data.csv'))
        return Response(df.to_json(orient='records'))

def index(request):
   # df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    return HttpResponse('<h1>utkarsh</h1>')


def test_form(request):
    if (request.method == 'POST'):
        form = forms.LoginForm(request.POST)
       # s = form['lag'].value()+" "+form['season'].value()
        recommended_crop= modelapi.crop_model(form['lat'].value(),form['lag'].value(),form['season'].value())
        return JsonResponse(recommended_crop.to_dict())

    elif (request.method == 'GET'):
        form = forms.LoginForm(request.GET)
        #s = form['lag'].value()+" "+form['season'].value()
        recommended_crop= modelapi.crop_model(form['lat'].value(),form['lag'].value(),form['season'].value())
        return JsonResponse(recommended_crop.to_dict())

    stu = forms.LoginForm(request.POST)
    return render(request, "student/register.html", {'form': stu})

