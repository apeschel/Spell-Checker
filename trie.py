#!/usr/bin/env python
class Node:
    def __init__(self, char, word):
        self.char = char
        self.word = word
        self.children = {}
        self.is_word = False


    def sub_word(self):
        if self.is_word:
            return self.word
        else:
            return self.children.itervalues()[0].sub_word()


class Trie:
    def __init__(self):
        self.root = Node('', '')


    def __getitem__(self, word):
        def helper(word, cur_node):
            children = cur_node.children
            first_ch = word[0] if word else ''

            if not len(word) or first_ch not in children:
                return cur_node.sub_word()
            else:
                return helper(word[1:], children[first_ch])

        word = word.rstrip()
        return helper(word, self.root)


    def __contains__(self, word):
        word = word.rstrip()
        cur_node = self.root

        for char in word:
            children = cur_node.children
            if char not in children:
                return False
            cur_node = children[char]

        return cur_node.is_word


    def __str__(self):
        pass


    def add(self, word):
        word = word.rstrip()
        cur_node = self.root

        for char in word:
            children = cur_node.children

            if char not in children:
                new_word = cur_node.word + char
                children[char] = Node(char, new_word)

            cur_node = children[char]

        cur_node.is_word = True
