"""
Fast wildcard pattern lookup against an English word list.

Pattern syntax: use '_' (or any char you choose) for unknown letters.
e.g. "q_ee_" matches any 5-letter word with 'q' at position 0,
'e' at position 2, 'e' at position 3, and any letter at 1 and 4.

Core idea: group words by length, then for each (position, letter)
build a bitmask (python int) marking which words in that length-group
have that letter there. A query just ANDs together the bitmasks for
its known letters -> O(#known letters) per query, independent of
dictionary size.
"""

import pickle
from collections import defaultdict


class PatternDict:
    def __init__(self, words, wildcard="_"):
        self.wildcard = wildcard

        # length -> list of words (index in this list = bit position)
        self.by_length = defaultdict(list)
        for w in words:
            w = w.strip().lower()
            if w.isalpha():
                self.by_length[len(w)].append(w)

        # length -> {(pos, letter): bitmask int}
        self.masks = {}
        # length -> "all words of this length" mask (for all-wildcard patterns)
        self.all_mask = {}

        for length, wlist in self.by_length.items():
            n = len(wlist)
            self.all_mask[length] = (1 << n) - 1
            pos_letter_masks = defaultdict(int)
            for i, w in enumerate(wlist):
                for p, ch in enumerate(w):
                    pos_letter_masks[(p, ch)] |= (1 << i)
            self.masks[length] = pos_letter_masks

    def exists(self, pattern: str) -> bool:
        """True/False: does any word match this pattern?"""
        length = len(pattern)
        if length not in self.masks:
            return False

        known = [(p, ch) for p, ch in enumerate(pattern) if ch != self.wildcard]

        if not known:
            return self.all_mask[length] != 0

        length_masks = self.masks[length]
        result = self.all_mask[length]
        for p, ch in known:
            m = length_masks.get((p, ch), 0)
            result &= m
            if result == 0:
                return False
        return True

    def matches(self, pattern: str):
        """Return the actual list of matching words (slower, for debugging/UI)."""
        length = len(pattern)
        if length not in self.masks:
            return []

        known = [(p, ch) for p, ch in enumerate(pattern) if ch != self.wildcard]
        length_masks = self.masks[length]
        result = self.all_mask[length]
        for p, ch in known:
            result &= length_masks.get((p, ch), 0)
            if result == 0:
                return []

        wlist = self.by_length[length]
        out = []
        i = 0
        r = result
        while r:
            if r & 1:
                out.append(wlist[i])
            r >>= 1
            i += 1
        return out

    def save(self, path: str):
        """Pickle the prebuilt index to disk so it doesn't need rebuilding."""
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "wildcard": self.wildcard,
                    "by_length": dict(self.by_length),
                    "masks": self.masks,
                    "all_mask": self.all_mask,
                },
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

    @classmethod
    def load(cls, path: str) -> "PatternDict":
        """Load a previously-saved index without rebuilding it."""
        with open(path, "rb") as f:
            data = pickle.load(f)
        obj = cls.__new__(cls)  # skip __init__, populate directly
        obj.wildcard = data["wildcard"]
        obj.by_length = defaultdict(list, data["by_length"])
        obj.masks = data["masks"]
        obj.all_mask = data["all_mask"]
        return obj


if __name__ == "__main__":
    import time

    with open("words_alpha.txt") as f:
        words = f.read().split()

    t0 = time.perf_counter()
    pd = PatternDict(words)
    t1 = time.perf_counter()
    print(f"Loaded {len(words)} words, built index in {t1 - t0:.3f}s")

    tests = ["q_ee_", "_a__n", "hello", "zzz__", "_____", "e_a_p_e"]
    for pat in tests:
        t0 = time.perf_counter()
        result = pd.exists(pat)
        t1 = time.perf_counter()
        print(f"{pat!r:12} -> {result!s:5}  ({(t1 - t0) * 1e6:.1f} us)")

    print()
    print("Sample matches for 'q_ee_':", pd.matches("q_ee_"))

    # bulk timing
    import random
    random.seed(0)
    n = 100_000
    sample_words = random.choices(words, k=n)
    patterns = []
    for w in sample_words:
        w = list(w.lower())
        for _ in range(random.randint(0, len(w) - 1)):
            i = random.randrange(len(w))
            w[i] = "_"
        patterns.append("".join(w))

    t0 = time.perf_counter()
    for p in patterns:
        pd.exists(p)
    t1 = time.perf_counter()
    print(f"\n{n} queries in {t1 - t0:.3f}s -> {(t1 - t0) / n * 1e6:.2f} us/query")