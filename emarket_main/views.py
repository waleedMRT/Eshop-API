
from django.http import JsonResponse

def custom_404(request , exception):
    message = {
        'success' : False,
        'status_code' : 404,
        'message' : 'page not found (mrt)'
    }

    return JsonResponse(message , status=404)

def custom_500(request):
    message = {
        'success' : False,
        'status_code' : 500,
        'message' : 'Internal server (mrt)'
    }

    return JsonResponse(message , status=500)