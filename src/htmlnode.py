class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_list = ""
        for key, value in self.props.items():
            props_list += f' {key}="{value}"'
        return props_list
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"