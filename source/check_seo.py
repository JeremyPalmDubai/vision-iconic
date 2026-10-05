from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,xml.etree.ElementTree as ET
root=Path(__file__).parent;out=root/'dist';origin='https://vision-iconic-residences.com';errors=[];pages={}
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.h1=0;self.canonical=[];self.alternates={};self.description='';self.title='';self.in_title=False;self.schemas=[];self.in_schema=False;self.buf=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if tag=='h1':self.h1+=1
  if tag=='title':self.in_title=True
  if tag=='meta' and a.get('name')=='description':self.description=a.get('content','')
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='link' and a.get('rel')=='alternate':self.alternates[a['hreflang']]=a['href']
  if tag=='script' and a.get('type')=='application/ld+json':self.in_schema=True;self.buf=''
 def handle_data(self,data):
  if self.in_title:self.title+=data
  if self.in_schema:self.buf+=data
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='script' and self.in_schema:self.schemas.append(json.loads(self.buf));self.in_schema=False
for p in out.rglob('*.html'):
 if p.name=='404.html':continue
 parser=Parser();parser.feed(p.read_text());url='/'+str(p.relative_to(out).parent)+'/' if p!=out/'index.html' else '/';pages[url]=parser
 if parser.h1!=1:errors.append((url,'h1',parser.h1))
 if len(parser.canonical)!=1 or not parser.canonical[0].startswith(origin):errors.append((url,'canonical'))
 if not parser.description or not parser.title:errors.append((url,'metadata'))
 if len(parser.alternates)!=7:errors.append((url,'hreflang count'))
 for tag,a in parser.tags:
  for key in ['href','src','data-plan']:
   v=a.get(key,'');u=urlparse(v)
   if v.startswith('/') or u.netloc=='vision-iconic-residences.com':
    if not (out/u.path.lstrip('/')).exists():errors.append((url,'missing ref',v))
for url,p in pages.items():
 for lang,alternate in p.alternates.items():
  target=urlparse(alternate).path
  if target not in pages:errors.append((url,'missing alternate',target));continue
  if p.canonical[0] not in pages[target].alternates.values():errors.append((url,'nonreciprocal',target))
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
x=ET.parse(out/'sitemap.xml');urls=x.findall('s:url',ns)
if len(urls)!=90:errors.append(('sitemap count',len(urls)))
for u in urls:
 if len(u.findall('x:link',ns))!=7:errors.append(('sitemap alternates'))
canonical=[p for u,p in pages.items() if u!='/']
if len({p.title for p in canonical})!=90:errors.append(('duplicate titles'))
if len({p.description for p in canonical})!=90:errors.append(('duplicate descriptions'))
print(json.dumps({'canonicalPages':len(canonical),'sitemapUrls':len(urls),'errors':errors},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
