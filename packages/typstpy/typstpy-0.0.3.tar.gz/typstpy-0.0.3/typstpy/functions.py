from typing import Optional, overload

from cytoolz.curried import assoc, valfilter  # type:ignore
from pymonad.reader import Pipe  # type:ignore

from .param_types import Block, Color, Content, Label, Length, Ratio, Relative
from .utils import ImplementType, RenderType, attach_func, implement_type, render


@implement_type(ImplementType.STANDARD)
def text(
    content: Block,
    *,
    font: Optional[str | tuple[str, ...]] = None,
    fallback: Optional[bool] = None,
    size: Optional[Length] = None,
    fill: Optional[Color] = None,
) -> Block:
    """Interface of `text` function in typst.

    Args:
        content (Block): Content in which all text is styled according to the other arguments.
        font (Optional[str  |  tuple[str, ...]], optional): A font family name or priority list of font family names. Defaults to None.
        fallback (Optional[bool], optional): Whether to allow last resort font fallback when the primary font list contains no match. This lets Typst search through all available fonts for the most similar one that has the necessary glyphs. Defaults to None.
        size (Optional[Length], optional): The size of the glyphs. Defaults to None.
        fill (Optional[Color], optional): The glyph fill paint. Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> text("Hello, World!", font="Arial", fallback=True)
        '#text(font: "Arial", fallback: true)[Hello, World!]'
        >>> text("Hello, World!", font=("Arial", "Times New Roman"), fallback=True)
        '#text(font: ("Arial", "Times New Roman"), fallback: true)[Hello, World!]'
        >>> text("Hello, World!", size=Length(12, "pt"))
        '#text(size: 12pt)[Hello, World!]'
        >>> text("Hello, World!", fill=color("red"))
        '#text(fill: rgb("#ff4136"))[Hello, World!]'
    """
    params = (
        Pipe({"font": font, "fallback": fallback, "size": size, "fill": fill})
        .map(valfilter(lambda x: x is not None))
        .flush()
    )
    if not params:
        return content
    return rf"#text({render(RenderType.DICT)(params)})[{content}]"


@implement_type(ImplementType.STANDARD)
def emph(content: Block) -> Block:
    """Interface of `emph` function in typst.

    Args:
        content (Block): The content to emphasize.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> emph("Hello, World!")
        '#emph[Hello, World!]'
    """
    return rf"#emph[{content}]"


@implement_type(ImplementType.STANDARD)
def strong(content: Block, *, delta: Optional[int] = None) -> Block:
    """Interface of `strong` function in typst.

    Args:
        content (Block): The content to strongly emphasize.
        delta (Optional[int], optional): The delta to apply on the font weight. Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> strong("Hello, World!")
        '#strong[Hello, World!]'
        >>> strong("Hello, World!", delta=300)
        '#strong(delta: 300)[Hello, World!]'
    """
    params = Pipe({"delta": delta}).map(valfilter(lambda x: x is not None)).flush()
    if not params:
        return rf"#strong[{content}]"
    return rf"#strong({render(RenderType.DICT)(params)})[{content}]"


@implement_type(ImplementType.STANDARD)
def par(
    content: Block,
    *,
    leading: Optional[Length] = None,
    justify: Optional[bool] = None,
    linebreaks: Optional[str] = None,
    first_line_indent: Optional[Length] = None,
    hanging_indent: Optional[Length] = None,
) -> Block:
    """Interface of `par` function in typst.

    Args:
        content (Block): The contents of the paragraph.
        leading (Optional[Length], optional): The spacing between lines. Defaults to None.
        justify (Optional[bool], optional): Whether to justify text in its line. Defaults to None.
        linebreaks (Optional[str], optional): How to determine line breaks. Options are "simple" and "optimized". Defaults to None.
        first_line_indent (Optional[Length], optional): The indent the first line of a paragraph should have. Defaults to None.
        hanging_indent (Optional[Length], optional): The indent all but the first line of a paragraph should have. Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> par("Hello, World!", leading=Length(1.5, "em"))
        '#par(leading: 1.5em)[Hello, World!]'
        >>> par("Hello, World!", justify=True)
        '#par(justify: true)[Hello, World!]'
        >>> par("Hello, World!")
        'Hello, World!'
    """
    if linebreaks and linebreaks not in ("simple", "optimized"):
        raise ValueError(f"Invalid value for linebreaks: {linebreaks}.")
    params = (
        Pipe(
            {
                "leading": leading,
                "justify": justify,
                "linebreaks": linebreaks,
                "first_line_indent": first_line_indent,
                "hanging_indent": hanging_indent,
            }
        )
        .map(valfilter(lambda x: x is not None))
        .flush()
    )
    if not params:
        return content
    return rf"#par({render(RenderType.DICT)(params)})[{content}]"


