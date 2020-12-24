from django.shortcuts import render, HttpResponse, redirect
from .models import requestCount, threshold

# Create your views here.
def indexPageView(request):
    return render(request, 'controler/index.html')

def addAndWait(response):
    if response.method == 'POST':
        requests = requestCount.objects.get(id=1)
        requests.count += 1
        requests.save()
        return render(response, 'controler/wait.html')
    else:
        return redirect('index')

def adminPageView(request):
    count = requestCount.objects.get(id=1)
    limit = threshold.objects.get(id=1)
    return render(request, 'controler/admin.html', {'count':count, 'threshold': limit})

def resetRequestCount(response):
    if response.method == 'POST':
        requests = requestCount.objects.get(id=1)
        requests.count = 0
        requests.save()
        return redirect('admin')
    else:
        return redirect('admin')

def changeThreshold(request):
    if request.GET['limit'] == '':
        return redirect('admin')
    else:
        limit = threshold.objects.get(id=1)
        limit.threshold = request.GET['limit']
        limit.save()
        return redirect('admin')
