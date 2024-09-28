from docutils import nodes


def get_separator_from_line(text: str, node: nodes.Node) -> str:
    line_num = node.line - 1
    line = text.splitlines()[line_num]
    separator = line.strip()[0]
    return separator

def get_marker_list_from_line(text: str, node: nodes.Node) -> str:
    line_num = node.line - 1
    line = text.splitlines()[line_num]
    separator = line.strip().split(' ', 1)[0]
    return separator

def post_parse_doctree(text: str, doctree: nodes.document) -> nodes.document:
    for node in doctree.traverse():
        if isinstance(node, nodes.title):
            node['separator'] = get_separator_from_line(text, node)

        elif isinstance(node, nodes.list_item):
            node['separator'] = get_marker_list_from_line(text, node)

        elif isinstance(node, nodes.table):
            if node.source != "<string>":
                colspecs = [col.attributes.get('colwidth', '') for col in node.traverse(nodes.colspec)]
                thead = node.next_node(nodes.thead)
                header_rows = len(thead) if thead else 0
                directive_text = ".. list-table::\n"
                directive_text += f"   :header-rows: {header_rows}\n"
                directive_text += f"   :widths: {' '.join(map(str, colspecs))}\n"
                node['list-table'] = directive_text

    return doctree

