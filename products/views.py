from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Artikeln, Kategorie
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import re
from django.http import HttpResponse
from django.urls import reverse
from .models import Artikeln  # falls in anderer App → anpassen
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from datetime import date
from .models import EmailUser
from collections import defaultdict
from django.utils.decorators import method_decorator
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View






def datenschutz(request):
    return render(request, 'home/datenschutz.html')


def home_view(request):
    return render(request, "home/index.html")


def about_view(request):
    return render(request, "home/about.html")


def detail_page_view(request):
    return render(request, "home/detail-page.html")


def listing_page_view(request):
    return render(request, "home/listing-page.html")


def search_api_view(request):
    query = request.GET.get('search', '').strip()
    if not query:
        return JsonResponse({'results': []})

    words = query.split()
    q_obj = Q()
    for word in words:
        q_obj &= Q(title__icontains=word)

    artikeln = Artikeln.objects.filter(q_obj).distinct()

    data = [{
        'id': artikel.id,  # ⬅️ DAS IST WICHTIG!
        'asin': artikel.asin,
        'title': artikel.title,
        'beschreibung': artikel.beschreibung,
        'preis': artikel.preis,
        'saving': artikel.saving,
        'picture': artikel.picture.url if artikel.picture else '',
        'datum': artikel.datum.isoformat() if artikel.datum else ''
    } for artikel in artikeln]

    return JsonResponse({'results': data})

def search_page(request):
    return render(request, 'home/search.html')


def artikel_detail_page(request, artikel_id):
    artikel = get_object_or_404(Artikeln, id=artikel_id)
    return render(request, 'home/artikel_detail.html', {
        'artikel': artikel,
        'artikel_id': artikel_id
    })

# API-View für JSON-Daten
def artikel_detail_api(request, artikel_id):
    artikel = get_object_or_404(Artikeln, id=artikel_id)
    data = {
        'asin': artikel.asin,
        'title': artikel.title,
        'beschreibung': artikel.beschreibung,
        'preis': artikel.preis,
        'saving': artikel.saving,
        'picture': artikel.picture.url if artikel.picture else '',
        'datum': artikel.datum.isoformat() if artikel.datum else ''
    }
    return JsonResponse(data)

def kategorie_page(request, kategorie_name):
    return render(request, 'home/kategorie_page.html', {'kategorie_name': kategorie_name})

def kategorie_api_view(request, kategorie_name):
    kategorie = get_object_or_404(Kategorie, name__iexact=kategorie_name)
    
    # ⬅️ Wichtig: nach Datum absteigend sortieren
    artikeln = Artikeln.objects.filter(kategorie=kategorie).order_by('-datum')

    data = [{
        'id': artikel.id,
        'asin': artikel.asin,
        'title': artikel.title,
        'beschreibung': artikel.beschreibung,
        'preis': artikel.preis,
        'saving': artikel.saving,
        'picture': artikel.picture.url if artikel.picture else '',
        'datum': artikel.datum.isoformat() if artikel.datum else ''
    } for artikel in artikeln]

    return JsonResponse({'results': data})


