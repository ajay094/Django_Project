from django.contrib import admin
from django.urls import path
from foodzone import views
from django.contrib.auth import views as v

urlpatterns = [ 
	path("",views.home,name="hom"),
	path('admin/', admin.site.urls),
	path("admlg/",v.LoginView.as_view(template_name="html/adminlogin.html"),name="adlgn"),
	path("adminds/",views.admindashboard,name="addsh"),
	path("prod/",views.products,name="prodt"),
	path("addprod/",views.addproducts,name="addprodt"),
	path("deleprod/<int:pk>",views.deleteproducts,name='del'),
	path("updatprod/<int:pk>",views.updateproducts,name="update"),
	path("abt/",views.about,name="abot"),
	path("cnt/",views.contact,name="cont"),
	path("reg/",views.register,name="regist"),
	path("myord/",views.myorder,name="myorde"),
	path('adcrt/<int:pk>', views.addtocart,name='adtcrt'),	
	path("lg/",v.LoginView.as_view(template_name="html/login.html"),name="lgn"),
	path("log/",v.LogoutView.as_view(template_name="html/logout.html"),name="logt"),
]