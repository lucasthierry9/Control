from django.contrib.auth import views as auth_views
from . import views 
from django.urls import path

app_name = 'usuarios'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

    path('perfil/', views.perfil, name="perfil"),
    path('editar_perfil/<int:id_usuario>/', views.editar_perfil, name="editar_perfil"),

    path('alterar_senha/', auth_views.PasswordChangeView.as_view(template_name='registration/alterar_senha.html', success_url='/accounts/alterar_senha/sucesso/'), name='alterar_senha'),
    path('alterar_senha/sucesso/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/alterar_senha_sucesso.html'), name='alterar_senha_sucesso'),
]
