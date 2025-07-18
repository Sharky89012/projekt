import os
import shutil
from pathlib import Path
from PIL import Image
import django
import sys

# Django Setup
sys.path.append('/Users/borisatanasov/Desktop/listcheck24_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestdeals.settings')
django.setup()

from products.models import Artikeln, Kategorie
from django.core.files import File
from django.utils import timezone

BASE_DIR = '/root/Desktop/produkte'
IMAGE_DEST = '/opt/listcheck24_project/media/artikeln'
os.makedirs(IMAGE_DEST, exist_ok=True)

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    asin = folder.strip()[:20]  # Sicherstellen, dass ASIN nicht länger als 20 Zeichen ist

    try:
        beschreibung = Path(os.path.join(folder_path, 'beschreibung.txt')).read_text().strip()[:10000]
        kategorie_name = Path(os.path.join(folder_path, 'kategorie.txt')).read_text().strip()[:100]
        preis = Path(os.path.join(folder_path, 'preis.txt')).read_text().strip()[:20]
        title = Path(os.path.join(folder_path, 'title.txt')).read_text().strip()[:255]
        saving_path = os.path.join(folder_path, 'savings.txt')
        saving = Path(saving_path).read_text().strip()[:20] if os.path.exists(saving_path) else ''
    except Exception as e:
        print(f"Fehler beim Lesen der Dateien in {folder}: {e}")
        continue

    # Bild finden
    img_path = None
    for ext in ['jpg', 'jpeg', 'png']:
        candidate = os.path.join(folder_path, f'main.{ext}')
        if os.path.exists(candidate):
            img_path = candidate
            break

    if not img_path:
        print(f"Kein Bild gefunden für {asin}")
        continue

    # Konvertieren zu .webp und speichern
    new_img_name = f"{asin}.webp"
    new_img_path = os.path.join(IMAGE_DEST, new_img_name)

    try:
        with Image.open(img_path) as img:
            img.save(new_img_path, format="WEBP")
    except Exception as e:
        print(f"Fehler beim Konvertieren des Bildes {img_path}: {e}")
        continue

    try:
        categorie, _ = Kategorie.objects.get_or_create(name=kategorie_name)

        try:
            artikel = Artikeln.objects.get(asin=asin)
            artikel.beschreibung = beschreibung
            artikel.preis = preis
            artikel.saving = saving
            artikel.title = title
            artikel.datum = timezone.now()
            artikel.kategorie = categorie

            # Altes Bild löschen, wenn der Bildname sich ändert
            if os.path.basename(artikel.picture.name) != new_img_name:
                old_image_path = artikel.picture.path
                with open(new_img_path, 'rb') as f:
                    artikel.picture.save(new_img_name, File(f), save=False)
                # Altes Bild löschen
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            artikel.save()
            print(f"Artikel {asin} wurde aktualisiert.")
        except Artikeln.DoesNotExist:
            with open(new_img_path, 'rb') as f:
                artikel = Artikeln.objects.create(
                    asin=asin,
                    beschreibung=beschreibung,
                    picture=File(f, name=new_img_name),
                    preis=preis,
                    saving=saving,
                    title=title,
                    datum=timezone.now(),
                    kategorie=categorie
                )
            print(f"Artikel {asin} wurde hinzugefügt.")

        if os.path.exists(new_img_path):
            os.remove(new_img_path)

    except Exception as e:
        print(f"Fehler beim Speichern des Artikels {asin}: {e}")
        continue

    try:
        shutil.rmtree(folder_path)
        print(f"Ordner {folder} wurde gelöscht.")
    except Exception as e:
        print(f"Fehler beim Löschen des Ordners {folder}: {e}")
