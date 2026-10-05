from pathlib import Path
import json,html,urllib.request,sys
root=Path(__file__).parent
out=root/'dist'
L=json.loads((root/'locales.json').read_text())
settings=json.loads((root/'site-settings.json').read_text()) if (root/'site-settings.json').exists() else {}
origin=(sys.argv[1] if len(sys.argv)>1 else settings.get('origin','')).rstrip('/')
E=lambda s:html.escape(str(s),quote=True)
BR=lambda s:E(s).replace('\n','<br>')
paths={k:f'/{k}/{v["slug"]}/' for k,v in L.items()}
icons=[]
for name in ['waves','bell-ring','sparkles','dumbbell','car-front','wifi']:
 target=out/'assets'/f'{name}.svg'
 if not target.exists():
  req=urllib.request.Request(f'https://unpkg.com/lucide-static@0.468.0/icons/{name}.svg',headers={'User-Agent':'VisionIconicSite/1.0'})
  target.write_bytes(urllib.request.urlopen(req).read())
 icons.append(target.read_text().replace('<svg ','<svg aria-hidden="true" '))
prices=[(1,False,2250000,612245,'76.45 m²',1),(2,False,3300000,897959,'95.22 m²',2),(2,True,4250000,1156463,'',0),(3,False,4999000,1360272,'111.29–121.91 m²',3),(3,True,6250000,1700680,'',0),(4,False,9999000,2720816,'287.03 m²',4),(5,False,14750000,4013605,'237.46 m²',5),(0,False,8712000,2370612,'',0)]
for lang,t in L.items():
 loc={'en':'en-US','fr':'fr-FR','es':'es-ES','nl':'nl-NL','de':'de-DE','pt':'pt-PT'}[lang]
 money=lambda n:f'{n:,}'.replace(',',' ' if lang=='fr' else '.' if lang in ['es','nl','de','pt'] else ',')
 cta=lambda text=None,unit='all',style='':f'<button class="btn {style}" data-enquire="{E(unit)}">{E(text or t["cta"])}</button>'
 loading='loading="lazy"'; priority='fetchpriority="high"'
 picture=lambda name,alt,cls='',lazy=True:f'<img class="{cls}" src="/assets/{name}.webp" alt="{E(alt)}" {loading if lazy else priority} decoding="async">'
 langs=''.join(f'<a href="{p}" lang="{k}" hreflang="{k}">{E(L[k]["countryTitle"])}</a>' for k,p in paths.items())
 nav=''.join(f'<a href="#{id}">{E(label)}</a>' for id,label in zip(['vision','residences','dubai','faq'],t['nav']))
 language_links=''.join(f'<a href="{p}" lang="{k}" hreflang="{k}" {"aria-current=page" if k==lang else ""}><span>{E(L[k]["name"])}</span><span class="language-code">{k.upper()}</span></a>' for k,p in paths.items())
 opts=''.join(f'<option value="{p}" {"selected" if k==lang else ""}>{E(L[k]["name"])}</option>' for k,p in paths.items())
 rows=''
 for i,(bed,royal,aed,usd,area,plan) in enumerate(prices):
  name=(f'{bed} {t["bed"]}'+(' · '+t['royal'] if royal else '')) if bed else t['retail']
  planbutton=f'<button class="text-link" data-plan="/assets/plan-{plan}.png" data-name="{E(name)}">{E(t["plans"])}</button>' if plan else ''
  unit=str(bed)+('-royal' if royal else '')
  rows+=f'<article class="res-row"><span class="res-num">0{i+1}</span><div><h3 class="res-name">{E(name)}</h3><span class="res-area">{E(area+" · "+t["area"]) if area else ""}</span></div><div class="res-price"><span data-price data-aed="{aed}" data-usd="{usd}">AED {money(aed)}</span><small>USD {money(usd)} · {E(t["from"])}</small></div><div class="res-actions">{planbutton}<button class="text-link" data-enquire="{E(unit)}">{E(t["quote"])}</button></div></article>'
 benefits=''.join(f'<article class="benefit reveal"><strong>{E(num)}</strong><h3>{E(title)}</h3><p>{E(body)}</p></article>' for num,title,body in t['benefits'])
 steps=''.join(f'<article class="step"><span>0{i+1}</span><div><h3>{E(title)}</h3><p>{E(body)}</p></div></article>' for i,(title,body) in enumerate(t['steps']))
 faqs=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in t['faq'])
 amenities=''.join(f'<div class="amenity">{icon}<span>{E(label)}</span></div>' for icon,label in zip(icons,t['amenities']))
 faqSchema={'@context':'https://schema.org','@type':'FAQPage','inLanguage':lang,'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in t['faq']]}
 projectSchema={'@context':'https://schema.org','@type':'ApartmentComplex','name':'Vision Iconic — Mercedes-Benz Places | Binghatti City','address':{'@type':'PostalAddress','addressLocality':'Nad Al Sheba 1, Dubai','addressCountry':'AE'},'numberOfAccommodationUnits':1426,'description':t['description']}
 if origin:projectSchema.update(url=origin+paths[lang],image=origin+'/assets/hero.webp')
 hreflang=''.join(f'<link rel="alternate" hreflang="{k}" href="{origin+p}">' for k,p in paths.items())+f'<link rel="alternate" hreflang="x-default" href="{origin+paths["en"]}">'
 site=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(t['title'])}</title><meta name="description" content="{E(t['description'])}"><meta name="theme-color" content="#080809"><link rel="canonical" href="{origin+paths[lang]}">{hreflang}<meta property="og:type" content="website"><meta property="og:locale" content="{loc.replace('-','_')}"><meta property="og:title" content="{E(t['title'])}"><meta property="og:description" content="{E(t['description'])}"><meta property="og:url" content="{origin+paths[lang]}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="preload" as="image" href="/assets/hero.webp"><link rel="stylesheet" href="/assets/style.css?v=2"><script type="application/ld+json">{json.dumps(faqSchema,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(projectSchema,ensure_ascii=False)}</script></head>
