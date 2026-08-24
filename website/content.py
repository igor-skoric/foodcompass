CONTACT = {
    'email': 'office@foodcompass.rs',
    'phone': '+381637707319',
    'phone_display': '+381 63 7707 319',
    'linkedin': 'https://www.linkedin.com/in/sandra-djukanovic-koji%C4%87-599277197/',
}

NAV = [
    {'label': 'O nama', 'url_name': 'about'},
    {'label': 'O meni', 'url_name': 'about_me'},
    {
        'label': 'Naše usluge',
        'url_name': 'services',
        'children': [
            {'label': 'Sistemi i standardi', 'url_name': 'service_detail', 'slug': 'sistemi-i-standardi'},
            {'label': 'ISO standardi', 'url_name': 'service_detail', 'slug': 'iso-standardi'},
            {'label': 'Deklarisanje', 'url_name': 'service_detail', 'slug': 'deklarisanje'},
            {'label': 'Gap analiza', 'url_name': 'service_detail', 'slug': 'gap-analiza'},
            {'label': 'Digitalizacija', 'url_name': 'service_detail', 'slug': 'digitalizacija'},
        ],
    },
    {'label': 'Od ideje do police', 'url_name': 'journey'},
    {'label': 'Stručna podrška', 'url_name': 'support'},
    {'label': 'Aktuelnosti', 'url_name': 'news'},
    {'label': 'Kontakt', 'url_name': 'contact'},
]

