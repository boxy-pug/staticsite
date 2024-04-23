import unittest
from block_markdown import markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        string = "This is **bolded** paragraph\n\n\n\n"   "\n\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n\n\n\n\n\n"
        actual = markdown_to_blocks(string)
        expected = ["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items" ]
    
    def test_block_to_block_heading(self):
        actual = block_to_block_type("### Hello there\nOkay")
        expected = "heading"
        self.assertEqual(actual, expected)

    def test_block_to_block_code(self):
        actual = block_to_block_type("```Hello there\nOkay```")
        expected = "code"
        self.assertEqual(actual, expected)

    def test_block_to_block_quote(self):
        actual = block_to_block_type("> Hello there\n>Okay```Shalom")
        expected = "quote"
        self.assertEqual(actual, expected)

    def test_block_to_block_ul(self):
        actual = block_to_block_type("* Hello there\n* Okay```Shaaa")
        expected = "unordered_list"
        self.assertEqual(actual, expected)

    def test_block_to_block_ol(self):
        actual = block_to_block_type("1. Hello there\n2. Okay```test\n3. Threeee")
        expected = "ordered_list"
        self.assertEqual(actual, expected)

    def test_block_to_block_paragraph(self):
        actual = block_to_block_type("Hello there\n2. Okay```test\n#. Threeee")
        expected = "paragraph"
        self.assertEqual(actual, expected)