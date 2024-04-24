from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):

    def test_html_props(self):
        node1 = HTMLNode(
            "p", "goodbye", None, {"class": "hello", "href": "https://www.google.com"}
        )
        self.assertEqual(
            node1.props_to_html(), ' class="hello" href="https://www.google.com"'
        )

    def test_empty_props(self):
        node1 = HTMLNode("p", "goodbye", None, {})
        self.assertEqual(node1.props_to_html(), "")


class TestLeafNode(unittest.TestCase):

    def test_leafnode(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node1.to_html(), node2)

    def test_leafnode_props(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node1.to_html(), node2)

    def test_leafnode_without_tag(self):
        node1 = LeafNode(None, "Just some text")
        node2 = "Just some text"
        self.assertEqual(node1.to_html(), node2)


class TestParentNode(unittest.TestCase):

    def test_parent_with_children(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node1.to_html(), node2)

    def test_parent_with_one_child(self):
        test_child = LeafNode(None, "Hello listy")
        node1 = ParentNode("b", [test_child])
        self.assertEqual(node1.to_html(), "<b>Hello listy</b>")

    def test_parent_without_children(self):
        node1 = ParentNode(tag="div", children=[])
        self.assertRaises(ValueError, node1.to_html)

    def test_nested_parent(self):
        inner_child = LeafNode(tag="span", value="Hello mister")
        inner_parent = ParentNode(tag="p", children=[inner_child])
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        self.assertEqual(
            outer_parent.to_html(), "<div><p><span>Hello mister</span></p></div>"
        )


if __name__ == "__main()__":
    unittest.main()
