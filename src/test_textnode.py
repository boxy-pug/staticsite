import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("Testy hello", "italic")
        node2 = TextNode("Testy hello", "italic")
        self.assertEqual(node, node2)

    def test_different_text(self):
        node1 = TextNode("Testy hello", "bold")
        node2 = TextNode("Testy goodbye", "bold")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("Testy hello", "bold")
        node2 = TextNode("Testy hello", "italic")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("Testy hello", "italic", "https://www.hello.com")
        node2 = TextNode("Testy hello", "italic", "https://www.goodbye.com")
        self.assertNotEqual(node1, node2)

    def test_text_to_html(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")


if __name__ == "__main__":
    unittest.main()
