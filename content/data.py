# -*- coding: utf-8 -*-
"""Site data for Ensō Foot Clinic.

Business facts (name, practitioner, services, NAP, socials) come from the
clinic's own published copy and its business card. Page bodies live in the
copy_*.py modules. Edit this file to change contact details, menus, the
practitioner's text or the legal identity shown on the contact page.

Opening hours are NOT published anywhere by the clinic and are therefore left
deliberately non-committal — confirm them before launch:
  · opening hours  → shown as «Κατόπιν ραντεβού», no openingHoursSpecification

Both addresses and all three phone lines come from the clinic's business card
(Sept 2026): Ρωμανού 11, Περαία and Ελ. Βενιζέλου 180, Καλλιθέα.
"""

SITE = {
    "name": "Ensō Foot Clinic",
    "legal": "ENSO FOOT CLINIC ΜΟΝΟΠΡΟΣΩΠΗ Ι.Κ.Ε.",
    "short": "Ensō Foot Clinic",
    "domain": "https://www.ensofootclinic.gr",
    "phone": "23920 21702",
    "phone_href": "+302392021702",
    "phone_alt": "210 958 6060",
    "phone_alt_href": "+302109586060",
    "phone_mob": "698 385 0193",
    "phone_mob_href": "+306983850193",
    "email": "podopure@gmail.com",
    "floor": "3ος όροφος",
    "address": "Ρωμανού 11, Περαία (3ος όροφος)",
    "street": "Ρωμανού 11",
    "address_en": "Romanou 11, Peraia, Thessaloniki (3rd floor)",
    "address_athens": "Ελ. Βενιζέλου 180, Καλλιθέα",
    "street_athens": "Λεωφ. Ελ. Βενιζέλου 180",
    "address_athens_en": "El. Venizelou 180, Kallithea, Athens",
    "postcode_athens": "176 75",
    # The pin of the Google Business Profile «Ensō Foot Clinic Athens» (read from
    # the Maps embed, Sept 2026); 11888.gr lists the same address, ΤΚ 17675.
    "lat_athens": 37.9541154,
    "lng_athens": 23.6989612,
    # The embeds search for the business by name + address, so Google shows its
    # own listing pin (the Business Profile card), not a bare street point.
    "embed_athens": "https://www.google.com/maps?q=Ens%C5%8D%20Foot%20Clinic%2C%20%CE%9B%CE%B5%CF%89%CF%86.%20%CE%95%CE%BB.%20%CE%92%CE%B5%CE%BD%CE%B9%CE%B6%CE%AD%CE%BB%CE%BF%CF%85%20180%2C%20%CE%9A%CE%B1%CE%BB%CE%BB%CE%B9%CE%B8%CE%AD%CE%B1%20176%2075&z=16&output=embed&hl=el",
    "embed": "https://www.google.com/maps?q=Enso%20Foot%20Clinic%20Christodoulou%20Elpiniki%2C%20%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D%2011%2C%20%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%20570%2019&z=16&output=embed&hl=el",
    "map_athens_full": "https://www.google.com/maps/search/?api=1&query=Ens%C5%8D%20Foot%20Clinic%2C%20%CE%9B%CE%B5%CF%89%CF%86.%20%CE%95%CE%BB.%20%CE%92%CE%B5%CE%BD%CE%B9%CE%B6%CE%AD%CE%BB%CE%BF%CF%85%20180%2C%20%CE%9A%CE%B1%CE%BB%CE%BB%CE%B9%CE%B8%CE%AD%CE%B1%20176%2075",
    "map_athens": "https://maps.google.com/?q=%CE%95%CE%BB.%20%CE%92%CE%B5%CE%BD%CE%B9%CE%B6%CE%AD%CE%BB%CE%BF%CF%85%20180%2C%20%CE%9A%CE%B1%CE%BB%CE%BB%CE%B9%CE%B8%CE%AD%CE%B1%2C%20%CE%91%CE%B8%CE%AE%CE%BD%CE%B1",
    "postcode": "570 19",
    "map": "https://maps.google.com/?q=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece",
    "map_full": ("https://www.google.com/maps/place/"
                 "%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11,+%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1"
                 "/@40.5067925,22.9252194,17z"),
    "waze": ("https://waze.com/ul?p=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+"
             "%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece&ll=40.5067925,22.9252194&navigate=yes"),
    "moovit": ("https://moovit.com/?to=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+"
               "%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece&tll=40.5067925_22.9252194&metroId=1"),
    # The pin of the Google Business Profile «Enso Foot Clinic Christodoulou
    # Elpiniki» (read from the Maps embed, Sept 2026).
    "lat": 40.5067435,
    "lng": 22.9252016,
    "region_iso": "GR-B",            # Κεντρική Μακεδονία, ISO 3166-2
    "locality": "Περαία",
    "locality_en": "Peraia",
    "region": "Θεσσαλονίκη",
    "region_en": "Thessaloniki",
    "founded": "2002",
    # The clinic does not publish fixed opening hours; it works by appointment.
    # Nothing here is invented — change it the day the client gives real hours.
    "hours": [("Δευτέρα – Παρασκευή", "Κατόπιν ραντεβού"),
              ("Σάββατο", "Κατόπιν ραντεβού"),
              ("Κυριακή", "Κλειστά")],
    # Areas the clinic actually draws patients from, declared once as areaServed
    # in the structured data.
    "areas": ["Περαία", "Νέοι Επιβάτες", "Αγία Τριάδα", "Νέα Μηχανιώνα", "Επανομή",
              "Πλαγιάρι", "Θέρμη", "Θεσσαλονίκη", "Καλαμαριά", "Ν. Κρήνη",
              "Χαλκιδική", "Αθήνα"],
    # ── Legal identity, shown on /epikoinonia/ ─────────────────────────────
    # The client asked for the company details (ΓΕΜΗ, ΑΦΜ κ.λπ.) on the contact
    # page. Every value that is still None renders as «θα συμπληρωθεί» and the
    # build prints a reminder. Fill them in and rebuild — nothing else changes.
    "legal_rows": [
        # From the ΓΕΜΗ «Ανακοίνωση – Βεβαίωση σύστασης εταιρείας», 23/07/2026.
        ("Επωνυμία", "ENSO FOOT CLINIC ΜΟΝΟΠΡΟΣΩΠΗ Ι.Κ.Ε."),
        ("Διακριτικός τίτλος", "ENSO FOOT CLINIC"),
        ("Δραστηριότητα", "Υπηρεσίες θεραπευτή νυχιών και κάλων (ΚΑΔ 86960007)"),
        ("Έδρα", "Ελ. Βενιζέλου 180, 176 75 Καλλιθέα"),
        ("ΑΦΜ", "803357198"),
        ("ΔΟΥ", "ΚΕΦΟΔΕ Αττικής"),
        ("Αρ. ΓΕΜΗ", "195249603000"),
        ("Email", "podopure@gmail.com"),
    ],
    # The band that replaced the old «Επόμενο βήμα» call to action, in the
    # clinic's own words (Oct 2026). First line stands alone as the headline.
    "motto": ("Η βαρύτητα είναι η σταθερά μας.",
              "Το πώς την αποδέχονται τα πέλματά μας καθορίζει όλη μας την κίνηση. "
              "Ας φροντίσουμε ώστε οι αποδέκτες αυτοί να είναι υγιείς και "
              "λειτουργικοί καθημερινά."),
    "credit": {"name": "CLINICBRAIN",
               "url": "https://clinicbrain.gr/?utm_source=client-site"
                      "&utm_medium=footer&utm_campaign=made-by"},
    "social": {
        "facebook": "https://www.facebook.com/lpodology",
        "tiktok": "https://www.tiktok.com/@enso.foot.clinic",
    },
}