SERVICES = [
    {
        'slug': 'sistemi-i-standardi',
        'title': 'Sistemi i standardi bezbednosti hrane',
        'short': 'HACCP | IFS | FSSC 22000 | BRCGS',
        'standards': ['HACCP', 'IFS', 'FSSC 22000', 'BRCGS'],
        'card': 'Uspostavljanje i unapređenje sistema bezbednosti hrane prema međunarodnim standardima.',
        'icon': 'haccp',
        'hero': 'haccp',
        'intro': (
            'Bezbednost hrane nije samo ispunjavanje zakonskih zahteva. Dobro postavljen sistem '
            'treba da bude razumljiv, funkcionalan i prilagođen stvarnom poslovanju.'
        ),
        'lead': (
            'Food Compass pruža stručnu podršku kompanijama u uspostavljanju, unapređenju, proveri '
            'i pripremi sistema bezbednosti hrane prema zahtevima nacionalnih propisa i međunarodno '
            'priznatih standarda.'
        ),
        'items': [
            {
                'title': 'HACCP',
                'text': (
                    'Uspostavljanje, revizija i unapređenje HACCP sistema, uključujući identifikaciju '
                    'opasnosti, procenu rizika, određivanje kontrolnih mera i verifikaciju sistema.'
                ),
            },
            {
                'title': 'FSSC 22000',
                'text': (
                    'Podrška u razvoju i unapređenju sistema upravljanja bezbednošću hrane prema zahtevima '
                    'FSSC 22000 i pripremi organizacije za sertifikaciju i audit.'
                ),
            },
            {
                'title': 'IFS',
                'text': (
                    'Podrška kompanijama u razumevanju i primeni IFS zahteva, proceni usaglašenosti, '
                    'unapređenju sistema i pripremi za IFS audit.'
                ),
            },
            {
                'title': 'BRC',
                'text': (
                    'Podrška u uspostavljanju i unapređenju sistema prema zahtevima BRCGS standarda '
                    'i pripremi organizacije za sertifikaciju.'
                ),
            },
        ],
    },
    {
        'slug': 'iso-standardi',
        'title': 'ISO standardi',
        'short': 'ISO 9001 | ISO 22000',
        'standards': ['ISO 9001', 'ISO 22000'],
        'card': 'Implementacija sistema upravljanja kvalitetom i bezbednošću hrane prilagođenih vašem poslovanju.',
        'icon': 'iso',
        'hero': 'iso',
        'intro': (
            'Podrška kompanijama u uspostavljanju, unapređenju i proveri sistema upravljanja prema '
            'međunarodno priznatim ISO standardima, sa fokusom na kvalitet i bezbednost hrane.'
        ),
        'lead': 'Od usklađenosti sa zahtevima do sistema koji funkcioniše u praksi.',
        'items': [
            {
                'title': 'ISO 9001 – Sistem menadžmenta kvalitetom',
                'text': (
                    'Podrška u uspostavljanju, unapređenju i internoj proveri sistema upravljanja kvalitetom '
                    'prema zahtevima ISO 9001, kao i u pripremi organizacije za sertifikaciju. '
                    'ISO 9001 Lead Auditor – IRCA/CQI sertifikovana obuka.'
                ),
            },
            {
                'title': 'ISO 22000 – Sistem menadžmenta bezbednošću hrane',
                'text': (
                    'Podrška u uspostavljanju, unapređenju i održavanju sistema upravljanja bezbednošću hrane '
                    'prema zahtevima ISO 22000, uz povezivanje sa HACCP principima i drugim relevantnim '
                    'zahtevima bezbednosti hrane.'
                ),
            },
        ],
    },
    {
        'slug': 'deklarisanje',
        'title': 'Deklarisanje prehrambenih proizvoda',
        'short': 'Od recepture do usaglašene deklaracije – jasno, precizno i bez nepotrebne komplikacije.',
        'standards': [],
        'card': 'Od recepture do usklađene deklaracije — jasno, precizno i bez nepotrebne komplikacije.',
        'icon': 'deklarisanje',
        'hero': 'deklarisanje',
        'intro': (
            'Pravilna deklaracija je više od ispunjavanja zakonske obaveze – ona je važan deo usaglašenosti '
            'proizvoda, bezbednosti potrošača i njegovog nastupa na tržištu.'
        ),
        'lead': (
            'Food Compass pruža stručnu podršku u izradi, proveri i unapređenju deklaracija prehrambenih '
            'proizvoda, od analize recepture i sastava do konačne provere informacija na ambalaži.'
        ),
        'items': [
            {
                'title': 'Kompletna izrada deklaracija',
                'text': (
                    'Definisanje i provera svih obaveznih elemenata deklaracije, uključujući naziv proizvoda, '
                    'spisak sastojaka, alergene, neto količinu, rok trajanja, uslove čuvanja, podatke o '
                    'odgovornom subjektu i druge obavezne informacije.'
                ),
            },
            {
                'title': 'Nutritivna deklaracija i proračuni',
                'text': (
                    'Proračun i provera nutritivnih vrednosti i priprema nutritivne deklaracije u skladu '
                    'sa važećim zahtevima.'
                ),
            },
            {
                'title': 'Alergeni, nutritivne i zdravstvene tvrdnje',
                'text': (
                    'Provera pravilnog navođenja i isticanja alergena, kao i stručna podrška u vezi sa '
                    'korišćenjem nutritivnih i zdravstvenih tvrdnji (nutrition & health claims).'
                ),
            },
            {
                'title': 'Compliance Check – provera usaglašenosti',
                'text': (
                    'Detaljna provera postojećih deklaracija i ambalaže u odnosu na važeće propise, uz '
                    'identifikaciju potencijalnih neusaglašenosti i preporuke za njihovo otklanjanje.'
                ),
            },
            {
                'title': 'Višejezične deklaracije i izvoz',
                'text': (
                    'Priprema i kontrola deklaracija za različita tržišta, uključujući usklađivanje sadržaja '
                    'sa zahtevima ciljne zemlje i stručnu kontrolu prevoda.'
                ),
            },
            {
                'title': 'Ažuriranje i kontinuirana podrška',
                'text': (
                    'Praćenje promena relevantnih propisa i ažuriranje deklaracija, uz stručnu podršku pri '
                    'promenama recepture, ambalaže, tržišta ili regulatornih zahteva.'
                ),
            },
        ],
    },
    {
        'slug': 'gap-analiza',
        'title': 'Gap analiza i priprema za audit',
        'short': 'Da li je vaš sistem zaista spreman za audit?',
        'standards': [],
        'card': 'Proveravamo koliko je vaš sistem zaista spreman za audit i definišemo šta treba unaprediti.',
        'icon': 'gap',
        'hero': 'gap',
        'intro': (
            'Kroz stručnu procenu postojećeg sistema utvrđujemo nivo usaglašenosti sa zahtevima relevantnog '
            'standarda i identifikujemo oblasti koje je potrebno unaprediti pre audita.'
        ),
        'lead': (
            'Podrška je namenjena kompanijama koje se pripremaju za IFS, FSSC 22000, BRCGS, ISO 22000 '
            'ili ISO 9001 audit.'
        ),
        'list_title': 'Gap analiza obuhvata:',
        'list_items': [
            'pregled dokumentacije i procedura',
            'proveru primene sistema u praksi',
            'identifikaciju neusaglašenosti i potencijalnih rizika',
            'definisanje potrebnih korektivnih i unapređujućih mera',
            'prioritizaciju aktivnosti i preporuke za pripremu audita',
        ],
        'closer': (
            'Cilj nije samo uspešno proći audit, već izgraditi sistem koji je usaglašen, funkcionalan '
            'i održiv u svakodnevnom poslovanju.'
        ),
        'items': [],
    },
    {
        'slug': 'digitalizacija',
        'title': 'Digitalizacija sistema bezbednosti hrane',
        'short': 'Digital HACCP | Digital IFS | Digital FSSC 22000 | Digital BRCGS',
        'standards': ['Digital HACCP', 'Digital IFS', 'Digital FSSC 22000', 'Digital BRCGS'],
        'card': 'Prebacite dokumentaciju, kontrolne liste i evidencije sa papira u jednostavan i pregledan digitalni sistem.',
        'icon': 'digitalizacija',
        'hero': 'digital',
        'intro': 'Manje papira. Više kontrole. Bolji sistem.',
        'lead': (
            'Digitalizacija omogućava da sistemi bezbednosti hrane pređu iz fascikli, tabela i papirnih '
            'evidencija u jedno povezano digitalno okruženje. Food Compass pruža podršku u digitalizaciji '
            'sistema kao što su HACCP, IFS, FSSC 22000 i BRCGS, sa ciljem da svakodnevno upravljanje '
            'zahtevima bezbednosti hrane bude jednostavnije, preglednije i efikasnije.'
        ),
        'items': [
            {
                'title': 'Digitalni HACCP i sistemi upravljanja',
                'text': (
                    'Digitalizacija procedura, planova, evidencija, kontrolnih lista i drugih elemenata '
                    'sistema bezbednosti hrane, uz mogućnost praćenja realizacije u realnom vremenu.'
                ),
            },
            {
                'title': 'Digitalne evidencije',
                'text': (
                    'Čišćenje, dezinfekcija, kontrola štetočina, održavanje, prijem sirovina, temperature '
                    'i druge operativne kontrole mogu se voditi digitalno, bez nepotrebne papirne administracije.'
                ),
            },
            {
                'title': 'Automatsko praćenje i upozorenja',
                'text': (
                    'Povezivanje sa senzorima i drugim digitalnim uređajima omogućava kontinuirano praćenje '
                    'ključnih parametara, uz automatska upozorenja u slučaju odstupanja.'
                ),
            },
            {
                'title': 'Zadaci i odgovornosti u realnom vremenu',
                'text': (
                    'Zaposleni dobijaju jasne zadatke i obaveze, dok odgovorna lica mogu pratiti njihovu '
                    'realizaciju i reagovati na odstupanja bez čekanja na papirne izveštaje.'
                ),
            },
            {
                'title': 'Spremnost za audit',
                'text': (
                    'Dokazi o sprovedenim kontrolama, evidencije, odstupanja, korektivne mere i izveštaji '
                    'dostupni su na jednom mestu, što značajno olakšava pripremu i sprovođenje internih '
                    'i eksternih audita.'
                ),
            },
            {
                'title': 'Sledljivost i dostupnost podataka',
                'text': (
                    'Digitalno praćenje podataka omogućava bolju sledljivost procesa i proizvoda, brži pristup '
                    'informacijama i jednostavnije donošenje odluka na osnovu dostupnih podataka.'
                ),
            },
        ],
        'closer': (
            'Digitalizacija nije samo zamena papira ekranom. To je način da sistem bezbednosti hrane '
            'postane vidljiv, merljiv i upravljiv u realnom vremenu.'
        ),
    },
]

