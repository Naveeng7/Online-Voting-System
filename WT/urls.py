"""WT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as u_views
from django.contrib.auth import views as a_views
from django.conf import settings
from django.conf.urls.static import static
from voting import views as v_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('register', u_views.register, name='register'),
    path('login/', a_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', a_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile', u_views.profile, name='profile'),
    path('voting', v_views.voting, name='voting'),
    path('addndel', v_views.mpos, name='addndel'),
    path('cadd', v_views.cadd, name='addcand'),
    path('cdel', v_views.cdel, name='delcand'),
    path('pollres', v_views.cres, name='rescand'),
    path('changepassword', u_views.ChangePassword, name='chngpass')
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)