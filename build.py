#!/usr/bin/env python3
"""Bouwt de statische site van Sleepdienst Janssen.

Pas de gegevens hieronder aan en draai:  python3 build.py
Alle pagina's (home, stadspagina's, redirects, sitemap) worden opnieuw gegenereerd.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

# ===== Bedrijfsgegevens — hier één keer aanpassen =====
NAME = "Sleepdienst Janssen"
SITE = "https://sleepdienstjanssen.nl"
PHONE_DISPLAY = "085 000 00 00"   # TODO: echt nummer
PHONE_TEL = "+31850000000"        # TODO: echt nummer, internationaal formaat
WHATSAPP = "31850000000"          # TODO: nummer zonder + voor wa.me
EMAIL = "info@sleepdienstjanssen.nl"
REGION = "Rotterdam, Drechtsteden, Brabant & Zeeland"

ROOT = Path(__file__).parent
SRC = ROOT / "src"


def svg(name):
    return (SRC / f"{name}.svg").read_text()


ICONS = svg("icons")

# ===== Stadspagina's =====
# Elke stad krijgt eigen, lokale inhoud: wegen, drukke punten, kernen en vragen.
CITIES = [
    {
        "slug": "rotterdam", "name": "Rotterdam", "prov": "Zuid-Holland",
        "intro": "Rotterdam is een van de drukste verkeersknooppunten van Nederland. Ring Rotterdam, de havens en de tunnels onder de Maas zorgen dag en nacht voor veel verkeer — en dus ook voor pech. Staat u stil op de ring, in de haven of gewoon voor de deur in een van de wijken? Wij komen naar u toe.",
        "roads": ["A13 richting Den Haag en Rotterdam The Hague Airport", "A15 langs de haven, de Botlek en de Maasvlakte", "A16 over de Van Brienenoordbrug", "A20 tussen Kethelplein en Terbregseplein", "A4 en de Beneluxtunnel"],
        "spots": "Pech in een tunnel of op een brug is extra gevaarlijk. Op plekken als de Maastunnel, de Beneluxtunnel en de Van Brienenoordbrug volgt u altijd de aanwijzingen van de weginspecteur of de verkeerscentrale; daarna halen wij uw auto op en brengen hem naar een veilige plek of uw garage.",
        "areas": ["Centrum", "Kralingen", "Feijenoord", "Charlois", "IJsselmonde", "Hillegersberg", "Prins Alexander", "Overschie", "Delfshaven", "Hoogvliet", "Schiedam", "Capelle aan den IJssel", "Barendrecht", "Ridderkerk"],
        "faq": [
            ("Kunnen jullie ook in de Rotterdamse haven slepen?", "Ja. We halen voertuigen op in het hele havengebied, van de Waalhaven tot de Botlek. Op afgesloten terreinen hebben we wel toestemming van de terreinbeheerder nodig; geef bij uw melding door waar u precies staat."),
            ("Mijn auto staat in een parkeergarage in het centrum. Kan dat?", "Vaak wel, maar niet elke garage is hoog genoeg voor een plateauwagen. Noem bij het bellen de naam van de garage en de verdieping, dan bekijken we vooraf de beste aanpak."),
        ],
        "near": ["spijkenisse", "dordrecht", "gorinchem"],
    },
    {
        "slug": "dordrecht", "name": "Dordrecht", "prov": "Zuid-Holland",
        "intro": "Dordrecht en de Drechtsteden liggen op een kruispunt van rivieren en snelwegen. Tussen Rotterdam en Brabant rijdt veel doorgaand verkeer over de A16, en de bruggen en tunnels in de regio zijn gevoelig voor stremmingen. Wij helpen u in Dordrecht en alle omliggende kernen.",
        "roads": ["A16 met de Drechttunnel richting Rotterdam", "A16 richting de Moerdijkbruggen en Breda", "N3 tussen Dordrecht en Papendrecht", "A15 langs Alblasserdam, Papendrecht en Sliedrecht", "N217 en de Kiltunnel richting de Hoeksche Waard"],
        "spots": "Stilstaan in de Drechttunnel of op de A16 bij de Moerdijk? Zet uw alarmlichten aan, blijf in de auto met de gordel om als er geen vluchtstrook is en bel 112 bij gevaar. Zodra het veilig kan, zijn wij er om uw voertuig weg te slepen.",
        "areas": ["Binnenstad", "Stadspolders", "Sterrenburg", "Dubbeldam", "Zwijndrecht", "Papendrecht", "Sliedrecht", "Hendrik-Ido-Ambacht", "Alblasserdam"],
        "faq": [
            ("Helpen jullie ook in Sliedrecht en Papendrecht?", "Ja. De hele Drechtsteden-regio valt binnen ons werkgebied, inclusief Sliedrecht, Papendrecht, Zwijndrecht, Hendrik-Ido-Ambacht en Alblasserdam."),
            ("Kunnen jullie mijn auto naar een garage in Rotterdam brengen?", "Zeker. We brengen uw auto naar elk adres dat u kiest, ook buiten Dordrecht. U hoort vooraf wat het transport kost."),
        ],
        "near": ["rotterdam", "gorinchem", "breda"],
    },
    {
        "slug": "breda", "name": "Breda", "prov": "Noord-Brabant",
        "intro": "Breda ligt aan de belangrijkste route tussen de Randstad en België. Op de A16 en de A58 rijdt veel internationaal verkeer, en juist daar strandt regelmatig iemand die ver van huis is. Of u nu op de snelweg staat of in de binnenstad niet meer kunt starten: wij helpen u verder.",
        "roads": ["A16 tussen de Moerdijk en de Belgische grens", "A58 richting Roosendaal en Tilburg", "A27 bij Breda-Noord richting Oosterhout en Gorinchem", "N263 richting Zundert"],
        "spots": "Rijdt u vanuit België of Duitsland en krijgt u pech rond Breda? Geen probleem: we brengen uw auto naar een garage in de buurt of naar een adres naar keuze, ook als het een buitenlands kenteken heeft.",
        "areas": ["Centrum", "Princenhage", "Haagse Beemden", "Ginneken", "Bavel", "Prinsenbeek", "Teteringen", "Etten-Leur", "Oosterhout", "Zundert"],
        "faq": [
            ("Slepen jullie ook auto's met een buitenlands kenteken?", "Ja. We slepen elk voertuig, ongeacht het land van registratie. Heeft u een buitenlandse pechhulpverzekering? Houd dan uw polisgegevens bij de hand."),
            ("Kan mijn auto bij jullie gestald worden tot de garage open is?", "Neem contact met ons op. We zoeken samen naar een veilige oplossing, bijvoorbeeld transport naar een garage die de volgende ochtend direct aan de slag kan."),
        ],
        "near": ["tilburg", "dordrecht", "goes"],
    },
    {
        "slug": "tilburg", "name": "Tilburg", "prov": "Noord-Brabant",
        "intro": "Tilburg is een grote studenten- en werkstad met veel woon-werkverkeer op de A58 en de A65. Op de ringweg en de invalswegen staat het in de spits vaak vast, en een kapotte auto zorgt dan snel voor extra hinder. Wij halen uw voertuig snel en veilig weg.",
        "roads": ["A58 tussen Breda en Eindhoven", "A65 richting 's-Hertogenbosch", "Ringbanen rond het centrum", "N261 richting Waalwijk"],
        "spots": "Pech op een drukke ringbaan? Zet uw auto als het kan in een zijstraat of op een parkeerplaats, zet de alarmlichten aan en bel ons. Zo houdt u het voor uzelf en ander verkeer veilig.",
        "areas": ["Centrum", "Reeshof", "Noord", "Oud-Zuid", "Berkel-Enschot", "Udenhout", "Goirle", "Oisterwijk", "Dongen", "Hilvarenbeek"],
        "faq": [
            ("Ik ben student en heb geen pechhulpverzekering. Wat nu?", "Geen probleem: u kunt ons ook zonder verzekering bellen. We noemen vooraf een vaste prijs, zodat u niet voor verrassingen komt te staan."),
            ("Kunnen jullie een auto ophalen die al lang stilstaat?", "Ja. Ook voertuigen zonder APK of die al tijden niet meer rijden, brengen we naar de garage, het demontagebedrijf of een ander adres."),
        ],
        "near": ["breda", "den-bosch"],
    },
    {
        "slug": "den-bosch", "name": "'s-Hertogenbosch", "prov": "Noord-Brabant",
        "intro": "'s-Hertogenbosch ligt aan de A2, een van de drukste snelwegen van het land, tussen Utrecht en Eindhoven. Rond de knooppunten bij Den Bosch staat het vaak vol, en bij pech wilt u daar zo snel mogelijk weg. Wij helpen in Den Bosch en de hele regio eromheen.",
        "roads": ["A2 tussen Zaltbommel en Eindhoven", "A59 richting Oss en Waalwijk", "A65 richting Tilburg", "Knooppunten Empel en Vught"],
        "spots": "Op de A2 rond Den Bosch rijdt veel vrachtverkeer. Staat u op de vluchtstrook? Ga achter de vangrail staan, trek een veiligheidshesje aan en bel ons. Wij komen met een plateauwagen en brengen uw auto naar uw garage.",
        "areas": ["Binnenstad", "Rosmalen", "Empel", "Engelen", "Maaspoort", "De Groote Wielen", "Vught", "Sint-Michielsgestel", "Den Dungen"],
        "faq": [
            ("Werken jullie ook in de Bommelerwaard?", "Ja. Vanuit Den Bosch helpen we ook in Zaltbommel, Rossum en de rest van de Bommelerwaard, en richting Gorinchem."),
            ("Mijn elektrische auto heeft een lege accu. Kunnen jullie die slepen?", "Ja. Elektrische auto's vervoeren we altijd op een plateauwagen, met alle vier de wielen van de grond, zodat de aandrijving niet beschadigt."),
        ],
        "near": ["tilburg", "gorinchem"],
    },
    {
        "slug": "gorinchem", "name": "Gorinchem", "prov": "Zuid-Holland",
        "intro": "Bij Gorinchem kruisen de A15 en de A27 elkaar, vlak bij de Merwede. Het is een knooppunt waar verkeer uit Rotterdam, Utrecht en Brabant samenkomt. Pech in Gorinchem of in de Alblasserwaard en het Land van Heusden en Altena? Bel ons.",
        "roads": ["A15 richting Rotterdam en Nijmegen", "A27 richting Utrecht en Breda", "Merwedebrug in de A27", "N216 richting Hardinxveld-Giessendam"],
        "spots": "Bruggen als de Merwedebrug hebben vaak geen vluchtstrook. Krijgt u daar pech? Zet uw alarmlichten aan, blijf met de gordel om in de auto zitten en bel 112 bij gevaar. Daarna slepen wij uw auto weg.",
        "areas": ["Binnenstad", "Lingewijk", "Laag-Dalem", "Arkel", "Hardinxveld-Giessendam", "Leerdam", "Sleeuwijk", "Woudrichem", "Werkendam", "Sliedrecht"],
        "faq": [
            ("Helpen jullie ook aan de Brabantse kant van de Merwede?", "Ja. Ook in Sleeuwijk, Werkendam, Woudrichem en de rest van Altena zijn we actief."),
            ("Kunnen jullie een aanhanger of caravan meenemen?", "Bel ons en vertel wat u vervoert. Vaak kunnen we auto én aanhanger in één keer meenemen of regelen we een tweede rit."),
        ],
        "near": ["dordrecht", "den-bosch", "rotterdam"],
    },
    {
        "slug": "spijkenisse", "name": "Spijkenisse", "prov": "Zuid-Holland",
        "intro": "Spijkenisse en Voorne aan Zee liggen naast de Rotterdamse haven. Veel inwoners rijden dagelijks via de Botlek en de A15 naar hun werk, en juist daar is het druk met vrachtverkeer. Wij helpen u in Spijkenisse, Hoogvliet en heel Voorne.",
        "roads": ["A15 bij de Botlek richting Rotterdam en de Maasvlakte", "Spijkenisserbrug over de Oude Maas", "Hartelbrug richting de Maasvlakte", "Provinciale wegen richting Hellevoetsluis en Brielle"],
        "spots": "Rijdt u naar de Maasvlakte of het strand bij Rockanje en krijgt u onderweg pech? We halen uw auto op en brengen hem terug naar huis of naar een garage in de buurt.",
        "areas": ["Centrum", "Maaswijk", "Groenewoud", "De Akkers", "Hoogvliet", "Geervliet", "Zuidland", "Hellevoetsluis", "Brielle", "Rozenburg"],
        "faq": [
            ("Komen jullie ook naar Hellevoetsluis en Brielle?", "Ja. Heel Voorne aan Zee valt binnen ons werkgebied, ook de stranden en campings bij Rockanje en Oostvoorne."),
            ("Kan ik met de sleepwagen meerijden?", "In de meeste gevallen wel, als er plek is in de cabine. Geef bij het bellen door met hoeveel personen u bent."),
        ],
        "near": ["rotterdam", "dordrecht"],
    },
    {
        "slug": "goes", "name": "Goes", "prov": "Zeeland",
        "intro": "Goes ligt midden in Zeeland aan de A58, de belangrijkste weg tussen Brabant en de Zeeuwse kust. In de zomer is het hier extra druk met toeristen op weg naar het strand, en wie ver van huis pech krijgt, wil snel geholpen worden. Wij zijn er voor u in Goes en op heel Zuid-Beveland.",
        "roads": ["A58 richting Bergen op Zoom en Vlissingen", "N256 en de Zeelandbrug richting Zierikzee", "Westerscheldetunnel richting Terneuzen en Zeeuws-Vlaanderen", "N289 langs Kruiningen en Yerseke"],
        "spots": "Bent u op vakantie en staat u met pech op een camping of bij het strand? Wij brengen uw auto naar een garage in de buurt, en denken mee over vervoer terug naar huis.",
        "areas": ["Centrum", "Goes-Oost", "Kloetinge", "'s-Heer Arendskerke", "Kapelle", "Wemeldinge", "Yerseke", "Kruiningen", "Middelburg", "Vlissingen"],
        "faq": [
            ("Helpen jullie ook toeristen met een caravan of camper?", "Ja. Meld bij het bellen dat het om een caravan of camper gaat, dan sturen we het juiste materieel."),
            ("Werken jullie ook in Zeeuws-Vlaanderen?", "Ja, via de Westerscheldetunnel helpen we ook in Terneuzen en omgeving."),
        ],
        "near": ["breda", "rotterdam"],
    },
]
BY_SLUG = {c["slug"]: c for c in CITIES}

# Pinnen op de kaart (coördinaten in het viewBox van de NL-kaart)
PINS = {"rotterdam": (66, 132), "dordrecht": (78, 144), "spijkenisse": (54, 140), "gorinchem": (94, 146),
        "breda": (82, 170), "tilburg": (102, 172), "den-bosch": (116, 160), "goes": (36, 168)}


def url(slug=None):
    return f"/sleepdienst-{slug}/" if slug else "/"


def page(*, title, desc, path, body, schema, crumbs=None):
    canonical = SITE + path
    crumb_html = ""
    if crumbs:
        parts = ['<a href="/">Home</a>'] + [f"<span>{escape(c)}</span>" for c in crumbs]
        crumb_html = f'<nav class="crumbs container" aria-label="Kruimelpad">{" › ".join(parts)}</nav>'
    city_links = "".join(f'<li><a href="{url(c["slug"])}">Sleepdienst {escape(c["name"])}</a></li>' for c in CITIES)
    return f"""<!doctype html>
