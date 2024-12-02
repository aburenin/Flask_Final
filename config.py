import hashlib
import os
from datetime import timedelta

from dotenv import find_dotenv, load_dotenv

SQLALCHEMY_DATABASE_URI = 'sqlite:///fotos-baby.db'
load_dotenv(find_dotenv())

# Настраиваем конфигурацию сессии
# app.config['SESSION_TYPE'] = 'redis'  # Указываем, что будем использовать Redis
SESSION_PERMANENT = True  # Сессия не будет постоянной
SESSION_USE_SIGNER = True  # Будем подписывать сессию
TEMPLATES_AUTO_RELOAD = True  # Перезапуск Tempates
# SESSION_REDIS'] = Redis(host='localhost', port=6379)  # Указываем настройки сервера Redis
SECRET_KEY = f'{hashlib.sha256(os.getenv("ADMIN_KEY").encode())}'  # замените на ваш секретный ключ
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)  # сессия будет жить сутки (days)
SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = True

# CACHE_TYPE = 'redis'
# CACHE_REDIS_HOST = 'localhost'
# CACHE_REDIS_PORT = 6379
# CACHE_REDIS_DB = 0
# CACHE_REDIS_URL = 'redis://localhost:6379/0'


# Mail configuration
MAIL_SERVER = 'mail.your-server.de'
MAIL_PORT = 465
MAIL_USERNAME = 'info@fotos-baby.de'
MAIL_PASSWORD = 'cashMONEY15288'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

REMEMBER_COOKIE_DURATION = timedelta(days=1)

