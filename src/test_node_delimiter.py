import unittest
from node_delimiter import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
 split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks,block_to_block_type,markdown_to_html_node)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )



class TestExtractwithRegex(unittest.TestCase):
    def test_image_regex(self):
        text = "Here is an image ![alt text](http://example.com/image.jpg)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "http://example.com/image.jpg")])

    def test_two_images(self):
        text = "First ![image1](https://example.com/img1.jpg) Second ![image2](http://example.com/img2.jpg)"
        self.assertEqual(extract_markdown_images(text), [("image1","https://example.com/img1.jpg"), ("image2","http://example.com/img2.jpg")])

    def test_link_regex(self):
        text = "Visit our [website](http://example.com)"
        self.assertEqual(extract_markdown_links(text), [("website","http://example.com")])

    def test_no_markdown_img(self):
        text = "This text has no images or links"
        self.assertEqual(extract_markdown_images(text),[])

    def test_no_markdown_link(self):
        text = "This text has no images or links"
        self.assertEqual(extract_markdown_links(text),[])

    
class TestDelimiterLinkandImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),],new_nodes,)

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),], new_nodes,)

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplitBlocks(unittest.TestCase):
    def test_basic_block(self):
        markdown = """First block
        
        Second block
        more text
        
        Third block"""
        self.assertEqual(markdown_to_blocks(markdown), ["First block","Second block\nmore text","Third block"])


    def test_extra_space_block(self):
        markdown = """    First block

        Second block  
        more text           

        Third block   """
        self.assertEqual(markdown_to_blocks(markdown), ["First block","Second block\nmore text", "Third block"])

    def test_multiple_space_block(self):
        markdown = """First block


Second block



Third block"""
        self.assertEqual(markdown_to_blocks(markdown), ["First block","Second block","Third block"])





class TestBlockTypes(unittest.TestCase):
    def test_only_paragraph(self):
        block = "This is just a paragraph"
        self.assertEqual(block_to_block_type(block),"paragraph")

    def test_ordered_list(self):
        block = "1. First element\n2. Second element\n3. Third element"
        self.assertEqual(block_to_block_type(block),"ordered_list")

    def test_unordered_list(self):
        block = "* First element\n* Second element\n* Third element"
        self.assertEqual(block_to_block_type(block),"unordered_list")
    
    def test_code_block(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block),"code")

    def test_heading_bloc(self):
        block = "#### heanding"
        self.assertEqual(block_to_block_type(block),"heading")



class TestBlocktoHTML(unittest.TestCase):
    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",)

    def test_quotes(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",)

    def test_bloditalics_inparagraph(self):
         md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
         node = markdown_to_html_node(md)
         html = node.to_html()
         self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)


    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()