<html lang="nl-NL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b2a5b">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="nl_NL">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icon-180.png">
<link rel="manifest" href="/assets/site.webmanifest">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
{ICONS}
<div class="topbar"><div class="container">
  <span><svg><use href="#i-clock"/></svg>24/7 hulp</span>
  <span><svg><use href="#i-pin"/></svg>{REGION}</span>
  <span><svg><use href="#i-bolt"/></svg>Snel ter plaatse</span>
</div></div>
<header class="navwrap" id="nav">
  <nav class="container">
    <a class="logo" href="/" aria-label="{NAME} — home">
      <svg><use href="#i-logo"/></svg>
      <span><b>sleepdienst <em>janssen</em></b><small>Wanneer u ons nodig heeft</small></span>
    </a>
    <ul class="navlinks" id="navlinks">
      <li><a href="/#diensten">Diensten</a></li>
      <li><a href="/#werkgebied">Werkgebied</a></li>
      <li><a href="/#werkwijze">Werkwijze</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
    <div class="navcta">
      <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Bel: {PHONE_DISPLAY}</a>
      <a class="btn btn-navy" href="#contact">Hulp aanvragen</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu openen" aria-expanded="false" aria-controls="navlinks">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </nav>
</header>
{crumb_html}
<main>
{body}
{cta()}
</main>
<footer>
  <svg class="wave-top" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0 H1440 V30 C 1180 90, 900 0, 620 40 S 180 80, 0 20Z" fill="#fff"/></svg>
  <div class="container">
    <div class="foot">
      <div>
        <a class="logo" href="/"><svg><use href="#i-logo"/></svg><span><b>sleepdienst <em>janssen</em></b><small>Wanneer u ons nodig heeft</small></span></a>
        <p>Sleepdienst, pechhulp en autotransport in {REGION}. 24 uur per dag, 7 dagen per week.</p>
      </div>
      <div><h4>Werkgebied</h4><ul>{city_links}</ul></div>
      <div><h4>Diensten</h4><ul><li><a href="/#diensten">Pechhulp</a></li><li><a href="/#diensten">Auto slepen</a></li><li><a href="/#diensten">Autotransport</a></li><li><a href="/#diensten">Bandenservice</a></li><li><a href="/#faq">Veelgestelde vragen</a></li></ul></div>
      <div><h4>Contact</h4><ul>
        <li>Tel: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> (24/7)</li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul></div>
    </div>
    <div class="foot-bottom">
      <span>© {date.today().year} {NAME}. Alle rechten voorbehouden.</span>
      <div><a href="/privacy/">Privacyverklaring</a></div>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>BEL DIRECT — 24/7 HULP</a>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def cta():
    wa = f"https://wa.me/{WHATSAPP}?text=Hallo%20{NAME.replace(' ', '%20')}%2C%20ik%20heb%20hulp%20nodig.%20Mijn%20locatie%20is%3A%20"
    return f"""<section class="cta" id="contact">
  <div class="container cta-grid">
    <div>
      <h2><span class="hl">Pech?</span> Wij helpen u direct</h2>
      <p>Bel ons of stuur een WhatsApp-bericht met uw locatie. U hoort meteen wanneer we er kunnen zijn en wat het kost.</p>
      <div class="actions">
        <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Bel {PHONE_DISPLAY}</a>
        <a class="btn btn-navy" href="{wa}" target="_blank" rel="noopener">WhatsApp ons</a>
      </div>
    </div>
    {svg("art-cta")}
  </div>
</section>"""