JOURNEY = [
    {
        'id': 'od-ideje',
        'title': 'Od ideje',
        'lead': 'Definisanje proizvoda i regulatornih zahteva',
        'intro': 'Prvi korak je da se proizvod pravilno definiše i utvrdi šta je potrebno da bi mogao da bude stavljen na tržište.',
        'items': [
            'analiza proizvoda i njegove namene',
            'definisanje odgovarajućeg naziva proizvoda',
            'izrada proizvođačke specifikacije',
            'identifikacija relevantnih propisa i zahteva',
            'usklađivanje proizvoda sa zahtevima tržišta',
        ],
        'image': '01-idea',
    },
    {
        'id': 'do-bezbednog-proizvoda',
        'title': '…I bezbednog proizvoda',
        'lead': 'HACCP sistemi bezbednosti hrane',
        'intro': 'Kada je proizvod definisan, potrebno je uspostaviti sistem koji obezbeđuje njegovu bezbednost tokom proizvodnje.',
        'items': [
            'procena objekta i procesa',
            'definisanje higijenskih i drugih preduslova',
            'identifikacija i procena opasnosti',
            'analiza bioloških, hemijskih i fizičkih/mehaničkih opasnosti',
            'uspostavljanje HACCP sistema i potrebne dokumentacije',
            'uspostavljanje sledljivosti',
            'obuka zaposlenih',
            'podrška u digitalizaciji sistema',
        ],
        'image': '02-direction',
    },
    {
        'id': 'do-police',
        'title': 'Do police',
        'lead': 'Deklarisanje i konačna provera usaglašenosti',
        'intro': 'Pre stavljanja proizvoda na tržište proveravamo da li su proizvod i njegova deklaracija usklađeni sa relevantnim zahtevima.',
        'items': [
            'planiranje potrebnih laboratorijskih analiza',
            'izrada i provera deklaracije',
            'pravilno označavanje alergena',
            'nutritivna deklaracija',
            'provera usaglašenosti proizvoda i dokumentacije',
            'podrška u pripremi za kontrole i audite',
        ],
        'image': '03-shelf',
    },
]

