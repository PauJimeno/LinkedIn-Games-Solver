"""
Build a PatternDict index from a word list file and save it to disk,
so your solver can load it instantly instead of rebuilding every run.

Usage:
    python build_index.py words_alpha.txt index.pkl
"""

import sys
import time

from utils.pattern_dict import PatternDict


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_index.py <wordlist.txt> <output_index.pkl>")
        sys.exit(1)

    wordlist_path, output_path = sys.argv[1], sys.argv[2]

    with open(wordlist_path) as f:
        words = f.read().split()

    print(f"Building index from {len(words)} words in {wordlist_path}...")
    t0 = time.perf_counter()
    pd = PatternDict(words)
    t1 = time.perf_counter()
    print(f"Built in {t1 - t0:.3f}s")

    pd.save(output_path)
    t2 = time.perf_counter()
    print(f"Saved to {output_path} in {t2 - t1:.3f}s")


if __name__ == "__main__":
    main()