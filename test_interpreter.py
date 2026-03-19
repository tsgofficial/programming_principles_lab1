# ============================================================
#  F.CSB305 Программчлалын хэлний зарчмууд
#  ЛАБОРАТОРИЙН АЖИЛ 1 — Тестийн багц (Алхам 4)
# ============================================================

import unittest
import sys
import os

# interpreter.py -г олохын тулд замыг нэмнэ
sys.path.insert(0, os.path.dirname(__file__))
from interpreter import interpret


class TestInterpreter(unittest.TestCase):

    # ── Нэмэх ────────────────────────────────────────────────
    def test_addition_simple(self):
        self.assertEqual(interpret("3 + 5"), 8)

    def test_addition_multiple(self):
        self.assertEqual(interpret("1 + 2 + 3 + 4"), 10)

    # ── Хасах ────────────────────────────────────────────────
    def test_subtraction_simple(self):
        self.assertEqual(interpret("7 - 2"), 5)

    def test_subtraction_negative_result(self):
        self.assertEqual(interpret("3 - 10"), -7)

    # ── Үржүүлэх ─────────────────────────────────────────────
    def test_multiplication(self):
        self.assertEqual(interpret("4 * 3"), 12)

    def test_multiplication_zero(self):
        self.assertEqual(interpret("100 * 0"), 0)

    # ── Хуваах ───────────────────────────────────────────────
    def test_division(self):
        self.assertEqual(interpret("10 / 2"), 5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            interpret("5 / 0")

    # ── Давуу эрэмбэ (operator precedence) ───────────────────
    def test_precedence_mul_before_add(self):
        # 2 + 3 * 4 = 2 + 12 = 14  (үржих нь нэмэхээс өмнө)
        self.assertEqual(interpret("2 + 3 * 4"), 14)

    def test_precedence_div_before_sub(self):
        # 10 - 6 / 2 = 10 - 3 = 7
        self.assertEqual(interpret("10 - 6 / 2"), 7)

    # ── Хашилт ───────────────────────────────────────────────
    def test_parentheses_basic(self):
        self.assertEqual(interpret("2 * (4 + 3)"), 14)

    def test_parentheses_nested(self):
        self.assertEqual(interpret("(2 + 3) * (4 - 1)"), 15)

    def test_parentheses_change_order(self):
        self.assertEqual(interpret("(1 + 2) * 3"), 9)

    # ── Олон оронтой тоо ─────────────────────────────────────
    def test_multidigit_numbers(self):
        self.assertEqual(interpret("100 + 200"), 300)

    def test_large_expression(self):
        self.assertEqual(interpret("100 - 50 + 25 * 2"), 100)

    # ── Захын тохиолдол (edge cases) ─────────────────────────
    def test_single_number(self):
        self.assertEqual(interpret("42"), 42)

    def test_zero(self):
        self.assertEqual(interpret("0"), 0)

    def test_extra_spaces(self):
        self.assertEqual(interpret("  3  +   5  "), 8)

    # ── Алдааны тохиолдол ────────────────────────────────────
    def test_invalid_character(self):
        with self.assertRaises(ValueError):
            interpret("3 @ 5")

    def test_missing_closing_paren(self):
        with self.assertRaises(SyntaxError):
            interpret("(3 + 5")


if __name__ == "__main__":
    # Дэлгэрэнгүй гаралттай ажиллуулна
    unittest.main(verbosity=2)