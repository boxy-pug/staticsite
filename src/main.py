from textnode import TextNode
from inline_markdown import *
from copy_dir import copy_directory
from block_markdown import *
import os
import shutil


FROM_PATH = "content/index.md"
TEMPLATE_PATH = "./template.html"
DESTINATION_PATH = "public/index.html"


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(FROM_PATH, "r") as f:
        markdown_content = f.read()

    with open(TEMPLATE_PATH, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(full_html)

def clear_directory(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir, exist_ok=True)


def main():

    source_dir, destination_dir = "static", "public"

    clear_directory(destination_dir)
    print("Destination directory has been cleared.")

    copy_directory(source_dir, destination_dir)
    print("Files and directories have been copied.")

    generate_page(FROM_PATH, TEMPLATE_PATH, DESTINATION_PATH)

if __name__ == "__main__":
    main()
