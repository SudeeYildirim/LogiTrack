from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Arac, Sofor, Sefer


def anasayfa(request):
    return redirect('/login/')


def kullanici_sofor_mu(request):
    return Sofor.objects.filter(user=request.user).exists()


@login_required
def dashboard(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    return render(request, 'dashboard.html', {
        'toplam_arac': Arac.objects.count(),
        'toplam_sofor': Sofor.objects.count(),
        'toplam_sefer': Sefer.objects.count(),
        'aktif_sefer': Sefer.objects.filter(durum="Devam Ediyor").count(),
        'son_seferler': Sefer.objects.all(),
    })


@login_required
def araclar(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    hata = ""

    if request.method == "POST":
        plaka = request.POST.get("plaka")
        marka = request.POST.get("marka")
        model = request.POST.get("model")
        durum = request.POST.get("durum")

        if not plaka or not marka or not model or not durum:
            hata = "Lütfen tüm araç bilgilerini doldurun."
        else:
            Arac.objects.create(
                plaka=plaka,
                marka=marka,
                model=model,
                durum=durum
            )

    return render(request, 'araclar.html', {
        'araclar': Arac.objects.all(),
        'hata': hata
    })


@login_required
def soforler(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    hata = ""

    if request.method == "POST":
        ad_soyad = request.POST.get("ad_soyad")
        telefon = request.POST.get("telefon")
        ehliyet_no = request.POST.get("ehliyet_no")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not ad_soyad or not telefon or not ehliyet_no or not username or not password:
            hata = "Lütfen tüm alanları doldurun."

        elif User.objects.filter(username=username).exists():
            hata = "Bu kullanıcı adı zaten kullanılıyor."

        else:
            user = User.objects.create_user(
                username=username,
                password=password
            )

            Sofor.objects.create(
                ad_soyad=ad_soyad,
                telefon=telefon,
                ehliyet_no=ehliyet_no,
                user=user
            )

    return render(request, 'soforler.html', {
        'soforler': Sofor.objects.all(),
        'hata': hata
    })


@login_required
def seferler(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    hata = ""

    if request.method == "POST":
        arac_id = request.POST.get("arac")
        sofor_id = request.POST.get("sofor")
        cikis_noktasi = request.POST.get("cikis_noktasi")
        varis_noktasi = request.POST.get("varis_noktasi")
        tahmini_sure = request.POST.get("tahmini_sure")

        if not arac_id or not sofor_id or not cikis_noktasi or not varis_noktasi or not tahmini_sure:
            hata = "Lütfen tüm sefer bilgilerini doldurun."
        else:
            arac = Arac.objects.get(id=arac_id)
            sofor = Sofor.objects.get(id=sofor_id)

            Sefer.objects.create(
                arac=arac,
                sofor=sofor,
                cikis_noktasi=cikis_noktasi,
                varis_noktasi=varis_noktasi,
                tahmini_sure=tahmini_sure,
                durum="Devam Ediyor"
            )

            arac.durum = "Meşgul"
            arac.save()

    return render(request, 'seferler.html', {
        'seferler': Sefer.objects.all(),
        'araclar': Arac.objects.all(),
        'soforler': Sofor.objects.all(),
        'hata': hata
    })


@login_required
def sefer_tamamla(request, sefer_id):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    sefer = Sefer.objects.get(id=sefer_id)
    sefer.durum = "Tamamlandı"
    sefer.save()

    sefer.arac.durum = "Müsait"
    sefer.arac.save()

    return redirect('/seferler/')


def login_sayfasi(request):
    hata = ""

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is not None:
            if Sofor.objects.filter(user=user).exists():
                hata = "Bu kullanıcı şoför hesabıdır. Lütfen Şoför Girişi ekranından giriş yapın."
            else:
                login(request, user)
                return redirect('/dashboard/')
        else:
            hata = "Kullanıcı adı veya şifre hatalı."

    return render(request, 'login.html', {'hata': hata})


@login_required
def cikis_yap(request):
    logout(request)
    return redirect('/login/')


@login_required
def sofor_cikis(request):
    logout(request)
    return redirect('/sofor-login/')


@login_required
def raporlar(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    toplam_arac = Arac.objects.count()
    musait_arac = Arac.objects.filter(durum="Müsait").count()
    mesgul_arac = Arac.objects.filter(durum="Meşgul").count()

    return render(request, 'raporlar.html', {
        'toplam_arac': toplam_arac,
        'musait_arac': musait_arac,
        'mesgul_arac': mesgul_arac,
        'toplam_sofor': Sofor.objects.count(),
        'toplam_sefer': Sefer.objects.count(),
        'aktif_sefer': Sefer.objects.filter(durum="Devam Ediyor").count(),
        'tamamlanan_sefer': Sefer.objects.filter(durum="Tamamlandı").count(),
    })


@login_required
def canli_takip(request):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    return render(request, 'canli_takip.html', {
        'seferler': Sefer.objects.all()
    })


def sofor_login(request):
    hata = ""

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user is not None:
            if Sofor.objects.filter(user=user).exists():
                login(request, user)
                return redirect('/sofor-panel/')
            else:
                hata = "Bu kullanıcı yönetici hesabıdır. Lütfen Yönetici Girişi ekranından giriş yapın."
        else:
            hata = "Kullanıcı adı veya şifre hatalı."

    return render(request, 'sofor_login.html', {'hata': hata})


@login_required
def sofor_panel(request):
    try:
        sofor = Sofor.objects.get(user=request.user)
    except Sofor.DoesNotExist:
        return redirect('/dashboard/')

    return render(request, 'sofor_panel.html', {
        'sofor': sofor,
        'seferler': Sefer.objects.filter(sofor=sofor)
    })
@login_required
def arac_sil(request, arac_id):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    arac = Arac.objects.get(id=arac_id)
    arac.delete()

    return redirect('/araclar/')
@login_required
def sofor_sil(request, sofor_id):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    sofor = Sofor.objects.get(id=sofor_id)

    if sofor.user:
        sofor.user.delete()

    sofor.delete()

    return redirect('/soforler/')

@login_required
def sefer_sil(request, sefer_id):
    if kullanici_sofor_mu(request):
        return redirect('/sofor-panel/')

    sefer = Sefer.objects.get(id=sefer_id)

    if sefer.durum == "Devam Ediyor":
        sefer.arac.durum = "Müsait"
        sefer.arac.save()

    sefer.delete()

    return redirect('/seferler/')