from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('araclar/', views.araclar, name='araclar'),
    path('soforler/', views.soforler, name='soforler'),
    path('sofor-sil/<int:sofor_id>/', views.sofor_sil, name='sofor_sil'),
    path('seferler/', views.seferler, name='seferler'),
    path('sefer-sil/<int:sefer_id>/', views.sefer_sil, name='sefer_sil'),
    path('login/', views.login_sayfasi, name='login'),
    path(
    'sefer-tamamla/<int:sefer_id>/',
    views.sefer_tamamla,
    name='sefer_tamamla'
),
path('cikis/', views.cikis_yap, name='cikis'),
path('raporlar/', views.raporlar, name='raporlar'),
path('canli-takip/', views.canli_takip, name='canli_takip'),
path('sofor-login/', views.sofor_login, name='sofor_login'),
path('sofor-panel/', views.sofor_panel, name='sofor_panel'),
path('sofor-cikis/', views.sofor_cikis, name='sofor_cikis'),
path('arac-sil/<int:arac_id>/', views.arac_sil, name='arac_sil'),
]