# ── The practitioner ─────────────────────────────────────────────────────────
# Ensō is one professional, not a multi-specialty team. The «Ποιοι είμαστε»
# text below is the clinic's own (Oct 2026), verbatim — it is the whole home page.
PRACTITIONER = {
    "slug": "elpiniki-christodoulou",
    "name": "Ελπινίκη Χριστοδούλου",
    "name_en": "Elpiniki Christodoulou",
    "role": "Εξειδικευμένη Ποδολόγος | Ιδρύτρια του Ensō Foot Clinic",
    "since": "2002",
    "years": "24",
    "about": [
        "Από το 2002, η φροντίδα του ανθρώπινου πέλματος αποτελεί για εμένα κάτι πολύ "
        "περισσότερο από ένα επάγγελμα· είναι μια συνεχής μελέτη της βάσης πάνω στην "
        "οποία στηρίζεται ολόκληρο το σώμα.",

        "Με 24 χρόνια αδιάλειπτης κλινικής παρουσίας, συνδυάζω την κλασική, εξειδικευμένη "
        "ποδολογική περιποίηση με τις αρχές της εμβιομηχανικής (biomechanics) και της "
        "λειτουργικής κίνησης. Πιστεύω βαθιά ότι τα πόδια δεν είναι απλώς απολήξεις που "
        "δέχονται φορτία, αλλά ένας ζωντανός αποσβεστήρας που καθορίζει τη στάση, τη "
        "βάδιση και την ποιότητα της καθημερινότητάς μας.",

        "Στα κέντρα μας στην Περαία Θεσσαλονίκης και στην Καλλιθέα Αθήνας, στόχος μου "
        "μαζί με την ομάδα μου είναι να προσφέρουμε εξατομικευμένη υποστήριξη, σωστή "
        "εκπαίδευση και πρακτικές λύσεις — ώστε κάθε σας βήμα να γίνεται με ασφάλεια, "
        "σταθερότητα και ελευθερία.",
    ],
    # One-liner for the structured data and meta descriptions.
    "blurb": ("Εξειδικευμένη ποδολόγος, ιδρύτρια του Ensō Foot Clinic. Από το 2002 "
              "συνδυάζει την κλασική ποδολογική περιποίηση με τις αρχές της "
              "εμβιομηχανικής και της λειτουργικής κίνησης, σε Περαία Θεσσαλονίκης "
              "και Καλλιθέα Αθήνας."),
}

# ── Short biography, by date ─────────────────────────────────────────────────
# The clinic asked for the CV «εν συντομία, βάση χρονολογίου» with a
# «περισσότερα» for whoever wants the rest. BIO_BRIEF is the summary;
# BIO_MORE is what the disclosure opens. Shown under «Ποιοι είμαστε» on the
# homepage (/#viografiko). Every line comes from the practitioner's own
# «Σχετικά» page — no date is inferred.
BIO_BRIEF = [
    ("2002", "Ξεκινά η πορεία στο άκρο πόδι — Owner, Trellis Podology &amp; Nails, "
             "Θεσσαλονίκη."),
    ("2006 – 2015", "NBM Germany — Exclusive Sales Supplier &amp; Academy Instructor "
                    "για τη Βόρεια Ελλάδα."),
    ("Εκπαίδευση", "Εκπαιδεύτρια ποδολογίας και nail art στο Ι.ΙΕΚ Ξίνη, Μουδανιά "
                   "Χαλκιδικής."),
    ("Σήμερα", "Δύο ποδολογικά κέντρα: Περαία Θεσσαλονίκης και Καλλιθέα Αθήνας."),
]

BIO_MORE = [
    ("Σεμινάρια", "Οργανώτρια και εισηγήτρια επαγγελματικών σεμιναρίων, workshops "
                  "και masterclasses ποδολογίας."),
    ("Β. Όλγας 181", "Ποδολογικό κέντρο, Θεσσαλονίκη."),
    ("Lefas coiffure", "In-store υπηρεσίες ποδολογίας και τεχνικού νυχιών."),
]