def nl_map(highlight=None):
    pins = ""
    for slug, (x, y) in PINS.items():
        cls = "pin on" if slug == highlight else "pin"
        name = escape(BY_SLUG[slug]["name"])
        pins += f'<a href="{url(slug)}" class="{cls}"><circle cx="{x}" cy="{y}" r="{6 if slug == highlight else 4.5}"/><title>Sleepdienst {name}</title></a>'
    return f"""<svg viewBox="0 0 220 260" role="img" aria-label="Kaart van het werkgebied in Zuidwest-Nederland">
  <defs>
    <pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="2.2" fill="#b9d7f5"/></pattern>
    <pattern id="dots-on" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="2.4" fill="#1e88e5"/></pattern>
    <clipPath id="nl">
      <path d="M66 50 L76 40 L96 34 L118 26 L146 22 L172 22 L196 34 L204 48 L198 70 L192 92 L204 112 L198 128 L182 140 L168 150 L160 164 L152 172 L150 192 L156 214 L148 240 L136 232 L134 208 L130 190 L112 186 L88 190 L66 188 L50 184 L36 190 L20 184 L16 172 L28 162 L22 152 L36 142 L46 124 L54 98 L60 72 Z"/>
      <ellipse cx="74" cy="26" rx="10" ry="4"/><ellipse cx="96" cy="16" rx="12" ry="4"/><ellipse cx="124" cy="10" rx="12" ry="3.5"/><ellipse cx="150" cy="8" rx="8" ry="3"/>
    </clipPath>
    <clipPath id="sw"><path d="M0 120 L72 120 L132 140 L132 192 L0 200Z"/></clipPath>
  </defs>
  <rect width="220" height="260" fill="url(#dots)" clip-path="url(#nl)"/>
  <g clip-path="url(#nl)"><rect width="220" height="260" fill="url(#dots-on)" clip-path="url(#sw)"/></g>
  <g class="pins">{pins}</g>
</svg>"""


