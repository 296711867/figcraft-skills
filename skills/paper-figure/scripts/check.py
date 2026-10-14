"""Small behavioral check for scientific semantics and shipped resources.

Run after generating all demos: python scripts/check.py
"""
from pathlib import Path
import hashlib
import json
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image
import numpy as np
import render


def rejects(call):
    try:
        call()
    except (ValueError, KeyError):
        return
    raise AssertionError('Invalid data was accepted')


def main():
    root=Path(__file__).resolve().parent.parent
    catalog=json.loads((root/'assets/catalog.json').read_text(encoding='utf-8'))
    assert len(catalog)==65 and len({r['id'] for r in catalog})==65
    assert sum(r['route']=='guided-svg' for r in catalog)==45
    assert {r['id'] for r in catalog if r['route']=='python'}==set(render.TYPES)
    for row in catalog:
        assert (root/row['reference']).is_file(), row['reference']
        assert (root/row['example']).is_file(), row['example']

    # Correct threshold grouping even when scores tie across positive/negative classes.
    fpr,recall,precision,base=render.binary_curve(dict(y_true=[0,1],score=[.5,.5]))
    assert np.allclose(fpr,[0,1]) and np.allclose(recall,[0,1])
    assert np.isclose(np.trapezoid(recall,fpr),.5) and np.isclose(precision[-1],.5)
    fpr,recall,precision,base=render.binary_curve(dict(y_true=[0,0,1,1],score=[.1,.2,.8,.9]))
    assert np.isclose(np.trapezoid(recall,fpr),1)
    assert np.isclose(np.sum(np.diff(recall)*precision[1:]),1)
    rejects(lambda:render.binary_curve(dict(y_true=[1,1],score=[.2,.4])))
    rejects(lambda:render.binary_curve(dict(y_true=[0,1],score=[.4])))
    rejects(lambda:render.vector(dict(values=[1,float('nan')]),'values'))
    rejects(lambda:render.bounds(dict(y=[2],lower=[3],upper=[4],interval_label='SD')))
    rejects(lambda:render.bounds(dict(y=[2],lower=[1],upper=[3])))

    for kind in render.TYPES:
        stem=root/'examples/renders'/kind
        spec=json.loads(stem.with_suffix('.json').read_text(encoding='utf-8'))
        report=json.loads(stem.with_suffix('.manifest.json').read_text(encoding='utf-8'))
        assert spec['synthetic'] is True and report['synthetic'] is True
        canonical=json.dumps(spec,ensure_ascii=False,sort_keys=True,allow_nan=False).encode('utf-8')
        assert report['spec_sha256']==hashlib.sha256(canonical).hexdigest()
        assert not report['text_outside_canvas'], (kind,report['text_outside_canvas'])
        svg=ET.parse(stem.with_suffix('.svg')).getroot()
        assert svg.tag.endswith('svg')
        assert 'SYNTHETIC DEMO' in stem.with_suffix('.svg').read_text(encoding='utf-8')
        assert stem.with_suffix('.pdf').read_bytes().startswith(b'%PDF-')
        with Image.open(stem.with_suffix('.png')) as img:
            assert abs(img.width-report['width_mm']/25.4*report['dpi'])<2
            assert abs(img.info['dpi'][0]-report['dpi'])<1
            if report['grayscale']:
                rgb=np.asarray(img.convert('RGB'))
                assert np.array_equal(rgb[:,:,0],rgb[:,:,1]) and np.array_equal(rgb[:,:,1],rgb[:,:,2]), f'{kind}: unexpected color in grayscale output'
        assert report['visual_review']=='pending'

    # Real-data path: explicit source, unchanged input, valid output without synthetic label.
    with tempfile.TemporaryDirectory(prefix='paper-figure-check-',dir=Path.cwd()) as folder:
        spec=dict(type='errorbar',data=dict(x=[1,2],y=[2,4],lower=[1,3],upper=[3,5],interval_label='Supplied SD'),
                  provenance={'source':'Behavior check fixture; not a research result'})
        before=json.dumps(spec,sort_keys=True)
        report=render.render(spec,Path(folder)/'real',width_mm=89,dpi=100)
        assert before==json.dumps(spec,sort_keys=True)
        assert not report['synthetic'] and report['visual_review']=='pending'
        assert 'SYNTHETIC DEMO' not in (Path(folder)/'real.svg').read_text(encoding='utf-8')
        rejects(lambda:render.render(dict(type='histogram',data={'values':[1,2]}),Path(folder)/'missing-source'))
    print('PASS: 65 unique types; resources; tied/perfect ROC and AP; invalid inputs; 20 demo export sets; real-data provenance and no mutation.')


if __name__=='__main__':
    main()
