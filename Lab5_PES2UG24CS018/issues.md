# Issues found in `pet_shelter.py`

Line numbers refer to the **original** file. Reports: `reports/before/` and `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608, Medium) | Security | 10 | `INSERT` built with `%` string formatting, so a pet name like `x'); DROP TABLE pets; --` becomes part of the SQL. | Parameterized query with `?` placeholders and a values tuple. |
| Insecure randomness (Bandit B311, Low) | Security | 22 | `random.randint` is a predictable PRNG, so adoption codes can be guessed. | Use `secrets.randbelow(9000) + 1000` (same `PET-1000`..`PET-9999` range). |
| try/except/pass (Bandit B110, Low; Pylint W0718) | Security / Bug | 34-37 | `except Exception: pass` silently swallows any database error, so a failed delete looks like success. | Removed the `try` block so real errors surface. |
| Mutable default argument (Pylint W0102) | Bug | 9 | `tags=[]` is created once and shared by every call, so tags pile up across pets. | Default to `None`, create a new list inside the function. |
| Bare `except:` (Pylint W0702, Flake8 E722) | Bug | 29-30 | Catches everything, including `KeyboardInterrupt`; it was really hiding the `TypeError` from `row[0]` when no pet is available. | Explicit `if row is None: return None`; no exception handling needed. |
| Global statement (Pylint W0603) | Design | 6, 16, 18 | `adoption_count` is mutable global state, and it went up even when `adopt()` was given an id that doesn't exist. | Removed the counter; `shelter_status()` counts adopted rows in the database. |
| Non-snake_case names (Pylint C0103) | Style | 9, 21, 25, 33, 40 | `registerPet`, `adoptionCode`, `oldestAvailable`, `clearUnadopted`, `shelterStatus` break PEP 8 naming. | Renamed to `register_pet`, `adoption_code`, `oldest_available`, `clear_unadopted`, `shelter_status`. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 9-45 | No module or function docstrings. | Added a one-line docstring to the module and every function. |
| Multiple statements on one line (Flake8 E701, Pylint C0321) | Style | 41 | `if adoption_count > 0: return "active"` | Split into an `if` block. |
| Line too long (Flake8 E501, Pylint C0301) | Style | 5, 10, 27 | Lines of 103-116 characters (limits: Flake8 79, Pylint 100). | Wrapped SQL strings using implicit string concatenation. |
| f-string suggestion (Pylint C0209) | Style | 10 | `%` formatting could be an f-string. | Fixed by the B608 change: the query no longer formats strings at all. An f-string would have kept the injection bug. |
| Code runs on import (best practice) | Design | 54 | `main()` called at module level, so importing the module runs the demo. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Bandit | 3 issues (1 Medium, 2 Low) | No issues identified |
| Pylint | 3.95/10 (23 messages) | 10.00/10 |
| Flake8 | 5 issues | 0 issues |

The program output is unchanged: `Kiwi PET-#### active`.