@implement_type(ImplementType.STANDARD)
def heading(
    content: Block,
    *,
    level: int = 1,
    supplement: Optional[Content] = None,
    numbering: Optional[str] = None,
    label: Optional[Label] = None,
) -> Block:
    """Interface of `heading` function in typst.

    Args:
        content (Block): The heading's title.
        level (int, optional): The absolute nesting depth of the heading, starting from one. Defaults to 1.
        supplement (Optional[Content], optional): A supplement for the heading. Defaults to None.
        numbering (Optional[str], optional): How to number the heading. Defaults to None.
        label (Optional[Label], optional): Cross-reference for the heading. Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> heading("Hello, World!", level=2, supplement=Content("Chapter"), label=Label("chap:chapter"))
        '#heading(supplement: [Chapter], level: 2)[Hello, World!] <chap:chapter>'
        >>> heading("Hello, World!", level=2)
        '== Hello, World!'
    """
    params = (
        Pipe({"supplement": supplement, "numbering": numbering})
        .map(valfilter(lambda x: x is not None))
        .flush()
    )
    if not params:
        result = rf"{"="*level} {content}"
    else:
        result = rf"#heading({render(RenderType.DICT)(assoc(params,'level',level))})[{content}]"
    if label:
        result += f" {label}"
    return result


@implement_type(ImplementType.STANDARD)
def image(
    path: str,
    *,
    format: Optional[str] = None,
    width: Optional[Relative] = None,
    height: Optional[Relative] = None,
    alt: Optional[str] = None,
    fit: Optional[str] = None,
) -> Block:
    """Interface of `image` function in typst.

    Args:
        path (str): Path to an image file.
        format (Optional[str], optional): The image's format. Detected automatically by default. Options are "png", "jpg", "gif", and "svg". Defaults to None.
        width (Optional[Relative], optional): The width of the image. Defaults to None.
        height (Optional[Relative], optional): The height of the image. Defaults to None.
        alt (Optional[str], optional): A text describing the image. Defaults to None.
        fit (Optional[str], optional): How the image should adjust itself to a given area (the area is defined by the width and height fields). Note that fit doesn't visually change anything if the area's aspect ratio is the same as the image's one. Options are "cover", "contain", and "stretch". Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> image("image.png")
        '#image("image.png")'
        >>> image("image.png", format="png")
        '#image("image.png", format: "png")'
    """
    if format and format not in ("png", "jpg", "gif", "svg"):
        raise ValueError(f"Invalid value for format: {format}.")
    if fit and fit not in ("cover", "contain", "stretch"):
        raise ValueError(f"Invalid value for fit: {fit}.")
    params = (
        Pipe(
            {"format": format, "width": width, "height": height, "alt": alt, "fit": fit}
        )
        .map(valfilter(lambda x: x is not None))
        .flush()
    )
    if not params:
        return rf"#image({render(RenderType.VALUE)(path)})"
    return (
        rf"#image({render(RenderType.VALUE)(path)}, {render(RenderType.DICT)(params)})"
    )


# region figure


@implement_type(ImplementType.STANDARD)
def _caption(content: Block, *, separator: Optional[Content] = None) -> Content:
    """Interface of `figure.caption` function in typst.

    Args:
        content (Block): The caption's body.
        separator (Optional[Content], optional): The separator which will appear between the number and body. Defaults to None.

    Returns:
        Content: The caption's content.
    """
    params = (
        Pipe({"separator": separator}).map(valfilter(lambda x: x is not None)).flush()
    )
    if not params:
        return Content(content)
    return Content(rf"#figure.caption({render(RenderType.DICT)(params)})[{content}]")