def get_top_saving(request, position):
    try:
        position = int(position)
        if position < 1:
            return JsonResponse({'error': 'Position muss >= 1 sein'}, status=400)

        now = timezone.localtime()
        jahr, monat, tag = now.year, now.month, now.day

        artikel_queryset = Artikeln.objects.exclude(saving__isnull=True)

        artikel_liste = []
        for artikel in artikel_queryset:
            d = artikel.datum
            if d.year != jahr or d.month != monat or d.day != tag:
                continue  # Nicht heute → überspringen

            cleaned = artikel.saving.replace(" ", "").replace("%", "").replace("-", "")
            if cleaned.isdigit():
                prozent = int(cleaned)
                artikel_liste.append((prozent, artikel))

        artikel_liste.sort(key=lambda x: x[0], reverse=True)

        if len(artikel_liste) >= position:
            artikel = artikel_liste[position - 1][1]
            return JsonResponse({
                'id': artikel.id,
                'asin': artikel.asin,
                'title': artikel.title,
                'beschreibung': artikel.beschreibung,
                'preis': artikel.preis,
                'saving': artikel.saving,
                'picture': artikel.picture.url if artikel.picture else '',
                'datum': artikel.datum.isoformat()
            })
        else:
            return JsonResponse({'error': 'Nicht genug Artikel mit Ersparnis vorhanden'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    



def all_sorted_savings_view(request):
    try:
        limit = int(request.GET.get("limit", 50))
        offset = int(request.GET.get("offset", 0))

        now = timezone.localtime()
        jahr, monat, tag = now.year, now.month, now.day

        artikel_queryset = Artikeln.objects.exclude(saving__isnull=True)

        artikel_liste = []

        for artikel in artikel_queryset:
            d = artikel.datum
            if d.year != jahr or d.month != monat or d.day != tag:
                continue  # ⛔️ Nur Artikel von heute

            cleaned = artikel.saving.replace(" ", "").replace("%", "").replace("-", "")
            if cleaned.isdigit():
                prozent = int(cleaned)
                artikel_liste.append((prozent, artikel))

        # 🔁 Sortieren nach Ersparnis (absteigend)
        artikel_liste.sort(key=lambda x: x[0], reverse=True)

        # 🔢 Maximal 500 Artikel
        artikel_liste = artikel_liste[:500]

        paginated = artikel_liste[offset:offset+limit]

        results = []
        for _, artikel in paginated:
            results.append({
                'id': artikel.id,
                'asin': artikel.asin,
                'title': artikel.title,
                'beschreibung': artikel.beschreibung,
                'preis': artikel.preis,
                'saving': artikel.saving,
                'picture': artikel.picture.url if artikel.picture else '',
                'datum': artikel.datum.isoformat()
            })

        return JsonResponse({
            'results': results,
            'total': min(len(artikel_liste), 500),
            'offset': offset,
            'limit': limit
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def all_produkt24_view(request):
    return render(request, 'home/all_produkt24.html')


def api_all_produkte_sorted_by_saving(request):
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))

    def extract_saving(s):
        match = re.search(r'(\d+)', s or '')
        return int(match.group(1)) if match else 0

    # Alle Artikel holen, auch alte
    artikel_qs = Artikeln.objects.all()
    
    # Sortiere nach Prozent-Rabatt ↓, dann Datum ↓
    artikel_liste = sorted(
        artikel_qs,
        key=lambda a: (extract_saving(a.saving), a.datum),
        reverse=True
    )

    # Pagination
    paginated = artikel_liste[offset:offset + limit]

    result = []
    for artikel in paginated:
        result.append({
            'id': artikel.id,
            'asin': artikel.asin,
            'title': artikel.title,
            'beschreibung': artikel.beschreibung,
            'preis': artikel.preis,
            'saving': artikel.saving,
            'picture': artikel.picture.url if artikel.picture else '',
            'datum': artikel.datum.strftime('%Y-%m-%d')
        })

    return JsonResponse({"results": result})


def sitemap_view(request):
    urlset = Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    })

    artikel_qs = Artikeln.objects.all().order_by('-datum')

    for artikel in artikel_qs:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = request.build_absolute_uri(f"/artikel/{artikel.id}/")

        lastmod = SubElement(url, 'lastmod')
        lastmod.text = artikel.datum.strftime('%Y-%m-%d')

        # Dynamische Priorität
        tage_alt = (date.today() - artikel.datum.date()).days
        if tage_alt <= 0:
            prio = '1.0'
        elif tage_alt == 1:
            prio = '0.9'
        elif tage_alt <= 3:
            prio = '0.8'
        elif tage_alt <= 7:
            prio = '0.7'
        elif tage_alt <= 14:
            prio = '0.6'
        else:
            prio = '0.5'

        SubElement(url, 'changefreq').text = 'weekly'
        SubElement(url, 'priority').text = prio

    raw_xml = tostring(urlset, 'utf-8')
    pretty_xml = parseString(raw_xml).toprettyxml(indent="  ")
    return HttpResponse(pretty_xml, content_type="application/xml")


def subscribe_email(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email or "@" not in email:
            return JsonResponse({"success": False, "message": "Ungültige E-Mail-Adresse."})

        if EmailUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Diese E-Mail ist bereits registriert."})

        EmailUser.objects.create(email=email)
        return JsonResponse({"success": True, "message": "Danke für deine Anmeldung!"})

    return JsonResponse({"success": False, "message": "Nur POST erlaubt."})





API_PASSWORD = os.getenv('API_PASSWORD', 'dein_sicheres_passwort')  # Passwort aus .env oder direkt hier

class ArtikelBeschreibungAPI(View):
    def dispatch(self, request, *args, **kwargs):
        password = request.headers.get('Authorization')
        if password and password.startswith('Token '):
            password = password[6:]
        if password != API_PASSWORD:
            return JsonResponse({'error': 'Unauthorized. Bitte Passwort mitsenden!'}, status=401)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, artikel_id):
        try:
            artikel = Artikeln.objects.get(id=artikel_id)
            data = json.loads(request.body.decode('utf-8'))
            neue_beschreibung = data.get('beschreibung')
            if neue_beschreibung:
                artikel.beschreibung = neue_beschreibung
                artikel.save(update_fields=['beschreibung'])  # Nur Beschreibung speichern
                return JsonResponse({
                    'status': 'Beschreibung aktualisiert',
                    'beschreibung': artikel.beschreibung,
                })
            else:
                return JsonResponse({'error': 'Beschreibung fehlt im Request'}, status=400)
        except Artikeln.DoesNotExist:
            return JsonResponse({'error': 'Artikel nicht gefunden'}, status=404)

    def get(self, request, artikel_id):
        try:
            artikel = Artikeln.objects.get(id=artikel_id)
            return JsonResponse({
                'beschreibung': artikel.beschreibung,
            })
        except Artikeln.DoesNotExist:
            return JsonResponse({'error': 'Artikel nicht gefunden'}, status=404)
        




