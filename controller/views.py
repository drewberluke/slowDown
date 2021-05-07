import time
import math 
from django.shortcuts import render, redirect
from .models import requestCount, threshold

# index page view
# when the user navigates to the root directory the view will check for a cookie called allowReload
# if this cookie exists then the user is not allowed to reload the page, the cookie value is the epoch timestamp
# of the cookies expiration, as soon as it is expired the user is allowed to submit another request
# if the cookie is present then the wait page is loaded and the current time is subtracted from the expiration to
# determine how much longer the user needs to wait, that value is passed into the view to be displayed
# if the cookie does not exist then the index page is rendered as usual 
def indexPageView(request):
    try:
        remaining = int(request.COOKIES['allowReload']) - int(time.time()) # check for cookie, calculate the wait time remaining
        context = {'rem': remaining} # set the number of seconds left equal to rem in the context to be sent to the template 
        return render(request, 'controller/wait.html', context) # render the template and send the time remaining to be displayed on the wait page
    except KeyError: # if a key error exception is thrown that means there is no cookie so the index page is displayed normally 
        return render(request, 'controller/index.html')

# wait page view
# this view should only be called if the response method is post, there is no other circumstance where this should be called 
# when called the function looks for the cookie and renders the wait page with the time remaining if the cookie exists
# if the cookie does not exist the key error exception is thrown which means the user is allowed to submit a request
# one is added to the current requests and then a 60 second timer is started and the wait page is rendered 
def addAndWait(response):
    if response.method == 'POST':
        try:
            remaining = int(response.COOKIES['allowReload']) - int(time.time())
            context = {'rem': remaining} 
            currentTime = time.time() 
            expirationTime = currentTime + 60
            cookieValue = int(expirationTime)
            resp = render(response, 'controller/wait.html', context)
        except KeyError:
            requests = requestCount.objects.get(id=1)
            requests.count += 1
            requests.save()
            context = {'rem': 60}
            currentTime = time.time()
            expirationTime = currentTime + 60
            cookieValue = int(expirationTime)
            resp = render(response, 'controller/wait.html', context)
            resp.set_cookie('allowReload', cookieValue, max_age=60)
        return resp
    else:
        return redirect('index')

# admin page view
# this function pulls the current requests and the threshold from the database and sends them when the admin page is rendered 
# the admin page is only shown if the user is logged in, if not logged in the user is redirected to the login page 
def adminPageView(request):
    if (request.user.is_authenticated):
        count = requestCount.objects.get(id=1)
        limit = threshold.objects.get(id=1)
        return render(request, 'controller/admin.html', {'count':count, 'threshold': limit})
    else:
        return redirect('/login/')

# this function is called when the count exceeds the threshold or the admin wants to reset the count to 0
def resetRequestCount(response):
    if response.method == 'POST':
        requests = requestCount.objects.get(id=1)
        requests.count = 0
        requests.save()
        return redirect('admin')
    else:
        return redirect('admin')

# this function receives a new value from the user and makes that value the new threshold
def changeThreshold(request):
    if request.GET['limit'] == '':
        return redirect('admin')
    else:
        limit = threshold.objects.get(id=1)
        newLimit = int(request.GET['limit'])
        newLimit = math.floor(newLimit)
        limit.threshold = newLimit
        limit.save()
        return redirect('admin')