def city_cards():
    return "".join(
        f'<a class="city" href="{url(c["slug"])}"><svg><use href="#i-pin"/></svg><span><b>Sleepdienst {escape(c["name"])}</b><small>{escape(c["prov"])}</small></span></a>'
        for c in CITIES)


SERVICES = f"""<section class="services" id="diensten">
  <div class="container svc-grid">
    <article class="svc">
      <div class="svc-head"><svg><use href="#i-car"/></svg>Pechhulp</div>
      <div class="svc-body">
        <ul class="checks">
          <li>24/7 hulp bij pech onderweg</li>
          <li>Reparatie ter plaatse waar mogelijk</li>
          <li>Starthulp, lege accu en brandstofproblemen</li>
          <li>Ook in het weekend en op feestdagen</li>
        </ul>
        <a class="btn btn-navy" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Bel: {PHONE_DISPLAY}</a>
      </div>
    </article>
    <article class="svc">
      <div class="svc-head"><svg><use href="#i-truck"/></svg>Autotransport</div>
      <div class="svc-body">
        <form class="route" id="routeForm">
          <div><label for="van">Vertrekpunt</label><div class="field"><svg><use href="#i-send"/></svg><input id="van" placeholder="Plaats of postcode" required></div></div>
          <div><label for="naar">Bestemming</label><div class="field"><svg><use href="#i-pin"/></svg><input id="naar" placeholder="Plaats of postcode" required></div></div>
        </form>
        <button class="btn btn-ghost" type="submit" form="routeForm">Vraag prijs aan</button>
      </div>
    </article>
    <article class="svc">
      <div class="svc-head"><svg><use href="#i-tire"/></svg>Bandenservice</div>
      <div class="svc-body">
        <p><strong>Lekke band?</strong> Wij wisselen uw band ter plaatse of brengen u veilig naar de dichtstbijzijnde bandenspecialist.</p>
        <ul class="checks">
          <li>24/7 bereikbaar</li>
          <li>Reservewiel monteren langs de weg</li>
          <li>Deskundig team</li>
        </ul>
        <a class="btn btn-navy" href="#contact">Meer weten</a>
      </div>
    </article>
  </div>
</section>"""