ABOUT = {
    'title': 'O nama',
    'eyebrow': 'Zašto izabrati baš nas?',
    'hero_lead': (
        'Food Compass je stručni i konsultantski koncept usmeren na bezbednost hrane, '
        'regulatornu usaglašenost i unapređenje sistema upravljanja u poslovanju hranom.'
    ),
    'quote': 'Da smo znali da to treba, sigurno bismo to i uradili – ali nismo znali.',
    'quote_context': (
        'Kao osnivač Food Compass-a i stručnjak sa više od 22 godine iskustva u oblasti '
        'bezbednosti hrane, ovu rečenicu sam čula bezbroj puta.'
    ),
    'origin': (
        'Upravo ona bila je jedan od glavnih motiva da pokrenem Food Compass – kao jasan '
        'vodič kroz sve zahteve koje bezbednost hrane podrazumeva, od ideje do police.'
    ),
    'what': [
        'Food Compass je stručni i konsultantski koncept usmeren na bezbednost hrane, '
        'regulatornu usaglašenost i unapređenje sistema upravljanja u poslovanju hranom.',
        'Naš pristup povezuje stručno znanje, praktično iskustvo i savremena rešenja kako '
        'bi kompanijama omogućio da zahteve bezbednosti hrane ne posmatraju samo kao obavezu, '
        'već kao deo efikasnog, održivog i dobro organizovanog poslovanja.',
    ],
    'principles': [
        {'title': 'Stručnost', 'text': 'Znanje i iskustvo'},
        {'title': 'Praktičnost', 'text': 'Rešenja primenljiva u svakodnevnom poslovanju'},
        {'title': 'Savremen pristup', 'text': 'Efikasniji i digitalizovani sistemi'},
    ],
    'areas_intro': (
        'Pružamo podršku u oblastima HACCP sistema, bezbednosti hrane, regulatorne '
        'usaglašenosti, pripreme za audite i sertifikaciju, kao i digitalizacije sistema '
        'upravljanja bezbednošću hrane.'
    ),
    'areas': [
        {'title': 'HACCP sistemi', 'icon': 'haccp'},
        {'title': 'Bezbednost hrane', 'icon': 'food'},
        {'title': 'Regulatorna usaglašenost', 'icon': 'iso'},
        {'title': 'Priprema za audite', 'icon': 'gap'},
        {'title': 'Priprema za sertifikaciju', 'icon': 'badge'},
        {'title': 'Digitalizacija sistema upravljanja bezbednošću hrane', 'icon': 'digitalizacija'},
    ],
    'value': (
        'Posebna vrednost Food Compass-a je u tome što složene stručne i regulatorne zahteve '
        'prevodimo u jasna, praktična i primenljiva rešenja koja mogu da se koriste u '
        'svakodnevnom poslovanju.'
    ),
    'founder_name': 'Sandra Đukanović Kojić',
    'founder_role': 'Master inženjer biohemijskog inženjerstva i biotehnologije',
    'founder_specialty': 'Specijalista za bezbednost hrane',
    'founder_body': [
        'Food Compass je nastao na osnovu više od dve decenije praktičnog iskustva Sandre Đukanović Kojić, master inženjera biohemijskog inženjerstva i biotehnologije i specijaliste za bezbednost hrane, u oblasti službenih kontrola, HACCP sistema, procene rizika i regulatorne usaglašenosti.',
        'Iskustvo stečeno u državnom sistemu kontrole hrane, rad na međunarodnim projektima i kontinuirano stručno usavršavanje u oblasti audita, sertifikacije i međunarodnih standarda predstavljaju stručnu osnovu na kojoj je razvijen Food Compass.',
    ],
    'expertise': [
        {'value': '22+', 'label': 'godine iskustva'},
        {'value': 'HACCP', 'label': 'sistemi i procena rizika'},
        {'value': 'Auditi', 'label': 'i sertifikacija'},
        {'value': 'Regulativa', 'label': 'i službene kontrole hrane'},
        {'value': 'Međunarodno iskustvo', 'label': 'projekti i standardi'},
    ],
    'goal_title': 'Bezbednost hrane treba da bude razumljiva, efikasna i laka za upravljanje.',
    'goal': 'Naš cilj je jednostavan – da bezbednost hrane učinimo razumljivijom, efikasnijom i lakšom za upravljanje.',
}

