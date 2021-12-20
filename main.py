from merkle_tree import MerkleTree


def main():
    arr = ['alice', 'bob', 'carol', 'david', 'eve', 'fred', 'george', 'hans', 'isabel', 'jeff', 'klaus', 'leon', 'mark',
           'noel']
    partial_arr = arr[:5]
    tree = MerkleTree(partial_arr)
    print(tree.get_root_hash())

    # TODO: write appropriate inclusion and consistency check functions, comment the code and make tests

if __name__ == '__main__':
    main()
