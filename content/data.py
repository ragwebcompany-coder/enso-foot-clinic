# -*- coding: utf-8 -*-
"""Site data for Ensō Foot Clinic.

Business facts (name, practitioner, credentials, services, NAP, socials) come
from the clinic's own published copy on ensofootclinic.gr. Clinical copy lives
in `copy.py`. Edit this file to change structure, contact details or menus.

Two things are NOT published anywhere by the clinic and are therefore left
deliberately non-committal — confirm them before launch:
  · opening hours  → shown as «Κατόπιν ραντεβού», no openingHoursSpecification
  · the Athens address → only the Athens phone lines are listed, no street
"""

SITE = {
    "name": "Ensō Foot Clinic",
    "legal": "Ensō Foot Clinic — Χριστοδούλου Ελπινίκη, Ποδολόγος",
    "short": "Ensō Foot Clinic",
    "domain": "https://www.ensofootclinic.gr",
    "phone": "23920 21702",
    "phone_href": "+302392021702",
    "phone_alt": "210 958 6060",
    "phone_alt_href": "+302109586060",
    "phone_mob": "698 385 0193",
    "phone_mob_href": "+306983850193",
    "email": "podopure@gmail.com",
    "address": "Ρωμανού 11, Περαία (3ος όροφος)",
    "address_en": "Romanou 11, Peraia, Thessaloniki (3rd floor)",
    "postcode": "570 19",
    "map": "https://maps.google.com/?q=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece",
    "map_full": ("https://www.google.com/maps/place/"
                 "%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11,+%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1"
                 "/@40.5067925,22.9252194,17z"),
    "waze": ("https://waze.com/ul?p=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+"
             "%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece&ll=40.5067925,22.9252194&navigate=yes"),
    "moovit": ("https://moovit.com/?to=%CE%A1%CF%89%CE%BC%CE%B1%CE%BD%CE%BF%CF%8D+11%2C+"
               "%CE%A0%CE%B5%CF%81%CE%B1%CE%AF%CE%B1%2C+Greece&tll=40.5067925_22.9252194&metroId=1"),
    "lat": 40.5067925,
    "lng": 22.9252194,
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
    "hours_en": [("Monday – Friday", "By appointment"),
                 ("Saturday", "By appointment"),
                 ("Sunday", "Closed")],
    # Where the clinic's work actually happens, from its own contact page.
    "venues": [
        ("Ποδολογικό κέντρο Περαίας", "Ρωμανού 11, Περαία — 3ος όροφος",
         "Η έδρα του ιατρείου. Αξιολόγηση άκρου ποδός, ιατρική ποδολογία, "
         "ορθονυχία και έλεγχος διαβητικού ποδιού."),
        ("Ραντεβού Αθήνας", "Τηλεφωνικά στο 210 958 6060 ή 698 385 0193",
         "Η Ελπινίκη Χριστοδούλου δέχεται περιστατικά και στην Αθήνα. "
         "Καλέστε για διαθεσιμότητα και τόπο συνάντησης."),
    ],
    # Areas the clinic actually draws patients from, declared once as areaServed
    # instead of one near-duplicate landing page per suburb (doorway pages).
    "areas": ["Περαία", "Νέοι Επιβάτες", "Αγία Τριάδα", "Νέα Μηχανιώνα", "Επανομή",
              "Πλαγιάρι", "Θέρμη", "Θεσσαλονίκη", "Καλαμαριά", "Ν. Κρήνη",
              "Χαλκιδική", "Αθήνα"],
    "credit": {"name": "CLINICBRAIN",
               "url": "https://clinicbrain.gr/?utm_source=client-site"
                      "&utm_medium=footer&utm_campaign=made-by"},
    "social": {
        "facebook": "https://www.facebook.com/lpodology",
        "tiktok": "https://www.tiktok.com/@enso.foot.clinic",
    },
}