ABOUT_ME = {
    'title': 'O meni',
    'name': 'Sandra Đukanović Kojić',
    'initials': 'SĐK',
    'role': 'Master inženjer biohemijskog inženjerstva i biotehnologije',
    'role_extra': 'Specijalista za bezbednost hrane',
    'lead': 'Više od 22 godine profesionalnog iskustva, uz dugogodišnji rad u oblasti bezbednosti hrane, službenih kontrola, HACCP sistema, procene rizika i usaglašenosti sa nacionalnim i evropskim propisima.',
    'quote': 'Verujem da dobar sistem bezbednosti hrane ne treba da bude samo dokumentacija.',
    'facts': [
        {'value': '22+', 'label': 'godina iskustva'},
        {'value': 'TMF', 'label': 'Univerzitet u Beogradu'},
        {'value': 'IRCA', 'label': 'ISO 9001 Lead Auditor'},
    ],
    'paragraphs': [
        'Moje stručno obrazovanje stekla sam na Tehnološko-metalurškom fakultetu Univerziteta u Beogradu, gde sam završila master studije biohemijskog inženjerstva i biotehnologije, kao i specijalizaciju u oblasti bezbednosti hrane.',
        'Tokom profesionalne karijere kontinuirano sam unapređivala svoja znanja kroz domaće i međunarodne obuke iz oblasti HACCP-a, higijene hrane, auditiranja, regulatorne usaglašenosti i sistema upravljanja bezbednošću hrane.',
        'Najveći deo profesionalne karijere provela sam u Ministarstvu poljoprivrede, šumarstva i vodoprivrede Republike Srbije, kao republički inspektor za bezbednost hrane. Rad u sistemu službenih kontrola omogućio mi je da bezbednost hrane sagledam izuzetno praktično – od procene rizika i planiranja kontrola, preko verifikacije HACCP sistema i tumačenja propisa, do neposrednog rada sa subjektima u poslovanju hranom i laboratorijama.',
        'Moje iskustvo obuhvata i rad u oblasti agrarne politike i analitike, kao i učešće u brojnim domaćim i međunarodnim projektima i programima, uključujući EU TAIEX i Twinning projekte, USAID, UNEP-GEF, WTO SPS i IPA projekte, kao i projekte povezane sa laboratorijama. Učestvovala sam i na projektu razvoja sistema bezbednosti hrane u saradnji sa KPMG-om.',
        'U narednoj fazi svog profesionalnog razvoja fokus usmeravam na stručno savetovanje, audite, sertifikaciju i digitalizaciju sistema bezbednosti hrane. Posedujem IRCA sertifikat za ISO 9001 Lead Auditor, a svoje znanje kontinuirano proširujem u oblastima ISO/FSSC 22000, IFS i drugih međunarodno priznatih standarda.',
        'Posebnu vrednost u svom radu vidim u povezivanju struke, propisa i praktične primene. Dugogodišnje iskustvo u državnom sistemu kontrole hrane omogućilo mi je da razumem ne samo šta propisi zahtevaju, već i sa kakvim se konkretnim izazovima kompanije suočavaju kada te zahteve treba primeniti u svakodnevnom poslovanju.',
        'Danas svoje iskustvo prenosim u drugačiji oblik – kroz Food Compass, sa ciljem da kompanijama pomognem da svoje sisteme bezbednosti hrane učine jasnijim, efikasnijim, transparentnijim i jednostavnijim za primenu i održavanje.',
    ],
}

