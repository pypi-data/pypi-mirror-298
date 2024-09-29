"""Show the most recent figure (for publication)"""
import matplotlib.pyplot as plt
import pathlib
from IPython.display import display, Markdown, Latex
import engcom.tufte

fignum = 0

def figure_markup(filename, caption, label, ext):
    return Markdown(f"![{caption}]({filename}){{#{label} .figure .{ext}}}")

def show(fig, filename=None, ext="pgf", caption="A caption.", label=None, figsize=(4, 4/1.618), lineage=False, pad_inches=0.0):
    global fignum
    plt.figure(fig)
    ax = plt.gca()
    fig.set_size_inches(*figsize)
    if filename is None:
        filename = f"figure-{fignum}.{ext}"
        fignum += 1
    elif not filename[-4] == ("."):
        filename = filename + f".{ext}"
    filename = pathlib.Path(filename)
    parent = filename.resolve().parent.name
    grandparent = filename.resolve().parent.parent.name
    # ax.xaxis.set_label_coords(1.02, 0) # the label can get cut off
    # ax.xaxis.label.set(ha='left',) # the label can get cut off
    # ax.yaxis.set_label_coords(0, 1.02)
    # ax.yaxis.label.set(rotation='horizontal', ha='center',)
    if ext == "pdf":
        plt.savefig(filename, bbox_inches='tight', pad_inches=pad_inches, dpi=600, backend="pgf")
    else:
        plt.savefig(filename, bbox_inches='tight', pad_inches=pad_inches, dpi=600)
    if ext == "pgf" or ext == "pdf":
        plt.savefig(filename.with_suffix(".svg"), bbox_inches='tight', pad_inches=pad_inches, dpi=600)
    if label is None:
        label = f"fig:{parent}-{filename.stem}"
    if lineage:
        return figure_markup(f"{grandparent}/{parent}/{filename}", caption, label, ext)
    else:
        return figure_markup(filename, caption, label, ext)