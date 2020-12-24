from django.urls import path
from .views import indexPageView, addAndWait, adminPageView, resetRequestCount, changeThreshold

urlpatterns = [
    path('', indexPageView, name='index'),
    path('addWait', addAndWait, name='addWait'),
    path('admin', adminPageView, name='admin'),
    path('resetRequestCount', resetRequestCount, name='resetRequestCount'),
    path('changeThreshold', changeThreshold, name='changeThreshold'),
]