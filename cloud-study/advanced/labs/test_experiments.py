"""Checks learning claims at meaningful edge cases. Run with unittest discover."""

import math
import unittest

from experiments import (
    break_even, cost, drain_time, longest_prefix, nearest_rank,
    new_database, persist_once, queue_history, retry_delays,
)


class LearningChecks(unittest.TestCase):
    def test_more_specific_route_wins_regardless_of_order(self):
        routes = [("10.0.1.0/24", "specific"), ("0.0.0.0/0", "default")]
        self.assertEqual(longest_prefix("10.0.1.2", routes), "specific")
        self.assertEqual(longest_prefix("10.0.1.2", routes[::-1]), "specific")
        self.assertIsNone(longest_prefix("192.0.2.1", routes[:1]))
        with self.assertRaises(ValueError):
            longest_prefix("10.0.1.2", routes[:1] * 2)

    def test_queue_conservation_and_insufficient_capacity(self):
        arrivals = [8, 8, 20, 20, 0, 0]
        rows = queue_history(0, arrivals, 10)
        self.assertEqual([row[3] for row in rows], [0, 0, 10, 20, 10, 0])
        self.assertEqual(sum(arrivals), sum(row[2] for row in rows) + rows[-1][3])
        self.assertEqual(drain_time(1200, 8, 12), 300)
        self.assertTrue(math.isinf(drain_time(10, 5, 5)))
        with self.assertRaises(ValueError):
            queue_history(0, [-1], 1)

    def test_latency_tail_and_invalid_input(self):
        samples = [100] * 95 + [3000] * 5
        self.assertEqual(nearest_rank(samples, 95), 100)
        self.assertEqual(nearest_rank(samples, 99), 3000)
        with self.assertRaises(ValueError):
            nearest_rank([], 95)
        with self.assertRaises(ValueError):
            nearest_rank([math.nan], 95)

    def test_cost_crossover_and_parallel_lines(self):
        n = break_even("20", ".000002", "2", ".000008")
        self.assertEqual(n, 3000000)
        self.assertEqual(cost("20", ".000002", n), cost("2", ".000008", n))
        self.assertIsNone(break_even("20", "1", "2", "1"))
        self.assertLess(cost("2", ".000008", 1000000), cost("20", ".000002", 1000000))

    def test_rollback_replay_payload_conflict(self):
        db = new_database()
        self.addCleanup(db.close)
        payload = {"features": [1, 2], "version": "v1"}
        with self.assertRaises(RuntimeError):
            persist_once(db, "a", payload, True)
        self.assertEqual(db.execute("SELECT COUNT(*) FROM results").fetchone()[0], 0)
        self.assertEqual(persist_once(db, "a", payload)[0], "created")
        self.assertEqual(persist_once(db, "a", {"version": "v1", "features": [1, 2]})[0], "duplicate")
        with self.assertRaises(ValueError):
            persist_once(db, "a", {"features": [1, 2], "version": "v2"})
        self.assertEqual(db.execute("SELECT COUNT(*) FROM results").fetchone()[0], 1)

    def test_jitter_bounds(self):
        self.assertEqual(retry_delays(5, 1, 8, [1] * 5), [1, 2, 4, 8, 8])
        self.assertEqual(retry_delays(3, 1, 8, [0, .5, 1]), [0, 1, 4])
        with self.assertRaises(ValueError):
            retry_delays(1, 1, 8, [2])


if __name__ == "__main__":
    unittest.main()
