from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import Article

BODY = """
<p>Od ideje do proizvoda na tržištu – šta sve treba uraditi pre nego što prehrambeni proizvod stigne do potrošača?</p>
<p>Imate ideju za prehrambeni proizvod. Možda ste osmislili recepturu, pronašli ambalažu i već razmišljate o prodaji.</p>
<p>Ali između dobre ideje i proizvoda koji se može staviti na tržište postoji niz koraka koje ne treba preskočiti.</p>
<p>Proizvodnja hrane podrazumeva mnogo više od samog procesa proizvodnje. Potrebno je obezbediti odgovarajuće uslove za rad objekta, ispuniti zahteve u pogledu higijene i bezbednosti hrane, uspostaviti odgovarajuće procedure i evidencije, definisati proizvod i njegovu specifikaciju, obezbediti potrebne provere i analize, pravilno deklarisati proizvod i obezbediti uslove za njegovo čuvanje i transport.</p>
<p>Drugim rečima – put od ideje do police ima nekoliko važnih stanica.</p>

<h2>1. Prvi korak – odgovarajući objekat</h2>
<p>Pre početka proizvodnje potrebno je utvrditi koje uslove objekat mora da ispuni za konkretnu vrstu delatnosti.</p>
<p>Zahtevi zavise od toga šta se proizvodi, prerađuje ili stavlja u promet, kao i od načina organizacije procesa.</p>
<p>Objekat mora biti odgovarajuće projektovan i organizovan tako da se obezbede higijenski uslovi i spreči kontaminacija hrane. To uključuje, između ostalog, odgovarajući raspored prostorija i opreme, tokove ljudi i materijala, uslove za čišćenje i održavanje, upravljanje otpadom i druge higijenske preduslove.</p>
<p>Pre nego što se uloži značajan novac u opremanje prostora, zato je korisno napraviti stručnu procenu planiranog objekta i procesa.</p>
<p>Dobra procena na početku može sprečiti skupe izmene kasnije.</p>

<h2>2. Registracija i uslovi za obavljanje delatnosti</h2>
<p>Pored samog objekta, potrebno je ispuniti i administrativne i regulatorne zahteve koji se odnose na konkretnu delatnost.</p>
<p>Za subjekte u poslovanju hranom važe posebni zahtevi u zavisnosti od vrste hrane i aktivnosti kojom se bave. Jedan od važnih elemenata sistema jeste i registracija objekta u odgovarajućem registru, odnosno Centralnom registru objekata kada je to propisano za konkretnu delatnost.</p>
<p>Zato prvi korak nije „napraviti HACCP dokumentaciju“, već utvrditi šta je konkretno potrebno za objekat i delatnost koju želite da registrujete.</p>

<h2>3. Higijena hrane – preduslov za bezbedan proizvod</h2>
<p>Bezbedan proizvod ne može nastati u neodgovarajućem okruženju.</p>
<p>Pre uspostavljanja HACCP sistema potrebno je obezbediti odgovarajuće higijenske preduslove. Oni obuhvataju sve ono što omogućava da se proizvodni proces odvija u kontrolisanim uslovima.</p>
<p>To uključuje, u zavisnosti od vrste delatnosti:</p>
<ul>
  <li>higijenu prostora i opreme;</li>
  <li>čišćenje i dezinfekciju;</li>
  <li>kontrolu štetočina;</li>
  <li>održavanje opreme;</li>
  <li>kvalitet i bezbednost vode;</li>
  <li>upravljanje otpadom;</li>
  <li>ličnu higijenu zaposlenih;</li>
  <li>kontrolu sirovina i dobavljača;</li>
  <li>odgovarajuće uslove skladištenja i transporta.</li>
</ul>
<p>Ovi elementi nisu samo formalna dokumentacija. Oni moraju biti uspostavljeni i primenjeni u svakodnevnom radu.</p>

<h2>4. HACCP – kako kontrolisati opasnosti u procesu?</h2>
<p>HACCP sistem predstavlja jedan od ključnih elemenata upravljanja bezbednošću hrane.</p>
<p>Njegova suština nije u tome da postoji fascikla sa HACCP dokumentacijom, već da se u stvarnom procesu prepoznaju i kontrolišu opasnosti koje mogu ugroziti bezbednost hrane.</p>
<p>To podrazumeva:</p>
<ul>
  <li>opis proizvoda i njegove namene;</li>
  <li>opis proizvodnog procesa;</li>
  <li>identifikaciju mogućih opasnosti;</li>
  <li>procenu rizika;</li>
  <li>definisanje kontrolnih mera;</li>
  <li>određivanje odgovarajućih kontrolnih tačaka, kada je primenljivo;</li>
  <li>definisanje načina praćenja;</li>
  <li>postupanje u slučaju odstupanja;</li>
  <li>verifikaciju sistema;</li>
  <li>odgovarajuće evidencije.</li>
</ul>
<p>HACCP treba da bude prilagođen konkretnom proizvodu i procesu, a ne generički dokument preuzet iz drugog poslovanja.</p>

<h2>5. Proizvođačka specifikacija – šta tačno proizvod jeste?</h2>
<p>Svaki proizvod treba jasno definisati.</p>
<p>Proizvođačka specifikacija predstavlja važan dokument koji objedinjuje podatke o proizvodu i njegovim karakteristikama, u skladu sa zahtevima koji se primenjuju na konkretnu kategoriju proizvoda.</p>
<p>U zavisnosti od proizvoda, specifikacija može obuhvatiti podatke o sastavu, karakteristikama proizvoda, zahtevima za sirovine, načinu proizvodnje, uslovima čuvanja, roku trajanja i druge relevantne podatke.</p>
<p>Ona nije samo dokument „za fioku“. Dobro izrađena specifikacija predstavlja osnovu za povezivanje recepture, proizvodnog procesa, bezbednosti, kvaliteta i deklaracije.</p>

<h2>6. Analize i dokazivanje usaglašenosti proizvoda</h2>
<p>U zavisnosti od vrste proizvoda i relevantnih zahteva, potrebno je definisati odgovarajuće laboratorijske analize i druge načine provere bezbednosti i kvaliteta proizvoda.</p>
<p>Plan analiza ne bi trebalo praviti nasumično. Potrebno je uzeti u obzir vrstu proizvoda, sirovine, proizvodni proces, potencijalne opasnosti, karakteristike proizvoda, rok trajanja, uslove čuvanja, relevantne propise i zahteve kupaca.</p>
<p>Drugim rečima, analize treba povezati sa procenom rizika i karakteristikama konkretnog proizvoda.</p>

<h2>7. Deklaracija – šta potrošač mora da zna?</h2>
<p>Pre nego što proizvod stigne do potrošača, potrebno je obezbediti odgovarajuće označavanje.</p>
<p>Deklaracija mora sadržati informacije koje su propisane za konkretnu vrstu hrane, a podaci moraju biti tačni, jasni i usklađeni sa zahtevima koji se primenjuju.</p>
<p>U zavisnosti od proizvoda i načina prodaje, mogu biti relevantni podaci kao što su naziv hrane, spisak sastojaka, alergeni, neto količina, rok trajanja, uslovi čuvanja, podaci o subjektu u poslovanju hranom, nutritivna deklaracija i druge obavezne informacije.</p>
<p>Posebnu pažnju treba posvetiti alergenima, nutritivnim i zdravstvenim tvrdnjama, kao i podacima o poreklu, kada su primenljivi.</p>
<p>Propisi o deklarisanju se menjaju, pa je pre štampanja ambalaže važno proveriti zahteve koji su važeći u trenutku stavljanja proizvoda na tržište.</p>

<h2>8. Ambalaža nije samo dizajn</h2>
<p>Ambalaža ima važnu ulogu u očuvanju bezbednosti i kvaliteta proizvoda tokom njegovog roka trajanja.</p>
<p>Zato izbor ambalaže treba posmatrati zajedno sa karakteristikama proizvoda, načinom pakovanja, uslovima čuvanja i transporta.</p>
<p>Lepa ambalaža privlači kupca. Odgovarajuća ambalaža štiti proizvod.</p>

<h2>9. Transport i skladištenje – lanac se ne završava proizvodnjom</h2>
<p>Proizvod može biti pravilno proizveden, ali njegova bezbednost i kvalitet mogu biti ugroženi ako se ne skladišti ili transportuje u odgovarajućim uslovima.</p>
<p>Potrebno je definisati odgovarajuće uslove skladištenja i transporta u zavisnosti od karakteristika proizvoda.</p>
<p>Temperatura, higijena transportnog sredstva, zaštita proizvoda od kontaminacije, način rukovanja i drugi uslovi mogu biti od ključnog značaja.</p>
<p>Zato transport treba posmatrati kao sastavni deo lanca bezbednosti hrane, a ne kao poslednji korak koji se rešava tek kada proizvod napusti objekat.</p>

<h2>10. A šta kada proizvod konačno stigne na policu?</h2>
<p>Tada posao nije nužno završen.</p>
<p>Proizvod treba pratiti kroz njegov životni ciklus – od proizvodnje i distribucije do tržišta.</p>
<p>To podrazumeva održavanje sistema bezbednosti hrane, praćenje promena propisa, ažuriranje dokumentacije i deklaracija, proveru sledljivosti, postupanje u slučaju odstupanja i pripremu za kontrole i audite, kada su primenljivi.</p>
<p>Za kompanije koje žele da posluju prema međunarodnim standardima, dodatni zahtevi mogu proisteći iz standarda kao što su IFS, FSSC 22000, BRCGS ili ISO 22000.</p>

<h2>Od ideje do police</h2>
<p>Pokretanje proizvodnje hrane zato nije jedan zadatak. To je niz međusobno povezanih koraka:</p>
<p><strong>IDEJA → PROIZVOD → OBJEKAT → HIGIJENSKI PREDUSLOVI → HACCP → SPECIFIKACIJA → ANALIZE → DEKLARACIJA → AMBALAŽA → SKLADIŠTENJE I TRANSPORT → TRŽIŠTE</strong></p>
<p>Kada su ovi elementi pravilno povezani, mnogo je lakše upravljati proizvodom, dokazivati njegovu usaglašenost i reagovati na zahteve tržišta.</p>

<h2>Food Compass – vaš vodič od ideje do police</h2>
<p>Razvoj prehrambenog proizvoda ne mora da bude put kroz nepovezane zahteve, dokumente i propise.</p>
<p>Food Compass pruža stručnu podršku u definisanju proizvoda, regulatornoj usaglašenosti, HACCP sistemima, proizvođačkim specifikacijama, deklarisanju i pripremi proizvoda za tržište.</p>
<p><strong>Vi imate ideju. Mi vam pomažemo da pronađete pravi put.</strong></p>
"""


class Command(BaseCommand):
    help = 'Dodaje početni članak u Aktuelnosti.'

    def handle(self, *args, **options):
        slug = 'sta-je-potrebno-za-pocetak-proizvodnje-hrane'
        article, created = Article.objects.get_or_create(
            slug=slug,
            defaults={
                'title': 'Šta je potrebno za početak proizvodnje hrane?',
                'excerpt': 'Od ideje do proizvoda na tržištu – šta sve treba uraditi pre nego što prehrambeni proizvod stigne do potrošača?',
                'body': BODY,
                'is_published': True,
                'published_at': timezone.now(),
                'language': 'sr',
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created article: {article.slug}'))
        else:
            article.body = BODY
            article.excerpt = 'Od ideje do proizvoda na tržištu – šta sve treba uraditi pre nego što prehrambeni proizvod stigne do potrošača?'
            article.is_published = True
            if not article.published_at:
                article.published_at = timezone.now()
            article.save()
            self.stdout.write(self.style.WARNING(f'Updated existing article: {article.slug}'))