SUPPORT = {
    'title': 'Stručna podrška za bezbednost hrane',
    'eyebrow': 'Kontinuirano praćenje i pomoć',
    'options': [
        {
            'slug': 'redovna',
            'title': 'Redovna stručna poseta',
            'subtitle': 'Budite sigurni da vaš sistem bezbednosti hrane funkcioniše u praksi',
            'intro': 'Redovna stručna podrška – kontinuirano praćenje i pomoć',
            'body': [
                'U svakodnevnom poslovanju lako se mogu prevideti važni detalji koji, ukoliko se ne uoče na vreme, mogu prerasti u ozbiljan problem.',
                'Kroz redovne stručne posete pružamo vam kontinuiranu podršku u održavanju HACCP sistema i usklađenosti poslovanja sa zahtevima bezbednosti hrane i važećim propisima.',
            ],
            'list_title': 'Mesečne posete, prema unapred dogovorenoj dinamici, obuhvataju:',
            'list_items': [
                'pregled objekta i higijenskih uslova',
                'proveru primene HACCP sistema u praksi',
                'pregled dokumentacije i evidencija',
                'kontrolu deklaracija proizvoda',
                'proveru usklađenosti sa zakonskim zahtevima',
                'identifikaciju potencijalnih neusaglašenosti i preporuke za njihovo pravovremeno otklanjanje',
            ],
            'closer': [
                'Naš cilj je da potencijalne probleme prepoznate i rešite pre nego što postanu stvarni problem.',
                'Tako vaš sistem ostaje funkcionalan, vaše poslovanje usklađeno, a vi spremni za kontrole, audite i zahteve kupaca – bez dodatnog stresa.',
            ],
            'cta': 'Zatraži ponudu',
            'icon': 'calendar',
            'highlights': [
                'Periodične stručne kontrole',
                'Praćenje sistema i dokumentacije',
                'Kontinuirana stručna podrška',
            ],
        },
        {
            'slug': 'vanredna',
            'title': 'Vanredna stručna poseta',
            'subtitle': 'Kada se pojavi nova poslovna prilika ili izazov, budite spremni za pravi korak.',
            'intro': 'Vanredna stručna podrška – kada se pojavi nova situacija, proizvod, audit ili promena',
            'body': [
                'Novi proizvod, promena objekta ili organizacije proizvodnje, priprema za eksterni audit ili novi zahtev poslovnog partnera – svaka promena nosi određene zahteve i rizike.',
                'Vanredna stručna poseta pruža vam mogućnost da pre donošenja važnih odluka sagledate šta je potrebno uraditi i kako promenu sprovesti na pravi način.',
                'Uz podršku našeg konsultanta dobijate jasne smernice, pravovremene preporuke i sigurnost u donošenju odluka, kako biste novu situaciju dočekali spremni i sa manjim rizikom od neusaglašenosti.',
            ],
            'closer': ['Kada se poslovanje menja, budite korak ispred.'],
            'cta': 'Zakaži posetu',
            'icon': 'alert',
            'highlights': [
                'Podrška kada vam je najpotrebnija',
                'Brza procena konkretne situacije',
                'Jasne preporuke za naredne korake',
            ],
        },
    ],
}

SEO_PAGES = {
    'home': {
        'title': 'Food Compass | HACCP, deklarisanje i digitalizacija',
        'description': (
            'HACCP sistemi, digitalizacija HACCP-a, deklarisanje i priprema za audit. '
            'Food Compass — stručna podrška u bezbednosti hrane od ideje do police.'
        ),
    },
    'about': {
        'title': 'O nama',
        'description': (
            'Food Compass je stručni i konsultantski koncept usmeren na HACCP, '
            'digitalizaciju HACCP sistema i regulatornu usaglašenost.'
        ),
    },
    'about_me': {
        'title': 'O meni',
        'description': (
            'Sandra Đukanović Kojić — specijalista za bezbednost hrane i HACCP '
            'sa više od 22 godine iskustva.'
        ),
    },
    'services': {
        'title': 'Naše usluge',
        'description': (
            'HACCP, digitalizacija HACCP-a, ISO standardi, deklarisanje, '
            'gap analiza i priprema za sertifikaciju.'
        ),
    },
    'journey': {
        'title': 'Od ideje do police',
        'description': (
            'Kompletna stručna podrška za razvoj proizvoda: HACCP, '
            'deklarisanje i usaglašenost do police.'
        ),
    },
    'support': {
        'title': 'Stručna podrška',
        'description': (
            'Redovne i vanredne stručne posete: kontinuirana podrška HACCP sistemu, '
            'higijeni i dokumentaciji.'
        ),
    },
    'news': {
        'title': 'Aktuelnosti',
        'description': (
            'Aktuelnosti Food Compass-a — stručni tekstovi o HACCP-u, '
            'digitalizaciji i bezbednosti hrane.'
        ),
    },
    'contact': {
        'title': 'Kontakt',
        'description': (
            'Kontaktirajte Food Compass za HACCP, digitalizaciju HACCP-a i deklarisanje. '
            'office@foodcompass.rs, +381 63 7707 319.'
        ),
    },
    'terms': {
        'title': 'Uslovi korišćenja',
        'description': 'Uslovi korišćenja sajta Food Compass — prava, obaveze i merodavno pravo.',
    },
}

