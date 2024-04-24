class HTMLNode:
    """The HTMLNode class will represent a "node" in an HTML document tree
    (like a <p> tag and its contents,
    or an <a> tag and its contents) and is purpose-built to render itself as HTML."""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """This method should return a string that represents the HTML attributes of the node."""
        if self.props == None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children."""

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        """This method should render a leaf node as an HTML string (by returning a string).
        If the leaf node has no value, it should raise a ValueError. All leaf nodes require a value.
        """
        if not self.value:
            raise ValueError("Leaf nodes need a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """This is the one that will handle the nesting of HTML nodes inside of one another.
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node."""

    def __init__(self, tag, children):
        super().__init__(tag=tag, children=children)

    def to_html(self):
        """return a string representing the HTML tag of the node and its children"""
        if not self.tag:
            raise ValueError("Parentnode needs tag")
        if not self.children:
            raise ValueError("Parentnode needs children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{children_html}</{self.tag}>"