@attach_func(_caption, "caption")
@implement_type(ImplementType.STANDARD)
def figure(
    content: Block, *, caption: Optional[Content] = None, label: Optional[Label] = None
) -> Block:
    """Interface of `figure` function in typst.

    Args:
        content (Block): The content of the figure. Often, an image.
        caption (Optional[Content], optional): The figure's caption. Defaults to None.
        label (Optional[Label], optional): Cross-reference for the figure. Defaults to None.

    Returns:
        Block: Executable typst block.

    Examples:
        >>> figure(image("image.png"))
        '#figure(image("image.png"))'
        >>> figure(image("image.png"), caption=Content("This is a figure."))
        '#figure(image("image.png"), caption: [This is a figure.])'
        >>> figure(image("image.png"), caption=Content("This is a figure."), label=Label("fig:figure"))
        '#figure(image("image.png"), caption: [This is a figure.]) <fig:figure>'
        >>> figure(image("image.png"), caption=figure.caption("This is a figure.", separator=Content("---")))
        '#figure(image("image.png"), caption: figure.caption(separator: [---])[This is a figure.])'
    """
    params = Pipe({"caption": caption}).map(valfilter(lambda x: x is not None)).flush()
    if not params:
        result = rf"#figure({Content.examine_sharp(content)})"
    else:
        result = rf"#figure({Content.examine_sharp(content)}, {render(RenderType.DICT)(params)})"
    if label:
        result += f" {label}"
    return result


# endregion
# region color


@overload
def rgb(
    red: int | Ratio,
    green: int | Ratio,
    blue: int | Ratio,
    alpha: Optional[int | Ratio] = None,
) -> Color:
    """Interface of `rgb` function in typst.

    Args:
        red (int | Ratio): The red component.
        green (int | Ratio): The green component.
        blue (int | Ratio): The blue component.
        alpha (Optional[int | Ratio], optional): The alpha component. Defaults to None.

    Returns:
        Color: The color in RGB space.
    """


@overload
def rgb(hex: str) -> Color:
    """Interface of `rgb` function in typst.

    Args:
        hex (str): The color in hexadecimal notation. Accepts three, four, six or eight hexadecimal digits and optionally a leading hash.

    Returns:
        Color: The color in RGB space.
    """


@implement_type(ImplementType.STANDARD)
def rgb(*args):
    if len(args) not in (1, 3, 4):
        raise ValueError(f"Invalid number of arguments: {len(args)}.")
    return Color(rf"#rgb{render(RenderType.VALUE)(args)}")


@implement_type(ImplementType.STANDARD)
def luma(lightness: int | Ratio, alpha: Optional[Ratio] = None) -> Color:
    """Interface of `luma` function in typst.

    Args:
        lightness (int | Ratio): The lightness component.
        alpha (Optional[Ratio], optional): The alpha component. Defaults to None.

    Returns:
        Color: The color in luma space.
    """
    if alpha:
        return Color(rf"#luma{render(RenderType.VALUE)((lightness, alpha))}")
    return Color(rf"#luma({render(RenderType.VALUE)(lightness)})")


@attach_func(rgb)
@attach_func(luma)
@implement_type(ImplementType.NOTSTANDARD)
def color(name: str) -> Color:
    """Return the corresponding color based on the color name.

    Args:
        name (str): The color name.

    Raises:
        ValueError: Unsupported color name.

    Returns:
        Color: The color in RGB/luma space.
    """
    match name:
        case "black":
            return luma(0)
        case "gray":
            return luma(170)
        case "silver":
            return luma(221)
        case "white":
            return luma(255)
        case "navy":
            return rgb("#001f3f")
        case "blue":
            return rgb("#0074d9")
        case "aqua":
            return rgb("#7fdbff")
        case "teal":
            return rgb("#39cccc")
        case "eastern":
            return rgb("#239dad")
        case "purple":
            return rgb("#b10dc9")
        case "fuchsia":
            return rgb("#f012be")
        case "maroon":
            return rgb("#85144b")
        case "red":
            return rgb("#ff4136")
        case "orange":
            return rgb("#ff851b")
        case "yellow":
            return rgb("#ffdc00")
        case "olive":
            return rgb("#3d9970")
        case "green":
            return rgb("#2ecc40")
        case "lime":
            return rgb("#01ff70")
        case _:
            raise ValueError(f"Unsupported color name: {name}.")


# endregion
