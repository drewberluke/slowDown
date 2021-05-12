from django.urls import path
from .views import indexPageView, addAndWait, adminPageView, resetRequestCount, changeThreshold, changeResetSetting, resetTimer, changeStudentWaitTime

urlpatterns = [
    path('', indexPageView, name='index'),
    path('Wait', addAndWait, name='addWait'),
    path('admin', adminPageView, name='admin'),
    path('admin/', adminPageView, name='admin'),
    path('resetRequestCount', resetRequestCount, name='resetRequestCount'),
    path('changeThreshold', changeThreshold, name='changeThreshold'),
    path('changeResetSetting', changeResetSetting, name='changeResetSetting'),
    path('resetTimer', resetTimer, name='resetTimer'),
    path('changeStudentWaitTime', changeStudentWaitTime, name='changeStudentWaitTime'),
]