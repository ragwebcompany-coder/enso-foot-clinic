# -*- coding: utf-8 -*-
"""Site data for Ensō Foot Clinic.

Business facts (name, practitioner, credentials, services, NAP, socials) come
from the clinic's own published copy on ensofootclinic.gr. Clinical copy lives
in `copy.py`. Edit this file to change structure, contact details or menus.

Opening hours are NOT published anywhere by the clinic and are therefore left
deliberately non-committal — confirm them before launch:
  · opening hours  → shown as «Κατόπιν ραντεβού», no openingHoursSpecification

Both addresses and all three phone lines come from the clinic's business card
(Sept 2026): Ρωμανού 11, Περαία and Ελ. Βενιζέλου 180, Καλλιθέα.
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
    "address_athens": "Ελ. Βενιζέλου 180, Καλλιθέα",
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
    "hours_en": [("Monday – Friday", "By appointment"),
                 ("Saturday", "By appointment"),
                 ("Sunday", "Closed")],
    # Where the clinic's work actually happens, from its own contact page.
    "venues": [
        ("Ποδολογικό κέντρο Περαίας", "Ρωμανού 11, Περαία — 3ος όροφος",
         "Η έδρα του ποδολογικού κέντρου. Κλινική ποδολογική φροντίδα, "
         "συμβουλευτική υποδήματος, ενδυνάμωση πέλματος και προληπτική φροντίδα."),
        ("Ποδολογικό κέντρο Αθήνας", "Ελ. Βενιζέλου 180, Καλλιθέα",
         "Η Ελπινίκη Χριστοδούλου δέχεται περιστατικά και στην Αθήνα. "
         "Ραντεβού στο 210 958 6060 ή στο 698 385 0193."),
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
    "role": "Ποδολόγος · υπεύθυνη του ποδολογικού κέντρου",
    "role_en": "Podologist · clinical lead",
    "since": "2002",
    "years": "25+",
    "photo": "elpiniki-christodoulou.svg",
    "quote": ("Η βαρύτητα μπορεί να γίνει ο καλύτερος σου σύμμαχος αφού πρώτα "
              "κάνεις τον ποδίατρο καλύτερο σου φίλο."),
    "quote_en": ("Gravity can become your best ally — once you have made the "
                 "podiatrist your best friend."),
    "blurb": ("Ποδολόγος με πάνω από 25 χρόνια στη θεραπεία του άκρου ποδός και "
              "στην αισθητική περιποίησή του. Από το 2002 προσφέρει θεραπείες με "
              "μετρήσιμο αποτέλεσμα σε όσους ταλαιπωρούνται από προβλήματα στα κάτω άκρα."),
    "blurb_en": ("Podologist with more than 25 years in foot therapy and foot "
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

# ── The two centres ──────────────────────────────────────────────────────────
# «Δύο πόλεις. Ένας στόχος.» Both centres are named in every heading, CTA and
# footer line — the clinic asked for that explicitly after seeing only Peraia
# mentioned in places.
#
# `photo` is the photograph of the space, with Ms Christodoulou and her
# collaborators in it, that the clinic asked for. Until those files arrive it
# stays None and the page renders a branded location card instead of captioning
# some other picture as a room we have never seen. Dropping a file into
# site/assets/img/ and naming it here is the whole change.
CENTRES = [
    dict(id="thessaloniki", city="Περαία Θεσσαλονίκης", short="Θεσσαλονίκη",
         address=SITE["address"], postcode=SITE["postcode"],
         phone=SITE["phone"], phone_href=SITE["phone_href"], map=SITE["map"],
         note="Η έδρα του ποδολογικού κέντρου, από το 2002.",
         photo=None, photo_size=None,
         photo_alt="Ο χώρος του ποδολογικού κέντρου στην Περαία Θεσσαλονίκης, "
                   "με την Ελπινίκη Χριστοδούλου και τους συνεργάτες της"),
    dict(id="athina", city="Καλλιθέα Αθήνας", short="Αθήνα",
         address=SITE["address_athens"], postcode=SITE["postcode_athens"],
         phone=SITE["phone_alt"], phone_href=SITE["phone_alt_href"],
         map=SITE["map_athens"],
         note="Το δεύτερο ποδολογικό κέντρο, στην Καλλιθέα.",
         photo=None, photo_size=None,
         photo_alt="Ο χώρος του ποδολογικού κέντρου στην Καλλιθέα Αθήνας, "
                   "με την Ελπινίκη Χριστοδούλου και τους συνεργάτες της"),
]

# ── The E.N.S.O. framework ───────────────────────────────────────────────────
# The clinic's own words, sent 29/09/2026. This is the meaning behind the name
# and it carries the «Ποιοι είμαστε» page. Nothing here is paraphrased: the
# four pillars, the headings and the «Επιστημονικό Δεδομένο» lines are hers.
ENSO_LEDE = "Δύο πόλεις. Ένας στόχος: να κινείστε χωρίς περιορισμούς."

ENSO_LEDE_BODY = ("Η βάση κάθε δραστηριότητας ξεκινά από τα πόδια σας. Στην Αθήνα "
                  "και τη Θεσσαλονίκη, δημιουργήσαμε δύο εξειδικευμένους χώρους "
                  "ποδολογικής φροντίδας αφιερωμένους στην υγεία και την αντοχή "
                  "της βάδισής σας.")

ENSO_INTRO = ("Στο Ensō Foot Clinic, η φροντίδα της κίνησής σας δεν είναι μια ευθεία "
              "γραμμή, αλλά ένας αδιάσπαστος κύκλος λειτουργικότητας. Το όνομά μας "
              "εκφράζει τη φιλοσοφία μας: το πλαίσιο E.N.S.O. αποτελεί την ποδολογική "
              "και εμβιομηχανική βάση για να διατηρήσετε τη λειτουργικότητα, τη "
              "σταθερότητα και τη δραστηριότητά σας σε κάθε ηλικία.")

ENSO_PILLARS = [
    dict(letter="E", en="Endurance", el="Αντοχή",
         head="Η βάση της κίνησης",
         body="Δεν αφορά μόνο τον αθλητισμό, αλλά την ικανότητα του σώματος να "
              "υποστηρίζει την καθημερινή βάδιση με άνεση και χωρίς άσκοπη "
              "καταπόνηση.",
         fact="Η καρδιοαναπνευστική αντοχή αποτελεί βασικό δείκτη γενικής ευεξίας "
              "και μακροζωίας. Ένα λειτουργικό πέλμα ευνοεί τη σταθερή βάδιση, "
              "υποστηρίζοντας την καθημερινή δραστηριότητα."),
    dict(letter="N", en="Neuromuscular Balance", el="Νευρομυϊκή ισορροπία",
         head="Η αισθητηριακή αντίληψη του πέλματος",
         body="Το πόδι λειτουργεί ως πρωταρχικός αισθητήρας. Η ισορροπία βασίζεται "
              "στην ταχύτητα με την οποία οι μηχανοϋποδοχείς του πέλματος "
              "μεταφέρουν ερεθίσματα στο κεντρικό νευρικό σύστημα "
              "(ιδιοδεκτικότητα / proprioception).",
         fact="Η επαρκής νευρομυϊκή συναρμογή συμβάλλει καθοριστικά στον έλεγχο "
              "της ισορροπίας και στη μείωση του κινδύνου αστάθειας. Στο Ensō "
              "εστιάζουμε στη βελτιστοποίηση της επαφής του πέλματος με το έδαφος "
              "μέσω κατάλληλων υποδημάτων και εξειδικευμένης φροντίδας."),
    dict(letter="S", en="Strength", el="Μυϊκή ισχύς",
         head="Η λειτουργική υποστήριξη",
         body="Οι μύες λειτουργούν ως φυσικοί αποσβεστήρες κραδασμών για τις "
              "αρθρώσεις. Χωρίς επαρκή μυϊκή υποστήριξη στα κάτω άκρα, οι αρθρικές "
              "δομές δέχονται αυξημένα φορτία.",
         fact="Η ενδυνάμωση των ενδογενών μυών του ποδιού (foot core) υποστηρίζει "
              "την ποδική καμάρα και προάγει την ομοιόμορφη κατανομή των "
              "πελματιαίων πιέσεων."),
    dict(letter="O", en="Optimal Flexibility", el="Βέλτιστη ευλυγισία",
         head="Η αρμονία της κίνησης",
         body="Η δυσκαμψία περιορίζει τη λειτουργικότητα. Η βέλτιστη ευλυγισία "
              "επιτρέπει στις αρθρώσεις να κινούνται στο φυσιολογικό λειτουργικό "
              "τους εύρος.",
         fact="Ο περιορισμός στη ραχιαία κάμψη της ποδοκνημικής (dorsiflexion "
              "limitation) μεταβάλλει τη μηχανική της βάδισης και σχετίζεται στενά "
              "με αυξημένες τάσεις στην πελματιαία περιτονία (plantar fascia)."),
]

ENSO_WHY = [
    ("Στην ποδολογία", "Όταν διαταραχθεί ένας κρίκος, η βάδιση χάνει την αρμονία της."),
    ("Η συνήθης προσέγγιση", "Συχνά παραβλέπεται η συνολική κινηματική αλυσίδα "
                             "και η πρόληψη."),
    ("Η δική μας προσέγγιση", "Αξιολογούμε εμβιομηχανικά τις ανάγκες του ποδιού "
                              "και στους τέσσερις πυλώνες, καθοδηγώντας σας στη "
                              "σωστή επιλογή υποδημάτων και καθημερινών συνηθειών "
                              "φροντίδας."),
]

ENSO_CLOSE = "Στο Ensō, ολοκληρώνουμε τον κύκλο της λειτουργικής σας κίνησης."

# ── Short biography, by date ─────────────────────────────────────────────────
# The clinic asked for the CV «εν συντομία, βάση χρονολογίου» with a
# «περισσότερα» for whoever wants the rest. The first four entries are the
# summary; `BIO_MORE` is what the disclosure opens. Every line comes from the
# practitioner's own «Σχετικά» page — no date is inferred.
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

# ── Services ─────────────────────────────────────────────────────────────────
# The four services the clinic publishes, defined by the client on 29/09/2026.
# The conditions section and the symptom guide were removed on the same brief:
# the site focuses on what is offered, not on a catalogue of pathologies.
# `matrix` powers the comparison tool on /ypiresies/.
# `kind`: care (ποδολογική πράξη) · advice (συμβουλευτική) ·
#         training (επανεκπαίδευση) · prevention (πρόληψη & έλεγχος)
TREATMENTS = [
    dict(slug="kliniki-podologiki-frontida", legacy="kliniki-podologia",
         title="Κλινική ποδολογική φροντίδα",
         en="Clinical Podology Care",
         short="Υπερκερατώσεις, σκληρύνσεις, ονυχοκρύπτωση",
         meta="Κλινική ποδολογική φροντίδα: εξειδικευμένη περιποίηση σε υπερκερατώσεις "
              "(κάλους), σκληρύνσεις και ονυχοκρύπτωση. Ανώδυνη, ασφαλής, υγιεινή.",
         lead="Εξειδικευμένη περιποίηση και ανακούφιση σε υπερκερατώσεις (κάλους), "
              "σκληρύνσεις και ονυχοκρύπτωση (είσφρυση όνυχος). Ανώδυνη, ασφαλής και "
              "υγιεινή φροντίδα για την αποκατάσταση της άνεσης του πέλματος.",
         kind="care",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνη",
                     sessions="Κάθε 6–8 εβδομάδες", duration="45–60 λεπτά",
                     after="Περπατάτε αμέσως", pain="Χωρίς πόνο"),
         treats=["Υπερκερατώσεις &amp; κάλοι", "Σκληρύνσεις", "Ονυχοκρύπτωση",
                 "Πάχυνση και φροντίδα νυχιών"]),

    dict(slug="athlitiko-ypodima", legacy="athlitiko-ypodima",
         title="Συμβουλευτική &amp; αξιολόγηση αθλητικού υποδήματος",
         en="Athletic Footwear Consulting",
         short="Επιλογή και αξιολόγηση υποδήματος",
         meta="Συμβουλευτική αθλητικού υποδήματος: επιλογή με βάση τη γεωμετρία, το drop "
              "και την απορρόφηση κραδασμών — από τα τεχνικά χαρακτηριστικά στην άνεση.",
         lead="Επιστημονική επιλογή του ιδανικού υποδήματος με βάση τη γεωμετρία, το "
              "drop, την απορρόφηση κραδασμών και τις ανάγκες σας. Καθοδήγηση που "
              "συνδέει τα εργαστηριακά τεχνικά χαρακτηριστικά με την καθημερινή άνεση "
              "ή την αθλητική δραστηριότητα.",
         kind="advice",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Συνεδρία αξιολόγησης",
                     sessions="1 συνεδρία · επανέλεγχος με νέο ζευγάρι",
                     duration="40–50 λεπτά",
                     after="Φεύγετε με γραπτά κριτήρια επιλογής",
                     pain="Χωρίς πόνο"),
         treats=["Γεωμετρία &amp; drop υποδήματος", "Απορρόφηση κραδασμών",
                 "Καθημερινή βάδιση", "Αθλητική δραστηριότητα"]),

    dict(slug="foot-core-training", legacy="foot-core-training",
         title="Λειτουργική επανεκπαίδευση &amp; ενδυνάμωση πέλματος",
         en="Foot Core Training",
         short="Ασκήσεις ενδυνάμωσης και ιδιοδεκτικότητας",
         meta="Foot core training: στοχευμένες ασκήσεις για τους ενδογενείς μύες του "
              "ποδιού και την ιδιοδεκτικότητα — σταθερότητα και ισορροπία.",
         lead="Στοχευμένες ασκήσεις ενδυνάμωσης των ενδογενών μυών και βελτίωσης της "
              "ιδιοδεκτικότητας (proprioception). Ενίσχυση της σταθερότητας και της "
              "ισορροπίας, ιδιαίτερα αποτελεσματική για άτομα μεγαλύτερης ηλικίας και "
              "αθλητές.",
         kind="training",
         matrix=dict(setting="Στο κέντρο &amp; στο σπίτι",
                     sensation="Ενεργητική συμμετοχή",
                     sessions="Πρόγραμμα με επαναξιολόγηση",
                     duration="30–45 λεπτά",
                     after="Ασκήσεις για το σπίτι, γραπτά",
                     pain="Χωρίς πόνο"),
         treats=["Ενδογενείς μύες του ποδιού", "Ιδιοδεκτικότητα",
                 "Σταθερότητα &amp; ισορροπία", "Τρίτη ηλικία και αθλητές"]),

    dict(slug="prolipsi-ypsilou-kindynou", legacy="elenchos-diavitikou-podiou",
         title="Προληπτική φροντίδα υψηλού κινδύνου",
         en="Preventive High-Risk Foot Care",
         short="Ευαίσθητα πέλματα &amp; διαβητικό πόδι",
         meta="Προληπτική φροντίδα υψηλού κινδύνου: έλεγχος και τακτική ποδολογική "
              "φροντίδα για ευαίσθητα πέλματα, όπως το διαβητικό πόδι.",
         lead="Εξειδικευμένος προληπτικός έλεγχος και τακτική ποδολογική φροντίδα για "
              "ευαίσθητα πέλματα (π.χ. διαβητικό πόδι). Έγκαιρη αναγνώριση σημείων "
              "πίεσης και καθοδήγηση για την αποφυγή επιπλοκών και τραυματισμών.",
         kind="prevention",
         matrix=dict(setting="Στο ποδολογικό κέντρο", sensation="Ανώδυνος έλεγχος",
                     sessions="Τακτικά · κατ' ελάχιστον 1 φορά/χρόνο",
                     duration="30–40 λεπτά",
                     after="Γραπτό πλάνο φροντίδας", pain="Χωρίς πόνο"),
         treats=["Διαβητικό πόδι", "Σημεία υπερπίεσης", "Ευαίσθητο δέρμα &amp; νύχια",
                 "Πρόληψη επιπλοκών"]),
]

KIND_LABELS = {
    "care": "Ποδολογική πράξη",
    "advice": "Συμβουλευτική &amp; αξιολόγηση",
    "training": "Λειτουργική επανεκπαίδευση",
    "prevention": "Πρόληψη &amp; έλεγχος",
}

# Column headers of the comparison table, in `matrix` key order.
MATRIX_COLS = [("setting", "Πού γίνεται"), ("sensation", "Αίσθηση"),
               ("sessions", "Συχνότητα"), ("duration", "Διάρκεια"),
               ("after", "Μετά τη συνεδρία")]

# ── When to stop and call someone ────────────────────────────────────────────
# Printed on the services hub. Podology has limits and the site states them
# rather than leaving a visitor to guess.
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
    ("clinical-podology", "en/clinical-podology", "Clinical Podology"),
]


# ── Ποιοι είμαστε: the practitioner's own text (07/10/2026) ──────────────────
# Replaces the old biography («Μια έμπειρη ποδολόγος… 25 χρόνια…») verbatim.
ABOUT_NAME = "Ελπινίκη Χριστοδούλου"
ABOUT_ROLE = "Εξειδικευμένη Ποδολόγος | Ιδρύτρια του Ensō Foot Clinic"
ABOUT_TEXT = [
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
]

# The band at the foot of every page, in the clinic's words (07/10/2026). It
# replaced «Επόμενο βήμα — Δείξτε μας το πόδι σας πριν το λύσετε μόνοι σας».
MOTTO = ("Η βαρύτητα είναι η σταθερά μας.",
         "Το πώς την αποδέχονται τα πέλματά μας καθορίζει όλη μας την κίνηση. "
         "Ας φροντίσουμε ώστε οι αποδέκτες αυτοί να είναι υγιείς και "
         "λειτουργικοί καθημερινά.")

# Company details for /epikoinonia/ and the terms page. A value left as None is
# shown as «θα συμπληρωθεί» and the build prints a reminder — fill in and rebuild.
LEGAL_ROWS = [
    ("Επωνυμία", "Χριστοδούλου Ελπινίκη — Ensō Foot Clinic"),
    ("Δραστηριότητα", "Ποδολογικό κέντρο"),
    ("Έδρα", "Ρωμανού 11, 570 19 Περαία Θεσσαλονίκης (3ος όροφος)"),
    ("Υποκατάστημα", "Λεωφ. Ελ. Βενιζέλου 180, 176 75 Καλλιθέα Αθήνας"),
    ("ΑΦΜ", None),
    ("ΔΟΥ", None),
    ("Αρ. ΓΕΜΗ", None),
    ("Email", "podopure@gmail.com"),
]
