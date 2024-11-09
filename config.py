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
# MAIL_SERVER = 'mail.your-server.de'
# MAIL_PORT = 465
# MAIL_USERNAME = 'info@fotos-baby.de'
# MAIL_PASSWORD = 'cashMONEY15288'
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True

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
    "Neugeborenen-Fotoshooting in Singen", "Happy Baby in Singen", "Glückliches Baby in Radolfzell",
    "Family photo in Radolfzell", "Baby-Porträt in Konstanz", "Kreatives Neugeborenes in Kreuzlingen",
    "Süßes Neugeborenes in Rottweil", "Newborn photography in Schaffhausen", "Neugeborenes und Eltern in Villingen",
    "Sleeping newborn in Villingen", "Familienfoto in Stockach", "Baby and dog in Zurich",
    "Neugeborenen-Shooting in Winterthur", "Glückliches Baby in Überlingen", "Baby am Bodensee in Überlingen",
    "Creative newborn in Friedrichshafen", "Herbstliches Fotoshooting in Singen", "Baby im Strampler in Radolfzell",
    "Baby and father in Konstanz", "Neugeborenes mit Mütze in Kreuzlingen", "Rottweil Baby in der Wiege",
    "First steps in Rottweil", "Neugeborenes mit Spielzeug in Schaffhausen", "Baby im Tragetuch in Villingen",
    "Stockach Baby am See", "Newborn with pacifier in Zurich", "Neugeborenes im Sommer in Winterthur",
    "Baby mit Sonnenhut in Überlingen", "Friedrichshafen Baby im Krankenhaus", "Newborn in hospital in Friedrichshafen",
    "Baby mit Teddybär in Singen", "Baby with teddy bear in Radolfzell", "Neugeborenes mit Schnuller in Konstanz",
    "Sleeping baby in Kreuzlingen", "Erste Tage eines Babys in Rottweil", "Newborn with toy car in Schaffhausen",
    "Baby und Mutter in Villingen", "Family photo after birth in Stockach", "Baby im Sonnenschein in Zurich",
    "Newborn with sunglasses in Winterthur", "Überlingen Baby auf der Decke", "Baby on the blanket in Überlingen",
    "Baby beim Krabbeln in Friedrichshafen", "Neugeborenes mit Rassel in Singen", "Baby with bib in Radolfzell",
    "Family photo with pet in Konstanz", "Baby in crib in Kreuzlingen", "Neugeborenes in der Schaukel in Rottweil",
    "Baby in playpen in Schaffhausen", "Mother feeding baby in Villingen", "Father changing newborn in Stockach",
    "Baby in tub in Zurich", "Newborn with children's book in Winterthur", "Baby mit Schnuffeltuch in Überlingen",
    "Family with newborn in car in Friedrichshafen", "Baby with bonnet in Singen",
    "Newborn with stuffed animal in Radolfzell",
    "Baby with rubber duck in Konstanz", "Baby in nursery in Kreuzlingen", "Neugeborenes beim Arzt in Rottweil",
    "Baby at dentist in Schaffhausen", "Mutter beim Stillen in Villingen", "Baby beim Füttern in Stockach",
    "Newborn falling asleep in Zurich", "Baby waking up in Winterthur", "Family with newborn in garden in Überlingen",
    "Baby taking a bath in Friedrichshafen", "Neugeborenes mit Schnullerkette in Singen",
    "Newborn at dentist in Radolfzell",
    "Neugeborenes im Kinderbett in Konstanz", "Baby with rubber ducks in Kreuzlingen",
    "Neugeborenes im Hochstuhl in Rottweil",
    "Baby with teething ring in Schaffhausen", "Neugeborenes im Tragetuch in Villingen",
    "Baby at pediatrician in Stockach",
    "Newborn with baby shoes in Zurich", "Baby with pacifier in Winterthur",
    "Neugeborenes im Kinderwagen in Überlingen",
    "Baby mit Mütze in Friedrichshafen", "Newborn in baby carrier in Singen",
    "Neugeborenes mit Babymütze in Radolfzell",
    "Baby with first tooth in Konstanz", "Neugeborenes im Schlafsack in Kreuzlingen",
    "Baby's first Christmas in Rottweil",
    "Newborn with baby bottle in Schaffhausen", "Neugeborenes im Laufgitter in Villingen",
    "Baby with first steps in Stockach",
    "Newborn and toddler sibling in Zurich", "Baby mit Spieluhr in Winterthur",
    "Neugeborenes und Kleinkind in Überlingen",
    "Baby with first haircut in Friedrichshafen", "Neugeborenes mit Windel in Singen", "Baby at beach in Radolfzell",
    "Newborn with grandmother in Konstanz", "Baby mit Großeltern in Kreuzlingen", "Erste Weihnachten in Rottweil",
    "Newborn with Christmas tree in Schaffhausen", "Neugeborenes und Weihnachtsbaum in Villingen",
    "Baby mit Geschenk in Stockach",
    "Newborn with Christmas tree in Schaffhausen", "Neugeborenes und Weihnachtsbaum in Villingen",
    "Baby mit Geschenk in Stockach",
    "Neugeborenes mit Familienhund in Singen", "Newborn with pet cat in Radolfzell",
    "Baby im ersten Outfit in Konstanz",
    "Newborn’s first outfit in Kreuzlingen", "Baby im ersten Bad in Rottweil", "Newborn’s first bath in Schaffhausen",
    "Baby und Geschwister in Villingen", "Newborn with siblings in Stockach", "Erste Nacht zu Hause in Zurich",
    "First night at home in Winterthur", "Baby im Kinderzimmer in Überlingen", "Newborn in nursery in Friedrichshafen",
    "Baby und Eltern beim Arzt in Singen", "Newborn and parents at doctor in Radolfzell",
    "Baby’s erste Reise in Konstanz",
    "Newborn’s first trip in Kreuzlingen", "Baby mit Oma und Opa in Rottweil",
    "Newborn with grandparents in Schaffhausen",
    "Neugeborenes mit Eltern im Garten in Villingen"
]

alt_tags_babybauch = [
    "Schwanger in Singen", "Pregnant woman in Singen", "Babybauch in Radolfzell", "Expecting mother in Radolfzell",
    "Schwangere Frau in Konstanz", "Baby bump in Konstanz", "Schwangerschaft in Kreuzlingen",
    "Pregnancy in Kreuzlingen",
    "Glückliche Schwangere in Rottweil", "Happy pregnant woman in Rottweil", "Babybauchshooting in Schaffhausen",
    "Maternity photoshoot in Schaffhausen", "Schwangerschaftsgymnastik in Villingen", "Pregnancy yoga in Villingen",
    "Paar erwartet Baby in Stockach", "Couple expecting in Stockach", "Schwangere mit Buch in Zurich",
    "Pregnant reading in Zurich",
    "Schwanger im Sommer in Winterthur", "Pregnant in summer in Winterthur", "Schwanger am Bodensee in Überlingen",
    "Pregnant at Bodensee in Überlingen", "Schwangere im Park in Friedrichshafen",
    "Pregnant in park in Friedrichshafen",
    "Babybauch in der Natur in Singen", "Maternity in nature in Radolfzell", "Schwangere beim Einkaufen in Konstanz",
    "Pregnant shopping in Konstanz", "Babybauch und Haustier in Kreuzlingen", "Maternity with pet in Kreuzlingen",
    "Schwangerschaftsmode in Rottweil", "Maternity fashion in Rottweil", "Schwangerschaftscheck in Schaffhausen",
    "Pregnancy check-up in Schaffhausen", "Schwanger und Yoga in Villingen", "Pregnant doing yoga in Villingen",
    "Babybauch und Blumen in Stockach", "Maternity with flowers in Stockach", "Schwangerschaftsdiät in Zurich",
    "Pregnancy diet in Zurich", "Schwanger und glücklich in Winterthur", "Pregnant and happy in Winterthur",
    "Babybauch im Winter in Überlingen", "Maternity in winter in Überlingen",
    "Schwangerschaft und Sport in Friedrichshafen",
    "Pregnancy and exercise in Friedrichshafen", "Schwanger am Strand in Singen", "Pregnant at the beach in Radolfzell",
    "Schwangerschaft und Arbeit in Konstanz", "Pregnancy and work in Konstanz", "Babybauch und Kunst in Kreuzlingen",
    "Maternity and art in Kreuzlingen", "Schwangerschaft und Reisen in Rottweil", "Pregnancy and travel in Rottweil",
    "Schwanger in der Küche in Schaffhausen", "Pregnant in the kitchen in Schaffhausen",
    "Schwangerschaft und Ernährung in Villingen",
    "Pregnancy and nutrition in Villingen", "Schwangerschaft und Familie in Stockach",
    "Pregnancy and family in Stockach",
    "Babybauch und Musik in Zurich", "Maternity and music in Zurich", "Schwanger im Frühling in Winterthur",
    "Pregnant in spring in Winterthur", "Schwangerschaft und Freizeit in Überlingen",
    "Pregnancy and leisure in Überlingen",
    "Schwanger und Wellness in Friedrichshafen", "Pregnant and wellness in Friedrichshafen",
    "Babybauch und Spaß in Singen",
    "Maternity and fun in Radolfzell", "Schwanger und Entspannung in Konstanz", "Pregnant and relaxation in Konstanz",
    "Babybauch und Bücher in Kreuzlingen", "Maternity and books in Kreuzlingen", "Schwangerschaft und Kino in Rottweil",
    "Pregnancy and movies in Rottweil", "Schwanger und Lächeln in Schaffhausen", "Pregnant and smiling in Schaffhausen",
    "Babybauch und Wochenende in Villingen", "Maternity and weekend in Villingen",
    "Schwangerschaft und Gesundheit in Stockach",
    "Pregnancy and health in Stockach", "Schwanger und Tanzen in Zurich", "Pregnant and dancing in Zurich",
    "Babybauch und Kochen in Winterthur", "Maternity and cooking in Winterthur",
    "Schwangerschaft und Spaziergang in Überlingen",
    "Pregnancy and walk in Überlingen", "Schwanger und Sonnenuntergang in Friedrichshafen",
    "Pregnant and sunset in Friedrichshafen",
    "Babybauch und Erholung in Singen", "Maternity and rest in Radolfzell", "Schwanger und Frühstück in Konstanz",
    "Pregnant and breakfast in Konstanz", "Babybauch und Abendessen in Kreuzlingen",
    "Maternity and dinner in Kreuzlingen",
    "Schwangerschaft und Kaffee in Rottweil", "Pregnancy and coffee in Rottweil", "Schwanger und Tee in Schaffhausen",
    "Pregnant and tea in Schaffhausen", "Babybauch und Berge in Villingen", "Maternity and mountains in Villingen",
    "Schwangerschaft und Strand in Stockach", "Pregnancy and beach in Stockach", "Schwanger und See in Zurich",
    "Pregnant and lake in Zurich", "Babybauch und Stadt in Winterthur", "Maternity and city in Winterthur",
    "Schwangerschaft und Dorf in Überlingen", "Pregnancy and village in Überlingen",
    "Schwanger und Wald in Friedrichshafen",
    "Pregnant and forest in Friedrichshafen"
]

