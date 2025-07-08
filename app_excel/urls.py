from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentListCreateAPIView, StudentRetrieveUpdateDestroyAPIView


router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')

urlpatterns = [
    path('api/', include(router.urls)),

    path('upload/', views.upload_excel, name='upload_excel'),
    path('export/', views.export_all_documents_zip, name='export_all_documents_zip'),
    path('generate/<str:company_name>/', views.generate_contract_for_company, name='generate_contract_for_company'),
    path('export/one/', views.export_to_word, name='export_to_word'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('api/', include(router.urls)),
    path('api2/students/', StudentListCreateAPIView.as_view()),
    path('api2/students/<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view()),

    path('pay/', views.pay_view, name='pay_view'),
    path('click/result/', views.click_result, name='click_result'),
    path('click/prepare/', views.click_prepare, name='click_prepare'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),

    path('balance/', views.balance_view, name='balance'),

]
