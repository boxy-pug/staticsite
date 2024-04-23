def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    strip_blocks = []
    for block in split_blocks:
        if block == "":
            continue
        strip_blocks.append(block.strip())
    return strip_blocks