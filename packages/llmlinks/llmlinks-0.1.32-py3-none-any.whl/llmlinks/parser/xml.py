import re


def parse(text):
    matcher_tag = r'(<([^>\s\n]+)([^>\n]*)?>)'
    cursor = 0
    tree = []
    text_split = re.split(matcher_tag, text)
    while cursor < len(text_split):
        if re.match(matcher_tag, text_split[cursor]) is None:
            tree.append(text_split[cursor])
            cursor += 1
            continue

        raw, tag, attributes = text_split[cursor:cursor+3]
        attributes = dict(re.findall(r'(\S*?)="(.*?)"', attributes))

        if '/' in tag:
            for j in range(len(tree)-1, -1, -1):
                if not isinstance(tree[j], dict):
                    continue
                if tree[j]['tag'] != tag[1:]:
                    continue
                tree[j]['content'] = tree[j+1:]
                tree = tree[:j+1]
                cursor += 3
                break
            continue

        element = {'tag': tag, 'attributes': attributes, 'content': None}
        tree.append(element)
        cursor += 3
    return tree


def _repr_tag(tag, content=None, **kwargs):
    if kwargs:
        attr = ' ' + ' '.join([f'{k}="{v}"' for k, v in kwargs.items()])
    else:
        attr = ''
    bra = f'<{tag}{attr}>'
    ket = f'</{tag}>'
    if content is None:
        return bra
    return ''.join([bra, content, ket])


def deparse(tree):
    if tree is None:
        return tree

    text = ''

    for element in tree:
        if isinstance(element, str):
            text += element
            continue
        element['content'] = deparse(element['content'])
        text += _repr_tag(element['tag'], element['content'],
                          **element['attributes'])
    return text


def findall(tree, tag):
    if tree is None:
        return []

    result = []
    for element in tree:
        if not isinstance(element, dict):
            continue
        if element['tag'] == tag:
            result.append(element)
        result += findall(element['content'], tag)
    return result


def normalize(tree, tags, outermost=True):
    if tree is None:
        return tree

    normalized = []
    for element in tree:
        if isinstance(element, str):
            if not outermost:
                normalized.append(element)
            continue
        if element['tag'] not in tags:
            continue
        element['content'] = normalize(element['content'], tags, False)
        normalized.append(element)
        if outermost:
            normalized.append('\n\n')
    return normalized
