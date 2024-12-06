from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Order

# Create your views here.

class API(GenericAPIView):
    def get(self,request):
        pass
    def post(self,request):
        pass
    def put(self,request):
        pass