# ── The practitioner ─────────────────────────────────────────────────────────
# Ensō is one professional, not a multi-specialty team. Every line below is from
# the clinic's own «Σχετικά» page.
PRACTITIONER = {
    "slug": "elpiniki-christodoulou",
    "name": "Ελπινίκη Χριστοδούλου",
    "name_en": "Elpiniki Christodoulou",
    "role": "Ποδολόγος · υπεύθυνη του ιατρείου",
    "role_en": "Podologist · clinical lead",
    "since": "2002",
    "years": "19+",
    "photo": "elpiniki-christodoulou.svg",
    "quote": ("Η βαρύτητα μπορεί να γίνει ο καλύτερος σου σύμμαχος αφού πρώτα "
              "κάνεις τον ποδίατρο καλύτερο σου φίλο."),
    "quote_en": ("Gravity can become your best ally — once you have made the "
                 "podiatrist your best friend."),
    "blurb": ("Ποδολόγος με πάνω από 19 χρόνια στη θεραπεία του άκρου ποδός και "
              "στην αισθητική περιποίησή του. Από το 2002 προσφέρει θεραπείες με "
              "μετρήσιμο αποτέλεσμα σε όσους ταλαιπωρούνται από προβλήματα στα κάτω άκρα."),
    "blurb_en": ("Podologist with more than 19 years in foot therapy and foot "
                 "aesthetics. Practising since 2002."),
    "credentials": [
        ("2002 → σήμερα", "Owner, Trellis Podology &amp; Nails — Θεσσαλονίκη"),
        ("Εκπαίδευση", "Οργανώτρια &amp; εισηγήτρια επαγγελματικών σεμιναρίων, "
                       "workshops &amp; masterclasses"),
        ("Ι.ΙΕΚ Ξίνη", "Εκπαιδεύτρια ποδολογίας και nail art, Μουδανιά Χαλκιδικής"),
        ("2006 – 2015", "NBM Germany — Exclusive Sales Supplier &amp; Academy "
                        "Instructor για τη Βόρεια Ελλάδα"),
        ("Lefas coiffure", "In-store υπηρεσίες ποδολογίας και τεχνικού νυχιών"),
        ("Β. Όλγας 181", "Ποδολογικό κέντρο, Θεσσαλονίκη"),
        ("Ρωμανού 11", "Ποδολογικό κέντρο, Περαία Θεσσαλονίκης"),
    ],
}