pakets = [
    ('- MINI -', '349,-',
     """<i class="fa-solid fa-person-half-dress"></i>  1-2 Kulissen | <i class="fa-solid fa-clock-rotate-left"></i>  Fotoshooting ca. 1.5 Std. | <i class="fa-solid fa-images"></i>  8 bearbeitete und voll retuschierte Fotos als Download | 
     <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- STANDART -', '449,-',
     """<i class="fa-solid fa-person-half-dress"></i>  2-3 Kulissen | <i class="fa-solid fa-clock-rotate-left"></i>  Fotoshooting ca. 2 Std. | <i class="fa-solid fa-people-group"></i>  Familien- und Geschwisterfoto inkl. | 
     <i class="fa-solid fa-images"></i>  15 bearbeitete und voll retuschierte Fotos als Download | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- MAXI -', '549,-',
     """<i class="fa-solid fa-person-half-dress"></i>  3-4-5 Kulissen | <i class="fa-solid fa-people-group"></i>  Familien- und Geschwisterfoto inkl. | <i class="fa-solid fa-images"></i>  15 bearbeitete und voll retuschierte Fotos als Download | 
      <i class="fa-brands fa-usb"></i>  Alle Fotos vom Fotoshooting auf USB | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- BABYFOTOS (5-24 MONATE) MINI -', '349,-',
     """<i class="fa-solid fa-person-half-dress"></i>  2 Kulissen | <i class="fa-solid fa-images"></i>  8 bearbeitete und voll retuschierte Fotos als Download | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- BABYFOTOS (5-24 MONATE) Standart -', '449,-',
     """<i class="fa-solid fa-person-half-dress"></i>  3 Kulissen + Familien- und Geschwisterfoto | <i class="fa-solid fa-images"></i>  15 bearbeitete und voll retuschierte Fotos als Download | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- BABYFOTOS (5-24 MONATE) MAXI -', '549,-',
     """<i class="fa-solid fa-person-half-dress"></i>  4 Kulissen | <i class="fa-solid fa-people-group"></i>  Familien- und Geschwisterfoto inkl. | <i class="fa-solid fa-images"></i>  20 bearbeitete und voll retuschierte Fotos als Download | 
      <i class="fa-brands fa-usb"></i>  Alle Fotos vom Fotoshooting auf USB | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder"""),

    ('- Babybauch -', '299,-',
     """<i class="fa-solid fa-person-half-dress"></i>  max. 5 Kulissen | <i class="fa-solid fa-people-group"></i>  Familien- und Geschwisterfoto inkl. | <i class="fa-solid fa-images"></i>  15 bearbeitete und voll retuschierte Fotos als Download | 
     <i class="fa-brands fa-usb"></i>  Alle Fotos vom Fotoshooting auf USB | <i class="fa-solid fa-key"></i>  Passwortgeschützte Online Galerie zur Auswahl der Bilder""")

]

qa_list = [
    (
        '1',
        "In welchem Alter ist es am besten, ein Neugeborenen-Fotoshooting durchzuführen?",
        "Das ideale Alter für ein Neugeborenen-Fotoshooting liegt zwischen 5 und 14 Tagen nach der Geburt. In diesem Alter schlafen Babys noch viel und tief, sodass sie leichter in verschiedene Posen gebracht werden können. Außerdem haben sie in diesem Alter noch die typischen Neugeborenen-Falten und -Merkmale, die auf Fotos besonders süß aussehen."
    ),
    (
        '2',
        "Was, wenn mein Baby während des Shootings unruhig ist oder weint?",
        "Keine Sorge, es ist ganz normal, dass Babys während eines Shootings manchmal unruhig sind oder weinen. Ich habe viel Erfahrung im Umgang mit Neugeborenen und werde alles tun, um Ihr Baby zu beruhigen und sicherzustellen, dass das Shooting so reibungslos wie möglich verläuft. Das Wichtigste ist, dass Sie sich entspannen und dem Prozess vertrauen."
    ),
    (
        '3',
        "Was soll ich für das Shooting anziehen?",
        "Es ist am besten, neutrale und unauffällige Kleidung zu wählen, die nicht von Ihrem Baby ablenkt. Pastellfarben oder Erdtöne funktionieren gut. Vermeiden Sie Muster oder Logos, die das Bild überladen könnten. Es ist auch eine gute Idee, mehrere Outfits zur Auswahl zu haben, falls eines schmutzig wird."
    ),
    (
        '4',
        "Kann ich Geschwister oder Haustiere in das Shooting einbeziehen?",
        "Ja, Geschwister und Haustiere können auf jeden Fall Teil des Shootings sein! Es ist eine großartige Möglichkeit, die besondere Beziehung zwischen Ihrem Neugeborenen und seinen älteren Geschwistern oder Haustieren festzuhalten. Ich werde sicherstellen, dass alle Beteiligten sicher und bequem sind und dass die Fotos authentisch und schön aussehen."
    ),
    (
        '5',
        "Wie lange dauert das Shooting?",
        "Ein Neugeborenen-Fotoshooting kann zwischen 1 und 3 Stunden dauern, je nachdem, wie oft Ihr Baby gefüttert werden muss oder wie unruhig es ist. Es ist wichtig, sich viel Zeit zu nehmen, um sicherzustellen, dass das Baby entspannt ist und die besten Fotos gemacht werden können."
    ),
    (
        '6',
        "Was, wenn ich das Shooting absagen oder verschieben muss?",
        "Ich verstehe, dass das Leben mit einem Neugeborenen unvorhersehbar sein kann, und bin flexibel, wenn es darum geht, Shootings zu verschieben. Wenn Sie das Shooting absagen müssen, geben Sie mir bitte so viel Vorlaufzeit wie möglich, damit ich den Termin für jemand anderen freigeben kann."
    ),
    (
        '7',
        "Wann erhalte ich die Fotos?",
        "Die bearbeiteten Fotos werden Ihnen innerhalb von 4-5 Wochen in einer Online-Galerie zur Verfügung gestellt, von der aus Sie sie herunterladen können."
    ),
    (
        '8',
        "Wie viele Fotos erhalte ich?",
        "Die genaue Anzahl der Fotos hängt vom gebuchten Paket und der Dauer des Shootings ab. Im Durchschnitt können Sie jedoch zwischen 15 und 30 bearbeitete Fotos erwarten."
    ),
    (
        '9',
        "Kann ich die unbearbeiteten Fotos sehen?",
        "Ich zeige normalerweise nur die bearbeiteten Fotos, da diese das beste Endergebnis darstellen. Wenn Sie jedoch einen speziellen Wunsch haben, lassen Sie es mich wissen, und ich werde sehen, was ich tun kann."
    ),
    (
        '10',
        "Bieten Sie auch Alben oder Drucke an?",
        "Ja, ich biete sowohl Alben als auch Drucke in verschiedenen Größen und Qualitäten an. Die Preise variieren je nach Produkt und Größe."
    ),
    (
        '11',
        "Kann ich die Fotos in sozialen Medien teilen?",
        "Ja, Sie können die Fotos gerne in sozialen Medien teilen! Ich bitte Sie nur, mich als Fotografen zu markieren oder zu erwähnen, damit auch andere meine Arbeit sehen können."
    ),
    (
        '12',
        "Was, wenn ich mit den Fotos nicht zufrieden bin?",
        "Es ist mir sehr wichtig, dass Sie mit den Fotos zufrieden sind. Wenn Sie Bedenken oder Wünsche haben, lassen Sie es mich wissen, und ich werde mein Bestes tun, um sicherzustellen, dass Sie glücklich sind."
    ),
    (
        '13',
        "Kann ich Sie für andere Arten von Shootings buchen?",
        "Ja, ich biete auch andere Arten von Shootings an, wie z.B. Familien-, Schwangerschafts- oder Einzelaufnahmen. Kontaktieren Sie mich für weitere Informationen und Preise."
    )
]

alt_tags_newborn = [
    "Neugeborenen Fotoshooting in Zürich", "Neugeborenenfotografie Winterthur",
    "Babyfotografie für Neugeborene in Schaffhausen", "Professionelle Neugeborenenbilder am Bodensee",
    "Süße Neugeborenenfotos in Thurgau", "Neugeborenenbilder Schweiz", "Natürliche Babyfotos Zürich",
    "Einzigartige Neugeborenenfotos in Winterthur", "Babyfotostudio Schaffhausen",
    "Neugeborenenporträts in Thurgau", "Familienfotos mit Neugeborenen am Bodensee",
    "Neugeborenenfotograf Zürich Umgebung", "Outdoor Babyfotografie Schweiz",
    "Neugeborenen Fotografie am Bodensee", "Künstlerische Neugeborenenbilder in Winterthur",
    "Babyfotografie zu Hause Schaffhausen", "Unvergessliche Neugeborenenfotos in Thurgau",
    "Spezialisierte Babyfotografie Schweiz", "Romantische Neugeborenenporträts Zürich",
    "Neugeborenen Fotoshooting Thurgau", "Studiofotografie für Neugeborene in Winterthur",
    "Lustige Neugeborenenbilder Schaffhausen", "Professionelle Babyfotos Zürich",
    "Schöne Neugeborenenbilder am Bodensee", "Neugeborenen Porträtfotografie Winterthur",
    "Babyfotografie für Familien in Thurgau", "Fotostudio für Neugeborene Zürich",
    "Natürliche Babyfotos Winterthur", "Süße Neugeborenenporträts Schaffhausen",
    "Kreative Neugeborenenbilder Bodensee", "Familienfotografie mit Babys in Thurgau",
    "Künstlerische Neugeborenenfotos Zürich", "Babyfotos in der Schweiz",
    "Einzigartige Babybilder Schaffhausen", "Neugeborenen Fotografie für Eltern am Bodensee",
    "Outdoor Fotoshooting für Babys in Winterthur", "Studio Babyfotografie Thurgau",
    "Neugeborenenporträts in Zürich Umgebung", "Lustige Familienfotos mit Neugeborenen",
    "Neugeborenenfotografie Schweiz", "Spezialisierte Neugeborenenbilder am Bodensee",
    "Professionelle Neugeborenenfotos Winterthur", "Schöne Babyfotos Schaffhausen",
    "Neugeborenenporträts in Thurgau", "Einzigartige Neugeborenenbilder Zürich",
    "Babyfotografie für Familien am Bodensee", "Fotostudio für Neugeborene in Winterthur",
    "Natürliche Babyfotos Schaffhausen", "Süße Neugeborenenfotos Thurgau",
    "Künstlerische Neugeborenenporträts Zürich", "Familienfotos mit Babys in der Schweiz",
    "Babyfotografie für Eltern in Winterthur", "Neugeborenenfotografie am Bodensee",
    "Romantische Neugeborenenbilder Schaffhausen", "Studiofotografie für Babys in Thurgau",
    "Neugeborenenporträts Zürich Umgebung", "Professionelle Babybilder Winterthur",
    "Einzigartige Familienfotos am Bodensee", "Neugeborenenporträts in Thurgau",
    "Kreative Babybilder Zürich", "Süße Neugeborenenfotos Winterthur", "Babyfotograf Schaffhausen",
    "Fotostudio für Neugeborene am Bodensee", "Natürliche Neugeborenenbilder Zürich",
    "Einzigartige Babyfotos Winterthur", "Familienfotografie mit Babys Thurgau",
    "Künstlerische Neugeborenenbilder am Bodensee", "Studiofotografie für Neugeborene Winterthur",
    "Spezialisierte Babyfotografie Schaffhausen", "Babyfotos am Bodensee",
    "Neugeborenenporträts Zürich Umgebung", "Natürliche Babybilder Thurgau",
    "Professionelle Familienfotos Winterthur", "Babyfotografie für Eltern Schaffhausen",
    "Outdoor Neugeborenenfotografie am Bodensee", "Einzigartige Babybilder Winterthur",
    "Neugeborenenporträts Zürich", "Kreative Babybilder Thurgau", "Schöne Babyfotos Winterthur",
    "Babyfotografie für Neugeborene am Bodensee", "Studiofotografie für Babys Schaffhausen",
    "Natürliche Familienfotos Zürich", "Neugeborenenfotografie Winterthur",
    "Einzigartige Neugeborenenbilder am Bodensee", "Spezialisierte Babyfotografie Thurgau",
    "Babyfotos für Eltern Zürich", "Studiofotografie für Neugeborene am Bodensee",
    "Schöne Babybilder Winterthur", "Babyfotografie für Familien in Schaffhausen",
    "Familienfotografie mit Neugeborenen Zürich", "Romantische Babyfotos Winterthur",
    "Einzigartige Neugeborenenbilder am Bodensee", "Studiofotografie für Babys Thurgau",
    "Kreative Neugeborenenporträts Zürich", "Professionelle Familienfotos Winterthur",
    "Babyfotografie für Eltern Schaffhausen", "Natürliche Neugeborenenbilder Thurgau",
    "Einzigartige Babybilder Zürich", "Babyfotograf Winterthur",
    "Spezialisierte Neugeborenenfotografie Schaffhausen", "Babybilder am Bodensee",
    "Studiofotografie für Babys Zürich Umgebung", "Neugeborenenfotografie Thurgau",
    "Romantische Babybilder Winterthur", "Studiofotografie für Neugeborene in Schaffhausen",
    "Süße Babybilder Thurgau", "Babyfotografie für Familien am Bodensee",
    "Natürliche Neugeborenenbilder Zürich", "Einzigartige Babybilder Winterthur",
    "Kreative Familienfotos mit Neugeborenen Schaffhausen", "Babyfotos Zürich Umgebung",
    "Romantische Neugeborenenporträts Thurgau", "Einzigartige Babybilder am Bodensee",
    "Familienfotos mit Babys in Thurgau", "Babyfotograf Zürich Umgebung",
    "Kreative Babyfotos Winterthur", "Spezialisierte Familienfotografie Bodensee",
    "Neugeborenenfotografie Zürich Umgebung", "Einzigartige Neugeborenenbilder Winterthur",
    "Professionelle Babyfotos in Schaffhausen", "Studiofotografie für Babys in Zürich",
    "Outdoor Babyfotografie in Thurgau", "Lustige Neugeborenenporträts Winterthur",
    "Babybilder mit Familien in Schaffhausen", "Natürliche Babybilder Bodensee",
    "Romantische Familienfotos in Zürich", "Neugeborenenporträts Winterthur",
    "Süße Babybilder Thurgau", "Künstlerische Babyfotografie Zürich", "Babyfotoshooting Bodensee",
    "Neugeborenenfotografie Winterthur", "Kreative Familienfotos in Schaffhausen",
    "Spezialisierte Neugeborenenfotografie Zürich", "Professionelle Familienbilder Bodensee",
    "Natürliche Babyfotos Thurgau", "Studiofotografie für Neugeborene Zürich",
    "Einzigartige Babybilder Winterthur", "Lustige Babyfotos Schaffhausen",
    "Babyfotograf für Familien in Zürich", "Süße Neugeborenenfotos Winterthur",
    "Einzigartige Neugeborenenbilder Bodensee", "Professionelle Babybilder Zürich",
    "Romantische Familienfotos Winterthur", "Neugeborenenporträts Schaffhausen",
    "Künstlerische Babyfotografie Thurgau", "Babyfotograf Bodensee Umgebung",
    "Spezialisierte Familienfotografie Winterthur", "Babyfotos mit Eltern in Zürich",
    "Studiofotografie für Babys Schaffhausen", "Kreative Neugeborenenbilder Winterthur",
    "Einzigartige Familienfotos Zürich Umgebung", "Natürliche Babyfotos Bodensee",
    "Lustige Neugeborenenbilder Winterthur", "Familienfotograf Thurgau",
    "Süße Babyfotos Zürich", "Neugeborenenporträts Bodensee",
    "Studiofotografie für Babys Winterthur", "Professionelle Neugeborenenbilder Schaffhausen",
    "Babybilder für Familien in Zürich", "Romantische Babybilder Bodensee",
    "Künstlerische Neugeborenenbilder Winterthur", "Familienfotos mit Babys Thurgau",
    "Natürliche Babyfotografie Bodensee", "Einzigartige Familienbilder Winterthur",
    "Studiofotografie für Babys Schaffhausen", "Süße Neugeborenenporträts Zürich",
    "Babybilder für Eltern Winterthur", "Familienfotos am Bodensee"
]


alt_tags_babybauch = [
    "Babybauch Fotoshooting in Schaffhausen",
    "Schwangerschaftsfotografie Winterthur",
    "Babybauchfotos Zürich",
    "Professionelle Schwangerschaftsfotos am Bodensee",
    "Romantische Babybauchbilder in Thurgau",
    "Kreative Schwangerschaftsfotos Zürich Umgebung",
    "Babybauchfotograf Winterthur",
    "Studio Babybauchfotos in Schaffhausen",
    "Outdoor Schwangerschaftsfotografie am Bodensee",
    "Familienfotos mit Babybauch in Thurgau",
    "Künstlerische Schwangerschaftsbilder in Zürich",
    "Babybauch und Familienfotografie Winterthur",
    "Einzigartige Schwangerschaftsfotos Bodensee",
    "Romantische Babybauchbilder in Schaffhausen",
    "Natürliche Schwangerschaftsbilder in Zürich",
    "Babybauchporträts am Bodensee",
    "Professionelle Schwangerschaftsfotos in Winterthur",
    "Studiofotografie für Schwangere Thurgau",
    "Unvergessliche Babybauchfotos Zürich",
    "Babybauchfotografie Schaffhausen",
    "Outdoor Babybauchfotos am Bodensee",
    "Kreative Babybauchbilder Winterthur",
    "Familienfotografie mit Schwangerschaft Zürich",
    "Spezialisierte Schwangerschaftsfotografie in Thurgau",
    "Romantische Babybauchporträts Schaffhausen",
    "Babybauchbilder Zürich Umgebung",
    "Studio Babybauchfotografie Winterthur",
    "Lustige Schwangerschaftsfotos Bodensee",
    "Professionelle Babybauchporträts Thurgau",
    "Natürliche Schwangerschaftsfotografie Schaffhausen",
    "Künstlerische Schwangerschaftsbilder Bodensee",
    "Babybauchbilder für Familien in Zürich",
    "Outdoor Schwangerschaftsporträts Winterthur",
    "Babybauchfotografie mit Partner am Bodensee",
    "Romantische Schwangerschaftsbilder Schaffhausen",
    "Studiofotografie für Babybauch in Thurgau",
    "Babybauchfotoshooting Zürich",
    "Natürliche Babybauchbilder Winterthur",
    "Familienfotos mit Schwangeren am Bodensee",
    "Unvergessliche Schwangerschaftsbilder in Schaffhausen",
    "Kreative Babybauchfotografie Zürich",
    "Babybauchporträts Bodensee Umgebung",
    "Professionelle Schwangerschaftsfotos Winterthur",
    "Studiofotografie für Schwangere in Schaffhausen",
    "Künstlerische Babybauchbilder Thurgau",
    "Natürliche Schwangerschaftsfotografie Zürich",
    "Einzigartige Babybauchporträts Winterthur",
    "Familienfotografie mit Schwangerschaft am Bodensee",
    "Lustige Babybauchbilder Schaffhausen",
    "Outdoor Schwangerschaftsfotografie Thurgau",
    "Romantische Babybauchfotos Zürich Umgebung",
    "Studio Babybauchfotografie Winterthur",
    "Professionelle Schwangerschaftsbilder am Bodensee",
    "Natürliche Babybauchfotos in Schaffhausen",
    "Kreative Schwangerschaftsporträts in Zürich",
    "Babybauchfotograf Winterthur Umgebung",
    "Spezialisierte Schwangerschaftsfotografie Thurgau",
    "Familienfotos mit Babybauch Bodensee",
    "Einzigartige Schwangerschaftsbilder in Zürich",
    "Romantische Babybauchporträts Winterthur",
    "Studio Babybauchfotografie in Thurgau",
    "Künstlerische Schwangerschaftsbilder Schaffhausen",
    "Natürliche Babybauchbilder Bodensee Umgebung",
    "Lustige Familienfotos mit Babybauch Zürich",
    "Outdoor Schwangerschaftsbilder Winterthur",
    "Professionelle Babybauchfotos Thurgau",
    "Kreative Schwangerschaftsfotografie Schaffhausen",
    "Romantische Schwangerschaftsporträts Bodensee",
    "Studiofotografie für Schwangere Winterthur",
    "Unvergessliche Babybauchbilder Zürich",
    "Natürliche Babybauchfotos am Bodensee",
    "Künstlerische Schwangerschaftsfotografie Schaffhausen",
    "Spezialisierte Babybauchporträts Thurgau",
    "Familienfotografie mit Schwangeren Zürich",
    "Studio Babybauchfotos Bodensee Umgebung",
    "Lustige Schwangerschaftsfotos in Winterthur",
    "Professionelle Schwangerschaftsbilder in Schaffhausen",
    "Natürliche Babybauchporträts Zürich",
    "Einzigartige Babybauchbilder Winterthur",
    "Romantische Schwangerschaftsfotografie am Bodensee",
    "Studiofotografie für Babybauch in Thurgau",
    "Outdoor Babybauchbilder Schaffhausen",
    "Familienfotos mit Schwangeren Winterthur",
    "Kreative Schwangerschaftsbilder Zürich",
    "Professionelle Babybauchfotos Bodensee Umgebung",
    "Lustige Babybauchporträts Thurgau",
    "Natürliche Schwangerschaftsfotografie Winterthur",
    "Künstlerische Babybauchbilder Zürich",
    "Babybauchfotografie für Familien am Bodensee",
    "Studiofotografie für Schwangere Schaffhausen",
    "Romantische Schwangerschaftsbilder Winterthur",
    "Professionelle Babybauchporträts Zürich Umgebung",
    "Einzigartige Schwangerschaftsbilder Bodensee",
    "Familienfotografie mit Babybauch in Thurgau",
    "Natürliche Babybauchbilder Schaffhausen",
    "Künstlerische Schwangerschaftsbilder Bodensee",
    "Spezialisierte Babybauchfotografie Zürich",
    "Studiofotografie für Schwangere Winterthur",
    "Lustige Babybauchfotos in Thurgau",
    "Romantische Schwangerschaftsfotografie Bodensee Umgebung",
    "Einzigartige Babybauchbilder Zürich",
    "Outdoor Schwangerschaftsbilder Winterthur",
    "Professionelle Familienfotos mit Babybauch Schaffhausen",
    "Kreative Schwangerschaftsporträts Bodensee",
    "Natürliche Babybauchbilder Winterthur",
    "Studio Babybauchfotografie Zürich Umgebung",
    "Lustige Schwangerschaftsbilder Bodensee",
    "Romantische Familienfotos mit Schwangeren Thurgau",
    "Babybauchfotografie in Schaffhausen",
    "Einzigartige Schwangerschaftsbilder Winterthur",
    "Professionelle Schwangerschaftsfotografie Zürich",
    "Natürliche Babybauchbilder Bodensee Umgebung",
    "Studiofotografie für Babybauch Winterthur",
    "Kreative Schwangerschaftsbilder Thurgau",
    "Romantische Babybauchbilder Zürich",
    "Familienfotos mit Schwangeren Bodensee",
    "Lustige Babybauchfotos Schaffhausen",
    "Natürliche Schwangerschaftsfotos Zürich Umgebung",
    "Professionelle Schwangerschaftsporträts Winterthur",
    "Babybauchbilder für Eltern in Bodensee",
    "Einzigartige Schwangerschaftsbilder Thurgau",
    "Künstlerische Babybauchfotografie Zürich",
    "Familienfotografie mit Schwangeren Winterthur",
    "Natürliche Babybauchporträts Schaffhausen",
    "Lustige Schwangerschaftsbilder Bodensee",
    "Professionelle Schwangerschaftsbilder Zürich",
    "Kreative Babybauchfotografie Winterthur",
    "Romantische Babybauchporträts Thurgau",
    "Einzigartige Familienfotos mit Schwangerschaft Bodensee",
    "Natürliche Schwangerschaftsfotos Winterthur",
    "Studio Babybauchbilder Zürich",
    "Lustige Schwangerschaftsbilder Schaffhausen",
    "Künstlerische Babybauchbilder Winterthur",
    "Einzigartige Babybauchbilder Bodensee",
    "Professionelle Schwangerschaftsbilder Thurgau",
    "Romantische Familienfotos mit Schwangeren Zürich",
    "Outdoor Schwangerschaftsbilder Winterthur",
    "Natürliche Schwangerschaftsporträts Bodensee",
    "Studiofotografie für Babybauch Thurgau",
    "Kreative Babybauchporträts Winterthur",
    "Lustige Schwangerschaftsbilder Zürich Umgebung",
    "Natürliche Babybauchbilder Bodensee",
    "Künstlerische Schwangerschaftsbilder Thurgau",
    "Einzigartige Schwangerschaftsporträts Winterthur",
    "Romantische Babybauchfotos Zürich Umgebung",
]

alt_tags_baby = ["Baby Fotoshooting in Zürich", "Kinderfotografie Winterthur", "Babyfotografie in Schaffhausen",
                 "Professionelle Babyfotos am Bodensee", "Süße Babybilder in Thurgau",
                 "Natürliche Kinderfotos in Zürich", "Einzigartige Babyfotografie Winterthur",
                 "Künstlerische Babybilder Schaffhausen", "Outdoor Baby Fotos am Bodensee",
                 "Familienfotos mit Babys in Thurgau", "Studio Babyfotografie in Zürich",
                 "Lustige Babyfotos Winterthur", "Professionelle Babybilder Schaffhausen",
                 "Spezialisierte Babyfotografie Bodensee", "Einzigartige Familienfotos mit Babys Thurgau",
                 "Romantische Babybilder Zürich Umgebung", "Natürliche Babyfotos Winterthur",
                 "Kreative Kinderfotografie Schaffhausen", "Professionelle Familienfotos am Bodensee",
                 "Studiofotografie für Babys in Thurgau", "Outdoor Babyfotografie Zürich",
                 "Lustige Kinderfotos Winterthur", "Natürliche Babybilder Schaffhausen",
                 "Romantische Familienfotos mit Babys Bodensee", "Einzigartige Kinderfotografie Thurgau",
                 "Künstlerische Babyfotos Zürich", "Professionelle Babybilder Winterthur",
                 "Lustige Babyfotografie Schaffhausen", "Einzigartige Babybilder Bodensee Umgebung",
                 "Familienfotografie mit Babys Thurgau", "Romantische Babyfotos Zürich Umgebung",
                 "Studiofotografie für Babys Winterthur", "Outdoor Kinderfotos Schaffhausen",
                 "Natürliche Babybilder Bodensee", "Kreative Babyfotos Thurgau", "Professionelle Familienfotos Zürich",
                 "Einzigartige Kinderfotografie Winterthur", "Lustige Babybilder Bodensee",
                 "Natürliche Familienfotos mit Babys Schaffhausen", "Studiofotografie für Babys in Thurgau",
                 "Cake Smash Fotoshooting Zürich", "Süße Cake Smash Fotos Winterthur",
                 "Cake Smash Fotografie in Schaffhausen", "Professionelle Cake Smash Bilder Bodensee",
                 "Einzigartige Cake Smash Fotos Thurgau", "Romantische Kinderfotos mit Kuchen Zürich",
                 "Studiofotografie für Cake Smash Winterthur", "Lustige Cake Smash Fotos Bodensee",
                 "Outdoor Cake Smash Bilder Schaffhausen", "Natürliche Cake Smash Fotografie Zürich",
                 "Künstlerische Cake Smash Bilder Winterthur", "Professionelle Cake Smash Fotos Bodensee",
                 "Spezialisierte Kinderfotografie für Cake Smash Thurgau", "Familienfotos mit Cake Smash in Zürich",
                 "Lustige Cake Smash Porträts Winterthur", "Studiofotografie für Cake Smash Schaffhausen",
                 "Einzigartige Cake Smash Bilder Bodensee Umgebung",
                 "Romantische Kinderfotografie mit Cake Smash Zürich", "Natürliche Cake Smash Fotos Winterthur",
                 "Kreative Cake Smash Fotografie Schaffhausen", "Natürliche Kinderfotos am Bodensee",
                 "Spezialisierte Cake Smash Fotografie Thurgau", "Einzigartige Familienfotos mit Cake Smash Zürich",
                 "Outdoor Cake Smash in Winterthur", "Cake Smash Bilder mit Familie in Schaffhausen",
                 "Romantische Cake Smash Bilder Bodensee", "Professionelle Cake Smash Kinderfotos Zürich",
                 "Lustige Cake Smash Bilder Winterthur", "Studiofotografie für Cake Smash in Bodensee",
                 "Kreative Kinderfotografie Cake Smash Zürich", "Cake Smash Bilder für Babys Winterthur",
                 "Cake Smash Familienfotografie in Thurgau", "Studio Cake Smash Bilder Schaffhausen",
                 "Süße Kinderfotos mit Cake Smash am Bodensee", "Natürliche Cake Smash Kinderbilder Zürich",
                 "Professionelle Cake Smash Fotografie Winterthur", "Romantische Cake Smash Porträts Bodensee",
                 "Kreative Cake Smash Studiofotografie Zürich", "Lustige Kinderbilder Cake Smash Winterthur",
                 "Natürliche Cake Smash Familienfotos Schaffhausen", "Cake Smash Outdoor Fotos in Thurgau",
                 "Studiofotografie für Kinder mit Cake Smash Zürich",
                 "Professionelle Cake Smash Kinderfotos Winterthur", "Süße Cake Smash Bilder am Bodensee",
                 "Romantische Kinderporträts mit Cake Smash Thurgau", "Kreative Cake Smash Familienfotografie Zürich",
                 "Lustige Kinderfotos mit Cake Smash in Winterthur", "Natürliche Cake Smash Fotos in Schaffhausen",
                 "Einzigartige Cake Smash Bilder Bodensee Umgebung", "Studio Cake Smash Kinderbilder Winterthur",
                 "Familienporträts mit Cake Smash in Zürich", "Professionelle Cake Smash Kinderporträts Winterthur",
                 "Cake Smash Outdoor Bilder Schaffhausen", "Romantische Cake Smash Kinderfotos Bodensee",
                 "Einzigartige Kinderfotos mit Cake Smash Zürich", "Natürliche Cake Smash Kinderporträts Thurgau",
                 "Studio Cake Smash Familienfotos Winterthur", "Professionelle Cake Smash Kinderbilder Schaffhausen",
                 "Spezialisierte Cake Smash Fotografie Bodensee", "Romantische Cake Smash Kinderporträts Zürich",
                 "Studiofotografie für Kinder mit Cake Smash Winterthur", "Natürliche Cake Smash Porträts Bodensee",
                 "Einzigartige Cake Smash Kinderbilder Thurgau", "Professionelle Cake Smash Familienbilder Zürich",
                 "Romantische Kinderfotos mit Cake Smash Winterthur", "Kreative Cake Smash Porträts Schaffhausen",
                 "Spezialisierte Kinderfotografie mit Cake Smash Bodensee",
                 "Natürliche Cake Smash Familienfotos Winterthur", "Lustige Cake Smash Porträts Thurgau",
                 "Professionelle Cake Smash Porträts Zürich", "Studio Cake Smash Familienfotografie Schaffhausen",
                 "Kreative Cake Smash Bilder Winterthur", "Süße Cake Smash Kinderfotos Zürich",
                 "Romantische Cake Smash Bilder Winterthur", "Professionelle Cake Smash Outdoor Porträts Bodensee",
                 "Cake Smash Studiofotografie Zürich", "Einzigartige Cake Smash Bilder Winterthur",
                 "Familienporträts mit Cake Smash am Bodensee", "Natürliche Cake Smash Kinderbilder Zürich",
                 "Lustige Cake Smash Kinderfotos Winterthur", "Studio Cake Smash Bilder Bodensee",
                 "Romantische Cake Smash Porträts Zürich", "Kreative Cake Smash Familienfotos Winterthur",
                 "Professionelle Cake Smash Studiofotografie Thurgau", "Natürliche Cake Smash Kinderfotos Schaffhausen",
                 "Einzigartige Cake Smash Bilder Winterthur", "Romantische Kinderporträts mit Cake Smash Bodensee",
                 "Studio Cake Smash Kinderfotos Zürich", "Kreative Cake Smash Porträts Winterthur",
                 "Süße Cake Smash Familienbilder Schaffhausen", "Natürliche Cake Smash Kinderbilder Bodensee",
                 "Professionelle Cake Smash Familienfotos Zürich", "Lustige Cake Smash Porträts Winterthur",
                 "Romantische Cake Smash Kinderbilder Bodensee", "Einzigartige Cake Smash Familienfotos Zürich",
                 "Natürliche Cake Smash Studiofotografie Winterthur", "Süße Cake Smash Kinderbilder Schaffhausen",
                 "Professionelle Cake Smash Familienporträts Bodensee", "Kreative Cake Smash Kinderfotos Winterthur",
                 "Romantische Cake Smash Familienporträts Zürich"]
