const fs=require('fs'),path=require('path'),{spawnSync}=require('child_process');
const {chromium}=require('C:/Users/86136/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const R='E:/0school/研二上/cvpr/uaca/draw',S=path.join(R,'scripts'),L=path.join(R,'logs/head_n39_swap_20261023'),P=path.join(R,'previews/head_n39_swap_20261023');
const python='C:/Users/86136/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const staticSvgPage=require(path.join(S,'static_svg_page_20261018.cjs'));
let manifest=JSON.parse(fs.readFileSync(path.join(L,'render_manifest.json'),'utf8'));
if(process.argv[2])manifest=manifest.filter(x=>process.argv.slice(2).includes(x.stem));
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--disable-gpu']});
 const records=[],errors=[];
 for(const item of manifest){
  const page=await browser.newPage({viewport:{width:2300,height:1500},deviceScaleFactor:2});
  page.on('pageerror',e=>errors.push(String(e)));await page.route(/^https?:/,r=>r.abort());
  await page.setContent('<html><head><style>html,body{margin:0;background:white;overflow:hidden;-webkit-print-color-adjust:exact;print-color-adjust:exact}#graph{position:absolute;width:2300px;height:1500px;overflow:visible}</style><script>window.mxLoadResources=false;window.mxLoadStylesheets=false;window.mxBasePath="";window.RESOURCES_PATH="";window.STYLE_PATH="";window.SHAPES_PATH="";window.STENCIL_PATH="";window.GRAPH_IMAGE_PATH="";</script></head><body><div id="graph"></div></body></html>');
  await page.addScriptTag({path:path.join(S,'vendor/viewer-static.min.js')});
  const info=await page.evaluate(async xml=>{
   const el=document.getElementById('graph');const doc=mxUtils.parseXml(xml),m=doc.getElementsByTagName('mxGraphModel')[0];window.currentEmbeddedFonts=m.getAttribute('extFonts')||'';
   for(const e of currentEmbeddedFonts.split('|')){const i=e.indexOf('^');if(i<0)continue;const f=new FontFace(e.slice(0,i),'url("'+e.slice(i+1)+'")');document.fonts.add(f);await f.load()}
   window.g=new Graph(el);g.setEnabled(false);g.pageVisible=false;const iso=mxUtils.parseXml(mxUtils.getXml(m));new mxCodec(iso).decode(iso.documentElement,g.getModel());g.view.scaleAndTranslate(1,0,0);g.refresh();await document.fonts.ready;
   const b=g.getGraphBounds();g.view.scaleAndTranslate(1,16-b.x,16-b.y);g.refresh();
   const imgs=await Promise.all(Array.from(document.querySelectorAll('image')).map(im=>new Promise(resolve=>{const t=new Image();t.onload=()=>resolve(true);t.onerror=()=>resolve(false);t.src=im.getAttribute('href')||im.getAttribute('xlink:href')})));
   await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
   const cells=Object.values(g.getModel().cells).filter(c=>c.vertex||c.edge);
   return {width:Math.ceil(b.width+32),height:Math.ceil(b.height+32),objects:cells.length,missing:cells.filter(c=>!g.view.getState(c)).length,images:imgs.length,failed:imgs.filter(x=>!x).length};
  },fs.readFileSync(item.file,'utf8'));
  if(info.missing||info.failed)throw Error(JSON.stringify(info));
  await page.setViewportSize({width:info.width,height:info.height});await page.evaluate(async()=>{g.view.invalidate();g.refresh();await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))});
  const raw=path.join(P,item.stem+'_uncropped.png');await page.screenshot({path:raw});
  const crop=spawnSync(python,['-X','utf8',path.join(S,'crop_native_preview_20261023.py'),raw,path.join(P,item.stem+'.png')],{encoding:'utf8'});if(crop.status!==0)throw Error(crop.stderr);
  const cropped=JSON.parse(crop.stdout);
  if(item.pdf){
   const fixed=await staticSvgPage(browser,page,info.width,info.height,2);
   await fixed.pdf({path:path.join(P,item.stem+'_uncropped.pdf'),width:info.width+'px',height:info.height+'px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0},pageRanges:'1',scale:1});await fixed.close();
   const trim=spawnSync(python,['-X','utf8',path.join(S,'trim_noise4_pdf_20261023.py'),path.join(P,item.stem+'_uncropped.pdf'),path.join(P,item.stem+'.pdf'),JSON.stringify(cropped.trim_bbox_pixels)],{encoding:'utf8'});if(trim.status!==0)throw Error(trim.stderr);
   cropped.pdf=JSON.parse(trim.stdout);
  }
  records.push({...item,...info,...cropped});await page.close();
  console.log(item.stem+' '+info.objects+' native objects; images '+info.images+'/'+info.images);
 }
 await browser.close();
 let all=[];const result=path.join(L,'render_result.json');if(fs.existsSync(result))all=JSON.parse(fs.readFileSync(result,'utf8')).records.filter(x=>!records.some(r=>r.stem===x.stem));
 fs.writeFileSync(result,JSON.stringify({records:all.concat(records),errors},null,2));
})().catch(e=>{console.error(e.stack);process.exit(1)});
