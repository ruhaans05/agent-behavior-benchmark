import unittest

from agent_behavior_benchmark.benchmark import run_benchmark


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


if __name__ == "__main__":
    unittest.main()
