"""Build a fully offline searchable 65-type gallery and a 20-template contact sheet."""
from pathlib import Path
import argparse
import base64
import html
import json
import re

from PIL import Image,ImageDraw,ImageFont


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('gallery.html'))
    parser.add_argument('--contact-sheet',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent.parent
    catalog=json.loads((root/'assets/catalog.json').read_text(encoding='utf-8'))
    cards=[]
    for row in catalog:
        title=f"{row['name']} · {row['id']}"
        if row['route']=='python':
            png=root/'examples/renders'/f"{row['id']}.png"
            data=base64.b64encode(png.read_bytes()).decode()
            preview=f'<img loading="lazy" alt="{html.escape(title)}: synthetic data" src="data:image/png;base64,{data}">'
            badge='可直接渲染 · 合成数据示例'
        else:
            source=(root/row['example']).read_text(encoding='utf-8')
            # Read-only source examples: remove font/network links for offline inspection.
            source=re.sub(r'<link\b[^>]*>','',source,flags=re.I)
            source=re.sub(r'@import\s+url\([^;]*;','',source,flags=re.I)
            source=source.replace('</head>','<style>body{padding:8px!important;min-height:0!important}h1{font-size:20px!important} .frame{width:100%!important}svg{min-width:0!important;width:100%!important}.summary,.cards,footer{display:none!important}</style></head>')
            preview=f'<iframe loading="lazy" sandbox title="{html.escape(title)}" srcdoc="{html.escape(source,quote=True)}"></iframe>'
            badge='布局指导 · 上游设计参考（需按论文规范重绘）'
        schema=row.get('schema',row['use'])
        search=html.escape(' '.join(str(row.get(k,'')) for k in ('name','english','id','use','route')),quote=True)
        cards.append(f'<article data-search="{search}" data-route="{row["route"]}"><h2>{html.escape(title)}</h2><p class="badge">{badge}</p><details><summary>展开预览</summary>{preview}</details><p>{html.escape(schema)}</p></article>')
    content='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>论文配图 · 65 类图型</title>
<style>body{font:15px/1.6 Arial,"Microsoft YaHei",sans-serif;color:#222;background:#f6f6f6;margin:0;padding:28px}main{max-width:1400px;margin:auto}h1{margin:0}header{margin-bottom:24px}input,select{font:inherit;padding:9px;border:1px solid #999;border-radius:4px}input{width:min(650px,70%)}#grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:18px}article{padding:18px;background:white;border:1px solid #ddd;border-radius:6px}h2{font-size:17px;margin:0}.badge{font-size:12px;color:#555}iframe{width:100%;height:300px;border:0;background:white}img{width:100%;height:auto}summary{cursor:pointer}article p{overflow-wrap:anywhere}[hidden]{display:none!important}</style>
<main><header><h1>论文配图 · 65 类图型</h1><p>45 类布局指导 + 20 类可直接运行的科研模板。上游参考示例保留其设计；科研预览是合成数据，不能作为实验结果。</p><input id="search" aria-label="搜索图型" placeholder="搜索：流程、roc、distribution、forest…"><select id="route" aria-label="生成路线"><option value="">全部路线</option><option value="guided-svg">按规范绘制 SVG · 45 类</option><option value="python">Python 直接渲染 · 20 类</option></select><p id="count"></p></header><section id="grid">'''+''.join(cards)+'''</section></main>
<script>const search=document.querySelector('#search'),route=document.querySelector('#route'),cards=[...document.querySelectorAll('article')];function filter(){const q=search.value.trim().toLowerCase();let n=0;for(const c of cards){const show=c.dataset.search.toLowerCase().includes(q)&&(!route.value||c.dataset.route===route.value);c.hidden=!show;n+=show?1:0}document.querySelector('#count').textContent=`显示 ${n} / 65 类`}search.addEventListener('input',filter);route.addEventListener('change',filter);filter();</script></html>'''
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(content,encoding='utf-8')
    if args.contact_sheet:
        plots=[r for r in catalog if r['route']=='python']
        cellw,cellh=480,430
        sheet=Image.new('RGB',(cellw*4,cellh*5),'white')
        draw=ImageDraw.Draw(sheet)
        font_path=Path('C:/Windows/Fonts/arial.ttf')
        font=ImageFont.truetype(str(font_path),18) if font_path.exists() else ImageFont.load_default()
        for i,row in enumerate(plots):
            x,y=(i%4)*cellw,(i//4)*cellh
            draw.text((x+15,y+10),row['id'],font=font,fill='#111111')
            with Image.open(root/'examples/renders'/f"{row['id']}.png") as im:
                im=im.convert('RGB');im.thumbnail((cellw-20,cellh-50))
                sheet.paste(im,(x+(cellw-im.width)//2,y+45))
        args.contact_sheet.parent.mkdir(parents=True,exist_ok=True)
        sheet.save(args.contact_sheet)
    print(f'Offline gallery: {args.out}; {len(catalog)} searchable types')


if __name__=='__main__':
    main()
