import json
import re
import sys

file = open("test.xml", "r")
declaration = file.__next__()
xml_dec = re.match("<\?(\s)?xml(.)*\?>", declaration)
if xml_dec:
    pass
else:
    print("Error in xml declaration")
    sys.exit(0)
stack = list()
tree = dict()
count = dict()
root = None
text = dict()
line_no = 2
for line in file:
    if len(line) == 1:  # blank line
        pass
    else:   # non-blank line
        parse_text = line[:-1]
        parse_text = parse_text.strip()
        open_tag = re.search("<\s?\w+(\s+\w+\s*=\s*\"\w+\")?\s?>", line)
        if open_tag:
            parse_text = re.split("<\s?\w+(\s+\w+\s*=\s*\"\w+\")?\s?>", parse_text)
            parse_text = str(parse_text[-1])
            # print(parse_text)
            tag = re.findall("<\s*\w+", line)[0][1:]
            length = len(stack)
            if length > 0:  # non-root element
                if stack[-1] == tag:
                    print("ERROR : Invalid syntax")
                    sys.exit(0)
                i = 1
                subtree = tree[root]
                while i < length:
                    subtree = subtree[-1][stack[i]]
                    i += 1
                a = dict()
                a[tag] = list()
                subtree.append(a)

                # if tree.get(tag):
                #     count[tag] += 1
                # else:
                #     tree[tag] = list()
                #     count[tag] = 1
                # tree[stack[-1]].append(tag)
                # curr = tree.get(length)
                # if curr is None:
                #     a = list()
                #     a.append((stack[-1], tag))
                #     tree[length] = a
                # else:
                #     tree[length].append((stack[-1], tag))
                # try:
                #     t = tree[length]
                #     t.append(tag)
                #     # print("Hello")
                # except IndexError:
                #     a = list()
                #     a.append(tag)
                #     tree.append(a)
                stack.append(tag)
                # tree[stack[-1]].child.append(tag)
            else:  # root element
                root = tag
                a = list()
                count[root] = 1
                tree[root] = a
                stack.append(tag)
            # print("opening", tag)
        close_tag = re.search("</\s*\w+\s*>", line)
        if close_tag:

            tag = re.findall("</\s*\w+\s*>", line)[0]
            # print("tag is ", tag)
            # print("Parse text ", parse_text)
            if tag in parse_text:
                parse_text = re.sub(tag, '', parse_text)
                if parse_text == "":
                    pass
                else:
                    length = len(stack)
                    i = 1
                    subtree = tree[root]
                    while i < length:
                        subtree = subtree[-1][stack[i]]
                        i += 1
                    subtree.append(parse_text)
                    text[stack[-1]] = parse_text
                    # print(parse_text)
                # parse_text.replace(tag, '')

            tag = tag[2:-1]
            if stack[-1] != tag:
                print("ERROR : Expected tag for ", stack[-1])
                sys.exit(0)
            else:
                stack.remove(stack[-1])
        else:
            if parse_text != "":
                length = len(stack)
                i = 1
                subtree = tree[root]
                while i < length:
                    subtree = subtree[-1][stack[i]]
                    i += 1
                subtree.append(parse_text)
                # a = dict()
                # a[tag] = list()
                # subtree.append(a)
                # tree[root][-1][stack[-1]].append(parse_text)
                pass

            text[stack[-1]] = parse_text
        # print(tag_text)

    line_no += 1
if len(stack) > 0:
    print("ERROR : Invalid XML ")
    sys.exit(0)

if count[root] != 1:
    print("ERROR : Invalid XML ")
    sys.exit(0)

# print(stack)
# print(tree)
# print(count)
# print(text)
file.close()
tree = json.dumps(tree)
parsed = json.loads(tree)
print(json.dumps(parsed, indent=4, sort_keys=True))