STEPS = f"""<section class="section steps-sec" id="werkwijze">
  <div class="container">
    <h2 class="title center">Zo <span class="hl">werkt het</span></h2>
    <div class="steps">
      <div class="step"><i>1</i><h3>Bel of WhatsApp</h3><p>Geef uw locatie, kenteken en wat er aan de hand is door. Wij nemen 24/7 op.</p></div>
      <div class="step"><i>2</i><h3>Vaste prijs vooraf</h3><p>U hoort direct wat het kost en hoe laat we er ongeveer zijn. Geen verrassingen achteraf.</p></div>
      <div class="step"><i>3</i><h3>Wij komen naar u toe</h3><p>De dichtstbijzijnde wagen rijdt naar u toe. Waar mogelijk lossen we het ter plaatse op.</p></div>
      <div class="step"><i>4</i><h3>Veilig naar bestemming</h3><p>Lukt dat niet, dan brengen we uw auto naar uw garage, huis of een adres naar keuze.</p></div>
    </div>
  </div>
</section>"""

WHY = f"""<section class="section" id="waarom">
  <div class="container">
    <h2 class="title center">Waarom <span class="hl">Sleepdienst Janssen?</span></h2>
    <div class="why">
      <div class="blob"><div class="bg"></div>{svg("art-driver")}</div>
      <div class="features">
        <div class="feat"><div class="fi" style="background:var(--blue)"><svg><use href="#i-clock"/></svg></div><div><h3>Snelle respons</h3><p>Wij nemen dag en nacht op en sturen direct de dichtstbijzijnde wagen naar uw locatie.</p></div></div>
        <div class="feat"><div class="fi" style="background:var(--red)"><svg><use href="#i-truck"/></svg></div><div><h3>Het juiste materieel</h3><p>Plateauwagens voor auto's, bestelbussen, motoren en elektrische auto's.</p></div></div>
        <div class="feat"><div class="fi" style="background:var(--yellow2)"><svg><use href="#i-pin"/></svg></div><div><h3>Lokaal bekend</h3><p>We kennen de wegen, tunnels en bruggen in de regio en weten waar we u veilig kunnen helpen.</p></div></div>
        <div class="feat"><div class="fi" style="background:var(--green)"><svg><use href="#i-euro"/></svg></div><div><h3>Eerlijke prijzen</h3><p>U hoort vooraf wat het kost. Geen verborgen toeslagen, ook niet 's nachts.</p></div></div>
      </div>
    </div>
  </div>
</section>"""

