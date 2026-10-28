# Reflection

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the style issues. Renaming functions to snake_case, adding docstrings, splitting the one-line `if`, and wrapping long lines are mechanical changes. The tool gives the exact line and the fix is obvious. The parameterized SQL query and swapping `random` for `secrets` were also quick, because each is a standard one-line replacement.

**Hardest:** the bare `except:` and the `global` statement. They took more thought because the warning was only a symptom.
- The bare `except` in `oldestAvailable` was hiding a real bug: when no pet is available, `fetchone()` returns `None` and `row[0]` raises `TypeError`. Swapping in a narrower exception would have kept that hidden. The fix was to remove the exception handling and check for `None` explicitly.
- Removing `global adoption_count` meant asking where the count should come from. The database already knows which pets are adopted, so `shelter_status()` now counts them with SQL. This also fixed a bug the tools didn't mention: the old counter went up even when `adopt()` was given an id that doesn't exist.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, partly.
- **Pylint C0103 on `adoption_count`** asked for UPPER_CASE because Pylint treats every module-level variable as a constant. The variable wasn't a constant (it changed on every adoption), so renaming it to `ADOPTION_COUNT` would have been misleading. The real problem was the global state itself, which is what I fixed.
- **Bandit B311 (`random`)** is borderline. For a demo shelter app the adoption code isn't a strong secret. But if the code is ever used to confirm or collect an adoption, a guessable code is a real weakness. `secrets` costs nothing, so I treated it as a true positive.
- **Pylint C0209** suggested turning the `%` SQL into an f-string. Following it literally would have kept the SQL injection. This shows why you read the warnings together instead of fixing them one at a time.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor so issues show up while typing, and add a `pre-commit` hook that runs `flake8`, `pylint` and `bandit` before each commit.
- **In CI:** run all three on every pull request (for example in a GitHub Actions job). Fail the build on any Bandit Medium/High finding, any Flake8 error, or a Pylint score below a threshold (for example 9.5).
- **Configuration:** keep the shared settings (line length, disabled checks) in `pyproject.toml` / `.flake8` so everyone uses the same rules. Any `# nosec` or `# pylint: disable` needs a comment explaining why.

### 4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?

- **Security:** the SQL injection is closed, and adoption codes are no longer predictable. Bandit went from 3 issues to none.
- **Correctness:** two latent bugs are gone. Tags no longer leak between calls (shared mutable default), and an empty register returns `None` instead of relying on a swallowed `TypeError`. Database errors in `clear_unadopted()` now surface instead of being silently ignored.
- **Readability:** consistent PEP 8 names, docstrings on every function, and short lines. Pylint went from 3.95 to 10.00/10 and Flake8 from 5 issues to 0.
- **Maintainability:** with no global counter, status comes from a single source of truth, the database. The `if __name__ == "__main__":` guard lets the module be imported and tested without running the demo.
