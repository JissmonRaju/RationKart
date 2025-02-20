from tkinter.font import names

from django.urls import path
from AdminApp import views

urlpatterns = [
    path('Index/',views.index,name='Index'),



    path('View_User/',views.display_user,name='View_User'),
        path('Delete_User/<int:u_id>/',views.delete_user,name='Delete_User'),

    path('Add_Category/', views.add_category, name='Add_Category'),
    path('Save_Category/', views.save_category, name='Save_Category'),
    path('View_Category/', views.display_category, name='View_Category'),
    path('Edit_Category/<int:c_id>/', views.edit_category, name='Edit_Category'),
    path('Update_Category/<int:c_id>/', views.update_category, name='Update_Category'),
    path('Delete_Category/<int:c_id>/', views.delete_category, name='Delete_Category'),


    path('Add_Stock/',views.add_stock,name='Add_Stock'),
    path('Save_Stock/',views.save_stock,name='Save_Stock'),
    path('View_Stock/',views.display_stock,name='View_Stock'),
    path('Edit_Stocks/<int:s_id>/',views.edit_stock,name='Edit_Stocks'),
    path('Update_Stock/<int:s_id>/',views.update_stock,name='Update_Stock'),
    path('Delete_Stock/<int:s_id>/',views.delete_stock,name='Delete_Stock'),

    path('AdminLoginPage/',views.admin_login_page,name='AdminLoginPage'),
    path('AdminLogin/',views.admin_login,name='AdminLogin'),
    path('AdminLogOut/',views.admin_logout,name='AdminLogOut'),

    path('ViewMsg/',views.view_message,name='ViewMsg'),
    path('DeleteMsg/<int:m_id>/',views.delete_message,name='DeleteMsg'),
]