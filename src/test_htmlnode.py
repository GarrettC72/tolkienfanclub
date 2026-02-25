import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "This is a link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_no_props_to_html(self):
        node = HTMLNode(
            "a",
            "This is a link",
            None,
            None
        )
        self.assertEqual(
            node.props_to_html(),
            ''
        )

    def test_attributes(self):
        node = HTMLNode(
            "a",
            "This is a link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.tag,
            'a'
        )
        self.assertEqual(
            node.value,
            'This is a link'
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

    def test_html_repr(self):
        node = HTMLNode(
            "a",
            "This is a link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(a, This is a link, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!", {"class": "special"})
        self.assertEqual(node.to_html(), '<div class="special">Hello, world!</div>')

    def test_leaf_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.__repr__(),
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})"
        )

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

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        second_child_node = LeafNode("span", "second child")
        parent_node = ParentNode("div", [child_node, second_child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>second child</span></div>")

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("b", "great grandchild")
        grandchild_node = ParentNode("span", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><span><b>great grandchild</b></span></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        second_grandchild_node = LeafNode("b", "second grandchild")
        child_node = ParentNode("span", [grandchild_node])
        second_child_node = ParentNode("span", [second_grandchild_node])
        parent_node = ParentNode("div", [child_node, second_child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span><span><b>second grandchild</b></span></div>")



if __name__ == "__main__":
    unittest.main()