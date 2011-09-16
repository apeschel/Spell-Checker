#!/usr/bin/env python
import random
import sys
import optparse
from trie import Trie
from watchdog import Watchdog

DICTIONARY_FILE="/usr/share/dict/american-english-small"
VOWELS="aeiouAEIOU"

def find_match(word):
    try:
        with Watchdog(5):
            matches = [pos_word for pos_word in var_iterative(word)
                         if pos_word in dictionary]
    except Watchdog:
        return "WORD IS TOO COMPLEX: %s" % (word)

    if not len(matches):
        return "NO SUGGESTION: %s" % (word)
    else:
        return matches[0]


# This function is not actually used.
def var_recursive(word):
    def gen_set(char):
        words = set()
        for postfix in var_recursive(word[1:]):
            for c in (char.lower(), char.upper()):
                words.add(c + postfix)
        return words


    if not len(word):
        return set([""])
    else:
        words = set()
        char      = word[0]
        next_char = word[1] if len(word) >= 2 else None

        if char == next_char:
            words |= var_recursive(word[1:])

        if char.lower() in VOWELS:
            for v in VOWELS:
                words |= gen_set(v)
        else:
            words |= gen_set(char)

        return words


def var_iterative(word):
    word_vars = {''}

    prev_char = ''
    for char in word:
        chars = {char, char.swapcase()}
        if char == prev_char:
            chars |= set([''])

        if char.lower() in VOWELS:
            chars |= set(VOWELS)

        word_vars = {prefix + c for prefix in word_vars for c in chars
                        if dictionary.has_prefix(prefix + c)}

        prev_char = char

    return word_vars


def mangle(word):
    case_prob = 0.6
    dup_prob = 0.1
    vowel_prob = 0.3
    max_dups = 3

    mangled_word = []
    for char in word:
        if random.random() < case_prob:
            char = char.swapcase()

        if random.random() < dup_prob:
            char = char * random.randint(2, max_dups)
        elif char in VOWELS and random.random() < vowel_prob:
            char = random.choice(list(VOWELS))

        mangled_word.append(char)

    return ''.join(mangled_word)


def create_dictionary():
    with open(DICTIONARY_FILE) as f:
        global dictionary
        dictionary = Trie()
        for word in f:
            dictionary.add(word.strip())


def spell_correct(quiet):
    prompt = '' if quiet else '>'
    create_dictionary()

    while True:
        try:
            word = raw_input(prompt)
            print find_match(word)
            sys.stdout.flush()
        except (EOFError, KeyboardInterrupt):
            print ""
            break


def spell_mangle():
    with open(DICTIONARY_FILE) as f:
        dictionary = {word.strip() for word in f}

    while True:
        try:
            word = random.sample(dictionary, 1)[0]
            print mangle(word)
            sys.stdout.flush()
        except KeyboardInterrupt:
            break


def parse_args():
    parser = optparse.OptionParser()

    parser.add_option("-m", "--mangle",
                      action="store_true",
                      default=False,
                      dest="mangle",
                      help="generate misspelt words",
                      )
    parser.add_option("-q", "--quiet",
                      action="store_true",
                      default=False,
                      dest="quiet",
                      help="do not print '>' character at start of each line",
                      )

    return parser.parse_args()


def main():
    options, args = parse_args()

    if options.mangle:
        spell_mangle()
    else:
        spell_correct(options.quiet)


if __name__ == "__main__":
    main()
