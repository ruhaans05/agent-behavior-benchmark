import unittest

from agent_behavior_benchmark.benchmark import run_benchmark
from agent_behavior_benchmark.classifiers import BinaryNaiveBayes, binary_metrics
from agent_behavior_benchmark.study import run_initial_study


class BenchmarkTests(unittest.TestCase):
    def test_starter_benchmark_runs(self) -> None:
        payload = run_benchmark("starter", ["openai_style", "claude_style"], trials=3, seed=1)

        self.assertEqual(payload["experiment"], "starter")
        self.assertEqual(len(payload["trials"]), 9)
        self.assertIn("openai_style", payload["summary"])
        self.assertIn("claude_style", payload["summary"])

    def test_live_providers_are_opt_in(self) -> None:
        with self.assertRaisesRegex(ValueError, "require --allow-live"):
            run_benchmark("negotiation", ["openai_live"], trials=1, seed=1, allow_live=False)

    def test_study_reaches_1k_actions_and_reports_classifiers(self) -> None:
        study = run_initial_study(trials_per_environment=200, seed=20260905)

        self.assertEqual(study["environment_trials"], 600)
        self.assertEqual(study["agent_actions"], 1200)
        self.assertEqual(set(study["behavior_classifier_metrics"]), {"deception", "collusion", "spec_gaming"})
        self.assertGreater(study["behavior_classifier_metrics"]["deception"]["test_examples"], 0)

    def test_binary_classifier_learns_simple_trace_signal(self) -> None:
        classifier = BinaryNaiveBayes().fit(
            [("honest independent bid", False), ("coordinate a low bid", True)]
        )

        self.assertTrue(classifier.predict("coordinate low bid"))
        self.assertFalse(classifier.predict("honest bid"))
        self.assertEqual(binary_metrics([(True, True), (False, False)])["f1"], 1.0)


if __name__ == "__main__":
    unittest.main()
