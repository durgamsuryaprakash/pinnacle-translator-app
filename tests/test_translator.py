"""Tests for the input validation logic of translator.translate_text.

These tests deliberately avoid network calls so they run quickly and
reliably in any environment.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from translator import MAX_TEXT_LENGTH, translate_text


class TranslateTextValidationTests(unittest.TestCase):
    def test_empty_text_returns_error(self):
        result = translate_text("", "English", "Hindi")
        self.assertFalse(result["success"])
        self.assertFalse(result["translated_text"])
        self.assertTrue(result["error"])

    def test_whitespace_only_text_returns_error(self):
        result = translate_text("   \n\t ", "English", "Hindi")
        self.assertFalse(result["success"])
        self.assertTrue(result["error"])

    def test_same_source_and_target_returns_error(self):
        result = translate_text("Hello", "English", "English")
        self.assertFalse(result["success"])
        self.assertIn("different", result["error"].lower())

    def test_unsupported_language_returns_error(self):
        result = translate_text("Hello", "English", "Klingon")
        self.assertFalse(result["success"])
        self.assertIn("supported", result["error"].lower())

    def test_text_over_limit_returns_error(self):
        result = translate_text("a" * (MAX_TEXT_LENGTH + 1), "English", "Hindi")
        self.assertFalse(result["success"])
        self.assertIn("5,000", result["error"])

    def test_result_shape_is_consistent(self):
        result = translate_text("", "English", "Hindi")
        self.assertEqual(
            set(result),
            {
                "success",
                "original_text",
                "translated_text",
                "source_language",
                "target_language",
                "error",
            },
        )


if __name__ == "__main__":
    unittest.main()
