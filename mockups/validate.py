import os, json, re
from playwright.sync_api import sync_playwright
OUT="/home/user/audit/mockups"
AXE="/home/user/audit/axe.min.js" if os.path.exists("/home/user/audit/axe.min.js") else "/home/user/audit/mockups/axe.min.js"

PAGES=["01-overview","02-order-detail","03-deposits","04-nav"]

def check(pg, tag):
    r={}
    r["mains"]=pg.evaluate("()=>[...document.querySelectorAll('main')].map(m=>m.id||'(no id)')")
    r["duplicate_ids"]=pg.evaluate("""()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
      const d={}; ids.forEach(i=>d[i]=(d[i]||0)+1); return Object.entries(d).filter(([k,v])=>v>1).map(([k,v])=>k+' x'+v);}""")
    r["comfort_visible"]=pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>/Lecture/i.test(x.innerText||''));
      if(!b) return 'no button'; const r=b.getBoundingClientRect(); return r.width>0&&r.height>0 ? 'VISIBLE '+Math.round(r.width)+'x'+Math.round(r.height) : 'HIDDEN';}""")
    r["context_bar"]=pg.evaluate("""()=>{const b=document.querySelector('.account-context-bar'); if(!b) return 'none';
      const r=b.getBoundingClientRect(); return Math.round(r.height)+'px tall';}""")
    r["nav_strip_removed"]=pg.evaluate("()=>!document.querySelector('nav[aria-label=\"Sections de votre compte\"] ul.overflow-x-auto')")
    r["nav_drawer"]=pg.evaluate("()=>!!document.querySelector('#account-nav-drawer')")
    r["spec_ids_left"]=pg.evaluate("""()=>{const t=document.body.innerText;
      return (t.match(/—\\s*(R|F|C|H|N)\\d+[^\\n]{0,20}/g)||[]).slice(0,6);}""")
    r["badge"]=pg.evaluate("""()=>{const b=[...document.querySelectorAll('span')].find(s=>/Solde/i.test(s.textContent||'')&&/€/.test(s.textContent||''));
      return b?b.textContent.trim():'not found';}""")
    r["small_text"]=pg.evaluate("""()=>{const c={}; document.querySelectorAll('*').forEach(e=>{
      if(e.children.length) return; const t=(e.textContent||'').trim(); if(!t) return;
      const rc=e.getBoundingClientRect(); if(!rc.width) return; const cs=getComputedStyle(e);
      if(cs.visibility==='hidden') return; const s=parseFloat(cs.fontSize); if(s>=14) return;
      c[cs.fontSize]=(c[cs.fontSize]||0)+1;}); return c;}""")
    r["small_targets"]=pg.evaluate("""()=>{const s=[]; document.querySelectorAll('a[href],button,input,select').forEach(e=>{
      const rc=e.getBoundingClientRect(); if(!rc.width||!rc.height) return;
      if(rc.width<24||rc.height<24) s.push(e.tagName+' '+Math.round(rc.width)+'x'+Math.round(rc.height)+' '+((e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,26)));});
      return s.slice(0,10);}""")
    return r

with sync_playwright() as p:
    b=p.chromium.launch()
    for vp,w,h in [("mobile",390,844),("desktop",1440,1000)]:
        ctx=b.new_context(viewport={"width":w,"height":h},locale="fr-FR"); pg=ctx.new_page()
        for slug in PAGES:
            for kind in ["before","after"]:
                url=f"file://{OUT}/screens/{slug}.{kind}.html"
                pg.goto(url, wait_until="networkidle"); pg.wait_for_timeout(700)
                if kind=="after":
                    try:
                        pg.add_script_tag(path=AXE)
                        ax=pg.evaluate("async()=>{const r=await axe.run(document,{resultTypes:['violations']}); return r.violations.map(v=>v.id+'('+v.nodes.length+')');}")
                    except Exception as e: ax=["AXE_ERR:"+str(e)[:60]]
                    print(f"\n=== {slug} [{vp}] AFTER ===")
                    print("   axe:", ax)
                    for k,v in check(pg,"after").items(): print(f"   {k}: {v}")
                    pg.screenshot(path=f"/home/user/audit/shots/after-{slug}-{vp}.png", full_page=False)
                else:
                    try:
                        pg.add_script_tag(path=AXE)
                        ax=pg.evaluate("async()=>{const r=await axe.run(document,{resultTypes:['violations']}); return r.violations.map(v=>v.id+'('+v.nodes.length+')');}")
                    except Exception as e: ax=["AXE_ERR"]
                    print(f"\n--- {slug} [{vp}] BEFORE : axe {ax}")
        ctx.close()
    b.close()
