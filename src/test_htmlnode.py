import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    def test_htmln(self):
        node = HTMLNode("p","This is a text",[],{})

        self.assertEqual(node.tag,"p")
        self.assertEqual(node.value,"This is a text")
        self.assertEqual(node.children,[])
        self.assertEqual(node.props,{})

    def test_htmln1(self):
        child_node = HTMLNode("p","This is a text",[],{})
        node = HTMLNode("div",None,[child_node],{})

        self.assertEqual(node.tag,"div")
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children),1)
        self.assertEqual(node.children[0].tag,"p")
        self.assertEqual(node.children[0].value,"This is a text")
        self.assertEqual(node.props,{})

    def test_htmln2(self):
        node = HTMLNode("a","Example Link",[],{"href": "https://www.example.com"})

        self.assertEqual(node.tag,"a")
        self.assertEqual(node.value,"Example Link")
        self.assertEqual(node.children,[])
        self.assertEqual(node.props,{"href": "https://www.example.com"})

    def test_htmln3(self):
        list_items = [
            HTMLNode("li","Item1",[],{}),
            HTMLNode("li","Item2",[],{}),
            HTMLNode("li","Item3",[],{}),
        ]

        node = HTMLNode("ul",None,list_items,{})
        
        self.assertEqual(node.tag,"ul")
        self.assertIsNone(node.value)

        self.assertEqual(len(node.children),3)
        self.assertEqual(node.children[0].tag,"li")
        self.assertEqual(node.children[0].value,"Item1")
        self.assertEqual(node.children[0].children,[])
        self.assertEqual(node.children[0].props,{})
        self.assertEqual(node.children[1].tag,"li")
        self.assertEqual(node.children[1].value,"Item2")
        self.assertEqual(node.children[1].children,[])
        self.assertEqual(node.children[1].props,{})
        self.assertEqual(node.children[2].tag,"li")
        self.assertEqual(node.children[2].value,"Item3")
        self.assertEqual(node.children[2].children,[])
        self.assertEqual(node.children[2].props,{})

        self.assertEqual(node.props,{})

# TEST for ParentNode

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )







if __name__ == "__main__":
    unittest.main()
 
