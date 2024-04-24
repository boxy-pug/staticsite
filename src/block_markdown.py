import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    """It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings."""
    split_blocks = markdown.split("\n\n")
    strip_blocks = []
    for block in split_blocks:
        strip_blocks.append(block.strip())
    return strip_blocks


def block_to_block_type(block):
    """function that takes a single block of markdown text as input and returns the type of block it is.
    You can assume it's had any leading or trailing whitespace stripped"""
    lines = block.split("\n")
    heading_pattern = r"^#{1,6}\s+.*$"
    if re.match(heading_pattern, lines[0]):
        return block_type_heading
    elif lines[0].startswith("```") and lines[-1].endswith("```"):
        return block_type_code
    elif all(line.startswith(">") for line in lines):
        return block_type_quote
    elif all(line.startswith(("* ", "- ")) for line in lines):
        return block_type_unordered_list
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def heading_block_to_html(block):
    heading_line = block.split("\n")[0]
    header_type = ""
    if heading_line.startswith("# "):
        header_type = "h1"
    elif heading_line.startswith("## "):
        header_type = "h2"
    elif heading_line.startswith("### "):
        header_type = "h3"
    elif heading_line.startswith("#### "):
        header_type = "h4"
    elif heading_line.startswith("##### "):
        header_type = "h5"
    elif heading_line.startswith("###### "):
        header_type = "h6"
    heading_line = heading_line.lstrip("#").lstrip()
    return HTMLNode(tag=header_type, value=heading_line)


def quote_block_to_html(block):
    block_lines = block.split("\n")
    stripped_block_lines = [line.lstrip(">").lstrip() for line in block_lines]
    stripped_block_string = "\n".join(stripped_block_lines)
    return HTMLNode(tag="blockquote", value=stripped_block_string)


def paragraph_block_to_html(block):
    block_lines = block.split("\n")
    html_block_lines = [f"<p>{line}</p>" for line in block_lines]
    html_block_string = "\n".join(html_block_lines)
    return HTMLNode(tag="p", value=html_block_string)


def code_block_to_html(block):
    stripped_block = block[3:-3]
    return ParentNode(
        tag="pre", children=[HTMLNode(tag="code", value=stripped_block)]
    )


def ul_block_to_html(block):
    block_lines = block.split("\n")
    li_block = [f"<li>{line}</li>" for line in block_lines]
    li_block_string = "\n".join(li_block)
    return ParentNode(tag="ul", children=[HTMLNode(tag="li", value="li_block_string")])


def ol_block_to_html(block):
    block_lines = block.split("\n")
    li_block = [f"<li>{line}</li>" for line in block_lines]
    li_block_string = "\n".join(li_block)
    return ParentNode(tag="ul", children=[HTMLNode(tag="li", value=li_block_string)])