# ── Conditions ────────────────────────────────────────────────────────────────
# The four conditions Ensō publishes. `zone` ties each entry to a hotspot in the
# foot diagram.
CONDITIONS = [
    dict(slug="diavitiko-podi", legacy="diavitiko-podi", zone="circulation",
         title="Διαβητικό πόδι",
         meta="Διαβητικό πόδι: γιατί η νευροπάθεια και η αγγειοπάθεια κρύβουν τις πληγές, "
              "τι περιλαμβάνει ο ετήσιος έλεγχος και πώς προλαμβάνεται το έλκος.",
         lead="Ο διαβήτης μειώνει την αίσθηση και την κυκλοφορία στα πόδια. Το πρόβλημα "
              "δεν είναι ότι πονάει — είναι ότι δεν πονάει, και έτσι περνά απαρατήρητο.",
         plain="Έχω διαβήτη και δεν νιώθω καλά τα πόδια μου.",
         stat=("1 φορά/χρόνο", "ο ελάχιστος έλεγχος"),
         treatments=["elenchos-diavitikou-podiou", "iatriki-podologia"]),

    dict(slug="skliryseis-kaloi-tyloi", legacy="skliryseis-kaloi-tyloi", zone="forefoot",
         title="Σκληρύνσεις, κάλοι & τύλοι",
         meta="Σκληρύνσεις, κάλοι και τύλοι: γιατί δημιουργούνται από την πίεση, ποια είναι "
              "η διαφορά τους και γιατί η αφαίρεση χωρίς αποφόρτιση τους φέρνει πίσω.",
         lead="Όπου το πέλμα δέχεται συνεχή πίεση και τριβή, το δέρμα αμύνεται πυκνώνοντας. "
              "Η σκλήρυνση εξελίσσεται σε τύλο και ο τύλος σε κάλο με πυρήνα που πονά.",
         plain="Πονάω σαν να πατάω πάνω σε πετραδάκι.",
         stat=("Πίεση", "το κοινό αίτιο και των τριών"),
         treatments=["afairesi-kalon-tylon", "iatriki-podologia"]),

    dict(slug="ksirodermia-pelmaton", legacy="ksirodermia-pelmaton", zone="heel",
         title="Ξηροδερμία πελμάτων & ραγάδες",
         meta="Ξηροδερμία πελμάτων και ραγάδες πτέρνας: γιατί η κρέμα μόνη της δεν αρκεί, "
              "πότε η ραγάδα γίνεται πύλη εισόδου για μικρόβια και τι κάνει η ποδολογία.",
         lead="Η τραχύτητα και η πάχυνση του δέρματος, ιδίως στην πτέρνα, είναι το σήμα της "
              "ξηρότητας. Χωρίς απομάκρυνση του νεκρού ιστού, η ενυδάτωση δεν φτάνει ποτέ "
              "εκεί που χρειάζεται.",
         plain="Οι φτέρνες μου σκάνε και πονάνε όταν περπατάω.",
         stat=("Πτέρνα", "η πιο συχνή εστία"),
         treatments=["therapeia-ksirodermias", "iatriki-podologia"]),

    dict(slug="eisfriksi-nychiou", legacy="eisfriksi-nychiou", zone="nail",
         title="Είσφρηση όνυχος (ονυχοκρύπτωση)",
         meta="Είσφρηση όνυχος: αίτια, συμπτώματα και ανώδυνη αντιμετώπιση με υαλώδεις "
              "νάρθηκες ορθονυχίας — αναίμακτα, χωρίς αφαίρεση του νυχιού.",
         lead="Συχνή και επίπονη παθολογία του νυχιού, συγγενής ή επίκτητη μετά από τραύμα. "
              "Η αυξημένη καμπυλότητα ή η ανισορροπία πλάτους νυχιού και κοίτης το σπρώχνει "
              "μέσα στην πτυχή του δέρματος.",
         plain="Το νύχι μου μπαίνει στο δέρμα και πονάει.",
         stat=("96%", "επιτυχία με νάρθηκα ορθονυχίας"),
         treatments=["orthonychia-narthikes", "iatriki-podologia"]),
]

