import argparse
import random
import urllib.request
from collections import Counter
from pathlib import Path
import cowsay

def bullscows(guess: str, secret: str) -> tuple[int, int]:
    bulls = sum(1 for g, s in zip(guess, secret) if g == s)
    common = sum((Counter(guess) & Counter(secret)).values())
    cows = common - bulls
    return bulls, cows

def gameplay(ask, inform, words: list[str]) -> int:
    secret = random.choice(words)
    attempts = 0
    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess == secret:
            return attempts

def ask(prompt: str, valid: list[str] | None = None) -> str:
    while True:
        print(cowsay.cowsay(prompt))
        s = input().strip()
        if not valid or s in valid:
            return s

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows)))

def _is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")

def _load_words_from_text(text: str) -> list[str]:
    return [w for w in (x.strip() for x in text.split()) if w]

def _load_dictionary(source: str) -> list[str]:
    if _is_url(source):
        with urllib.request.urlopen(source) as resp:
            data = resp.read()
        return _load_words_from_text(data.decode("utf-8", errors="replace"))

    return _load_words_from_text(Path(source).read_text(encoding="utf-8", errors="replace"))

def _filter_words(words: list[str], length: int) -> list[str]:
    out = []
    seen = set()
    for w in words:
        if len(w) != length:
            continue
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary")
    parser.add_argument("length", nargs="?", type=int, default=5)
    args = parser.parse_args()

    words = _filter_words(_load_dictionary(args.dictionary), args.length)

    if not words:
        print("Список слов пуст")
    else:
        attempts = gameplay(ask, inform, words)
        print(attempts)