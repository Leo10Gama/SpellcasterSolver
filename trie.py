"""Data involving the creation, generation, and querying of Tries."""


class TrieNode:
    """Representation of a Trie node.
    
    Attributes
    ----------
    char: str
        The character stored in the node.
    is_word: bool
        Whether or not this node marks the end of a word. Default is None.
    children: dict
        The set of all child nodes, where the keys of the dictionary is the character
        stored in the TrieNode value.
    """
    char: str
    is_word: bool
    children: dict

    def __init__(self, char, is_word = False):
        self.char = char
        self.is_word = is_word
        self.children = {}


class Trie:
    """Representation of a Trie object."""

    root: TrieNode

    def __init__(self, populate=False):
        self.root = TrieNode("")
        if populate:
            self.populate_trie()
    
    def add_word(self, word: str):
        """Add a word to the trie."""
        node = self.root
        for character in word:
            if character not in "abcdefghijklmnopqrstuvwxyz":
                raise Exception(f"Unexpected character '{character}' found in word '{word}'")
            if character in node.children:
                node = node.children[character]
            else:
                new_node = TrieNode(character)
                node.children.update({character: new_node})
                node = node.children[character]
        node.is_word = True

    def is_word(self, word: str) -> bool:
        """Given a word, check if it is in the Trie."""
        node = self.root
        for character in word:
            if character in node.children:
                node = node.children[character]
            else:
                return False
        return node.is_word
    
    def word_can_continue(self, word: str) -> bool:
        """Given a prefix, check if the word can be continued."""
        node = self.root
        for character in word:
            if character in node.children:
                node = node.children[character]
            else:
                return False
        return True if node.children else False
    
    def populate_trie(self):
        """Populate the trie with words from the English dictionary."""
        trie = Trie()
        print(f"Populating trie...", end="", flush=True)
        with open("dictionary.txt", "r") as f:
            for line in f.readlines():
                trie.add_word(line.strip())
        print(f" Done.")
        self.root = trie.root