SERVICE_SEO = {
    'sistemi-i-standardi': {
        'description': (
            'Uspostavljanje, revizija i unapređenje HACCP, IFS, FSSC 22000 i BRCGS sistema '
            'bezbednosti hrane, uz pripremu za audit i sertifikaciju.'
        ),
    },
    'iso-standardi': {
        'description': (
            'Implementacija ISO 9001 i ISO 22000, povezivanje sa HACCP principima '
            'i priprema organizacije za sertifikaciju.'
        ),
    },
    'deklarisanje': {
        'description': (
            'Izrada i provera deklaracija, alergeni, nutritivne vrednosti i usaglašenost '
            'označavanja hrane sa važećim propisima.'
        ),
    },
    'gap-analiza': {
        'description': (
            'Procena usaglašenosti HACCP i standarda IFS, FSSC 22000, BRCGS i ISO '
            'pre sertifikacionog audita.'
        ),
    },
    'digitalizacija': {
        'description': (
            'Digitalizacija HACCP-a: procedure, kontrolne liste i evidencije sa papira '
            'u pregledan digitalni sistem.'
        ),
    },
}

CRUMB_LABELS = {
    'o-nama': 'O nama',
    'o-meni': 'O meni',
    'usluge': 'Naše usluge',
    'od-ideje-do-police': 'Od ideje do police',
    'strucna-podrska': 'Stručna podrška',
    'haccp-nadzor': 'Stručna podrška',
    'aktuelnosti': 'Aktuelnosti',
    'kontakt': 'Kontakt',
    'uslovi-koriscenja': 'Uslovi korišćenja',
}


def get_service(slug):
    return next((item for item in SERVICES if item['slug'] == slug), None)


def get_service_cards():
    cards = []
    for index, service in enumerate(SERVICES, start=1):
        cards.append({
            'number': f'{index:02d}',
            'title': service['title'],
            'standards': service.get('standards') or [],
            'desc': service.get('card') or service['short'],
            'icon': service['icon'],
            'url_name': 'service_detail',
            'slug': service['slug'],
            'flagship': False,
        })
    cards.append({
        'number': '06',
        'title': 'Od ideje do police',
        'standards': [],
        'desc': 'Kompletna stručna podrška od prve ideje i recepture do proizvoda spremnog za tržište.',
        'icon': 'journey',
        'url_name': 'journey',
        'slug': None,
        'flagship': True,
    })
    return cards


