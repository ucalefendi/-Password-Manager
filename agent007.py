"""agent007.py — a secret-agent themed password generator.

Generates cryptographically strong passwords using the `secrets` module.
Run interactively, or pass options on the command line.
"""

import argparse
import secrets
import string


# Character pools available to the generator.
POOLS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{};:,.<>?",
}

# Characters that are easy to confuse with one another.
AMBIGUOUS = set("O0oIl1|`'\"")


def build_alphabet(use_lower, use_upper, use_digits, use_symbols, no_ambiguous):
    """Assemble the character set from the selected pools."""
    alphabet = ""
    if use_lower:
        alphabet += POOLS["lower"]
    if use_upper:
        alphabet += POOLS["upper"]
    if use_digits:
        alphabet += POOLS["digits"]
    if use_symbols:
        alphabet += POOLS["symbols"]

    if not alphabet:
        raise ValueError("At least one character type must be enabled.")

    if no_ambiguous:
        alphabet = "".join(c for c in alphabet if c not in AMBIGUOUS)

    return alphabet


def generate(length, alphabet):
    """Return a random password of the given length using `secrets`."""
    if length < 1:
        raise ValueError("Length must be at least 1.")
    return "".join(secrets.choice(alphabet) for _ in range(length))


def parse_args():
    parser = argparse.ArgumentParser(
        description="agent007 — generate strong passwords."
    )
    parser.add_argument(
        "-l", "--length", type=int, default=16, help="password length (default: 16)"
    )
    parser.add_argument(
        "-n", "--count", type=int, default=1, help="how many to generate (default: 1)"
    )
    parser.add_argument(
        "--no-lower", action="store_true", help="exclude lowercase letters"
    )
    parser.add_argument(
        "--no-upper", action="store_true", help="exclude uppercase letters"
    )
    parser.add_argument("--no-digits", action="store_true", help="exclude digits")
    parser.add_argument(
        "--no-symbols", action="store_true", help="exclude symbols"
    )
    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="exclude easily confused characters (O0oIl1 ...)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    alphabet = build_alphabet(
        use_lower=not args.no_lower,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        no_ambiguous=args.no_ambiguous,
    )
    for _ in range(max(args.count, 1)):
        print(generate(args.length, alphabet))


if __name__ == "__main__":
    main()
