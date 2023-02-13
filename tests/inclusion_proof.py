from merkle_tree import MerkleTree, get_hash


def check_inclusion(tree, elem):
    """ Check if tree contains passed element as one of the leaves """

    def _dfs(struct, hash, dct=dict()):
        if struct.left_child is not None:
            if get_hash(struct.left_child.value) == hash:
                dct[struct.left_child.name] = get_hash(struct.left_child.value)
            else:
                _dfs(struct.left_child, unverified_hash, dct)
        if struct.right_child is not None:
            if get_hash(struct.right_child.value) == hash:
                dct[struct.right_child.name] = get_hash(struct.right_child.value)
            else:
                _dfs(struct.right_child, unverified_hash, dct)

    unverified_hash = get_hash(elem)
    result = dict()
    _dfs(tree.structure, unverified_hash, result)
    if (elem, unverified_hash) in result.items():
        return True
    else:
        return False