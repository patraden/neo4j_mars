import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . import magic_squares
from django.utils.cache import patch_cache_control

def index(request):
	max_age=180
	if request.method == 'GET':
		if request.GET.get('s1') and request.GET.get('s2'):
			try:
				s1=json.loads(request.GET.get('s1'))
				s2=json.loads(request.GET.get('s2'))
				res_=magic_squares.magic_square_calculate(0,0,s1,s2)
				res={"Res type":"New", "Count": len(res_),"Solutions":res_}
			except ValueError:
				res=["Failed to read parameters"]
			response=JsonResponse(res,safe=False)
			patch_cache_control(response,public=True,max_age=max_age)
		else:
			res_=magic_squares.magic_square_calculate(0,0,[7,8],[7,8])
			res={"Res type":"Default", "Count": len(res_),"Solutions":res_}
			response=JsonResponse(res,safe=False)
			patch_cache_control(response,public=True,max_age=max_age)
		return response

# Create your views here.