# ── Services / treatments ────────────────────────────────────────────────────
# `matrix` powers the comparison table on /ypiresies/.
# `kind`: prevention (έλεγχος) · care (ποδολογική πράξη) · device (θεραπευτική εφαρμογή)
TREATMENTS = [
    dict(slug="elenchos-diavitikou-podiou",
         title="Έλεγχος διαβητικού ποδιού",
         short="Αξιολόγηση & πρόληψη",
         meta="Έλεγχος διαβητικού ποδιού: αξιολόγηση αίσθησης με μονόινο, έλεγχος σφύξεων, "
              "δέρματος και υποδημάτων. Μία φορά τον χρόνο κατ' ελάχιστον.",
         lead="Δομημένη αξιολόγηση αίσθησης, κυκλοφορίας, δέρματος και υποδημάτων, ώστε το "
              "πρόβλημα να βρεθεί πριν γίνει πληγή.",
         kind="prevention",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνος έλεγχος",
                     sessions="1 φορά/χρόνο κατ' ελάχιστον", duration="30–40 λεπτά",
                     after="Γραπτό πλάνο φροντίδας", pain="Χωρίς πόνο"),
         treats=["Διαβητική νευροπάθεια", "Περιφερική αγγειοπάθεια",
                 "Σημεία υπερπίεσης", "Πρόληψη έλκους"]),

    dict(slug="iatriki-podologia",
         title="Ιατρική ποδολογία",
         short="Κλινική περιποίηση άκρου ποδός",
         meta="Ιατρική ποδολογία: αποστειρωμένη, ανώδυνη κλινική περιποίηση πελμάτων και "
              "νυχιών με φρέζα και νυστέρι. Δεν είναι pedicure — είναι θεραπευτική πράξη.",
         lead="Η βασική συνεδρία του ποδολογικού κέντρου: αξιολόγηση, αποστειρωμένα εργαλεία, "
              "θεραπευτική περιποίηση δέρματος και νυχιών, οδηγίες για το σπίτι.",
         kind="care",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνη",
                     sessions="Κάθε 6–8 εβδομάδες", duration="45–60 λεπτά",
                     after="Περπατάτε αμέσως", pain="Χωρίς πόνο"),
         treats=["Πάχυνση νυχιών", "Σκληρύνσεις", "Ξηροδερμία", "Φροντίδα ευπαθούς ποδιού"]),

    dict(slug="afairesi-kalon-tylon",
         title="Αφαίρεση κάλων & τύλων",
         short="Αποφόρτιση & καθαρισμός",
         meta="Αφαίρεση κάλων και τύλων με νυστέρι και φρέζα, χωρίς πόνο και χωρίς αίμα, "
              "μαζί με αποφόρτιση του σημείου ώστε να μην επιστρέψουν.",
         lead="Ο πυρήνας του κάλου αφαιρείται στρώση-στρώση με αποστειρωμένο νυστέρι. Η "
              "ανακούφιση είναι άμεση — αλλά η δουλειά είναι να φύγει και η πίεση.",
         kind="care",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνη",
                     sessions="1 συνεδρία · επανέλεγχος 6–8 εβδ.", duration="30–45 λεπτά",
                     after="Περπατάτε αμέσως", pain="Χωρίς πόνο"),
         treats=["Κάλοι με πυρήνα", "Τύλοι", "Σκληρύνσεις", "Μεσοδακτύλιοι κάλοι"]),

    dict(slug="therapeia-ksirodermias",
         title="Θεραπεία ξηροδερμίας & ραγάδων",
         short="Απολέπιση & ενυδάτωση",
         meta="Θεραπεία ξηροδερμίας πελμάτων και ραγάδων πτέρνας: απομάκρυνση νεκρού ιστού, "
              "κλείσιμο των ραγάδων και πρωτόκολλο ενυδάτωσης με ουρία για το σπίτι.",
         lead="Πρώτα φεύγει ο νεκρός ιστός, μετά μπαίνει η ενυδάτωση. Με την αντίστροφη "
              "σειρά, η κρέμα μένει πάνω στο σκληρό δέρμα και δεν κάνει τίποτα.",
         kind="care",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνη",
                     sessions="1–3 συνεδρίες", duration="40–50 λεπτά",
                     after="Ενυδάτωση καθημερινά στο σπίτι", pain="Χωρίς πόνο"),
         treats=["Ραγάδες πτέρνας", "Ξηροδερμία πελμάτων", "Απολέπιση", "Πρόληψη λοίμωξης"]),

    dict(slug="orthonychia-narthikes",
         title="Ορθονυχία με υαλώδεις νάρθηκες",
         short="Διόρθωση καμπυλότητας νυχιού",
         meta="Ορθονυχία: υαλώδης νάρθηκας που ανασηκώνει σταδιακά το νύχι που εισφρύει. "
              "Ανώδυνη, αναίμακτη θεραπεία με προσωπικό ποσοστό επιτυχίας 96%.",
         lead="Ένας λεπτός υαλώδης νάρθηκας κολλάται πάνω στο νύχι και το ξαναμαθαίνει να "
              "μεγαλώνει επίπεδο. Καμία τομή, κανένα ράμμα, καμία απώλεια νυχιού.",
         kind="device",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνη &amp; αναίμακτη",
                     sessions="Επανατοποθέτηση κάθε 4–6 εβδ.", duration="30 λεπτά",
                     after="Περπατάτε και φοράτε παπούτσια αμέσως",
                     pain="Ανακούφιση από την πρώτη μέρα"),
         treats=["Είσφρηση όνυχος", "Αυξημένη καμπυλότητα", "Υποτροπές μετά από χειρουργείο",
                 "Παιδική ονυχοκρύπτωση"]),
]

