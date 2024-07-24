
from __future__ import annotations

class RadixNode:
    children: dict[str, RadixNode]
    # add metadata like count here
    is_leaf: bool

    def __init__(self, leaf=False):
        self.children = {}
        self.is_leaf = leaf

class RadixTree:
    def __init__(self):
        self._store = RadixNode()

    def dump(self):
        print("-----")
        def _dump(node, indent=0):
            for key, child in node.children.items():
                print(" " * indent, key.replace(" ", "_"))
                _dump(child, indent + len(key))
        _dump(self._store)

    def insert(self, item: str):
        debug = False
        if debug: print(f"Inserting '{item}'")
        node, remainder = self.locate_insertion_point(item)
        
        if not remainder:
            # The item is already in the tree
            if debug:
                print("Item already in tree")
            node.is_leaf = True
            return
        
        if debug:
            head = item[:-len(remainder)]
            print(f"Split as '{head}' and '{remainder}'")

        

        # We have the rough insertion point. We went as far down existing
        # nodes as possible.
        # See if we can find a node here that we can split
        # e.g. key is "hello" and we are trying to insert "hallo"
        maxprefixlen = len(remainder)
        commonprefix = None
        tosplit = None
    
        for prefixlen in range(1, maxprefixlen+1):
            if debug: print("checking prefix of length", prefixlen)
            for key in node.children:
                if remainder[:prefixlen] == key[:prefixlen]:
                    commonprefix = remainder[:prefixlen]
                    tosplit = key
                    if debug: print(f"Found prefix of '{commonprefix}' in '{tosplit}'")
                    break
            else:
                # No matches for this prefixlen,
                # so we can stop searching
                break

        if debug:
            if not commonprefix:
                print(f"No common prefix found for '{remainder}'")
            else:
                print(f"longest common prefix is '{commonprefix}' in '{tosplit}'")
            
        if commonprefix:
            # We have a node that we can split
            oldremainder = tosplit[len(commonprefix):]
            newremainder = remainder[len(commonprefix):]
            if debug:
                print(f"Splitting old item '{tosplit}' into '{commonprefix}' and '{oldremainder}'")
                print(f"Splitting new item '{remainder}' into '{commonprefix}' and '{newremainder}'")
                print("before:")
                print("Is the old node a leaf?", node.children[tosplit].is_leaf)
                self.dump()
            # commonprefix: h
            # tosplit: hello
            oldnode = node.children[tosplit]
            del node.children[tosplit]
            newnode = RadixNode(leaf=False)
            node.children[commonprefix] = newnode
            newnode.children[tosplit[len(commonprefix):]] = oldnode
            node = newnode
            if newremainder:
                node.children[newremainder] = RadixNode(leaf=True)
            else:
                node.is_leaf = True

            
            if debug:
                print("after:")
                self.dump()
        else:
            # No node to split, just insert a new node
            node.children[remainder] = RadixNode(leaf=True)

    def locate_insertion_point(self, item: str):
        remainder = item
        node = self._store
        while remainder:
            # find a prefix match
            for key, child in node.children.items():
                if remainder.startswith(key):
                    node = child
                    remainder = remainder[len(key):]
                    break
            else:
                return node, remainder
            
        return node, remainder
    
    def locate_insertion_point2(self, item: str):
        # return the one above the insertion point

        fullstr = ""
        history = []
        remainder = item
        parent = None
        parentremainder = None
        node = self._store
        while remainder:
            # find a prefix match
            for key, child in node.children.items():
                if remainder.startswith(key):
                    parent = node
                    parentremainder = remainder
                    node = child
                    remainder = remainder[len(key):]
                    fullstr += key
                    history.append(fullstr)
                    break
            else:
                return history
            
        return history
        
    def __contains__(self, item: str):
        print("Checking", item)
        node, remainder = self.locate_insertion_point(item)
        return not remainder
    
    def __len__(self):
        def _count(node):
            count = 0
            if node.is_leaf:
                count += 1
            for child in node.children.values():
                count += _count(child)
            return count
        return _count(self._store)
    
    def __iter__(self):
        def _iter(node, prefix=""):
            for key, child in node.children.items():
                if child.is_leaf:
                    yield prefix+key
                yield from _iter(child, prefix+key)
        return _iter(self._store)


def main():
    tree = RadixTree()
    # # tree.insert("ABC")
    # tree.insert("AB")
    # tree.insert("A")
#     tree.insert("hel")
#     tree.insert("he")
    # tree.insert("hello")
    # tree.insert("world")
    # tree.insert("hello world")
    # tree.insert("hello kitty")
    # tree.insert("hell yeah")
    # tree.insert("hallo")
    # tree.insert("hasso")
    # # tree.insert("hello")
    # # tree.insert("hallo")
    # # tree.insert("hasso")

    tree.insert('https://www.weltderphysik.de/gebiet/teilchen/experimente/teilchenbeschleuniger/')
    tree.insert('https://www.weltderphysik.de/gebiet/teilchen/experimente/teilchenbeschleuniger/cern-lhc/')
    tree.insert('https://www.weltderphysik.de/gebiet/teilchen/experimente/teilchenbeschleuniger/cern-lhc/lhc-experimente/atlas/')
    tree.insert('https://www.weltderphysik.de/gebiet/teilchen/experimente/teilchenbeschleuniger/cern-lhc/lhc-experimente/cms/')
    tree.insert('https://www.weltderphysik.de/gebiet/teilchen/experimente/')


    tree.dump()
    for item in tree:
        print(item)

if __name__ == "__main__":
    main()