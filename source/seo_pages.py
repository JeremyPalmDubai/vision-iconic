from pathlib import Path
import json,html,re
ROOT=Path(__file__).parent
DATA=json.loads((ROOT/'seo-data.json').read_text())
E=lambda s:html.escape(str(s),quote=True)

def unit_path(lang,index):
 d=DATA[lang];return f'/{lang}/{d["hubSlug"]}/{d["unitSlugs"][index]}/'
def hub_path(lang):return f'/{lang}/{DATA[lang]["hubSlug"]}/'
def guide_path(lang,index):return f'/{lang}/guides/{DATA[lang]["guideSlugs"][index]}/'

def extend_site(out,locales,homes,prices,origin):
 all_paths=list(homes.values());equiv_by_path={p:homes for p in homes.values()};section_heads={
 'en':['What the source confirms','Conditions to verify','Before you decide'],
 'fr':['Ce que les sources confirment','Conditions à vérifier','Avant de vous décider'],
 'es':['Qué confirman las fuentes','Condiciones a verificar','Antes de decidir'],
 'nl':['Wat de bronnen bevestigen','Te controleren voorwaarden','Voordat je beslist'],
 'de':['Was die Quellen bestätigen','Zu prüfende Bedingungen','Vor Ihrer Entscheidung'],
 'pt':['O que as fontes confirmam','Condições a verificar','Antes de decidir']}
 areas=['76.45 m²','95.22 / 193.38 m²',None,'111.29 / 121.91 m²',None,'287.03 m²','237.46 m²',None]
 photos=['detail','hero','lobby','lifestyle','arrival','city','hero','arrival']
 refs=[('Mercedes-Benz / Binghatti City','https://media.mercedes-benz.com/en/article/d9b4aab7-a355-4be3-b952-c151800e5dbc'),('Dubai Land Department','https://dubailand.gov.ae/en/frequently-asked-questions'),('UAE Golden Visa','https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa'),('ICP Golden Residency','https://icp.gov.ae/en/services/uae-golden-residency/'),('UAE taxation','https://u.ae/en/information-and-services/finance-and-investment/taxation'),('Federal Tax Authority','https://tax.gov.ae/en/content/real.estate.investment.for.natural.persons.ctgrei1.aspx')]
 for lang,t in locales.items():
  d=DATA[lang];z=d['labels'];home=(out/homes[lang].lstrip('/')/'index.html').read_text()
  header=home.split('<main id="main">')[0].split('<body>')[1]
  tail=home.split('</main>')[1].replace('</body></html>','')
  # Every navigation link on inner pages resolves to a real page or home section.
  header=header.replace('href="#','href="'+homes[lang]+'#')
  header=header.replace('href="'+homes[lang]+'#residences"','href="'+hub_path(lang)+'"')
  tail=tail.replace('href="#','href="'+homes[lang]+'#')
  fmt=lambda n:f'{n:,}'.replace(',',' ' if lang=='fr' else '.' if lang in ['es','nl','de','pt'] else ',')
  def cta(unit='all'):return f'<button class="btn red" data-enquire="{E(unit)}">{E(t["cta"])}</button>'
  def cards(skip=-1):
   result=''
   for i,p in enumerate(prices):
    if i==skip:continue
    result+=f'<a class="residence-card" href="{unit_path(lang,i)}"><span class="eyebrow">VISION ICONIC / {i+1:02}</span><h3>{E(d["unitNames"][i])}</h3><p>{E(z["price"])}</p><strong>AED {fmt(p[2])}</strong><span>USD {fmt(p[3])}</span><span class="card-link">{E(t["plans"] if p[5] else z["specs"])}</span></a>'
   return result
  def guides():return ''.join(f'<a class="guide-card" href="{guide_path(lang,j)}"><span class="eyebrow">{j+1:02}</span><h3>{E(g[0])}</h3><p>{E(g[1])}</p><span class="card-link">{E(z["read"])}</span></a>' for j,g in enumerate(d['guides']))
  def faq_html(pairs):return '<div class="seo-faq">'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in pairs)+'</div>'
  def hero(title,intro,img,unit='all',price=None):
   price_html=f'<div class="seo-hero-price"><span>{E(z["price"])}</span><strong>AED {fmt(price[2])}</strong><span>USD {fmt(price[3])}</span></div>' if price else ''
   return f'<section class="hero seo-hero"><img class="hero-image" src="/assets/{img}.webp" alt="Vision Iconic — Mercedes-Benz Places | Binghatti City" width="1600" height="1100" fetchpriority="high"><div class="seo-hero-copy"><p class="eyebrow">VISION ICONIC / DUBAI</p><h1>{E(title)}</h1><p>{E(intro)}</p>{price_html}{cta(unit)}</div></section>'
  def breadcrumbs(title,path):return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{homes[lang]}">{E(z["home"])}</a><span>/</span><a href="{hub_path(lang)}">{E(d["hub"])}</a><span>/</span><span aria-current="page">{E(title)}</span></nav>'
  def write(path,title,desc,body,equivalents,faq=None,breadcrumb=None):
   alternates=''.join(f'<link rel="alternate" hreflang="{k}" href="{origin+u}">' for k,u in equivalents.items())+f'<link rel="alternate" hreflang="x-default" href="{origin+equivalents["en"]}">'
   menu=''.join(f'<a href="{u}" lang="{k}" hreflang="{k}" {"aria-current=page" if k==lang else ""}><span>{E(locales[k]["name"])}</span><span class="language-code">{k.upper()}</span></a>' for k,u in equivalents.items())
   h=re.sub(r'(<nav class="language-panel"[^>]*>).*?(</nav>)',lambda m:m[1]+menu+m[2],header)
   schema={'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'inLanguage':lang,'about':{'@type':'ApartmentComplex','name':'Vision Iconic — Mercedes-Benz Places | Binghatti City'}}
   if origin:schema['url']=origin+path
   schemas=[schema]
   if faq:schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]})
   if origin:
    crumbs=[(z['home'],homes[lang]),(d['hub'],hub_path(lang))]
    if path!=hub_path(lang):crumbs.append((breadcrumb or title,path))
    schemas.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':origin+u} for i,(n,u) in enumerate(crumbs)]})
   js=''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False)+'</script>' for s in schemas)
   page=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#080809"><link rel="canonical" href="{origin+path}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{origin+path}"><link rel="icon" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/style.css?v=4">{js}</head><body>{h}<main id="main">{body}</main>{tail}</body></html>'
   target=out/path.lstrip('/');target.mkdir(parents=True,exist_ok=True);(target/'index.html').write_text(page);all_paths.append(path);equiv_by_path[path]=equivalents
  # Real editorial directory: every category can be reached with ordinary HTML links.
  hub_body=hero(d['hub'],d['hubIntro'],'hero')+f'<section class="section seo-catalogue"><div class="residence-cards">{cards()}</div><p class="price-note">{E(t["priceNote"])}</p></section><section class="section"><h2 class="seo-section-title">{E(z["guides"])}</h2><div class="guide-cards">{guides()}</div></section>'
  write(hub_path(lang),d['hub']+' | Dubai',d['hubIntro'],hub_body,{k:hub_path(k) for k in locales})
  for i,p in enumerate(prices):
   name=d['unitNames'][i];unit=str(p[0])+('-royal' if p[1] else '')
   title=name+' — Vision Iconic, Dubai'
   intro=d['unitBodies'][i]
   desc=name+' · Vision Iconic · AED '+fmt(p[2])+' / USD '+fmt(p[3])+'. '+z['specs']+'.'
   pairs=[(z['qprice'],z['aprice'].format(name=name,aed=fmt(p[2]),usd=fmt(p[3]))),(z['qplan'],intro if p[5] else z['noPlan']),(z['qremote'],z['aremote']),(z['qvisa'],z['avisa'])]
   plan=f'<img class="unit-plan" src="/assets/plan-{p[5]}.png" alt="{E(name+" — "+t["plans"])}" loading="lazy" width="2538" height="970"><button class="text-link" data-plan="/assets/plan-{p[5]}.png" data-name="{E(name)}">{E(t["plans"])}</button>' if p[5] else f'<p class="missing-plan">{E(z["noPlan"])}</p>'
   facts=f'<dl class="unit-facts"><div><dt>{E(z["price"])}</dt><dd>AED {fmt(p[2])}<small>USD {fmt(p[3])}</small></dd></div>'+(f'<div><dt>{E(z["area"])}</dt><dd>{E(areas[i])}</dd></div>' if areas[i] else '')+'</dl>'
   body=hero(name+'\nVision Iconic',intro,photos[i],unit,p)+breadcrumbs(name,unit_path(lang,i))
   body+=f'<section class="section unit-specs"><div><p class="eyebrow">VISION ICONIC / {i+1:02}</p><h2 class="seo-section-title">{E(z["specs"])}</h2>{facts}<p>{E(t["priceNote"])}</p><p class="caption">{E(z["context"])}</p></div><div><h3>{E(z["layout"])}</h3>{plan}</div></section>'
   body+=f'<section class="section seo-check"><h2 class="seo-section-title">{E(z["facts"])}</h2><ol>'+''.join(f'<li>{E(s)}</li>' for s in z['checklist'])+f'</ol>{cta(unit)}</section>'
   body+=f'<section class="section"><h2 class="seo-section-title">{E(z["faq"])}</h2>{faq_html(pairs)}</section><section class="section residences"><h2 class="seo-section-title">{E(z["other"])}</h2><div class="residence-cards">{cards(i)}</div></section><section class="section"><h2 class="seo-section-title">{E(z["guides"])}</h2><div class="guide-cards">{guides()}</div></section>'
   write(unit_path(lang,i),title,desc,body,{k:unit_path(k,i) for k in locales},pairs,name)
  for j,g in enumerate(d['guides']):
   title,desc,*paragraphs=g
   body=hero(title,desc,['detail','city','arrival','lifestyle','hero'][j],'guide:'+str(j))
   body+=f'<nav class="breadcrumbs"><a href="{homes[lang]}">{E(z["home"])}</a><span>/</span><a href="{hub_path(lang)}">{E(d["hub"])}</a><span>/</span><span>{E(title)}</span></nav>'
   body+=f'<section class="section article-grid"><article class="guide-article"><p class="caption">{E(z["updated"])}</p>'+''.join(f'<section><h2>{E(section_heads[lang][k])}</h2><p>{E(p)}</p></section>' for k,p in enumerate(paragraphs))+'</article>'
   body+=f'<aside class="guide-aside"><h2>{E(z["facts"])}</h2><ul>'+''.join(f'<li>{E(s)}</li>' for s in z['checklist'])+f'</ul>{cta("guide:"+str(j))}<a class="text-link" href="{hub_path(lang)}">{E(z["all"])}</a></aside></section>'
   if j==0:
    body+=f'<section class="section residences"><h2 class="seo-section-title">{E(z["specs"])}</h2><div class="residence-cards">{cards()}</div></section>'
   source_refs=[refs[1]] if j in [0,1] else [refs[0]] if j==2 else refs[2:4] if j==3 else refs[4:6]
   body+=f'<section class="section source-links"><h2>{E(z["sources"])}</h2>'+''.join(f'<a href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n,u in source_refs)+'</section>'
   body+=f'<section class="section"><h2 class="seo-section-title">{E(z["guides"])}</h2><div class="guide-cards">'+''.join(f'<a class="guide-card" href="{guide_path(lang,k)}"><h3>{E(v[0])}</h3><p>{E(v[1])}</p><span class="card-link">{E(z["read"])}</span></a>' for k,v in enumerate(d['guides']) if k!=j)+'</div></section>'
   write(guide_path(lang,j),title+' | Vision Iconic',desc,body,{k:guide_path(k,j) for k in locales},breadcrumb=title)
  # Upgrade existing landing page and default English copy, preserving imagery and interactions.
  for i,p in enumerate(prices):
   name=(f'{p[0]} {t["bed"]}'+(' · '+t['royal'] if p[1] else '')) if p[0] else t['retail']
   home=home.replace(f'<h3 class="res-name">{E(name)}</h3>',f'<h3 class="res-name"><a href="{unit_path(lang,i)}">{E(name)}</a></h3>')
  content=f'<section class="section seo-discover" id="buyer-guides"><div class="seo-discover-title"><h2 class="seo-section-title">{E(d["hub"])}</h2><a class="btn outline" href="{hub_path(lang)}">{E(z["all"])}</a></div><h3>{E(z["guides"])}</h3><div class="guide-cards">{guides()}</div></section>'
  home=home.replace('</main>',content+'</main>').replace('/assets/style.css?v=2','/assets/style.css?v=4')
  (out/homes[lang].lstrip('/')/'index.html').write_text(home)
  if lang=='en':(out/'index.html').write_text(home)
 # Production-only sitemap: no fake origin or localhost submitted to search engines.
 if origin:
  xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
  for p in all_paths:
   alts=equiv_by_path[p]
   xml+=f'<url><loc>{E(origin+p)}</loc>'+''.join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{E(origin+u)}"/>' for k,u in alts.items())+f'<xhtml:link rel="alternate" hreflang="x-default" href="{E(origin+alts["en"])}"/></url>'
  xml+='</urlset>'
  (out/'sitemap.xml').write_text(xml)
 (ROOT/'seo-route-map.json').write_text(json.dumps({'canonicalPageCount':len(all_paths),'routes':all_paths,'origin':origin or None},indent=2,ensure_ascii=False))
 print(f'SEO: {len(all_paths)} canonical pages in six languages.')
