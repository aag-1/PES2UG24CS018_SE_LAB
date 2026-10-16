import random
from words import WORDS, HINTS
from stats import SessionStats

DIFFICULTIES = {
    "easy": {"lives": 8, "points": 3, "hint_cost": 1},
    "medium": {"lives": 6, "points": 5, "hint_cost": 2},
    "hard": {"lives": 4, "points": 8, "hint_cost": 3},
}


class HangmanGame:
    def __init__(self):
        # Session state: kept across rounds
        self.score = 0
        self.streak = 0
        self.stats = SessionStats()
        self.category = "technology"
        self.difficulty = "medium"
        # Round state: reset by start_round()
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 0
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if len(letter) != 1 or not ("a" <= letter <= "z"):
            return "Enter a single letter a-z."
        if letter in self.guessed or letter in self.wrong:
            return f"Already tried '{letter}'."
        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."
        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        hint = HINTS.get(self.secret, "No hint available.")
        if self.hint_used:
            return f"Hint (already used): {hint}"
        self.hint_used = True
        cost = DIFFICULTIES[self.difficulty]["hint_cost"]
        return f"Hint: {hint} (-{cost} points if you win)"

    def round_points(self):
        rules = DIFFICULTIES[self.difficulty]
        points = rules["points"] + self.streak
        if self.hint_used:
            points -= rules["hint_cost"]
        return points

    def stats_line(self):
        s = self.stats
        return (f"Rounds: {s.rounds}  Won: {s.wins}  Best streak: {s.best_streak}"
                f"  Score: {self.score}")

    def play_round(self):
        self.start_round()
        print(f"\nCategory: {self.category}  Difficulty: {self.difficulty}")
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print("Lives:", self.lives, " Score:", self.score, " Streak:", self.streak)
            raw = input("Letter, /hint, or /quit: ").strip().lower()
            if raw == "/quit":
                return False
            if raw == "/hint":
                print(self.use_hint())
            elif raw.startswith("/"):
                print("Unknown command. Use /hint or /quit.")
            else:
                print(self.guess(raw))

        won = self.won()
        if won:
            self.streak += 1
            points = self.round_points()
            self.score += points
            print(f"Solved: {self.secret} (+{points} points)")
        else:
            self.streak = 0
            print("Out of lives. The word was:", self.secret)
        self.stats.record(won, self.streak)
        return True

    def choose(self, label, options, current):
        names = list(options)
        print(f"\n{label}:", "  ".join(f"{i}) {n}" for i, n in enumerate(names, 1)))
        while True:
            raw = input(f"Choose {label.lower()} [Enter = {current}, q = quit]: ").strip().lower()
            if raw == "":
                return current
            if raw == "q":
                return None
            if raw.isdigit() and 1 <= int(raw) <= len(names):
                return names[int(raw) - 1]
            if raw in options:
                return raw
            print(f"Unknown {label.lower()}.")

    def ask_again(self):
        while True:
            raw = input("Another round? [y/n]: ").strip().lower()
            if raw in ("y", "n"):
                return raw == "y"
            print("Enter y or n.")

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        while True:
            category = self.choose("Category", WORDS, self.category)
            if category is None:
                break
            difficulty = self.choose("Difficulty", DIFFICULTIES, self.difficulty)
            if difficulty is None:
                break
            self.category, self.difficulty = category, difficulty
            if not self.play_round() or not self.ask_again():
                break
        print("\nSession over.", self.stats_line())
