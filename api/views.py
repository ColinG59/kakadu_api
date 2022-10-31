from django.shortcuts import render
from django.http import JsonResponse
from kakadu_cache import get_cache, get_random_picture

# Create your views here.


def api_response(request):
    
    picture_dict = get_random_picture()
    return JsonResponse(picture_dict)
    
    
    