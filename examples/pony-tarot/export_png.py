"""Join the two figcraft browser captures, retain 600 dpi metadata, check text budgets."""
from pathlib import Path
from PIL import Image, ImageFont
import make_architecture as figure

root = Path(__file__).resolve().parent
top = Image.open(root / 'export-top.png').convert('RGB')
bottom = Image.open(root / 'export-bottom.png').convert('RGB')
assert top.size == bottom.size == (figure.W * 2, figure.H)
canvas = Image.new('RGB', (figure.W * 2, figure.H * 2), 'white')
canvas.paste(top, (0, 0))
canvas.paste(bottom, (0, top.height))
canvas.save(root / 'pony-tarot-architecture.png', dpi=(600, 600))

# Measure the actual installed Chinese font, rather than shrinking overflowing text.
for node, (_, _, width, _, kind) in figure.NODES.items():
    title, code, lines = figure.CONTENT[node]
    items = [(title, 21, True), (code, 14, False)] + [(line, 16 if kind == 'neutral' else 17, False) for line in lines]
    for value, size, bold in items:
        filename = 'msyhbd.ttc' if bold else 'msyh.ttc'
        font = ImageFont.truetype(f'C:/Windows/Fonts/{filename}', size)
        assert font.getlength(value) <= width - 56, (node, value, font.getlength(value))
print(f'PNG exported: {canvas.width}x{canvas.height}, 600 dpi; all node text fits the declared width budget.')
