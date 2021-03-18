from django.urls import path, include
from . import views
from rest_framework import routers
# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'user', views.EmployeeViewSet)
router.register(r'product', views.ProductViewSet)
# router.register(r'customuser', views.CustomUserViewSet)
urlpatterns = [
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home', views.home),

    path('emp', views.emp),
    path('show/', views.show),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('deleteUser/<int:id>', views.destroy, name="deleteUser"),

    path('prd', views.prd),
    path('showp/',  views.showp),
    path('editp/<int:id>', views.editp),
    path('updatep/<int:id>', views.updatep),
    path('deletep/<int:id>', views.destroyp),

    path('user/', views.showdata, name='user'),

]