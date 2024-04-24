import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """It takes a list of "old nodes", a delimiter, and a text type.
    It should return a new list of nodes,
    where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, missing delimiter in text node")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], text_type_text))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(string):
    """return markdown image tuple (tag and url)"""
    return re.findall(r"!\[(.*?)\]\((.*?)\)", string)


def extract_markdown_links(string):
    """return markdown link tuple (tag and url)"""
    return re.findall(r"\[(.*?)\]\((.*?)\)", string)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            delimiter = f"![{image[0]}]({image[1]})"
            parts = original_text.split(delimiter)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, forgot closing image tag")
            before_tag = parts[0]
            if before_tag != "":
                new_nodes.append(TextNode(before_tag, text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        text_remaining = node.text
        for alt_text, link_url in links:
            before_link, text_remaining = text_remaining.split(
                f"[{alt_text}]({link_url})"
            )
            if before_link:
                new_nodes.append(TextNode(before_link, text_type_text))
            new_nodes.append(TextNode(alt_text, text_type_link, link_url))
        if text_remaining:
            new_nodes.append(TextNode(text_remaining, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    """Time to put all the "splitting" functions together into a function that can
    convert a raw string of markdown flavored text into a list of TextNode objects."""
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