<body><a class="skip-link" href="#main">{E(t['nav'][0])}</a>
<header class="masthead"><a href="{paths[lang]}" aria-label="Vision Iconic"><img class="brand" src="/assets/brand.svg" alt="Mercedes-Benz Places | Binghatti City" width="175" height="100"></a><nav class="nav" aria-label="{E(t['nav'][0])}">{nav}</nav><div class="nav-control"><div class="language-picker" data-language-picker><button class="language-trigger" type="button" aria-expanded="false" aria-controls="language-panel" aria-label="{E(t['select'])}" data-language-trigger><span>{lang.upper()}</span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button><nav class="language-panel" id="language-panel" aria-label="{E(t['select'])}" hidden>{language_links}</nav></div><button class="btn nav-cta" data-enquire="all">{E(t['cta'])}</button></div></header>
<main id="main"><section class="hero">{picture('hero','Vision Iconic — Mercedes-Benz Places | Binghatti City','hero-image',False)}<div class="hero-content"><p class="eyebrow">{E(t['eyebrow'])}</p><h1><span class="sr-only">Vision Iconic — {E(t['title'])}. </span>{''.join('<span>'+E(x)+'</span>' for x in t['hero'])}</h1><div class="hero-copy"><div><p>{E(t['intro'])}</p>{cta(style='red')}</div><div class="hero-price"><span class="eyebrow">{E(t['from'])}</span><br>AED 2,250,000<br><span class="muted">USD 612,245</span></div></div></div><div class="hero-bottom"><a href="#vision">{E(t['scroll'])}</a><span>VISION ICONIC / DUBAI</span></div></section>
<div class="stats"><div class="location">{E(t['labels'][0])}</div>{''.join(f'<div class="stat"><strong>{v}</strong><small>{E(k)}</small></div>' for v,k in zip(['67','1,426','1–5'],t['labels'][1:]))}</div>
<section class="section" id="vision"><div class="vision-top reveal"><p class="eyebrow">{E(t['chapter'])}</p><h2>{BR(t['headline'])}</h2></div><div class="vision-grid"><div>{picture('detail',t['caption'],'photo')}<p class="caption">VISION ICONIC / MERCEDES-BENZ PLACES</p></div><div class="copy reveal"><p>{E(t['body'])}</p>{cta(style='outline')}{picture('car','Mercedes-Benz Vision Iconic','mini')}<p class="caption">{E(t['caption'])}</p></div></div></section>
<section class="section life">{picture('arrival',t['lifeTitle'].replace(chr(10),' '),'wide-photo')}<div class="life-content"><div class="reveal"><p class="eyebrow">{E(t['lifeTag'])}</p><h2>{BR(t['lifeTitle'])}</h2></div><div class="reveal"><p>{E(t['lifeBody'])}</p><div class="amenities">{amenities}</div></div></div></section>
<section class="section residences" id="residences"><p class="eyebrow">{E(t['resTag'])}</p><div class="res-heading reveal"><h2>{BR(t['resTitle'])}</h2><p>{E(t['resBody'])}</p></div><div class="currency-toggle" role="group" aria-label="{E(t['currency'])}"><button data-currency="AED" aria-pressed="true">AED</button><button data-currency="USD" aria-pressed="false">USD</button></div><div class="res-list">{rows}</div><p class="price-note">{E(t['priceNote'])}</p><div class="plan-inline"><div><p class="eyebrow">VISION ICONIC / 01</p><h3>1 {E(t['bed'])}</h3><p>76.45 m² / 822.90 ft²</p><button class="text-link" data-plan="/assets/plan-1.png" data-name="1 {E(t['bed'])}">{E(t['plans'])}</button></div><img src="/assets/plan-1.png" alt="{E(t['plans'])} — 1 {E(t['bed'])}" loading="lazy"></div></section>
<section class="section invest" id="dubai"><p class="eyebrow">{E(t['investTag'])}</p><div class="invest-intro reveal"><h2>{BR(t['investTitle'])}</h2><p>{E(t['investBody'])}</p></div><div class="benefit-grid">{benefits}</div></section>
<section class="section process"><div class="process-grid"><h2 class="reveal">{BR(t['processTitle'])}</h2><div>{steps}</div></div></section>
<section class="visa">{picture('lifestyle',t['visaTitle'].replace(chr(10),' '))}<div class="visa-copy"><p class="eyebrow">{E({"en":"Investor Visa / Golden Visa","fr":"Visa investisseur / Golden Visa","es":"Visado de inversor / Golden Visa","nl":"Investeerdersvisum / Golden Visa","de":"Investorenvisum / Golden Visa","pt":"Visto de investidor / Golden Visa"}[lang])}</p><h2>{BR(t['visaTitle'])}</h2><p>{E(t['visaBody'])}</p>{cta(t['visaCta'],style='outline')}</div></section>
<section class="section country"><h2>{E(t['countryTitle'])}</h2><p>{E(t['countryBody'])}</p></section>
<section class="section" id="faq"><div class="faq-grid"><div><p class="eyebrow">05 / FAQ</p><h2>{BR(t['faqTitle'])}</h2></div><div>{faqs}</div></div></section>
<section class="section final"><div class="reveal"><h2>{BR(t['finalTitle'])}</h2><p>{E(t['finalBody'])}</p>{cta(style='red')}</div></section></main>
<footer class="footer"><div class="footer-top"><div><h3>VISION ICONIC</h3><p>{E(t['footer'])}</p></div><div><h3>{E(t['rooms'])}</h3>{''.join(f'<a href="#residences">{n} {E(t["bed"])}</a>' for n in range(1,6))}<a href="#faq">FAQ</a></div><div><h3>{E(t['guide'])}</h3>{langs}</div></div><div class="footer-mark">VISION ICONIC</div><p class="fineprint">{E(t['legal'])}</p><div class="footer-bottom"><span>© {2026} VISION ICONIC</span><div><button data-privacy>{E(t['privacy'])}</button> · <a href="https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa" target="_blank" rel="noopener">{E(t['sources'])}</a></div></div></footer>
<button class="btn sticky-cta" data-enquire="all">{E(t['cta'])}</button>
<dialog id="plan-dialog" aria-labelledby="plan-name"><div class="dialog-top"><span id="plan-name" data-plan-name></span><button data-close>{E(t['close'])}</button></div><h2>{E(t['plans'])}</h2><img alt="" src="/assets/plan-1.png"><p class="caption">{E(t['area'])} · {E(t['priceNote'])}</p></dialog>
<dialog class="dialog-small" id="enquiry-dialog" aria-label="{E(t['cta'])}"><div class="dialog-top"><span>VISION ICONIC</span><button data-close>{E(t['close'])}</button></div><iframe title="Tally" data-tally-frame hidden></iframe><h2 id="enquiry-title" data-enquiry-empty>{E(t['unavailable'])}</h2><p data-enquiry-empty>{E(t['unavailableBody'])}</p></dialog>
<dialog class="dialog-small" id="privacy-dialog" aria-labelledby="privacy-title"><div class="dialog-top"><span>VISION ICONIC</span><button data-close>{E(t['close'])}</button></div><h2 id="privacy-title">{E(t['privacy'])}</h2><p>{E(t['privacyText'])}</p></dialog>
<script id="page-data" type="application/json">{json.dumps({'lang':lang,'locale':loc})}</script><script src="/assets/config.js?v=3"></script><script src="/assets/app.js?v=3" defer></script></body></html>'''
 folder=out/lang/t['slug'];folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(site)
 if lang=='en':(out/'index.html').write_text(site)
(out/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#090909"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-size="42" fill="white">V</text></svg>')
(out/'robots.txt').write_text('User-agent: *\nAllow: /\n'+(f'Sitemap: {origin}/sitemap.xml\n' if origin else ''))
if origin:
 (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{origin+p}</loc></url>' for p in paths.values())+'</urlset>')
print('Generated six language routes and English root.')

from seo_pages import extend_site
extend_site(out,L,paths,prices,origin)