HOME_FAQ = [
    ("Waar is Sleepdienst Janssen actief?", "Wij werken in Zuidwest-Nederland: Rotterdam en omgeving, de Drechtsteden, West- en Midden-Brabant en Zeeland. Bekijk hierboven de plaatsen in ons werkgebied."),
    ("Hoe snel kunnen jullie ter plaatse zijn?", "Dat hangt af van uw locatie en de drukte op de weg. Bij uw telefoontje sturen wij direct de dichtstbijzijnde wagen en krijgt u een inschatting van de aankomsttijd."),
    ("Wat moet ik doen als ik pech heb op de snelweg?", "Zet de alarmlichten aan, trek een veiligheidshesje aan, plaats de gevarendriehoek als dat veilig kan en ga achter de vangrail staan. Bel 112 bij direct gevaar. Bel ons daarna met uw locatie en kenteken."),
    ("Hoeveel kost een sleepdienst?", "De prijs hangt af van de afstand, het type voertuig en het tijdstip. U krijgt altijd vooraf een duidelijke prijsopgave."),
    ("Slepen jullie ook elektrische auto's?", "Ja. Elektrische auto's vervoeren we op een plateauwagen, met alle wielen van de grond, zodat de aandrijving niet beschadigt."),
]


def faq_html(items, open_first=True):
    out = ""
    for i, (q, a) in enumerate(items):
        out += f'<details{" open" if i == 0 and open_first else ""}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
    return out


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def business_schema(area):
    return {"@type": "AutomotiveBusiness", "@id": SITE + "/#business", "name": NAME, "url": SITE + "/",
            "telephone": PHONE_TEL, "email": EMAIL, "openingHours": "Mo-Su 00:00-23:59",
            "areaServed": [{"@type": "City", "name": n} for n in area]}