TERMS = {
    'title': 'Uslovi korišćenja',
    'updated': '18. avgust 2026.',
    'intro': (
        'Ovi uslovi uređuju korišćenje sajta foodcompass.rs. Korišćenjem sajta smatra se da ste ih '
        'pročitali i prihvatili. Ako se sa njima ne slažete, molimo vas da sajt ne koristite.'
    ),
    'sections': [
        {
            'title': '1. Operater sajta',
            'paragraphs': [
                'Sajt foodcompass.rs (u daljem tekstu: „Sajt“) vodi Food Compass, stručni i konsultantski '
                'koncept u oblasti bezbednosti hrane, sa sedištem u Republici Srbiji.',
                'Kontakt: office@foodcompass.rs, telefon +381 63 7707 319.',
            ],
        },
        {
            'title': '2. Svrha sajta',
            'paragraphs': [
                'Sajt služi za predstavljanje delatnosti, usluga i stručnih tekstova Food Compass-a, '
                'kao i za ostvarivanje kontakta sa zainteresovanim licima.',
                'Sadržaj na Sajtu je informativnog karaktera. Ne predstavlja obavezujuću ponudu, pravni, '
                'poreski ili regulatorni savet, niti zamenjuje ugovor o pružanju usluga.',
            ],
        },
        {
            'title': '3. Usluge',
            'paragraphs': [
                'Konkretne usluge (HACCP, deklarisanje, ISO i drugi standardi, gap analiza, digitalizacija, '
                'stručne posete i slično) ugovaraju se posebno, pismenim putem, nakon dogovora o obimu, '
                'rokovima i naknadi.',
                'Objavljivanje opisa usluga na Sajtu ne stvara obavezu pružanja usluge niti prihvatanje '
                'svakog zahteva.',
            ],
        },
        {
            'title': '4. Intelektualna svojina',
            'paragraphs': [
                'Tekstovi, fotografije, logotip, grafička rešenja, struktura i ostali sadržaj Sajta '
                'zaštićeni su autorskim i srodnim pravima i pripadaju Food Compass-u ili davacima licence, '
                'osim ako je drugačije navedeno.',
                'Dozvoljeno je pregledanje i deljenje javnih stranica uz navođenje izvora. Zabranjeno je '
                'kopiranje, prepravka, preprodaja ili korišćenje sadržaja u komercijalne svrhe bez prethodne '
                'pisane saglasnosti.',
            ],
        },
        {
            'title': '5. Tačnost informacija i odgovornost',
            'paragraphs': [
                'Trudimo se da informacije na Sajtu budu tačne i ažurne, ali ne garantujemo potpunost, '
                'tačnost ni podobnost sadržaja za konkretnu situaciju. Propisi i standardi se menjaju, '
                'a svaki slučaj zahteva posebnu stručnu procenu.',
                'Food Compass nije odgovoran za štetu nastalu korišćenjem ili nemogućnošću korišćenja Sajta, '
                'uključujući prekid rada, greške u prikazu, viruse ili postupke trećih lica, osim u meri '
                'u kojoj je odgovornost po zakonu neisključiva.',
            ],
        },
        {
            'title': '6. Korisničko ponašanje',
            'paragraphs': [
                'Obavezujete se da Sajt koristite u skladu sa zakonom i dobrim običajima. Zabranjeno je '
                'narušavanje rada Sajta, slanje štetnog koda, neovlašćeni pristup, zloupotreba kontakt forme '
                'i slanje lažnih ili uvredljivih sadržaja.',
            ],
        },
        {
            'title': '7. Kontakt forma i lični podaci',
            'paragraphs': [
                'Ako nam pošaljete upit, obrađujemo podatke koje navedete (ime, email, telefon, sadržaj '
                'poruke) isključivo radi odgovora i, po potrebi, pripreme ponude. Podatke ne prodajemo '
                'trećim licima.',
                'Pravni osnov je preduzimanje koraka na vaš zahtev pre zaključenja ugovora, odnosno '
                'legitimni interes da odgovorimo na upit. Podatke čuvamo onoliko koliko je potrebno za '
                'tu svrhu, a zatim ih brišemo, osim ako zakon nalaže duže čuvanje.',
                'Imate pravo na uvid, ispravku, brisanje i ograničenje obrade, kao i pravo prigovora. '
                'Za zahteve pišite na office@foodcompass.rs. Poverenik za informacije od javnog značaja '
                'i zaštitu podataka o ličnosti je nadležno telo u Republici Srbiji.',
            ],
        },
        {
            'title': '8. Kolačići i analitika',
            'paragraphs': [
                'Sajt može da koristi tehnički neophodne kolačiće radi rada stranice, jezika i bezbednosti. '
                'Ako se naknadno uvedu analitički ili marketinški kolačići, o tome ćete biti obavešteni '
                'i, gde je to propisano, zatražićemo saglasnost.',
            ],
        },
        {
            'title': '9. Linkovi ka drugim sajtovima',
            'paragraphs': [
                'Sajt može sadržati linkove ka LinkedIn-u i drugim spoljnim stranicama. Food Compass ne '
                'kontroliše njihov sadržaj ni politiku privatnosti i nije odgovoran za štetu nastalu '
                'njihovim korišćenjem.',
            ],
        },
        {
            'title': '10. Izmene uslova',
            'paragraphs': [
                'Zadržavamo pravo da ove uslove izmenimo. Izmene stupaju na snagu objavljivanjem na ovoj '
                'stranici, uz navođenje datuma ažuriranja. Nastavak korišćenja Sajta nakon izmene smatra '
                'se prihvatanjem novih uslova.',
            ],
        },
        {
            'title': '11. Merodavno pravo',
            'paragraphs': [
                'Na ove uslove i korišćenje Sajta primenjuje se pravo Republike Srbije. Za sporove su '
                'nadležni sudovi u Republici Srbiji, u skladu sa važećim propisima.',
            ],
        },
        {
            'title': '12. Kontakt',
            'paragraphs': [
                'Za pitanja u vezi sa ovim uslovima pišite na office@foodcompass.rs ili koristite stranicu Kontakt.',
            ],
        },
    ],
}
