from textnode import TextNode
from inline_markdown import extract_markdown_images, text_to_textnodes


def main():

    print("Hello, testing")
    test_node = TextNode("Hello, texty testing", "bold", "https://www.google.com")
    print(test_node)

    node1 = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and thats it."
    print(extract_markdown_images(node1))

    print(
        text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
    )


if __name__ == "__main__":
    main()
