# Lab 4 — Vibe Coding: Hangman Challenge (Scenario 16)

**Name:** Aayush Gupta  
**SRN:** PES2UG24CS018

## Contents

| Path | Deliverable |
|---|---|
| `16_hangman/` | Updated code |
| `screenshots/before.png` | Original code: repeating wrong letter `q` drops lives 6 → 5 → 4 → 3 |
| `screenshots/after_1_bugfix_input.png` | Updated code: repeat rejected, invalid input and unknown command rejected, hint not charged twice |
| `screenshots/after_2_difficulty_scoring_stats.png` | Updated code: hard difficulty (4 lives), hint cost, win scoring, streak reset, session summary |
| `chat_history.pdf` | Complete LLM chat history |

## Run

```bash
cd 16_hangman
python3 main.py
python3 -m unittest -v test_game
```

Standard library only. No persistence.

## Changes

**Task 1 — Guess-state correctness.** `guess()` only checked correct letters, so a repeated
wrong letter cost a life each time. It now checks correct and wrong letters; each distinct
letter affects the round once.

**Task 2 — Session model.** `SessionStats` (`stats.py`, unchanged) is integrated into
`HangmanGame`. Rounds played, rounds won and best streak persist across the session;
`start_round()` resets only round state. A round abandoned with `/quit` is not recorded.
A summary prints on every exit path.

**Task 3 — Difficulty and scoring.**

| Difficulty | Lives | Win points | Hint cost |
|---|---|---|---|
| easy | 8 | 3 | 1 |
| medium | 6 | 5 | 2 |
| hard | 4 | 8 | 3 |

Win = win points + streak − hint cost (if used). Loss = 0. Category and difficulty are
chosen each round; Enter keeps the previous choice.

**Task 4 — Input and feedback.** Guesses must be one letter a–z; anything else is rejected
without changing state. Unknown `/` commands are reported. A repeated `/hint` re-shows the
hint without a second charge. Menus accept a name or number and re-prompt on invalid input;
`y/n` re-prompts on anything else. Each action gets one message.

## Testing

`16_hangman/test_game.py` (11 tests, all passing) covers repeated correct and incorrect
guesses, hints, category changes, multiple rounds, streak resets, difficulty changes,
invalid input and quitting.
