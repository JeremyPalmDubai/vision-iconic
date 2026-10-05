(()=>{
const data=JSON.parse(document.getElementById('page-data').textContent);
const config=window.VISION_CONFIG||{};
let currency='AED';
const openDialog=d=>{d.showModal();document.body.classList.add('modal-open')};
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('close',()=>{if(!document.querySelector('dialog[open]'))document.body.classList.remove('modal-open')}));
const closeButtons=document.querySelectorAll('[data-close]');
closeButtons.forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}));
const picker=document.querySelector('[data-language-picker]');
const languageTrigger=picker.querySelector('[data-language-trigger]');
const languagePanel=picker.querySelector('.language-panel');
const setLanguageOpen=(open)=>{languageTrigger.setAttribute('aria-expanded',String(open));languagePanel.hidden=!open};
languageTrigger.addEventListener('click',()=>setLanguageOpen(languagePanel.hidden));
languageTrigger.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();setLanguageOpen(true);languagePanel.querySelector('a').focus()}});
document.addEventListener('click',e=>{if(!picker.contains(e.target))setLanguageOpen(false)});
picker.addEventListener('keydown',e=>{if(e.key==='Escape'){setLanguageOpen(false);languageTrigger.focus()}});
picker.addEventListener('focusout',e=>{if(!picker.contains(e.relatedTarget))setLanguageOpen(false)});
document.querySelectorAll('[data-currency]').forEach(b=>b.addEventListener('click',()=>{currency=b.dataset.currency;document.querySelectorAll('[data-currency]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('[data-price]').forEach(x=>{const value=Number(x.dataset[currency.toLowerCase()]);x.textContent=(currency==='USD'?'USD ':'AED ')+new Intl.NumberFormat(data.locale).format(value)})}));
document.querySelectorAll('[data-plan]').forEach(b=>b.addEventListener('click',()=>{const d=document.getElementById('plan-dialog');d.querySelector('img').src=b.dataset.plan;d.querySelector('img').alt=b.dataset.name;d.querySelector('[data-plan-name]').textContent=b.dataset.name;openDialog(d)}));
document.querySelectorAll('[data-enquire]').forEach(b=>b.addEventListener('click',()=>{if(config.tallyUrl){let url;try{url=new URL(config.tallyUrl);if(url.protocol!=='https:'||!/(^|\.)tally\.so$/.test(url.hostname))throw Error('Invalid Tally URL')}catch{openDialog(document.getElementById('enquiry-dialog'));return}url.searchParams.set('language',data.lang);url.searchParams.set('residence',b.dataset.enquire||'all');url.searchParams.set('currency',currency);url.searchParams.set('source',location.pathname);const utm=new URLSearchParams(location.search);['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(k=>{if(utm.has(k))url.searchParams.set(k,utm.get(k))});const dialog=document.getElementById('enquiry-dialog');const frame=dialog.querySelector('[data-tally-frame]');url.pathname='/embed/'+url.pathname.split('/').filter(Boolean).pop();url.searchParams.set('hideTitle','1');url.searchParams.set('transparentBackground','1');url.searchParams.set('alignLeft','1');frame.title='ICONIC VISION - Gpt';frame.setAttribute('data-tally-src',url.href);frame.src=url.href;frame.hidden=false;if(!document.querySelector('script[data-tally-widget]')){const script=document.createElement('script');script.src='https://tally.so/widgets/embed.js';script.dataset.tallyWidget='true';script.onload=()=>{if(window.Tally)window.Tally.loadEmbeds()};document.body.appendChild(script)}else if(window.Tally)window.Tally.loadEmbeds();dialog.querySelectorAll('[data-enquiry-empty]').forEach(x=>x.hidden=true);openDialog(dialog)}else openDialog(document.getElementById('enquiry-dialog'))}));
document.querySelector('[data-privacy]').addEventListener('click',()=>openDialog(document.getElementById('privacy-dialog')));
if('IntersectionObserver'in window){if(!matchMedia('(prefers-reduced-motion: reduce)').matches){document.documentElement.classList.add('js-motion');const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('seen');observer.unobserve(e.target)}}),{threshold:.07});document.querySelectorAll('.reveal').forEach(e=>observer.observe(e))}const cta=document.querySelector('.sticky-cta');new IntersectionObserver(entries=>entries.forEach(e=>cta.classList.toggle('show',!e.isIntersecting)),{threshold:0}).observe(document.querySelector('.hero'))}
if(config.siteOrigin){const origin=config.siteOrigin.replace(/\/$/,'');document.querySelectorAll('link[rel="canonical"],link[rel="alternate"]').forEach(e=>e.href=origin+new URL(e.href).pathname)}
})();
