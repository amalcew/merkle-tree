from merkle_tree import MerkleTree


def check_consistency(prev_tree, next_tree):
    """ Check consistency of given next_tree in comparison to prev_tree """

    prev_tree_leaves_lst = [node.name for node in prev_tree.nodes_list[::-1] if node.left_child is None and node.right_child is None]
    next_tree_leaves_lst = [node.name for node in next_tree.nodes_list[::-1] if node.left_child is None and node.right_child is None]
    flag = True
    n = len(prev_tree_leaves_lst)

    tmp_next_tree = MerkleTree(next_tree_leaves_lst[:n])
    tmp_prev_tree = MerkleTree(prev_tree_leaves_lst + next_tree_leaves_lst[n:])

    # test if next_tree fully contain prev_tree
    if prev_tree.get_root_hash() != tmp_next_tree.get_root_hash():
        flag = False

    # test if adding additional nodes to prev_tree returns next_tree
    if next_tree.get_root_hash() != tmp_prev_tree.get_root_hash():
        flag = False

    return flag