# ── Services / treatments ────────────────────────────────────────────────────
# `matrix` powers the comparison tool on /ypiresies/.
# `kind`: prevention (έλεγχος) · care (ποδολογική πράξη) · device (θεραπευτική εφαρμογή)
TREATMENTS = [
    dict(slug="elenchos-diavitikou-podiou", legacy="elenchos-diavitikou-podiou",
         title="Έλεγχος διαβητικού ποδιού",
         short="Αξιολόγηση & πρόληψη",
         meta="Έλεγχος διαβητικού ποδιού: αξιολόγηση αίσθησης με μονόινο, έλεγχος σφύξεων, "
              "δέρματος και υποδημάτων. Μία φορά τον χρόνο κατ' ελάχιστον.",
         lead="Δομημένη αξιολόγηση αίσθησης, κυκλοφορίας, δέρματος και υποδημάτων, ώστε το "
              "πρόβλημα να βρεθεί πριν γίνει πληγή.",
         kind="prevention",
         matrix=dict(setting="Στο ιατρείο", sensation="Ανώδυνος έλεγχος",
                     sessions="1 φορά/χρόνο κατ' ελάχιστον", duration="30–40 λεπτά",
                     after="Γραπτό πλάνο φροντίδας", pain="Χωρίς πόνο"),
         treats=["Διαβητική νευροπάθεια", "Περιφερική αγγειοπάθεια",
                 "Σημεία υπερπίεσης", "Πρόληψη έλκους"]),

    dict(slug="iatriki-podologia", legacy="iatriki-podologia",
         title="Ιατρική ποδολογία",
         short="Κλινική περιποίηση άκρου ποδός",
         meta="Ιατρική ποδολογία: αποστειρωμένη, ανώδυνη κλινική περιποίηση πελμάτων και "
              "νυχιών με φρέζα και νυστέρι. Δεν είναι pedicure — είναι θεραπευτική πράξη.",
         lead="Η βασική συνεδρία του ιατρείου: αξιολόγηση, αποστειρωμένα εργαλεία, "
              "θεραπευτική περιποίηση δέρματος και νυχιών, οδηγίες για το σπίτι.",
         kind="care",
         matrix=dict(setting="Στο ιατρείο", sensation="Ανώδυνη",
                     sessions="Κάθε 6–8 εβδομάδες", duration="45–60 λεπτά",
                     after="Περπατάτε αμέσως", pain="Χωρίς πόνο"),
         treats=["Πάχυνση νυχιών", "Σκληρύνσεις", "Ξηροδερμία", "Φροντίδα ευπαθούς ποδιού"]),

    dict(slug="afairesi-kalon-tylon", legacy="afairesi-kalon-tylon",
         title="Αφαίρεση κάλων & τύλων",
         short="Αποφόρτιση & καθαρισμός",
         meta="Αφαίρεση κάλων και τύλων με νυστέρι και φρέζα, χωρίς πόνο και χωρίς αίμα, "
              "μαζί με αποφόρτιση του σημείου ώστε να μην επιστρέψουν.",
         lead="Ο πυρήνας του κάλου αφαιρείται στρώση-στρώση με αποστειρωμένο νυστέρι. Η "
              "ανακούφιση είναι άμεση — αλλά η δουλειά είναι να φύγει και η πίεση.",
         kind="care",
         matrix=dict(setting="Στο ιατρείο", sensation="Ανώδυνη",
                     sessions="1 συνεδρία · επανέλεγχος 6–8 εβδ.", duration="30–45 λεπτά",
                     after="Περπατάτε αμέσως", pain="Χωρίς πόνο"),
         treats=["Κάλοι με πυρήνα", "Τύλοι", "Σκληρύνσεις", "Μεσοδακτύλιοι κάλοι"]),

    dict(slug="therapeia-ksirodermias", legacy="therapeia-ksirodermias",
         title="Θεραπεία ξηροδερμίας & ραγάδων",
         short="Απολέπιση & ενυδάτωση",
         meta="Θεραπεία ξηροδερμίας πελμάτων και ραγάδων πτέρνας: απομάκρυνση νεκρού ιστού, "
              "κλείσιμο των ραγάδων και πρωτόκολλο ενυδάτωσης με ουρία για το σπίτι.",
         lead="Πρώτα φεύγει ο νεκρός ιστός, μετά μπαίνει η ενυδάτωση. Με την αντίστροφη "
              "σειρά, η κρέμα μένει πάνω στο σκληρό δέρμα και δεν κάνει τίποτα.",
         kind="care",
         matrix=dict(setting="Στο ιατρείο", sensation="Ανώδυνη",
                     sessions="1–3 συνεδρίες", duration="40–50 λεπτά",
                     after="Ενυδάτωση καθημερινά στο σπίτι", pain="Χωρίς πόνο"),
         treats=["Ραγάδες πτέρνας", "Ξηροδερμία πελμάτων", "Απολέπιση", "Πρόληψη λοίμωξης"]),

    dict(slug="orthonychia-narthikes", legacy="orthonychia-narthikes",
         title="Ορθονυχία με υαλώδεις νάρθηκες",
         short="Διόρθωση καμπυλότητας νυχιού",
         meta="Ορθονυχία: υαλώδης νάρθηκας που ανασηκώνει σταδιακά το νύχι που εισφρύει. "
              "Ανώδυνη, αναίμακτη θεραπεία με προσωπικό ποσοστό επιτυχίας 96%.",
         lead="Ένας λεπτός υαλώδης νάρθηκας κολλάται πάνω στο νύχι και το ξαναμαθαίνει να "
              "μεγαλώνει επίπεδο. Καμία τομή, κανένα ράμμα, καμία απώλεια νυχιού.",
         kind="device",
         matrix=dict(setting="Στο ιατρείο", sensation="Ανώδυνη &amp; αναίμακτη",
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

# ── Symptom guide ─────────────────────────────────────────────────────────────
# Plain-language statements, weighted towards the four conditions above. This is
# orientation, not diagnosis — the result screen says so explicitly.
GUIDE_STEPS = [
    dict(id="main", type="multi",
         q="Τι σας απασχολεί περισσότερο;",
         help="Διαλέξτε όσα σας ταιριάζουν. Δεν υπάρχει σωστή απάντηση.",
         options=[
             ("hard-spot", "Έχω ένα σκληρό, κιτρινωπό σημείο στο πέλμα",
              {"skliryseis-kaloi-tyloi": 4}),
             ("stone", "Πονάω σαν να πατάω πάνω σε πετραδάκι",
              {"skliryseis-kaloi-tyloi": 4}),
             ("between-toes", "Έχω κάτι σκληρό ανάμεσα στα δάχτυλα",
              {"skliryseis-kaloi-tyloi": 3}),
             ("cracks", "Οι φτέρνες μου έχουν σκάσει",
              {"ksirodermia-pelmaton": 4}),
             ("rough", "Το δέρμα των πελμάτων μου είναι τραχύ και παχύ",
              {"ksirodermia-pelmaton": 3, "skliryseis-kaloi-tyloi": 1}),
             ("nail-pain", "Το νύχι μου πονάει στην άκρη ή στο πλάι",
              {"eisfriksi-nychiou": 4}),
             ("nail-red", "Το δέρμα γύρω από το νύχι είναι κόκκινο και πρησμένο",
              {"eisfriksi-nychiou": 4}),
             ("nail-curve", "Τα νύχια μου είναι πολύ κυρτά ή χοντρά",
              {"eisfriksi-nychiou": 2}),
             ("numb", "Νιώθω μούδιασμα, κάψιμο ή μυρμήγκιασμα στα πόδια",
              {"diavitiko-podi": 4}),
             ("cold", "Τα πόδια μου είναι κρύα ή αλλάζουν χρώμα",
              {"diavitiko-podi": 3}),
             ("wound", "Έχω πληγή ή δορά που δεν κλείνει",
              {"diavitiko-podi": 4}),
             ("look", "Με ενοχλεί κυρίως η εμφάνιση των ποδιών μου", {}),
         ]),
    dict(id="diabetes", type="single",
         q="Έχετε διαβήτη ή προδιαβήτη;",
         help="Αλλάζει τελείως το πόσο επείγει ένα φαινομενικά μικρό πρόβλημα.",
         options=[("yes", "Ναι", {"diavitiko-podi": 5}),
                  ("borderline", "Οριακά σάκχαρα / προδιαβήτης", {"diavitiko-podi": 3}),
                  ("no", "Όχι", {}),
                  ("unsure", "Δεν ξέρω", {"diavitiko-podi": 1})]),
    dict(id="context", type="multi",
         q="Ισχύει κάτι από τα παρακάτω;",
         help="Προαιρετικό. Μας δείχνει από πού έρχεται η πίεση.",
         options=[
             ("standing", "Στέκομαι ή περπατάω πολλές ώρες την ημέρα",
              {"skliryseis-kaloi-tyloi": 2, "ksirodermia-pelmaton": 1}),
             ("tight", "Φοράω στενά, μυτερά ή ψηλοτάκουνα παπούτσια",
              {"skliryseis-kaloi-tyloi": 2, "eisfriksi-nychiou": 2}),
             ("cut", "Κόβω μόνος/η μου τα νύχια στρογγυλά ή πολύ κοντά",
              {"eisfriksi-nychiou": 3}),
             ("sport", "Τρέχω ή κάνω άθλημα με πολλή επιβάρυνση στο πέλμα",
              {"skliryseis-kaloi-tyloi": 1, "eisfriksi-nychiou": 1}),
             ("none", "Τίποτα από αυτά", {}),
         ]),
    dict(id="impact", type="single",
         q="Πόσο επηρεάζει την καθημερινότητά σας;",
         help="",
         options=[("low", "Ελάχιστα — απλώς με ενοχλεί", {}),
                  ("mid", "Αρκετά — αλλάζω παπούτσια ή αποφεύγω το περπάτημα", {}),
                  ("high", "Πολύ — πονάω κάθε μέρα", {})]),
]

RED_FLAGS = [
    "Πληγή ή έλκος στο πόδι που δεν κλείνει",
    "Έντονη ερυθρότητα που απλώνεται, πύον ή πυρετός",
    "Δάχτυλο ή περιοχή που μαυρίζει ή χάνει τελείως την αίσθηση",
]

# ── Daily foot-care tracker ──────────────────────────────────────────────────
# Replaces nothing clinical: it just paces the home routine the clinic gives out
# after a session. Everything is stored in the visitor's browser.
TRACKER = [
    dict(id="diabetic", name="Διαβητικό πόδι", desc="Καθημερινή ρουτίνα ασφαλείας",
         meta="5 βήματα · κάθε μέρα",
         items=[
             dict(title="Οπτικός έλεγχος πελμάτων",
                  hint="Και κάτω από τα δάχτυλα, με καθρέφτη ή με βοήθεια."),
             dict(title="Έλεγχος μεσοδακτύλιων χώρων",
                  hint="Υγρασία, μύκητας, μικρές σχισμές."),
             dict(title="Πλύσιμο με χλιαρό νερό & καλό στέγνωμα",
                  hint="Ποτέ μούλιασμα, ποτέ καυτό νερό — η αίσθηση σας ξεγελά."),
             dict(title="Ενυδάτωση — όχι ανάμεσα στα δάχτυλα",
                  hint="Πέλμα και πτέρνα ναι· μεσοδακτύλια όχι."),
             dict(title="Έλεγχος υποδημάτων πριν τα φορέσω",
                  hint="Πετραδάκι, ραφή ή τσαλακωμένος πάτος περνούν απαρατήρητα."),
         ]),
    dict(id="daily", name="Καθημερινή φροντίδα", desc="Για κάθε πόδι, χωρίς πάθηση",
         meta="4 βήματα · κάθε μέρα",
         items=[
             dict(title="Πλύσιμο και στέγνωμα",
                  hint="Ιδίως ανάμεσα στα δάχτυλα."),
             dict(title="Ενυδατική κρέμα με ουρία",
                  hint="Πτέρνα και πέλμα, με ελαφρύ μασάζ."),
             dict(title="Καθαρές, στεγνές κάλτσες",
                  hint="Φυσικές ίνες, χωρίς σφιχτό λάστιχο."),
             dict(title="Εναλλαγή παπουτσιών",
                  hint="Το ίδιο ζευγάρι κάθε μέρα δεν προλαβαίνει να στεγνώσει."),
         ]),
    dict(id="after", name="Μετά τη συνεδρία", desc="Τις πρώτες 7 ημέρες",
         meta="4 βήματα · μία εβδομάδα",
         items=[
             dict(title="Ενυδάτωση πρωί και βράδυ",
                  hint="Το νέο δέρμα χρειάζεται περισσότερη από όση νομίζετε."),
             dict(title="Άνετα παπούτσια, χωρίς πίεση στο σημείο",
                  hint="Αν το σημείο πιέζεται ξανά, ο κάλος επιστρέφει."),
             dict(title="Έλεγχος για ερυθρότητα ή πόνο",
                  hint="Τηλεφωνήστε μας αν κάτι δεν σας αρέσει."),
             dict(title="Χρήση των πελμάτων/επιθεμάτων που σας δόθηκαν",
                  hint="Η αποφόρτιση είναι η μισή θεραπεία."),
         ]),
]

# ── Seminars ─────────────────────────────────────────────────────────────────
# Scaffolding for the teaching side of the practice, which is real and documented
# (organiser and instructor of professional seminars, workshops and masterclasses;
# instructor at Ι.ΙΕΚ Ξίνη; NBM Germany Academy Instructor 2006–2015) but has no
# published programme right now.
#
# Adding a seminar is ONE entry below plus its body in copy_seminars.py. The hub,
# the detail page, the schema, the sitemap and the search index all follow from it.
# Nothing here is invented: the single entry is the seminar the clinic actually
# announced, with only the facts it published.
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
         lead="Το πρώτο διαδικτυακό σεμινάριο του ιατρείου, μια εισαγωγή στη σύγχρονη "
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

# ── Articles ─────────────────────────────────────────────────────────────────
MONTHS = {"Ιαν": "01", "Φεβ": "02", "Μάρ": "03", "Απρ": "04", "Μάιος": "05", "Μάι": "05",
          "Ιούν": "06", "Ιούλ": "07", "Αύγ": "08", "Σεπ": "09", "Οκτ": "10",
          "Νοέ": "11", "Δεκ": "12"}

ARTICLES = [
    ("diavitiko-podi-kathimerinos-elenchos", "Διαβήτης"),
    ("kaloi-kai-tyloi-giati-epistrefoun", "Κάλοι"),
    ("ragades-pternas-ti-na-kanete", "Ξηροδερμία"),
    ("onychokryptosi-narthikas-i-cheirourgeio", "Νύχια"),
    ("onychomykitiasi-anagnorisi-antimetopisi", "Νύχια"),
    ("sosta-ypodimata-pos-ta-epilegoume", "Πρόληψη"),
    ("podologia-i-pedicure-poia-i-diafora", "Ποδολογία"),
    ("frontida-podion-sto-spiti", "Πρόληψη"),
    ("idrosi-kai-kakosmia-podion", "Δέρμα"),
]

# ── Gallery ──────────────────────────────────────────────────────────────────
# Original illustrations drawn for this site — the clinic publishes no clinical
# photography and none was invented. Each entry: (file stem, category, caption).
GALLERY = [
    ("gal-foot-anatomy", "anatomia", "Ζώνες πίεσης του πέλματος — πού εμφανίζονται οι τύλοι"),
    ("gal-nail-anatomy", "anatomia", "Τομή νυχιού: πλάκα, κοίτη και πλάγια πτυχή"),
    ("gal-arch-types", "anatomia", "Κοίλη, φυσιολογική και πλατυποδία — πώς αλλάζει η φόρτιση"),
    ("gal-callus", "pathiseis", "Τύλος και κάλος με πυρήνα σε τομή δέρματος"),
    ("gal-heel-fissure", "pathiseis", "Ραγάδα πτέρνας: πώς σχίζεται το ξηρό δέρμα"),
    ("gal-ingrown", "pathiseis", "Είσφρηση όνυχος — το νύχι πιέζει την πλάγια πτυχή"),
    ("gal-diabetic-foot", "pathiseis", "Διαβητικό πόδι: νευροπάθεια, αγγειοπάθεια, σημεία έλκους"),
    ("gal-onychomycosis", "pathiseis", "Ονυχομυκητίαση: πάχυνση και αποχρωματισμός του νυχιού"),
    ("gal-brace", "therapeies", "Υαλώδης νάρθηκας ορθονυχίας πάνω στο νύχι"),
    ("gal-debridement", "therapeies", "Αφαίρεση τύλου στρώση-στρώση με αποστειρωμένο νυστέρι"),
    ("gal-offloading", "therapeies", "Αποφόρτιση με πέλμα σιλικόνης στο σημείο πίεσης"),
    ("gal-nail-cutting", "frontida", "Σωστό κόψιμο νυχιών: ίσια, όχι στρογγυλά"),
    ("gal-shoe-fit", "frontida", "Πώς πρέπει να πατάει το πόδι μέσα στο παπούτσι"),
    ("gal-daily-check", "frontida", "Ο καθημερινός έλεγχος πελμάτων με καθρέφτη"),
]

GALLERY_CATS = [("anatomia", "Ανατομία"), ("pathiseis", "Παθήσεις"),
                ("therapeies", "Θεραπείες"), ("frontida", "Φροντίδα")]

# ── English pages ────────────────────────────────────────────────────────────
EN_PAGES = [
    ("the-clinic", "en/the-clinic", "The Clinic"),
    ("diabetic-foot-care", "en/diabetic-foot-care", "Diabetic Foot Care"),
    ("calluses-and-corns", "en/calluses-and-corns", "Calluses & Corns"),
    ("dry-cracked-heels", "en/dry-cracked-heels", "Dry & Cracked Heels"),
    ("ingrown-toenail", "en/ingrown-toenail", "Ingrown Toenail"),
    ("medical-pedicure", "en/medical-pedicure", "Medical Pedicure"),
]
