from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_title,
)
import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_delimiter(self):
        node = TextNode("This is text with a **bold** word.", text_type_text)
        actual = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word.", text_type_text),
        ]
        self.assertListEqual(actual, expected)

    def test_extract_markdown_images(self):
        node1 = extract_markdown_images(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and that's it."
        )
        node2 = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            )
        ]
        self.assertEqual(node1, node2)

    def test_extract_title(self):
        markdown = """
        This is some introductory text.

        # My Title

        Some more text here.
        """
        expected = "My Title"
        self.assertEqual(extract_title(markdown), expected)

    def test_no_title(self):
        markdown = """
        This is some introductory text.

        Some more text here.
        """
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 found")


    def test_split_nodes_image(self):
        node1 = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        actual = split_nodes_image([node1])

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(actual, expected)

    def test_split_nodes_link(self):
        node1 = TextNode(
            "Hello this is a [link](https://www.google.com)", text_type_text
        )
        actual = split_nodes_link([node1])
        expected = [
            TextNode("Hello this is a ", text_type_text),
            TextNode("link", text_type_link, "https://www.google.com"),
        ]

    def test_split_nodes_multiple(self):
        node1 = TextNode(
            "Hello heres one [link](www.example.com) and [another link](www.anotherlink.com) for you.",
            text_type_text,
        )
        actual = split_nodes_link([node1])
        expected = [
            TextNode("Hello heres one ", text_type_text),
            TextNode("link", text_type_link, "www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "www.anotherlink.com"),
            TextNode(" for you.", text_type_text),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes(self):
        node1 = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        actual = text_to_textnodes(node1)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(actual, expected)