def home():
    body = f"""<section class="hero">
  <div class="container hero-grid">
    <div>
      <h1>Sleepdienst in <span>Rotterdam, Brabant &amp; Zeeland</span></h1>
      <p>Pech onderweg, een ongeval of een auto die niet meer start? {NAME} staat dag en nacht voor u klaar in Zuidwest-Nederland — van pechhulp ter plaatse tot veilig transport naar uw garage.</p>
      <div class="actions">
        <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Bel direct: {PHONE_DISPLAY}</a>
        <a class="btn btn-navy" href="#contact">Hulp aanvragen</a>
      </div>
      <div class="trust">
        <span><svg><use href="#i-clock"/></svg>24/7 bereikbaar</span>
        <span><svg><use href="#i-shield"/></svg>Vakkundig &amp; verzekerd</span>
        <span><svg><use href="#i-euro"/></svg>Vooraf duidelijke prijs</span>
      </div>
    </div>
    <div class="hero-art">
      <div class="badge24"><div><b>24uur</b><span>SERVICE</span><i>ELKE DAG</i></div></div>
      {svg("art-truck")}
    </div>
  </div>
  <svg class="wave" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70 C 240 130, 480 10, 760 50 S 1220 120, 1440 30 L1440 120 L0 120Z" fill="#fff"/></svg>
</section>
{SERVICES}
{WHY}
<section class="section area" id="werkgebied">
  <div class="container area-grid">
    <div>
      <h2 class="title">Altijd <span class="hl">in de buurt</span></h2>
      <p>Wij richten ons op Zuidwest-Nederland. Daardoor zijn we snel bij u — of u nu op de ring van Rotterdam staat, op de A16 bij de Moerdijk, in de binnenstad van Breda of op weg naar de Zeeuwse kust.</p>
      <div class="cities-grid">{city_cards()}</div>
    </div>
    <div class="map">{nl_map()}<div class="map-label">Rotterdam, Brabant<br>&amp; Zeeland</div></div>
  </div>
</section>
{STEPS}
<section class="section" id="faq">
  <div class="container">
    <h2 class="title center">Veelgestelde vragen</h2>
    <div class="faq-grid">
      <div>
        <p class="muted">Staat uw vraag er niet tussen? Bel ons gerust — we helpen u 24 uur per dag verder.</p>
        <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Stel uw vraag</a>
      </div>
      <div class="faq">{faq_html(HOME_FAQ)}</div>
    </div>
  </div>
</section>"""
    schema = {"@context": "https://schema.org", "@graph": [
        business_schema([c["name"] for c in CITIES]), faq_schema(HOME_FAQ)]}
    return page(title=f"{NAME} | 24/7 Sleepdienst Rotterdam, Brabant & Zeeland",
                desc=f"24/7 sleepdienst en pechhulp in Rotterdam, de Drechtsteden, Brabant en Zeeland. Snel ter plaatse, vooraf een duidelijke prijs. Bel {PHONE_DISPLAY}.",
                path="/", body=body, schema=schema)


