from merkle_tree import MerkleTree


def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve', 'fred', 'george', 'hans', 'isabel', 'jeff', 'klaus', 'leon', 'mark',
           'noel']
    tree = MerkleTree(arr)
    print("Root hash: %s\n" % (tree.get_root_hash()))


if __name__ == '__main__':
    main()
