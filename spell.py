#!/usr/bin/env python
import random
import sys
import optparse
from watchdog import Watchdog

with open("/usr/share/dict/words") as f:
    dictionary = {word.strip() for word in f}


def find_match(word):
    try:
        with Watchdog(5):
            matches = variations(word) & dictionary
    except Watchdog:
        return "WORD IS TOO COMPLEX" % (word)

    if not len(matches):
        return "NO SUGGESTION: %s" % (word)
    else:
        return list(matches)[0]


def variations(word):
    def gen_set(char):
        words = set()
        for postfix in variations(word[1:]):
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
            words |= variations(word[1:])

        if char.lower() in "aeiou":
            for v in "aeiou":
                words |= gen_set(v)
        else:
            words |= gen_set(char)

        return words


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
        elif char in "aieou" and random.random() < vowel_prob:
            char = random.choice(list("aieou"))

        mangled_word.append(char)

    return ''.join(mangled_word)


def spell_correct(quiet):
    prompt = '' if quiet else '>'

    while True:
        try:
            word = raw_input(prompt)
            print find_match(word)
            sys.stdout.flush()
        except (EOFError, KeyboardInterrupt):
            print ""
            break


def spell_mangle():
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