def city_page(c):
    n = escape(c["name"])
    roads = "".join(f"<li>{escape(r)}</li>" for r in c["roads"])
    areas = "".join(f"<span>{escape(a)}</span>" for a in c["areas"])
    near = "".join(f'<a class="city" href="{url(s)}"><svg><use href="#i-pin"/></svg><span><b>Sleepdienst {escape(BY_SLUG[s]["name"])}</b><small>{escape(BY_SLUG[s]["prov"])}</small></span></a>' for s in c["near"])
    faqs = c["faq"] + [
        (f"Hoe snel zijn jullie in {c['name']}?", f"Bij uw melding sturen wij direct de dichtstbijzijnde wagen. U krijgt aan de telefoon een inschatting van de aankomsttijd in {c['name']}, afhankelijk van uw exacte locatie en de verkeersdrukte."),
        (f"Wat kost een sleepdienst in {c['name']}?", "Dat hangt af van de afstand, het voertuig en het tijdstip. U krijgt altijd vooraf een vaste prijs, zodat u weet waar u aan toe bent."),
    ]
    body = f"""<section class="hero hero-city">
  <div class="container hero-grid">
    <div>
      <h1>Sleepdienst <span>{n}</span></h1>
      <p>Pech of een ongeval in {n}? {NAME} helpt u 24/7 met pechhulp, slepen en autotransport in {n} en omgeving. Bel ons en u hoort direct wanneer we er zijn en wat het kost.</p>
      <div class="actions">
        <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>Bel direct: {PHONE_DISPLAY}</a>
        <a class="btn btn-navy" href="#contact">Hulp aanvragen</a>
      </div>
      <div class="trust">
        <span><svg><use href="#i-clock"/></svg>24/7 in {n}</span>
        <span><svg><use href="#i-euro"/></svg>Vooraf duidelijke prijs</span>
      </div>
    </div>
    <div class="hero-art">{svg("art-truck")}</div>
  </div>
  <svg class="wave" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70 C 240 130, 480 10, 760 50 S 1220 120, 1440 30 L1440 120 L0 120Z" fill="#fff"/></svg>
</section>
<section class="section city-body">
  <div class="container city-grid">
    <article class="prose">
      <h2>Sleepdienst en pechhulp in {n}</h2>
      <p>{escape(c["intro"])}</p>
      <h3>Wegen in en rond {n}</h3>
      <ul class="roads">{roads}</ul>
      <h3>Pech op een lastige plek</h3>
      <p>{escape(c["spots"])}</p>
      <h3>Wat wij doen in {n}</h3>
      <ul class="checks">
        <li>Auto slepen na pech of een ongeval</li>
        <li>Pechhulp ter plaatse: starthulp, lege accu, band wisselen</li>
        <li>Autotransport naar garage, huis of demontagebedrijf</li>
        <li>Transport van elektrische auto's op een plateauwagen</li>
      </ul>
    </article>
    <aside class="side">
      <div class="side-card">
        <h3>Direct hulp in {n}</h3>
        <p>24 uur per dag, 7 dagen per week bereikbaar.</p>
        <a class="btn btn-yellow" href="tel:{PHONE_TEL}"><svg class="ico"><use href="#i-phone"/></svg>{PHONE_DISPLAY}</a>
      </div>
      <div class="side-card">
        <h3>Wij helpen ook in</h3>
        <div class="cities">{areas}</div>
      </div>
      <div class="map small">{nl_map(c["slug"])}</div>
    </aside>
  </div>
</section>
{STEPS}
<section class="section" id="faq">
  <div class="container">
    <h2 class="title center">Vragen over onze sleepdienst in {n}</h2>
    <div class="faq narrow">{faq_html(faqs)}</div>
  </div>
</section>
<section class="section area">
  <div class="container">
    <h2 class="title center">Ook actief in de <span class="hl">buurt</span></h2>
    <div class="cities-grid near">{near}</div>
  </div>
</section>"""
    path = url(c["slug"])
    schema = {"@context": "https://schema.org", "@graph": [
        business_schema([c["name"]] + c["areas"]),
        {"@type": "Service", "name": f"Sleepdienst {c['name']}", "serviceType": "Sleepdienst en pechhulp",
         "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "City", "name": c["name"]}},
        faq_schema(faqs),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": f"Sleepdienst {c['name']}", "item": SITE + path}]},
    ]}
    return page(title=f"Sleepdienst {c['name']} 24/7 | {NAME}",
                desc=f"Sleepdienst in {c['name']} nodig? {NAME} helpt 24/7 met pechhulp, slepen en autotransport in {c['name']} en omgeving. Vooraf een vaste prijs. Bel {PHONE_DISPLAY}.",
                path=path, body=body, schema=schema, crumbs=[f"Sleepdienst {c['name']}"])


def privacy():
    body = f"""<section class="section"><div class="container prose narrow">
<h1 class="title">Privacyverklaring</h1>
<p>{NAME} gaat zorgvuldig om met uw gegevens. Deze website gebruikt geen trackingcookies en slaat geen formuliergegevens op een server op.</p>
<h3>Contact via telefoon of WhatsApp</h3>
<p>Belt of WhatsAppt u ons, dan gebruiken we uw naam, telefoonnummer, locatie en voertuiggegevens alleen om u te helpen en de opdracht af te handelen. We bewaren deze gegevens niet langer dan nodig voor de uitvoering en de wettelijke administratieplicht.</p>
<h3>Externe diensten</h3>
<p>Voor de lettertypen gebruiken we Google Fonts. Het formulier voor autotransport opent WhatsApp; daarop is het privacybeleid van WhatsApp van toepassing.</p>
<h3>Vragen</h3>
<p>Voor vragen over uw gegevens kunt u mailen naar <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    return page(title=f"Privacyverklaring | {NAME}", desc=f"Privacyverklaring van {NAME}.",
                path="/privacy/", body=body, schema={"@context": "https://schema.org", "@type": "WebPage", "name": "Privacyverklaring"})


def redirect(to):
    return f"""<!doctype html>
<html lang="nl-NL"><head><meta charset="utf-8"><title>{NAME}</title>
<link rel="canonical" href="{SITE}{to}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={to}"></head>
<body><p>Deze pagina is verhuisd: <a href="{to}">{SITE}{to}</a></p></body></html>
"""


# Oude URL's van het vorige domein → nieuwe pagina's (behoudt bezoekers van oude links)
REDIRECTS = {
    "diensten": "/#diensten", "contact": "/#contact", "galerie": "/", "vloot": "/",
    "index.php": "/", "index.php/gastenboek": "/", "index.php/links": "/",
    "index.php/onze-vloot": "/", "index.php/onze-vloot/5-boreas": "/", "index.php/diensten": "/#diensten", "index.php/contact": "/#contact",
}


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def main():
    write("assets/style.css", (SRC / "style.css").read_text())
    write("assets/site.js", (SRC / "site.js").read_text())
    write("assets/favicon.svg", (SRC / "favicon.svg").read_text())
    write("assets/site.webmanifest", (SRC / "site.webmanifest").read_text())
    for f in ["favicon.ico", "icon-180.png", "icon-192.png", "icon-512.png"]:
        dest = ROOT / ("favicon.ico" if f == "favicon.ico" else f"assets/{f}")
        dest.write_bytes((SRC / f).read_bytes())
    write("index.html", home())
    for c in CITIES:
        write(f"sleepdienst-{c['slug']}/index.html", city_page(c))
    write("privacy/index.html", privacy())
    for old, new in REDIRECTS.items():
        write(f"{old}/index.html", redirect(new))
    today = date.today().isoformat()
    urls = ["/"] + [url(c["slug"]) for c in CITIES] + ["/privacy/"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Gebouwd: home + {len(CITIES)} stadspagina's + {len(REDIRECTS)} redirects")


if __name__ == "__main__":
    main()
