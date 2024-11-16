from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
import re

# Separamos el markdown en diferentes bloques de markdown
def markdown_to_blocks(markdown):
    new_block = []
    markdown = markdown.strip()
    blocks = re.split(r"\n\s*\n", markdown)
    for block in blocks:
        lines = block.split("\n")
        cleaned_lines = [line.strip() for line in lines]  #List comprehension
        cleaned_block = "\n".join(cleaned_lines)
        if cleaned_block:  #checa que el bloque no esté vacio
            new_block.append(cleaned_block)
    return new_block

#identificamos que tipo de bloque es el bloque markdown
def block_to_block_type(block):
    lines = block.split("\n")
    block_length = len(lines)
    quote_length = 0
    ordered_length = 0
    unordered_length = 0
    expected_number = 1
    for line in lines:
        if line.startswith("#") and (len(line)-len(line.lstrip("#"))) <= 6 and line.lstrip("#").startswith(" "):
            return "heading"
        if line.startswith(">") and line.lstrip(">").startswith(" "):
            quote_length += 1
        if (line.startswith("*") or line.startswith("-")) and line.lstrip("*-").startswith(" "):
            unordered_length += 1
        if line[0].isdigit():
            number = int(line[0])
            if number == expected_number and line[1:].startswith(". "):
                ordered_length += 1
                expected_number += 1
    if quote_length == block_length:
        return "quote"
    if unordered_length == block_length:
        return "unordered_list"
    if ordered_length == block_length:
        return "ordered_list"
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    else:
        return "paragraph"

    
#Genera el bloque completo de markdown a html node        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

#convierte cada bloque de markdown a un nodo html según su tipo
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

# convierte un texto en children de un nodo html
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

 # ------------------------------------------------------------------
 #        Logicas para convertir bloque de markdown a node html     

#lógica paragraph
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


#lógica heading
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

#lógica code
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

#lógica ordered_list
def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
    return ParentNode("ol",html_items)

#lógica unordered_list
def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
    return ParentNode("ul",html_items)

#lógica quotes
def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote",children)


# -------------------------------------------------------------------


# separa un texto en nodos markdown según el tipo de nodo
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"*",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1],))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


# Extract images and links from markdown with regex

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