KIND_LABELS = {
    "prevention": "Πρόληψη & έλεγχος",
    "care": "Ποδολογική πράξη",
    "device": "Θεραπευτική εφαρμογή",
}

# Column headers of the comparison table, in `matrix` key order.
MATRIX_COLS = [("setting", "Πού γίνεται"), ("sensation", "Αίσθηση"),
               ("sessions", "Συχνότητα"), ("duration", "Διάρκεια"),
               ("after", "Μετά τη συνεδρία")]

# ── Seminars ─────────────────────────────────────────────────────────────────
# The teaching side of the practice is real and documented (organiser and
# instructor of professional seminars, workshops and masterclasses; instructor
# at Ι.ΙΕΚ Ξίνη; NBM Germany Academy Instructor 2006–2015) but has no published
# programme right now.
#
# Adding a seminar is ONE entry below plus its body in copy_seminars.py. The hub,
# the detail page, the schema and the sitemap all follow from it.
#
#   status   "open"      — registration is live
#            "announced" — dated, registration not yet open
#            "past"      — archive
#   register how people sign up. Swap the whole tuple when a real platform lands:
#            ("email", addr)  composes a message, no server needed  ← today
#            ("url",   href)  hands off to a booking platform
#            ("closed", "")   archive / registrations closed
#   mode     "online" · "onsite" · "hybrid"
#
# Template for a new seminar — copy, fill in, delete the comment markers:
#
#   dict(slug="onychokryptosi-masterclass",
#        title="Masterclass ορθονυχίας",
#        kicker="Masterclass · με φυσική παρουσία",
#        status="open",
#        start="2026-11-14T10:00:00+02:00", end="2026-11-14T17:00:00+02:00",
#        human="14 Νοεμβρίου 2026 · 10:00–17:00",
#        mode="onsite", venue="Ρωμανού 11, Περαία Θεσσαλονίκης",
#        level="Για ποδολόγους & σπουδαστές", duration="7 ώρες",
#        seats=12, price="120 € (προεγγραφή 100 €)", price_eur=120,
#        register=("email", SITE["email"]),
#        lead="…", topics=["…", "…"]),

SEMINARS = [
    dict(slug="1o-seminario-podologias",
         title="1ο Σεμινάριο Ποδολογίας",
         kicker="Εισαγωγικό · διαδικτυακό",
         status="past",
         start="2025-08-24T21:00:00+03:00",
         end="2025-08-24T22:00:00+03:00",
         human="24 Αυγούστου 2025 · 21:00–22:00",
         mode="online",
         venue="Ηλεκτρονική εκδήλωση",
         level="Ανοιχτό σε επαγγελματίες και σπουδαστές",
         duration="1 ώρα",
         seats=None,
         price="Δωρεάν συμμετοχή",
         price_eur=0,          # numeric, for schema.org Offer. None = do not state one.
         register=("closed", ""),
         lead="Το πρώτο διαδικτυακό σεμινάριο του ποδολογικού κέντρου, μια εισαγωγή στη σύγχρονη "
              "ποδολογική πράξη. Οι εγγραφές έχουν λήξει.",
         topics=["Τι είναι η ποδολογία και πού σταματά", "Αποστείρωση και ασφάλεια",
                 "Το διαβητικό πόδι στην καθημερινή πράξη",
                 "Ερωτήσεις από τους συμμετέχοντες"]),
]

SEMINAR_STATUS = {
    "open":      ("Ανοιχτές εγγραφές", "open"),
    "announced": ("Ανακοινώθηκε",      "announced"),
    "past":      ("Ολοκληρώθηκε",      "past"),
}
SEMINAR_MODES = {"online": "Διαδικτυακό", "onsite": "Με φυσική παρουσία",
                 "hybrid": "Υβριδικό"}

# Where «ενημερώστε με» goes while there is no platform. One place to change.
SEMINAR_NOTIFY = ("mailto:" + SITE["email"]
                  + "?subject=" + "Ενδιαφέρομαι%20για%20επόμενο%20σεμινάριο"
                  + "&body=" + "Θα%20ήθελα%20να%20ενημερωθώ%20για%20το%20επόμενο%20"
                    "σεμινάριο%20ποδολογίας.%0A%0AΟνοματεπώνυμο%3A%0AΙδιότητα%3A%0A"
                    "Τηλέφωνο%3A")
