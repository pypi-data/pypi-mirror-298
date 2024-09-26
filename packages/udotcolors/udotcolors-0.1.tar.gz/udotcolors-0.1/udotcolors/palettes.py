from .colors import get_color, get_color_list
import seaborn as sns
import ColorKit as ck
import pprint


def palette(palette="main", reverse=False):
    color_list = _palette_gen(palette, list_palette=False)
    if reverse:
        color_list.reverse()

    p = sns.set_palette(sns.color_palette(color_list))
    return p


def list_palettes(palette="all"):
    p = _palette_gen(palette=palette, list_palette=True)
    return p


def palette_seq(color="dark_blue", start=None, reverse=False):
    p = _palette_gen_seq(color, start, reverse)
    return p


def palette_div(neg="red", pos="dark_blue", center="light", s=75, l=50, sep=1):
    p = _palette_gen_div(
        neg=get_color(neg), pos=get_color(pos), center=center, s=s, l=l, sep=sep
    )
    return p


def _palette_gen(palette="main", list_palette=False):
    palettes = {
        "main": get_color_list(
            "light_blue",
            "orange",
            "dark_blue",
            "gray",
            "medium_blue",
            "light_green",
            "dark_gray",
            "turquoise",
            "tacao",
            "brown",
        ),
        "alt": get_color_list(),
        "grayscale": get_color_list(),
        "highlight": get_color_list(),
    }

    if list_palette:
        if palette == "all":
            pprint.pprint(palettes)
            return None
        pprint.pprint(palettes[palette])
        return None

    return palettes[palette]


def _palette_gen_seq(color, start, reverse):
    if start is None:
        l = ck.rgb_to_hsl(ck.hex_to_rgb(get_color(color)))
        if l < 50:
            start = "light"
        else:
            start = "dark"

    if start == "light":
        p = sns.light_palette(get_color(color), reverse=reverse, as_cmap=True)
    if start == "dark":
        p = sns.dark_palette(get_color(color), reverse=reverse, as_cmap=True)

    return p


def _palette_gen_div(neg, pos, center, s, l, sep):
    p = sns.diverging_palette(
        h_neg=neg, h_pos=pos, s=s, l=l, sep=sep, center=center, as_cmap=True
    )
    return p
