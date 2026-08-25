from django.contrib.auth import get_user_model
from django.test import TestCase

from .views import (
    calculate_prompt_score,
    compare_prompt_scores,
    get_prompt_analysis,
)


class PromptScoringTests(TestCase):
    def test_calculate_prompt_score_handles_none(self):
        self.assertEqual(calculate_prompt_score(None), 0)

    def test_compare_prompt_scores_handles_missing_optimized_prompt(self):
        original_score, optimized_score, improvement = compare_prompt_scores(
            "Write a Python script to parse a CSV file.",
            None,
        )

        self.assertGreater(original_score, 0)
        self.assertEqual(optimized_score, 0)
        self.assertLess(improvement, 0)

    def test_dashboard_post_does_not_crash_for_valid_prompt(self):
        user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="secret123",
        )
        self.client.force_login(user)

        response = self.client.post(
            "/accounts/dashboard/",
            {
                "original_prompt": "Write a Python script to parse a CSV file.",
                "technique": "zero_shot",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_prompt_analysis_returns_actionable_metrics(self):
        analysis = get_prompt_analysis(
            "Write a Python script to parse a CSV file and return results in JSON."
        )

        self.assertIn("word_count", analysis)
        self.assertIn("task_strength", analysis)
        self.assertIn("context_strength", analysis)
        self.assertIn("output_strength", analysis)
        self.assertIn("overall_score", analysis)
        self.assertGreater(analysis["word_count"], 0)
        self.assertGreaterEqual(analysis["overall_score"], 0)
        self.assertLessEqual(analysis["overall_score"], 100)
