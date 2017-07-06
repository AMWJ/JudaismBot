# This is an unconventional trie, in that its nodes are per-word. There's a hash table at each node to hold those lower nodes.
class Trie():
    def __init__(self, parent=None, phrase=None, **kwargs):
        self.hash = {}
        self.phrase = phrase
        self.parent = parent
        return super().__init__(**kwargs)
    def setPhrase(self, phrase):
        self.phrase = phrase
    def add(self, after, phrase=None):
        if not phrase:
            phrase = after
        partition = after.split(' ',1)
        if len(partition)>1:
            if partition[0] in self.hash:
                trie = self.hash[partition[0]]
            else:
                trie = Trie(self)
                self.hash[partition[0]] = trie
            trie.add(partition[1],phrase)
        else:
            if partition[0] in self.hash:
                self.hash[partition[0]].setPhrase(phrase)
            else:
                trie = Trie(self, phrase)
                self.hash[partition[0]] = trie