import json
from playwright.sync_api import sync_playwright
AXE="/home/user/audit/axe.min.js"
M="/home/user/audit/mockups/screens"
OUT="/home/user/audit/shots"

def probe(pg):
    return pg.evaluate("""()=>{
      const q=(s)=>[...document.querySelectorAll(s)];
      // 1. in-scope text below 14px
      const smallIn=[]; q('*').forEach(e=>{
        if(e.children.length) return; const t=(e.textContent||'').trim(); if(!t) return;
        const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
        const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none') return;
        if(parseFloat(cs.fontSize)<14 && e.closest('[data-scope="account"]'))
          smallIn.push(cs.fontSize+' '+(e.className||'').toString().slice(0,34)+' :: '+t.slice(0,28));
      });
      // 2. context bar occlusion
      const bar=document.querySelector('.account-context-bar');
      let occl=0, barH=0;
      if(bar){ const br=bar.getBoundingClientRect(); barH=Math.round(br.height);
        q('[data-scope="account"] h1,[data-scope="account"] h2,[data-scope="account"] h3,[data-scope="account"] p,[data-scope="account"] a,[data-scope="account"] button').forEach(e=>{
          const r=e.getBoundingClientRect();
          if(r.width===0||r.height===0) return;
          if(r.bottom>br.top && r.top<br.bottom && r.left<br.right && r.right>br.left) occl++;
        }); }
      // 3. nav coverage
      const nav=document.querySelector('nav[aria-label="Sections de votre compte"]');
      const links=nav?nav.querySelectorAll('a'):[];
      // 4. tap targets < 24px inside the account scope
      const small=[]; q('[data-scope="account"] a[href],[data-scope="account"] button,[data-scope="account"] input,[data-scope="account"] select').forEach(e=>{
        const r=e.getBoundingClientRect(); if(!r.width||!r.height) return;
        if(r.width<24||r.height<24) small.push(e.tagName+' '+Math.round(r.width)+'x'+Math.round(r.height)+' '+((e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,24)));
      });
      // 5. contrast-critical colours still present
      const muted=q('[data-scope="account"] .text-ardoise-300').map(e=>getComputedStyle(e).color);
      return {smallIn, barH, occl, navLinks:links.length, navLabels:[...links].map(a=>a.textContent.trim()).slice(0,20),
              smallTargets:small.slice(0,8), mutedCount:muted.length, mutedSample:muted.slice(0,3),
              mains:q('main').length, dupIds:(()=>{const d={};q('[id]').forEach(e=>d[e.id]=(d[e.id]||0)+1);
                     return Object.entries(d).filter(([k,v])=>v>1).map(([k,v])=>k+' x'+v);})()};
    }""")

def axe_targets(pg):
    pg.add_script_tag(path=AXE)
    return pg.evaluate("""async()=>{const r=await axe.run(document,{resultTypes:['violations']});
      return r.violations.map(v=>({id:v.id,n:v.nodes.length,t:v.nodes.map(n=>n.target.join(' ')+' :: '+n.html.slice(0,80))}));}""")

with sync_playwright() as p:
    b=p.chromium.launch()
    for vp,w,h in [("mobile",390,844),("desktop",1440,1000)]:
        ctx=b.new_context(viewport={"width":w,"height":h},locale="fr-FR", device_scale_factor=1)
        pg=ctx.new_page()
        for slug in ["01-overview","02-order-detail","03-deposits","04-nav"]:
            for kind in ["before","after"]:
                pg.goto(f"file://{M}/{slug}.{kind}.html", wait_until="networkidle"); pg.wait_for_timeout(700)
                d=probe(pg)
                ax=axe_targets(pg)
                print(f"\n{'='*74}\n{slug.upper()} · {kind.upper()} · {vp} ({w}×{h})")
                print(f"  axe violations : {[(v['id'],v['n']) for v in ax]}")
                for v in ax:
                    for t in v['t'][:4]: print(f"       - {t[:140]}")
                print(f"  <main> count   : {d['mains']}   duplicate ids: {d['dupIds']}")
                print(f"  in-scope text <14px : {len(d['smallIn'])} {d['smallIn'][:4]}")
                print(f"  context bar    : {d['barH']}px  ·  elements overlapped: {d['occl']}")
                print(f"  account nav    : {d['navLinks']} links")
                print(f"  text-ardoise-300 remaining in scope: {d['mutedCount']} {d['mutedSample']}")
                print(f"  tap targets <24px in scope : {len(d['smallTargets'])} {d['smallTargets'][:4]}")
                pg.screenshot(path=f"{OUT}/{kind}-{slug}-{vp}.png", full_page=(kind=="after" and vp=="mobile"))
        ctx.close()
    b.close()
print("\nDONE")
