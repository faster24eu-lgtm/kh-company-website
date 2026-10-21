// sticky nav schaduw
const nav=document.getElementById('nav');
addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>10),{passive:true});
// mobiel menu
const burger=document.getElementById('burger'),links=document.getElementById('navlinks');
burger.addEventListener('click',()=>{const o=links.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
links.addEventListener('click',e=>{if(e.target.tagName==='A'){links.classList.remove('open');burger.setAttribute('aria-expanded',false)}});
// autotransport-aanvraag via WhatsApp
const route=document.getElementById('routeForm');
if(route)route.addEventListener('submit',e=>{
  e.preventDefault();
  const v=id=>document.getElementById(id).value.trim();
  const wa=document.querySelector('a[href^="https://wa.me/"]').href.split('?')[0];
  const msg=`Hallo Sleepdienst Janssen, ik wil graag een prijs voor autotransport.\nVan: ${v('van')}\nNaar: ${v('naar')}`;
  window.open(wa+'?text='+encodeURIComponent(msg),'_blank','noopener');
});
