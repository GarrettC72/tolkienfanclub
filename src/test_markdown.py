import unittest

from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestMarkdown(unittest.TestCase):
    def test_delimiter_plain_text(self):
        node = TextNode("This is some plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is some plain text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_bold(self):
        node = TextNode("This is some **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_italic(self):
        node = TextNode("This is some _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_code(self):
        node = TextNode("This is some text with a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delimiter_multiple(self):
        node = TextNode("This is some text with a **bold** word, an _italic_ word, and a `code block` inside", TextType.TEXT)
        new_nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_italic = split_nodes_delimiter(new_nodes_bold, "_", TextType.ITALIC)
        new_nodes_final = split_nodes_delimiter(new_nodes_italic, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" inside", TextType.TEXT)
            ],
            new_nodes_final
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_and_links(self):
        image_matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)"
        )
        link_matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        self.assertListEqual([("link", "https://www.boot.dev")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_split_repeat_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_split_repeat_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_image_with_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_with_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_multiple(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev). Here is a second sentence with a [new link](https://www.youtube.com), an ![image](https://i.imgur.com/zjjcJKZ.png), `another code block`, _another_ italic and a **bold ending**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(". Here is a second sentence with a ", TextType.TEXT),
                TextNode("new link", TextType.LINK, "https://www.youtube.com"),
                TextNode(", an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", ", TextType.TEXT),
                TextNode("another code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
                TextNode(" italic and a ", TextType.TEXT),
                TextNode("bold ending", TextType.BOLD)
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()