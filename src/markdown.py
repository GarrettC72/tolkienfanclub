from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        split_texts = old_node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise Exception("Invalid Markdown syntax: matching closing delimiter not found")
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_texts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\])]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\])]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        image_matches = extract_markdown_images(current_text)
        if len(image_matches) == 0:
            new_nodes.append(old_node)
            continue
        for image_match in image_matches:
            split_texts = current_text.split(f'![{image_match[0]}]({image_match[1]})', 1)
            if len(split_texts) != 2:
                raise Exception("Invalid Markdown syntax: image delimiter not found")
            if split_texts[0] != "":
                new_nodes.append(TextNode(split_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_match[0], TextType.IMAGE, image_match[1]))
            current_text = split_texts[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        link_matches = extract_markdown_links(current_text)
        if len(link_matches) == 0:
            new_nodes.append(old_node)
            continue
        for link_match in link_matches:
            split_texts = current_text.split(f'[{link_match[0]}]({link_match[1]})', 1)
            if len(split_texts) != 2:
                raise Exception("Invalid Markdown syntax: link delimiter not found")
            if split_texts[0] != "":
                new_nodes.append(TextNode(split_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_match[0], TextType.LINK, link_match[1]))
            current_text = split_texts[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes