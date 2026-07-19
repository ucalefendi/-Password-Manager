# Code Recommendations

A review of the two CLI tools in this repo — `pg.py` (password manager) and
`password checker/pc.py` (strength checker) — with concrete, prioritized fixes.
Each item explains the **problem**, shows the **current code**, and gives a
**suggested** replacement.

> Legend: 🔴 bug (wrong behavior) · 🟠 security · 🟡 robustness · 🟢 style/cleanup

---

## `pg.py` — Password Manager

### 🔴 1. The `password` dict is clobbered by the input variable

The menu reuses the name `password` for the initial-values dict *and* for the
value read at menu option 5. After the user adds one password, the original dict
is destroyed, so a later "create password file" writes a single string instead
of the seed entries.

**Current**
```python
password = {
    "email": "myemailpassword",
    ...
}
...
elif choice == "5":
    site = input("Enter the site name:   ")
    password = input("Enter the password:   ")   # overwrites the dict
    pm.add_password(site, password)
```

**Suggested** — use distinct names:
```python
seed_passwords = { "email": "myemailpassword", ... }
...
elif choice == "5":
    site = input("Enter the site name:   ")
    new_password = getpass.getpass("Enter the password:   ")
    pm.add_password(site, new_password)
```

### 🔴 2. Decryption is fragile — split on first `:` and strip the newline

`line.split(":")` breaks if a site name contains a colon, and the token still
carries the trailing `\n`, which is passed into `decrypt`.

**Current**
```python
site, encrypted = line.split(":")
self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
```

**Suggested**
```python
site, encrypted = line.rstrip("\n").split(":", 1)
self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
```

### 🟠 3. Hide password input with `getpass`

`input()` echoes the password to the terminal. Use `getpass.getpass()` so it is
not shown or stored in shell history/scrollback.

```python
import getpass
new_password = getpass.getpass("Enter the password:   ")
```

### 🟡 4. Guard against a missing key / missing site / bad token

Every crypto path assumes a key is loaded and the site exists. Add friendly
errors instead of raw tracebacks.

```python
def get_password(self, site):
    if site not in self.password_dict:
        raise KeyError(f"No password stored for '{site}'")
    return self.password_dict[site]
```
Wrap the menu dispatch in `try/except (FileNotFoundError, KeyError, InvalidToken)`
and print a readable message. Import `from cryptography.fernet import InvalidToken`.

### 🟡 5. `create_password_file` appends instead of truncating

`add_password` opens the file with `'a+'`, so "creating" a file that already
exists appends duplicate seed rows. Truncate on create:
```python
def create_password_file(self, path, initial_values=None):
    self.password_file = path
    open(path, "w").close()          # start fresh
    if initial_values:
        for site, value in initial_values.items():
            self.add_password(site, value)
```

### 🟢 6. Cache one `Fernet` instance

Each encrypt/decrypt builds a new `Fernet(self.key)`. Build it once when the key
is set (in `create_key`/`load_key`: `self.fernet = Fernet(self.key)`) and reuse
`self.fernet`.

### 🟢 7. Reprint the menu each loop / extract it to a constant

The menu prints once before the loop, so after the first action the options
scroll away. Move the menu string to a module constant and print it at the top of
each iteration (or after each action).

---

## `password checker/pc.py` — Strength Checker

### 🔴 8. A perfect password (score 7) prints no verdict

The final `if/elif` chain covers `< 4`, `== 4`, and `> 4 and < 7` — score **7**
falls through and nothing is printed.

**Current**
```python
elif score > 4 and score < 7:
    print(f"Password is strong. Score: {score}/7")
```

**Suggested**
```python
else:  # 5, 6, or 7
    print(f"Password is strong. Score: {score}/7")
```

### 🔴 9. Dead condition — `sum(characters) > 4` can never be true

There are only 4 character classes, so `sum(characters)` maxes at 4 and the
fourth `+= 1` never runs. It also makes the "adding N points" message
(`sum(characters) - 1`) misleading. Drop the impossible branch:
```python
variety = sum(characters)
score += max(variety - 1, 0)   # 0–3 points for 1–4 classes
```

### 🟡 10. `common.txt` path is relative to the CWD

The script only works when run from inside `password checker/`. Anchor the path
to the file's location:
```python
from pathlib import Path
common_path = Path(__file__).parent / "common.txt"
with open(common_path, "r", encoding="utf-8") as f:
    common = f.read().splitlines()
```

### 🟡 11. Handle empty input and use `sys.exit`

Guard the empty-password case, and prefer `sys.exit()` over the interpreter-only
builtin `exit()`:
```python
import sys
if not password:
    print("No password entered.")
    sys.exit(1)
```

### 🟢 12. Simplify the class-detection checks

The list-comprehension + `any([...])` form is verbose. Use generator expressions:
```python
upper_case   = any(c in string.ascii_uppercase for c in password)
lower_case   = any(c in string.ascii_lowercase for c in password)
special_case = any(c in string.punctuation     for c in password)
digits       = any(c in string.digits          for c in password)
```

### 🟢 13. Remove noise / redundant `str()` calls

`print("len carachters >>>", len(characters))` is always `4` and is debug noise.
Inside f-strings, `{length}` already stringifies — drop the explicit `str(...)`.

### 🟢 14. Wrap logic in `main()` / `if __name__ == "__main__"`

Matches `pg.py`'s structure and makes the checker importable/testable rather than
running at import time.

---

## Cross-cutting

| Item | Recommendation |
|------|----------------|
| **`requirements.txt`** | Add one pinning `cryptography` so the venv is reproducible (`CLAUDE.md` notes it's missing). |
| **Secrets in git** | Ensure `.gitignore` excludes `*.key` and `mypasswords.men` so keys/vaults are never committed. |
| **`pf.py`** | Currently empty — remove it or give it a purpose. |
| **Tests** | Add `pytest` tests for the scorer (boundaries 8/12/16/20, each verdict tier) and a round-trip encrypt→decrypt test for `PasswordManager`. |
| **Type hints & docstrings** | Both files would benefit from parameter/return type hints for clarity and tooling support. |

---

*Prioritize the 🔴 items first (#1, #2, #8, #9) — they are real behavioral bugs.
Then the 🟠 security item (#3), then robustness (🟡), then cleanups (🟢).*
