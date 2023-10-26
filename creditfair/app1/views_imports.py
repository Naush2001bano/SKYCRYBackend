from django.shortcuts import render,redirect
from datetime import datetime,timedelta,time,date
from django.db.models import Count,Sum,Case,When,F,Q
from django.db import connection
from .models import *
from .serializers import * 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
import pandas as pd
import requests
from django.http import FileResponse
import io
import json
import xlwt
import random



# for rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from functools import wraps


def validate_bearer_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Extract the Bearer token from the Authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token_key = parts[1]
                    token = Token.objects.get(key=token_key)
                    request.user = token.user  # Attach the user to the request
                    print(token.user,'tokenuser')
                else:
                    raise Token.DoesNotExist
            else:
                raise Token.DoesNotExist
        except Token.DoesNotExist:
            return JsonResponse({'status': 401, 'message': 'Unauthorized'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

@api_view(['GET'])
@validate_bearer_token
def checktoken(request):
    process=request.user.process
    user_level=request.user.user_level
    return JsonResponse({'status':200,'msg':'Valid Token',"user_level":user_level,"process":process})