alt_tags_baby = [
    "5-monatiges Baby in Singen", "5-month-old in Singen", "Kleinkind in Radolfzell", "Toddler in Radolfzell",
    "1-jähriges Kind in Konstanz", "1-year-old in Konstanz", "Cakesmash Fotoshooting in Kreuzlingen",
    "Cakesmash photoshoot in Kreuzlingen",
    "Baby beim Krabbeln in Rottweil", "Crawling baby in Rottweil", "Kleinkind mit Spielzeug in Schaffhausen",
    "Toddler with toy in Schaffhausen",
    "Baby mit Eltern in Villingen", "Baby with parents in Villingen", "Kleinkind beim Malen in Stockach",
    "Toddler painting in Stockach",
    "Baby beim Schlafen in Zurich", "Sleeping baby in Zurich", "2-jähriges Kind in Winterthur",
    "2-year-old in Winterthur",
    "Kleinkind im Garten in Überlingen", "Toddler in garden in Überlingen", "Baby beim Essen in Friedrichshafen",
    "Eating baby in Friedrichshafen",
    "1. Geburtstag in Singen", "1st birthday in Radolfzell", "Baby mit Hund in Konstanz", "Baby with dog in Konstanz",
    "Kleinkind und Katze in Kreuzlingen", "Toddler with cat in Kreuzlingen", "Kleinkind beim Spielen in Rottweil",
    "Toddler playing in Rottweil",
    "Baby mit Großeltern in Schaffhausen", "Baby with grandparents in Schaffhausen",
    "Kleinkind beim Lesen in Villingen", "Toddler reading in Villingen",
    "Baby beim Baden in Stockach", "Bathing baby in Stockach", "Kleinkind beim Essen in Zurich",
    "Toddler eating in Zurich",
    "Baby beim Spazieren in Winterthur", "Strolling baby in Winterthur", "Kleinkind im Zoo in Überlingen",
    "Toddler at zoo in Überlingen",
    "Baby mit Bruder in Friedrichshafen", "Baby with brother in Friedrichshafen", "Kleinkind mit Schwester in Singen",
    "Toddler with sister in Radolfzell",
    "Baby im Hochstuhl in Konstanz", "Baby in highchair in Konstanz", "Kleinkind in der Schule in Kreuzlingen",
    "Toddler at school in Kreuzlingen",
    "Baby beim Arzt in Rottweil", "Baby at doctor in Rottweil", "Kleinkind im Park in Schaffhausen",
    "Toddler at park in Schaffhausen",
    "Baby beim Schwimmen in Villingen", "Swimming baby in Villingen", "Kleinkind beim Tanzen in Stockach",
    "Dancing toddler in Stockach",
    "Baby im Auto in Zurich", "Baby in car in Zurich", "Kleinkind auf dem Fahrrad in Winterthur",
    "Toddler on bike in Winterthur",
    "Baby im Flugzeug in Überlingen", "Baby in airplane in Überlingen", "Kleinkind im Boot in Friedrichshafen",
    "Toddler in boat in Friedrichshafen",
    "Baby beim Singen in Singen", "Singing baby in Radolfzell", "Kleinkind beim Musizieren in Konstanz",
    "Musical toddler in Konstanz",
    "Baby beim Cakesmash in Kreuzlingen", "Cakesmash baby in Kreuzlingen", "Kleinkind beim Backen in Rottweil",
    "Baking toddler in Rottweil",
    "Baby mit Mutter in Schaffhausen", "Baby with mother in Schaffhausen", "Kleinkind mit Vater in Villingen",
    "Toddler with father in Villingen",
    "Baby mit Schnuller in Stockach", "Baby with pacifier in Stockach", "Kleinkind mit Flasche in Zurich",
    "Toddler with bottle in Zurich",
    "Baby mit Mütze in Winterthur", "Baby with hat in Winterthur", "Kleinkind mit Schuhen in Überlingen",
    "Toddler with shoes in Überlingen",
    "Baby mit Strampler in Friedrichshafen", "Baby in onesie in Friedrichshafen", "Baby im Sommer in Singen",
    "Summer baby in Radolfzell", "Kleinkind im Herbst in Konstanz", "Autumn toddler in Konstanz",
    "Baby mit Teddybär in Kreuzlingen", "Baby with teddy bear in Kreuzlingen", "Kleinkind im Schnee in Rottweil",
    "Snowy toddler in Rottweil",
    "Baby im Blumenfeld in Schaffhausen", "Baby in flower field in Schaffhausen",
    "Kleinkind auf der Rutsche in Villingen", "Toddler on slide in Villingen",
    "Baby im Sandkasten in Stockach", "Baby in sandbox in Stockach", "Kleinkind beim Klettern in Zurich",
    "Toddler climbing in Zurich",
    "Baby im Streichelzoo in Winterthur", "Baby in petting zoo in Winterthur", "Kleinkind beim Fischen in Überlingen",
    "Toddler fishing in Überlingen",
    "Baby im Einkaufszentrum in Friedrichshafen", "Baby in shopping mall in Friedrichshafen",
    "Kleinkind im Restaurant in Singen", "Toddler in restaurant in Radolfzell",
    "Baby beim Zahnarzt in Konstanz", "Baby at the dentist in Konstanz", "Kleinkind mit Bauklötzen in Kreuzlingen",
    "Toddler with building blocks in Kreuzlingen",
    "Baby mit Luftballons in Rottweil", "Baby with balloons in Rottweil", "Kleinkind beim Malen in Schaffhausen",
    "Toddler drawing in Schaffhausen",
    "Baby mit Kuscheltier in Villingen", "Baby with stuffed animal in Villingen", "Kleinkind mit Puzzle in Stockach",
    "Toddler with puzzle in Stockach",
    "Baby mit Lätzchen in Zurich", "Baby with bib in Zurich", "Kleinkind mit Töpfchen in Winterthur",
    "Toddler with potty in Winterthur",
    "Baby mit Milchflasche in Überlingen", "Baby with milk bottle in Überlingen",
    "Kleinkind mit Schnuffeltuch in Friedrichshafen", "Toddler with security blanket in Friedrichshafen"
]
