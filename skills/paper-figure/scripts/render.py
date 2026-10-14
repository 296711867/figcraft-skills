"""Render a declared scientific figure. Demo data requires an explicit --demo.

Dependencies: numpy, matplotlib. No network access or implicit data loading.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
from statistics import NormalDist

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

SKILL = Path(__file__).resolve().parent.parent
TYPES = ('histogram box violin ecdf errorbar confidence-band regression residual qq '
         'bland-altman forest roc precision-recall calibration confusion correlation '
         'contour surface spectrogram multi-panel').split()


def vector(data, key, minimum=1):
    value = np.asarray(data[key], dtype=float)
    if value.ndim != 1 or value.size < minimum or not np.isfinite(value).all():
        raise ValueError(f'{key}: require >= {minimum} finite numbers in a one-dimensional array')
    return value


def paired(data, *keys, minimum=1):
    arrays = [vector(data, key, minimum) for key in keys]
    if len({a.size for a in arrays}) != 1:
        raise ValueError(f'{keys}: lengths must match')
    return arrays


def bounds(data, center='y'):
    y, low, high = paired(data, center, 'lower', 'upper')
    if np.any(low > y) or np.any(y > high):
        raise ValueError('Require lower <= estimate <= upper')
    if not data.get('interval_label'):
        raise ValueError('interval_label must declare CI, SD, SE or another interval meaning')
    return y, low, high


def binary_curve(data):
    truth, score = paired(data, 'y_true', 'score', minimum=2)
    if set(truth) != {0., 1.}:
        raise ValueError('Binary curves require both classes encoded as 0 and 1')
    order = np.argsort(-score, kind='stable')
    truth, score = truth[order], score[order]
    # Evaluate only the end of each tied threshold; ties cannot be ordered to improve AUC.
    ends = np.r_[np.flatnonzero(np.diff(score)), len(score)-1]
    tp = np.r_[0., np.cumsum(truth)[ends]]
    fp = np.r_[0., np.cumsum(1-truth)[ends]]
    recall, fpr = tp / truth.sum(), fp / (1-truth).sum()
    precision = np.divide(tp, tp+fp, out=np.ones_like(tp), where=(tp+fp)>0)
    return fpr, recall, precision, float(truth.mean())


def style(gray):
    colors = ['#222222','#666666','#999999','#444444'] if gray else ['#0072B2','#D55E00','#009E73','#CC79A7']
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Arial','Microsoft YaHei','SimHei','Noto Sans CJK SC','DejaVu Sans'] if f in available]
    plt.rcParams.update({'font.family': fonts, 'font.size': 8, 'axes.titlesize': 9,
                         'axes.labelsize': 8, 'legend.fontsize': 7, 'axes.linewidth': .7,
                         'lines.linewidth': 1.2, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'pdf.fonttype': 42, 'axes.unicode_minus': False,
                         'figure.facecolor': 'white', 'axes.facecolor': 'white'})
    return colors


def draw(ax, kind, data, colors, gray):
    ink = colors[0]
    if kind == 'histogram':
        ax.hist(vector(data,'values'), bins=data.get('bins',15), color=colors[1], edgecolor='white', linewidth=.5)
        ax.set(xlabel='Value', ylabel='Count')
    elif kind in ('box','violin','ecdf'):
        groups = data['groups']
        if not groups:
            raise ValueError('groups cannot be empty')
        values = [vector(g,'values',2 if kind=='violin' else 1) for g in groups]
        labels = [g['label'] for g in groups]
        if kind == 'box':
            bp = ax.boxplot(values, tick_labels=labels, patch_artist=True, widths=.5,
                            medianprops={'color':'#111111'}, whiskerprops={'color':'#444444'},
                            capprops={'color':'#444444'}, flierprops={'markeredgecolor':'#444444'})
            for i, box in enumerate(bp['boxes']):
                box.set(facecolor=colors[i%len(colors)], alpha=.55, hatch=['','///','xx','..'][i%4] if gray else '')
            ax.set_ylabel('Value')
        elif kind == 'violin':
            if any(np.ptp(v)==0 for v in values):
                raise ValueError('Violin density requires variation within each group; use box or ECDF for constant groups')
            vp = ax.violinplot(values,showmeans=False,showmedians=True)
            for key in ('cbars','cmins','cmaxes','cmedians'):
                vp[key].set_color('#444444')
            for i, body in enumerate(vp['bodies']):
                body.set(facecolor=colors[i%len(colors)],edgecolor='#222222',alpha=.55)
            ax.set_xticks(range(1,len(labels)+1),labels)
            ax.set_ylabel('Value')
        else:
            for i, (v, label) in enumerate(zip(values,labels)):
                ax.step(np.sort(v),np.arange(1,len(v)+1)/len(v),where='post',label=label,
                        color=colors[i%len(colors)],linestyle=['-','--',':','-.'][i%4])
            ax.set(xlabel='Value',ylabel='Cumulative probability',ylim=(0,1.02))
            ax.legend(frameon=False)
    elif kind in ('errorbar','confidence-band'):
        x = vector(data,'x')
        y, low, high = bounds(data)
        if len(x)!=len(y):
            raise ValueError('x and intervals must have equal lengths')
        if kind == 'errorbar':
            ax.errorbar(x,y,yerr=[y-low,high-y],fmt='o',capsize=3,color=ink,label=data['interval_label'])
        else:
            order = np.argsort(x)
            x,y,low,high = [v[order] for v in (x,y,low,high)]
            ax.plot(x,y,color=ink)
            ax.fill_between(x,low,high,color=ink,alpha=.18,label=data['interval_label'])
        ax.set(xlabel='X',ylabel='Estimate')
        ax.legend(frameon=False)
    elif kind == 'regression':
        x,y = paired(data,'x','y',minimum=3)
        if np.ptp(x)==0:
            raise ValueError('Regression requires varying x')
        coefficients = np.polyfit(x,y,1)
        grid = np.linspace(x.min(),x.max(),100)
        ax.scatter(x,y,s=10,color=ink,alpha=.6)
        ax.plot(grid,np.polyval(coefficients,grid),color=colors[1],label='OLS fit')
        ax.set(xlabel='X',ylabel='Y')
        ax.legend(frameon=False)
    elif kind == 'residual':
        fitted,residual = paired(data,'fitted','residuals')
        ax.scatter(fitted,residual,s=12,color=ink,alpha=.65)
        ax.axhline(0,color=colors[1],ls='--')
        ax.set(xlabel='Fitted value',ylabel='Residual')
    elif kind == 'qq':
        values = np.sort(vector(data,'values',minimum=2))
        theoretical = np.array([NormalDist().inv_cdf(float(p)) for p in (np.arange(len(values))+.5)/len(values)])
        ax.scatter(theoretical,values,s=12,color=ink)
        qx = np.array([NormalDist().inv_cdf(.25),NormalDist().inv_cdf(.75)])
        slope = np.diff(np.quantile(values,[.25,.75]))[0]/np.diff(qx)[0]
        intercept = np.quantile(values,.25)-slope*qx[0]
        ax.plot(theoretical,intercept+slope*theoretical,color=colors[1],ls='--',label='Quartile reference')
        ax.set(xlabel='Theoretical normal quantile',ylabel='Sample quantile')
    elif kind == 'bland-altman':
        a,b = paired(data,'a','b',minimum=2)
        difference, mean = a-b,(a+b)/2
        bias,sd = difference.mean(),difference.std(ddof=1)
        ax.scatter(mean,difference,s=12,color=ink,alpha=.65)
        for value,label,ls in [(bias,'Mean difference','-'),(bias-1.96*sd,'Lower LoA','--'),(bias+1.96*sd,'Upper LoA',':')]:
            ax.axhline(value,color=colors[1],ls=ls,label=f'{label}: {value:.3g}')
        ax.set(xlabel='Mean of paired measurements',ylabel='Difference (A - B)')
        ax.legend(frameon=False,fontsize=6,loc='upper center',bbox_to_anchor=(.5,-.22))
    elif kind == 'forest':
        y,low,high = bounds(data,'effect')
        labels = data['labels']
        if len(labels)!=len(y):
            raise ValueError('labels and effects must have equal lengths')
        null = float(data.get('null',0))
        scale = data.get('xscale','linear')
        if scale not in ('linear','log') or (scale=='log' and (np.any(low<=0) or null<=0)):
            raise ValueError('Log effect plots require positive bounds and a positive null (usually 1)')
        positions = np.arange(len(y))
        ax.errorbar(y,positions,xerr=[y-low,high-y],fmt='s',color=ink,capsize=3,label=data['interval_label'])
        ax.axvline(null,color=colors[1],ls='--')
        ax.set_yticks(positions,labels)
        ax.set(xlabel='Effect estimate',xscale=scale)
        ax.invert_yaxis()
        ax.legend(frameon=False,fontsize=6,loc='upper center',bbox_to_anchor=(.5,-.22))
    elif kind in ('roc','precision-recall'):
        fpr,recall,precision,prevalence = binary_curve(data)
        if kind == 'roc':
            auc = np.trapezoid(recall,fpr)
            ax.plot(fpr,recall,color=ink,label=f'AUC = {auc:.3f}')
            ax.plot([0,1],[0,1],color=colors[1],ls='--',label='Chance')
            ax.set(xlabel='False positive rate',ylabel='True positive rate')
        else:
            ap = np.sum(np.diff(recall)*precision[1:])
            ax.step(recall,precision,where='pre',color=ink,label=f'AP = {ap:.3f}')
            ax.axhline(prevalence,color=colors[1],ls='--',label=f'Prevalence = {prevalence:.3f}')
            ax.set(xlabel='Recall',ylabel='Precision')
        ax.set(xlim=(0,1),ylim=(0,1.02))
        ax.legend(frameon=False)
    elif kind == 'calibration':
        truth,p = paired(data,'y_true','probability')
        if not set(truth).issubset({0.,1.}) or np.any((p<0)|(p>1)):
            raise ValueError('Calibration requires binary truth and probabilities in [0,1]')
        bins = data.get('bins',10)
        if not isinstance(bins,int) or bins<1:
            raise ValueError('bins must be a positive integer')
        indices = np.minimum((p*bins).astype(int),bins-1)
        pairs = [(p[indices==i].mean(),truth[indices==i].mean()) for i in range(bins) if np.any(indices==i)]
        ax.plot(*np.array(pairs).T,'o-',color=ink,label='Equal-width bins')
        ax.plot([0,1],[0,1],ls='--',color=colors[1],label='Perfect calibration')
        ax.set(xlabel='Mean predicted probability',ylabel='Observed positive fraction',xlim=(0,1),ylim=(0,1))
        ax.legend(frameon=False)
    elif kind in ('confusion','correlation'):
        matrix = np.asarray(data['matrix'],dtype=float)
        labels = data['labels']
        if matrix.ndim!=2 or not np.isfinite(matrix).all() or not labels:
            raise ValueError('matrix must be finite and two-dimensional; labels cannot be empty')
        if kind == 'confusion':
            if matrix.shape!=(len(labels),len(labels)) or np.any(matrix<0) or np.any(matrix!=np.floor(matrix)):
                raise ValueError('Confusion matrix must be square nonnegative integer counts')
            normalize = data.get('normalize',False)
            if normalize:
                totals = matrix.sum(axis=1,keepdims=True)
                if np.any(totals==0):
                    raise ValueError('Cannot normalize a true class with zero observations')
                matrix = matrix/totals
            image = ax.imshow(matrix,cmap='Greys' if gray else 'Blues',vmin=0,vmax=1 if normalize else None)
            ax.set(xlabel='Predicted class',ylabel='True class')
            label = 'Row fraction' if normalize else 'Count'
        else:
            if matrix.shape[1]!=len(labels) or matrix.shape[0]<2 or np.any(matrix.std(axis=0)==0):
                raise ValueError('Correlation needs >=2 rows, one label per column and no constant columns')
            matrix = np.corrcoef(matrix,rowvar=False)
            matrix = np.atleast_2d(matrix)
            image = ax.imshow(matrix,cmap='gray' if gray else 'coolwarm',vmin=-1,vmax=1)
            label = 'Pearson r'
        ax.set_xticks(range(len(labels)),labels,rotation=35,ha='right')
        ax.set_yticks(range(len(labels)),labels)
        for i in range(len(labels)):
            for j in range(len(labels)):
                value=matrix[i,j]
                rgba=image.cmap(image.norm(value))
                luminance=.2126*rgba[0]+.7152*rgba[1]+.0722*rgba[2]
                ax.text(j,i,f'{value:.2f}' if kind=='correlation' or data.get('normalize') else f'{value:.0f}',
                        ha='center',va='center',fontsize=7,color='white' if luminance<.45 else '#111111')
        ax.figure.colorbar(image,ax=ax,label=label,shrink=.8)
    elif kind in ('contour','surface'):
        x,y=vector(data,'x',2),vector(data,'y',2)
        z=np.asarray(data['z'],dtype=float)
        if z.shape!=(len(y),len(x)) or not np.isfinite(z).all() or np.any(np.diff(x)<=0) or np.any(np.diff(y)<=0):
            raise ValueError('z shape must be (len(y),len(x)); grid coordinates must increase strictly')
        xx,yy=np.meshgrid(x,y)
        cmap='gray' if gray else 'viridis'
        if kind=='contour':
            image=ax.contourf(xx,yy,z,levels=data.get('levels',12),cmap=cmap)
        else:
            image=ax.plot_surface(xx,yy,z,cmap=cmap,linewidth=0,antialiased=True)
            ax.set_zlabel(data.get('zlabel','Value'))
        ax.figure.colorbar(image,ax=ax,label=data.get('zlabel','Value'),shrink=.7)
        ax.set(xlabel='X',ylabel='Y')
    elif kind=='spectrogram':
        signal=vector(data,'signal',minimum=4)
        rate=float(data['sample_rate'])
        nfft=data.get('nfft',min(128,len(signal)))
        overlap=data.get('overlap',nfft//2)
        if not np.isfinite(rate) or rate<=0 or not isinstance(nfft,int) or not 2<=nfft<=len(signal) or not isinstance(overlap,int) or not 0<=overlap<nfft:
            raise ValueError('Require sample_rate > 0, integer 2 <= nfft <= signal length and 0 <= overlap < nfft')
        _,_,_,image=ax.specgram(signal,NFFT=nfft,Fs=rate,noverlap=overlap,cmap='gray' if gray else 'viridis')
        ax.set(xlabel='Time (s)',ylabel='Frequency (Hz)')
        ax.figure.colorbar(image,ax=ax,label='Power spectral density (dB/Hz)',shrink=.8)
    else:
        raise ValueError(f'Unknown or nested panel type: {kind}')


def demo(kind):
    rng=np.random.default_rng(20261013)
    values=rng.normal(0,1,100)
    groups=[dict(label=label,values=rng.normal(i*.6,1,60).tolist()) for i,label in enumerate(['A','B','C'])]
    x=np.linspace(0,10,30)
    y=.7*x+rng.normal(0,.6,len(x))
    low,high=(.7*x-.6).tolist(),(.7*x+.6).tolist()
    truth=rng.integers(0,2,200)
    probability=np.clip(.2+.6*truth+rng.normal(0,.18,len(truth)),.001,.999)
    grid=np.linspace(-2,2,30)
    xx,yy=np.meshgrid(grid,grid)
    cases={
      'histogram':dict(values=values.tolist(),bins=15),
      'box':dict(groups=groups),'violin':dict(groups=groups),'ecdf':dict(groups=groups),
      'errorbar':dict(x=x[::4].tolist(),y=(.7*x[::4]).tolist(),lower=low[::4],upper=high[::4],interval_label='Synthetic interval (not an estimated CI)'),
      'confidence-band':dict(x=x.tolist(),y=(.7*x).tolist(),lower=low,upper=high,interval_label='Synthetic interval (not an estimated CI)'),
      'regression':dict(x=x.tolist(),y=y.tolist()),
      'residual':dict(fitted=(.7*x).tolist(),residuals=(y-.7*x).tolist()),
      'qq':dict(values=values.tolist()),
      'bland-altman':dict(a=(10+values).tolist(),b=(10+values+rng.normal(.15,.3,len(values))).tolist()),
      'forest':dict(labels=['Study A','Study B','Study C'],effect=[.2,.5,.35],lower=[-.1,.2,.12],upper=[.5,.8,.58],interval_label='Synthetic interval (not an estimated CI)'),
      'roc':dict(y_true=truth.tolist(),score=probability.tolist()),
      'precision-recall':dict(y_true=truth.tolist(),score=probability.tolist()),
      'calibration':dict(y_true=truth.tolist(),probability=probability.tolist(),bins=8),
      'confusion':dict(labels=['Negative','Positive'],matrix=[[82,18],[11,89]]),
      'correlation':dict(labels=['A','B','C'],matrix=np.column_stack([values,.6*values+rng.normal(0,.5,len(values)),rng.normal(0,1,len(values))]).tolist()),
      'contour':dict(x=grid.tolist(),y=grid.tolist(),z=np.exp(-xx**2-yy**2).tolist()),
      'surface':dict(x=grid.tolist(),y=grid.tolist(),z=np.exp(-xx**2-yy**2).tolist()),
      'spectrogram':dict(signal=(np.sin(2*np.pi*15*np.arange(1000)/200)+.5*np.sin(2*np.pi*40*np.arange(1000)/200)+rng.normal(0,.15,1000)).tolist(),sample_rate=200,nfft=128),
    }
    cases['multi-panel']=dict(columns=2,panels=[dict(type=t,data=cases[t],title=title) for t,title in [('histogram','Distribution'),('regression','Relationship'),('roc','Discrimination'),('calibration','Calibration')]])
    return dict(type=kind,title=kind.replace('-',' ').title(),data=cases[kind],synthetic=True,
                provenance={'source':'Explicit synthetic demonstration; RNG seed 20261013','note':'Do not use as experimental results'})


def render(spec,out,gray=True,width_mm=89,dpi=600):
    kind=spec['type']
    if kind not in TYPES:
        raise ValueError(f'Unsupported type {kind}')
    if not np.isfinite(width_mm) or width_mm<=0 or dpi<1:
        raise ValueError('width_mm and dpi must be positive')
    if not spec.get('synthetic') and not spec.get('provenance',{}).get('source'):
        raise ValueError('Real-data figures require provenance.source')
    colors=style(gray)
    data=spec['data']
    width=width_mm/25.4
    if kind=='multi-panel':
        panels=data['panels']
        cols=data.get('columns',2)
        if not panels or not isinstance(cols,int) or not 1<=cols<=len(panels):
            raise ValueError('Require nonempty panels and 1 <= columns <= panel count')
        rows=(len(panels)+cols-1)//cols
        fig=plt.figure(figsize=(width,width*.72*rows/cols),layout='constrained')
        if spec.get('title'):
            fig.suptitle(spec['title'],fontsize=9)
        for i,p in enumerate(panels):
            ax=fig.add_subplot(rows,cols,i+1,projection='3d' if p['type']=='surface' else None)
            draw(ax,p['type'],p['data'],colors,gray)
            ax.set_title(f'({chr(97+i)}) '+p.get('title',p['type']),loc='left')
            for key in ('xlabel','ylabel'):
                if key in p: getattr(ax,'set_'+key)(p[key])
    else:
        fig=plt.figure(figsize=(width,width*.78),layout='constrained')
        ax=fig.add_subplot(111,projection='3d' if kind=='surface' else None)
        draw(ax,kind,data,colors,gray)
        ax.set_title(spec.get('title',''),loc='left')
        for key in ('xlabel','ylabel'):
            if key in spec: getattr(ax,'set_'+key)(spec[key])
    if spec.get('synthetic'):
        fig.supxlabel('SYNTHETIC DEMO — NOT EXPERIMENTAL RESULTS',fontsize=6,color='#555555')
    # Force a layout pass; report likely clipped text rather than hiding it.
    fig.canvas.draw()
    outside=[]
    from matplotlib.text import Text
    for text in fig.findobj(Text):
        if text.get_visible() and text.get_text() and text.get_clip_on() is False:
            box=text.get_window_extent(fig.canvas.get_renderer())
            if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width+1 or box.y1 > fig.bbox.height+1:
                outside.append(text.get_text())
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    files=[]
    for ext in ('svg','pdf','png'):
        target=out.with_suffix('.'+ext)
        fig.savefig(target,dpi=dpi,facecolor='white')
        files.append(target.name)
    canonical=json.dumps(spec,ensure_ascii=False,sort_keys=True,allow_nan=False).encode('utf-8')
    out.with_suffix('.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    report=dict(type=kind,synthetic=bool(spec.get('synthetic')),provenance=spec.get('provenance'),
                spec_sha256=hashlib.sha256(canonical).hexdigest(),data_sha256=hashlib.sha256(json.dumps(data,sort_keys=True,allow_nan=False).encode()).hexdigest(),
                width_mm=width_mm,dpi=dpi,grayscale=gray,fonts=plt.rcParams['font.family'],
                python=platform.python_version(),matplotlib=matplotlib.__version__,numpy=np.__version__,
                files=files,text_outside_canvas=outside,visual_review='pending',
                method={'roc':'trapezoidal ROC AUC; ties grouped','precision-recall':'AP = sum(delta recall * precision at threshold)',
                        'bland-altman':'A-B; sample SD ddof=1; LoA=bias +/- 1.96 SD; assumption-dependent',
                        'correlation':'Pearson correlation; complete finite rows only','qq':'Normal quantiles (i+0.5)/n; quartile reference',
                        'spectrogram':'Matplotlib specgram; default Hann window, PSD scaling',
                        'calibration':'Equal-width probability bins; empty bins omitted','regression':'Unweighted OLS line; no inferred uncertainty'}.get(kind,'Declared data; see scientific-recipes.md'))
    out.with_suffix('.manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    plt.close(fig)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec',type=Path,help='UTF-8 JSON with type, data and provenance.source')
    parser.add_argument('--demo',choices=TYPES+['all'],help='Explicitly generate labeled synthetic examples')
    parser.add_argument('--list',action='store_true')
    parser.add_argument('--out',type=Path,default=Path('figure-output'))
    parser.add_argument('--width-mm',type=float,help='Defaults: 89 mm single / 180 mm multi-panel')
    parser.add_argument('--dpi',type=int,default=600)
    parser.add_argument('--color',action='store_true',help='Use Okabe-Ito categorical colors; default is grayscale')
    args=parser.parse_args()
    if args.list:
        catalog=SKILL/'assets/catalog.json'
        if catalog.exists():
            for row in json.loads(catalog.read_text(encoding='utf-8')):
                print(f"{row['id']:22} {row['route']:12} {row['name']}")
        else: print('\n'.join(TYPES))
        return
    if bool(args.spec)==bool(args.demo):
        parser.error('Choose exactly one of --spec or --demo')
    kinds=TYPES if args.demo=='all' else [args.demo]
    specs=[json.loads(args.spec.read_text(encoding='utf-8-sig'))] if args.spec else [demo(k) for k in kinds]
    for spec in specs:
        width=args.width_mm if args.width_mm is not None else (180 if spec['type']=='multi-panel' else 89)
        report=render(spec,args.out/spec['type'],not args.color,width,args.dpi)
        print(f"{report['type']}: SVG/PDF/PNG saved; clipping candidates={len(report['text_outside_canvas'])}; visual review pending")


if __name__=='__main__':
    main()
