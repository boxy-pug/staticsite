import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

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
    return LeafNode(tag=header_type, value=heading_line)


def quote_block_to_html(block):
    block_lines = block.split("\n")
    stripped_block_lines = [line.lstrip(">").lstrip() for line in block_lines]
    stripped_block_string = "\n".join(stripped_block_lines)
    return LeafNode(tag="blockquote", value=stripped_block_string)


def paragraph_block_to_html(block):
    block_lines = block.split("\n")
    paragraph_nodes = []
    for line in block_lines:
        text_nodes = text_to_textnodes(line)
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            paragraph_nodes.append(html_node)
    return ParentNode(tag="div", children=paragraph_nodes)


def code_block_to_html(block):
    stripped_block = block[3:-3]
    return ParentNode(
        tag="pre", children=[LeafNode(tag="code", value=stripped_block)]
    )


def ul_block_to_html(block):
    block_lines = block.split("\n")
    li_nodes = []
    for line in block_lines:
        stripped_line = line.lstrip().lstrip("*").lstrip("-").strip()
        if stripped_line:
            text_nodes = text_to_textnodes(stripped_line)
            inline_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            li_nodes.append(ParentNode(tag="li", children=inline_nodes))
    return ParentNode(tag="ul", children=li_nodes)


def ol_block_to_html(block):
    block_lines = block.split("\n")
    li_nodes = []
    for line in block_lines:
        stripped_line = line.split(". ", 1)[1].strip() if ". " in line else line.strip()
        if stripped_line:
            text_nodes = text_to_textnodes(stripped_line)
            inline_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            li_nodes.append(ParentNode(tag="li", children=inline_nodes))
    return ParentNode(tag="ol", children=li_nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_heading:
        return heading_block_to_html(block)
    elif block_type == block_type_paragraph:
        return paragraph_block_to_html(block)
    elif block_type == block_type_code:
        return code_block_to_html(block)
    elif block_type == block_type_unordered_list:
        return ul_block_to_html(block)
    elif block_type == block_type_ordered_list:
        return ol_block_to_html(block)
    elif block_type == block_type_quote:
        return quote_block_to_html(block)
    else:
        raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    """This one should make use of a lot of the previous functionality 
    to convert a full markdown document into an HTMLNode. 
    That top-level HTMLNode should just be a <div>, where each child is a block of the document. 
    Each block should have its own "inline" children."""
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block) 
        children_nodes.append(html_node)
    return ParentNode("div", children_nodes)

