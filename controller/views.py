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
            context = buildContex(remaining)
            return render(request, 'controller/wait.html', context) # render the template and send the time remaining to be displayed on the wait page
        except KeyError: # if a key error exception is thrown that means there is no cookie so the index page is displayed normally 
            remaining = 'n/a'
            context = buildContex(remaining)
            context 
            return render(request, 'controller/index.html', context)
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
                remaining = int(response.COOKIES['allowReload']) - int(time.time())
                context = buildContex(remaining)
                currentTime = time.time() 
                defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
                expirationTime = currentTime + defaultWaitTime
                cookieValue = int(expirationTime)
                resp = render(response, 'controller/wait.html', context)
            except KeyError:
                defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
                requests = getRequests('obj')
                requests.count += 1
                requests.save()
                context = buildContex(defaultWaitTime)
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
# calculates time since last login and if it has been more than 4 hours automatically logs out 
def adminPageView(request):
    # lastLogin = request.user.last_login   # **** auto logout after x min 
    # currentTime = time.time()
    # lastLogin = time.mktime(lastLogin.timetuple())
    # minSinceLastLogin = (currentTime - lastLogin) / 60
    # # print('*** ' + str(minSinceLastLogin))
    # if minSinceLastLogin > 240:
    #     return redirect('/logout/')
    # else:    
    if request.user.is_authenticated:
        try:
            defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
            timeToReset, timerStatus = getTimeToReset(request)
            alertStatus = getAlertStatus(request)
            resetSetting = requestReset.objects.get(id=1).requestReset
            currentRequests = getRequests('count')
            threshold = getThreshold('count')
            return render(request, 'controller/admin.html', {'count': currentRequests, 'threshold': threshold, 'timeToReset': timeToReset, 'resetSetting': resetSetting, 'studentWaitTime': defaultWaitTime, 'timerStatus': timerStatus, 'alertStatus': alertStatus})
        except KeyError:
            defaultWaitTime = studentWaitTime.objects.get(id=1).studentWaitTime
            resetSetting, timerStatus = getResetSetting(request)
            alertStatus = getAlertStatus(request)
            currentRequests = getRequests('count')
            threshold = getThreshold('count')
            currentTime = time.time()
            expirationTime = currentTime + requestReset.objects.get(id=1).requestReset
            cookieValue = int(expirationTime)
            resp = render(request, 'controller/admin.html', {'count': currentRequests, 'threshold': threshold, 'timeToReset': resetSetting, 'resetSetting': resetSetting, 'studentWaitTime': defaultWaitTime, 'timerStatus': timerStatus, 'alertStatus': alertStatus})
            resp.set_cookie('resetTime', cookieValue, max_age=resetSetting)
            return resp
    else:
        return redirect('/login/')
    
# this function is called when the count exceeds the threshold or the admin wants to reset the count to 0
def resetRequestCount(response):
    if (response.user.is_authenticated):
        if response.method == 'GET':
            currentRequests = getRequests('obj')
            currentRequests.count = 0
            currentRequests.save()
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
            threshold = getThreshold('obj')
            newLimit = int(request.GET['limit'])
            newLimit = math.floor(newLimit)
            threshold.threshold = newLimit
            threshold.save()
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

# heroku loader.io addon verification string 
def loader(request):
    return HttpResponse('loaderio-06425f874f86c9f72b69533f40af5a0c')

# function to determine the amount of padding to put in the progress bar
# depends on what the percentage is, it needs to change so that 10% and 
# lower does not look weird 
def getSpace(pct):  
    space = ''
    if pct > 0 and pct < 11:
        pct2 = pct/2
        pct2 = math.floor(pct2)
        pct2 = pct2 + 1
        if pct2 > 3:
            pct2 = pct2 + 1
        for x in range(0, pct2):
            space = space + '&nbsp;'
        return space
    else:
        space = '&nbsp;'
        return space

# get the current number of requests or the requests object 
def getRequests(type):
    if type == 'count':
        return requestCount.objects.get(id=1).count
    elif type == 'obj':
        return requestCount.objects.get(id=1)        
    else:
        return 'Error'

# get the current threshold or the threshold object
def getThreshold(type):
    if type == 'count':
        return threshold.objects.get(id=1).threshold 
    elif type == 'obj':
        return threshold.objects.get(id=1)
    else:
        return 'Error'

# build the context for the index and wait pages. 
# takes the remaining time as an argument and builds the 
# context accordingly. If the threshold has been bet then the 
# values are changed so that the styling stays consistent 
# notifies students when the limit has been met by putting text into 
# the loading bar 
def buildContex(remaining):
    currentRequests = getRequests('count')
    currentThreshold = getThreshold('count')
    pct = (currentRequests / currentThreshold) * 100
    align = 'right'
    space = getSpace(pct)
    if currentRequests >= currentThreshold:
        currentRequests = "Dr. Gaskin has been notified"
        pct = 100
        currentThreshold = ''
        align = 'center'
    context = {'rem': remaining, 'current': currentRequests, 'threshold': currentThreshold, 'pct': pct, 'align': align, 'space': space} # set the number of seconds left equal to rem in the context to be sent to the template 
    return context
    
# determine whether the playAlert button needs to be checked or unchecked 
# this loads the page the way it should be so the javascript doesn't make 
# the button flicker
def getAlertStatus(request):
    try:
        alert = request.COOKIES['playAlert']
        if alert == 'true':
            return 'checked'
        elif alert == 'false':
            return 'unchecked'
        else:
            return 'Error'
    except KeyError:
        return 'checked'

# determine what to send to the view. if there is no cookie then just send the time and 
# 'checked' to make the button show up correctly. otherwise check what the cookie is and 
# send the appropriate values button checked/unchecked and what to display in the timer box
# ***** this one is a little different than getTimeToReset() because it is called when the the value needs to be 
# the default wait time value
def getResetSetting(request):
    try:
        timerStatus = request.COOKIES['timerStatus']
        # print('*** ' + str(timerStatus))
        if timerStatus == 'on':
            return requestReset.objects.get(id=1).requestReset, 'checked'
        elif timerStatus == 'off': 
            return '--', 'unchecked'
        else: 
            return 'Error', 'checked'
    except KeyError:
        return requestReset.objects.get(id=1).requestReset, 'checked'

# determine what to send to the view. if there is no cookie then just send the time and 
# 'checked' to make the button show up correctly. otherwise check what the cookie is and 
# send the appropriate values button checked/unchecked and what to display in the timer box
def getTimeToReset(request):
    try:
        timerStatus = request.COOKIES['timerStatus']
        # print('****** ' + str(timerStatus))
        if timerStatus == 'on':
            return int(request.COOKIES['resetTime']) - int(time.time()), 'checked'
        elif timerStatus == 'off':
            return '--', 'unchecked'
        else:
            return 'Error', 'checked'
    except KeyError:
        return int(request.COOKIES['resetTime']) - int(time.time()), 'checked'
