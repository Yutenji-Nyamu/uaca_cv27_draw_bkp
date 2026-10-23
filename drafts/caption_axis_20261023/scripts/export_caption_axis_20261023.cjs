const fs=require('fs'),path=require('path'),{spawnSync}=require('child_process');
const {chromium}=require('C:/Users/86136/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const staticSvgPage=require('./static_svg_page_20261018.cjs');
const R=path.resolve(__dirname,'..'),F=path.join(R,'previews/caption_axis_20261023'),P=F;
const python='C:/Users/86136/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const manifest=JSON.parse(fs.readFileSync(path.join(R,'logs/caption_axis_20261023/render_manifest.json'),'utf8'));
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--disable-gpu']});
 const page=await browser.newPage({viewport:{width:2200,height:1500},deviceScaleFactor:2});const errors=[],records=[];
 page.on('pageerror',e=>errors.push(String(e)));await page.route(/^https?:/,r=>r.abort());
 await page.setContent('<html><head><style>html,body{margin:0;background:white;overflow:hidden;-webkit-print-color-adjust:exact;print-color-adjust:exact}#graph{position:absolute;width:2200px;height:1500px;overflow:visible}</style><script>window.mxLoadResources=false;window.mxLoadStylesheets=false;window.mxBasePath="";window.RESOURCES_PATH="";window.STYLE_PATH="";window.SHAPES_PATH="";window.STENCIL_PATH="";window.GRAPH_IMAGE_PATH="";</script></head><body><div id="graph"></div></body></html>');
 await page.addScriptTag({path:path.join(__dirname,'vendor/viewer-static.min.js')});
 for(const item of manifest){
  await page.setViewportSize({width:2200,height:1500});
  const xml=fs.readFileSync(item.file,'utf8');
  const info=await page.evaluate(async xml=>{
   if(window.g)g.destroy();const el=document.getElementById('graph');el.innerHTML='';el.style.left='0px';el.style.top='0px';el.style.width='2200px';el.style.height='1500px';
   const doc=mxUtils.parseXml(xml),m=doc.getElementsByTagName('mxGraphModel')[0];window.currentEmbeddedFonts=m.getAttribute('extFonts')||'';
   window.loadedFontNames=window.loadedFontNames||new Set();
   for(const e of (m.getAttribute('extFonts')||'').split('|')){const cut=e.indexOf('^');if(cut<0)continue;const name=e.slice(0,cut);if(loadedFontNames.has(name))continue;const f=new FontFace(name,'url("'+e.slice(cut+1)+'")');document.fonts.add(f);await f.load();loadedFontNames.add(name);}
   window.g=new Graph(el);g.setEnabled(false);g.pageVisible=false;const iso=mxUtils.parseXml(mxUtils.getXml(m));new mxCodec(iso).decode(iso.documentElement,g.getModel());g.view.scaleAndTranslate(1,0,0);g.refresh();await document.fonts.ready;
   const b=g.getGraphBounds();g.view.scaleAndTranslate(1,16-b.x,16-b.y);g.refresh();
   const imgs=await Promise.all(Array.from(document.querySelectorAll('image')).map(im=>new Promise(resolve=>{const t=new Image();t.onload=()=>resolve(true);t.onerror=()=>resolve(false);t.src=im.getAttribute('href')||im.getAttribute('xlink:href')})));
   const cells=Object.values(g.getModel().cells).filter(c=>c.vertex||c.edge);return {width:Math.ceil(b.width+32),height:Math.ceil(b.height+32),objects:cells.length,missing:cells.filter(c=>!g.view.getState(c)).length,images:imgs.length,failed:imgs.filter(x=>!x).length};
  },xml);
  if(info.missing||info.failed)throw Error('Missing elements '+JSON.stringify(info));
  await page.setViewportSize({width:info.width,height:info.height});await page.evaluate(()=>{g.view.invalidate();g.refresh()});await page.waitForTimeout(150);const raw=path.join(P,path.basename(item.stem)+'_uncropped.png');await page.screenshot({path:raw});
  const p=spawnSync(python,['-X','utf8',path.join(__dirname,'content_bbox_20261017.py'),raw],{encoding:'utf8'});if(p.status!==0)throw Error(p.stderr);const b=JSON.parse(p.stdout).map(x=>x/2),pad=1.5,w=b[2]-b[0]+2*pad,h=b[3]-b[1]+2*pad;
  await page.evaluate(({x,y,w,h,pad})=>{const el=document.getElementById('graph');g.view.scaleAndTranslate(1,g.view.translate.x+pad-x,g.view.translate.y+pad-y);g.refresh();el.style.width=w+'px';el.style.height=h+'px';document.body.style.width=w+'px';document.body.style.height=h+'px';},{x:b[0],y:b[1],w,h,pad});
  await page.setViewportSize({width:Math.ceil(w),height:Math.ceil(h)});
  const shot=await staticSvgPage(browser,page,Math.ceil(w),Math.ceil(h),2);await shot.screenshot({path:path.join(F,item.stem+'.png')});
  if(item.pdf)await shot.pdf({path:path.join(F,item.stem+'.pdf'),width:w+'px',height:h+'px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0},preferCSSPageSize:false,pageRanges:'1',scale:1});await shot.close();
  records.push({...item,...info,trim_bbox:b,width_css:w,height_css:h,white_margin_css:pad,png_pixels:[Math.ceil(w)*2,Math.ceil(h)*2]});
 }
 await browser.close();fs.writeFileSync(path.join(R,'logs/caption_axis_20261023/render_result.json'),JSON.stringify({renderer:'Native diagrams.net Graph/mxCodec; Chromium vector print',records,errors},null,2));console.log(JSON.stringify({files:records.length,errors,records:records.map(x=>({stem:x.stem,objects:x.objects,pdf:x.pdf,width:x.width_css,height:x.height_css}))}));
})().catch(e=>{console.error(String(e));process.exit(1)});