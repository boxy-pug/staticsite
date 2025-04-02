from textnode import TextNode
from inline_markdown import *
from copy_dir import copy_directory
from block_markdown import *
import os
import shutil
import sys


CONTENT_DIR = "content"
TEMPLATE_PATH = "./template.html"
DESTINATION_DIR = "docs"


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, dir_path_content)
                dest_dir = os.path.join(dest_dir_path, rel_path)
                dest_file_path = os.path.join(dest_dir, file.replace('.md', '.html'))

                os.makedirs(dest_dir, exist_ok=True)
                generate_page(file_path, template_path, dest_file_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(full_html)

def clear_directory(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir, exist_ok=True)


def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"Basepath set to {basepath}")


    source_dir, destination_dir = "static", DESTINATION_DIR

    clear_directory(destination_dir)
    print("Destination directory has been cleared.")

    copy_directory(source_dir, destination_dir)
    print("Files and directories have been copied.")

    # generate_page("content/majesty/index.md", TEMPLATE_PATH, "public/index.html")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, DESTINATION_DIR, basepath)

if __name__ == "__main__":
    main()
