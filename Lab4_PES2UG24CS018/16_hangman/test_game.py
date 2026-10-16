import random
import unittest
from unittest.mock import patch

from game import HangmanGame


def new_round(word="python", difficulty="medium", category="technology"):
    g = HangmanGame()
    g.category, g.difficulty = category, difficulty
    with patch.object(random, "choice", return_value=word):
        g.start_round()
    return g


def run_session(inputs, word="python"):
    g = HangmanGame()
    with patch("builtins.input", side_effect=inputs), \
         patch.object(random, "choice", return_value=word), \
         patch("builtins.print"):
        g.run()
    return g


class TestGuesses(unittest.TestCase):
    def test_repeated_wrong_guess_costs_one_life(self):
        g = new_round()
        g.guess("q")
        self.assertEqual(g.guess("q"), "Already tried 'q'.")
        self.assertEqual(g.lives, 5)

    def test_repeated_correct_guess_not_counted_again(self):
        g = new_round()
        g.guess("p")
        self.assertEqual(g.guess("p"), "Already tried 'p'.")
        self.assertEqual((g.guessed, g.lives), ({"p"}, 6))

    def test_invalid_input_changes_nothing(self):
        g = new_round()
        for bad in ["", "ab", "1", "#", "é", "/hnt"]:
            g.guess(bad)
        self.assertEqual((g.guessed, g.wrong, g.lives), (set(), set(), 6))


class TestHintsAndDifficulty(unittest.TestCase):
    def test_lives_per_difficulty(self):
        for diff, lives in [("easy", 8), ("medium", 6), ("hard", 4)]:
            self.assertEqual(new_round(difficulty=diff).lives, lives)

    def test_hint_charged_once_and_consistently(self):
        g = new_round(difficulty="hard")
        g.use_hint()
        self.assertTrue(g.use_hint().startswith("Hint (already used)"))
        g.streak = 1
        self.assertEqual(g.round_points(), 8 + 1 - 3)
        self.assertEqual(g.score, 0)  # hint never touches score directly

    def test_new_round_resets_round_state_only(self):
        g = new_round(difficulty="easy")
        g.guess("q"); g.use_hint(); g.score, g.streak = 10, 2
        g.difficulty = "hard"
        g.start_round()
        self.assertEqual((g.wrong, g.hint_used, g.lives), (set(), False, 4))
        self.assertEqual((g.score, g.streak), (10, 2))


class TestSession(unittest.TestCase):
    WIN = list("python")
    LOSE = list("abcdfg")  # 6 wrong letters

    def test_stats_and_streak_across_rounds(self):
        g = run_session(["1", "2", *self.WIN, "y", "", "", *self.WIN, "y",
                         "", "", *self.LOSE, "n"])
        s = g.stats
        self.assertEqual((s.rounds, s.wins, s.best_streak, g.streak), (3, 2, 2, 0))
        self.assertEqual(g.score, (5 + 1) + (5 + 2))

    def test_category_and_difficulty_change(self):
        g = run_session(["science", "hard", *self.WIN, "y", "3", "1", *self.WIN, "n"])
        self.assertEqual((g.category, g.difficulty), ("culture", "easy"))

    def test_invalid_menu_input_reprompts(self):
        g = run_session(["sports", "9", "1", "extreme", "1", *self.WIN, "maybe", "n"])
        self.assertEqual((g.stats.rounds, g.difficulty), (1, "easy"))

    def test_quit_mid_round_not_recorded(self):
        g = run_session(["1", "1", "p", "/quit"])
        self.assertEqual(g.stats.rounds, 0)

    def test_quit_at_menu(self):
        self.assertEqual(run_session(["q"]).stats.rounds, 0)


if __name__ == "__main__":
    unittest.main()
