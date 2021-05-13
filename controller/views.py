import time
import math 
from django.shortcuts import render, redirect, HttpResponse
from .models import requestCount, threshold, requestReset, studentWaitTime

# index page view
# when the user navigates to the root directory the view will check for a cookie called allowReload
# if this cookie exists then the user is not allowed to reload the page, the cookie value is the epoch timestamp
# of the cookies expiration, as soon as it is expired the user is allowed to submit another request
# if the cookie is present then the wait page is loaded and the current time is subtracted from the expiration to
# determine how much longer the user needs to wait, that value is passed into the view to be displayed
# if the cookie does not exist then the index page is rendered as usual 
# if a csrf error is thrown it will redirect to itself which will refresh and renew the token
def indexPageView(request):
    try:
        try:
            remaining = int(request.COOKIES['allowReload']) - int(time.time()) # check for cookie, calculate the wait time remaining
            context = {'rem': remaining} # set the number of seconds left equal to rem in the context to be sent to the template 
            return render(request, 'controller/wait.html', context) # render the template and send the time remaining to be displayed on the wait page
        except KeyError: # if a key error exception is thrown that means there is no cookie so the index page is displayed normally 
            return render(request, 'controller/index.html')
    except:
        return redirect('index')

# wait page view
# this view should only be called if the response method is post, there is no other circumstance where this should be called 
# when called the function looks for the cookie and renders the wait page with the time remaining if the cookie exists
# if the cookie does not exist the key error exception is thrown which means the user is allowed to submit a request
# one is added to the current requests and then a timer is started and the wait page is rendered 
# the seconds to wait is calculated based off of the value stored in the database, which can be edited on the admin page
def addAndWait(response):
    try:
        if response.method == 'POST':
            try:
                defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
                remaining = int(response.COOKIES['allowReload']) - int(time.time())
                context = {'rem': remaining} 
                currentTime = time.time() 
                expirationTime = currentTime + defaultWaitTime
                cookieValue = int(expirationTime)
                resp = render(response, 'controller/wait.html', context)
            except KeyError:
                defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
                requests = requestCount.objects.get(id=1)
                requests.count += 1
                requests.save()
                context = {'rem': defaultWaitTime}
                currentTime = time.time()
                expirationTime = currentTime + defaultWaitTime 
                cookieValue = int(expirationTime)
                resp = render(response, 'controller/wait.html', context)
                resp.set_cookie('allowReload', cookieValue, max_age=defaultWaitTime)
            return resp
        else:
            return redirect('index')
    except:
        return redirect('index')

# admin page view
# this function pulls the current requests and the threshold from the database and sends them when the admin page is rendered 
# the admin page is only shown if the user is logged in, if not logged in the user is redirected to the login page 
def adminPageView(request):
    try:
        if (request.user.is_authenticated):
            defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
            timeToReset = int(request.COOKIES['resetTime']) - int(time.time())
            resetSetting = requestReset.objects.get(id=1).requestReset
            count = requestCount.objects.get(id=1)
            limit = threshold.objects.get(id=1)
            return render(request, 'controller/admin.html', {'count':count, 'threshold': limit, 'timeToReset': timeToReset, 'resetSetting': resetSetting, 'studentWaitTime': defaultWaitTime})
        else:
            return redirect('/login/')
    except KeyError:
        if (request.user.is_authenticated):
            defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
            resetSetting = requestReset.objects.get(id=1).requestReset
            count = requestCount.objects.get(id=1)
            limit = threshold.objects.get(id=1)
            currentTime = time.time()
            expirationTime = currentTime + resetSetting
            cookieValue = int(expirationTime)
            resp = render(request, 'controller/admin.html', {'count':count, 'threshold': limit, 'timeToReset': resetSetting, 'resetSetting': resetSetting, 'studentWaitTime': defaultWaitTime})
            resp.set_cookie('resetTime', cookieValue, max_age=resetSetting)
            return resp
        else:
            return redirect('/login/')

# this function is called when the count exceeds the threshold or the admin wants to reset the count to 0
def resetRequestCount(response):
    if (response.user.is_authenticated):
        if response.method == 'GET':
            requests = requestCount.objects.get(id=1)
            requests.count = 0
            requests.save()
            resetSetting = requestReset.objects.get(id=1).requestReset
            currentTime = time.time()
            expirationTime = currentTime + resetSetting
            cookieValue = int(expirationTime)
            resp = redirect('admin')
            resp.set_cookie('resetTime', cookieValue, max_age=resetSetting)
            return resp
        else:
            return redirect('admin')
    else:
        return redirect('/login/')

# this function receives a new value from the user and makes that value the new threshold
def changeThreshold(request):
    if (request.user.is_authenticated):
        if request.GET['limit'] == '':
            return redirect('admin')
        else:
            limit = threshold.objects.get(id=1)
            newLimit = int(request.GET['limit'])
            newLimit = math.floor(newLimit)
            limit.threshold = newLimit
            limit.save()
            return redirect('admin')
    else:
        return redirect('/login/')

# uses a cookie to keep track of the time elapsed from the last request reset 
# lets the admin change how often they want the requests to be reset to zero
def changeResetSetting(request):
    if (request.user.is_authenticated):
        if request.GET['setting'] == '':
            return redirect('admin')
        else:
            setting = requestReset.objects.get(id=1)
            newSetting = int(request.GET['setting'])
            newSetting = math.floor(newSetting)
            setting.requestReset = newSetting
            setting.save()
            resp = redirect('admin')
            resetSetting = requestReset.objects.get(id=1).requestReset
            currentTime = time.time()
            expirationTime = currentTime + resetSetting
            cookieValue = int(expirationTime)
            resp = redirect('admin')
            resp.set_cookie('resetTime', cookieValue, max_age=resetSetting)
            return resp
    else: 
        return redirect('/login/')

# reset the request timer to the max time
def resetTimer(request):
    if (request.user.is_authenticated):
        resp = redirect('admin')
        resetSetting = requestReset.objects.get(id=1).requestReset
        currentTime = time.time()
        expirationTime = currentTime + resetSetting
        cookieValue = int(expirationTime)
        resp = redirect('admin')
        resp.set_cookie('resetTime', cookieValue, max_age=resetSetting)
        return resp
    else:
        return redirect('/login/')

# change the time that the student has to wait before requesting again
def changeStudentWaitTime(request):
    if (request.user.is_authenticated):
        if (request.GET['newStudentWaitTime'] == ''):
            return redirect('admin')
        else:
            defaultWaitTime = studentWaitTime.objects.get(id=1)
            newDefaultWaitTime = int(request.GET['newStudentWaitTime'])
            newDefaultWaitTime = math.floor(newDefaultWaitTime)
            defaultWaitTime.studentWaitTime = newDefaultWaitTime
            defaultWaitTime.save()
            return redirect('admin')
    else:
        return redirect('/login/')

def loader(request):
    return HttpResponse('loaderio-06425f874f86c9f72b69533f40af5a0c')