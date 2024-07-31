from .radix import RadixTree
from textwrap import dedent

def test_radix_tree():
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("world")
    tree.insert("hello world")
    
    assert "hello" in tree
    assert "world" in tree
    assert "dragon" not in tree

    assert len(tree) == 3
    assert len(list(tree)) == 3

def test_internals():
    # Test that it splits the string correctly
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("world")
    tree.insert("helloworld")
    tree.insert("hellokitty")
    
    root = tree._store
    assert len(root.children) == 2
    assert len(root.children["hello"].children) == 2

def test_splits_entry():
    # It should split a string if a smaller string comes along
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("h")

    root = tree._store
    assert len(root.children) == 1

def dump_tree(tree: RadixTree) -> str:
    out = []
    def _dump(node, indent=0):
        for key, child in node.children.items():
            out.append(" " * indent + "'" + key + "'")
            _dump(child, indent + 2)
    _dump(tree._store)
    return "\n".join(out)


def test_splits_entry_2():
    # It should also split the entry if the second string
    # just has a common prefix
    tree = RadixTree()
    tree.insert("AB1")
    tree.insert("AB")

    assert (dump_tree(tree) == dedent("""\
        'AB'
          '1'"""))

    root = tree._store
    assert len(root.children) == 1
    assert len(root.children["AB"].children) == 1

def test_splits_entry_3():
    # It should also split the entry if the second string
    # just has a common prefix
    tree = RadixTree()
    tree.insert("AB")
    tree.insert("AB1")

    assert (dump_tree(tree) == dedent("""\
        'AB'
          '1'"""))

    root = tree._store
    assert len(root.children) == 1
    assert len(root.children["AB"].children) == 1

def test_find_prefix_lt_one():
    # It should find a prefix that is larger than one character
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("hallo")
    tree.insert("hasso")

    assert (dump_tree(tree) == dedent("""\
        'h'
          'ello'
          'a'
            'llo'
            'sso'"""))

# TODO:
# we need a way to tell non-leaf nodes from leaf nodes
# tree.insert("hello")
# tree.insert("hello world")
# tree.insert("hello kitty")
# In this case we have "hello" + " " as a node which is not what we stored

def test_respects_leafs():
    # It should respect leaf nodes
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("hello world")
    tree.insert("hello kitty")

    assert (dump_tree(tree) == dedent("""\
        'hello'
          ' '
            'world'
            'kitty'"""))
    
    lst = sorted(list(tree))
    assert lst == ["hello", "hello kitty", "hello world"]

def test_counts_correctly():
    # It should count the number of entries correctly
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("hello world")
    tree.insert("hello kitty")

    assert len(list(tree)) == 3

def test_no_duplicates():
    tree = RadixTree()
    tree.insert("hello")
    tree.insert("hello")
    assert len(tree) == 1

def test_promote_to_leaf():
    tree = RadixTree()
    tree.insert("A")
    tree.insert("ABC")
    tree.insert("ABD")

    assert (dump_tree(tree) == dedent("""\
        'A'
          'B'
            'C'
            'D'"""))
    
    assert len(tree) == 3
    tree.insert("AB")
    assert len(tree) == 4


# promote to leaf on split?


def test_promote_to_leaf_reverse():
    tree = RadixTree()
    tree.insert("AB")
    tree.insert("A")

    assert len(tree) == 2