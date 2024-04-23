import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    strip_blocks = []
    for block in split_blocks:
        strip_blocks.append(block.strip())
    return strip_blocks

def block_to_block_type(block):
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