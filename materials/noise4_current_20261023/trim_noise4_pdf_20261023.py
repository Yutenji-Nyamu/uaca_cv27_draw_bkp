import sys,json,subprocess
from pathlib import Path
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import RectangleObject
import pdfplumber
reader=PdfReader(sys.argv[1]);p=reader.pages[0]
b=json.loads(sys.argv[3]);h=float(p.mediabox.height)
x0,y0,x1,y1=(b[0]-3)*.375,h-(b[3]+3)*.375,(b[2]+3)*.375,h-(b[1]-3)*.375
p.add_transformation(Transformation().translate(-x0,-y0))
p.mediabox=RectangleObject([0,0,x1-x0,y1-y0]);p.cropbox=RectangleObject([0,0,x1-x0,y1-y0])
w=PdfWriter();w.add_page(p)
with open(sys.argv[2],'wb') as f:w.write(f)
poppler=r'C:\Users\86136\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
prefix=str(Path(sys.argv[2]).with_suffix(''))+'_pdf'
subprocess.run([poppler,'-r','110','-png','-singlefile',sys.argv[2],prefix],check=True,capture_output=True)
with pdfplumber.open(sys.argv[2]) as d:
 p=d.pages[0]
 print(json.dumps(dict(pages=len(d.pages),size=[p.width,p.height],vector_paths=len(p.curves)+len(p.lines)+len(p.rects),text_characters=len(p.chars),raster_images=len(p.images))))
