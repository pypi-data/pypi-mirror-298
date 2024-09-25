""" Tests of the debugger
"""
import unittest

import sys
sys.path.append("..")

from debugger.debug_interface import DebuggerInterface


EXAMPLE_ADD = "../../examples/add.bs"
EXAMPLE_SWAP = "../../examples/swap.bs"


class DebuggerTests(unittest.TestCase):
    """ Tests of the debugger
    """
    def setUp(self):
        self.dbif = DebuggerInterface()
        self.dbif.set_noisy(False)

    def test_file(self):
        """ Simple file load
        """
        self.assertFalse(self.dbif.db_context.has_script())
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertTrue(self.dbif.db_context.has_script())

    def test_run(self):
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertIsNone(self.dbif.db_context.ip)

        self.dbif.process_input(["run"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [3])

    def test_step(self):
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertIsNone(self.dbif.db_context.ip)

        self.dbif.process_input(["s"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [1])
        self.assertEqual(self.dbif.db_context.ip, 1)

        self.dbif.process_input(["step"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 2])
        self.assertEqual(self.dbif.db_context.ip, 2)

        self.dbif.process_input(["step"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [3])
        self.assertEqual(self.dbif.db_context.ip, 3)

    def test_step_and_reset(self):
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertIsNone(self.dbif.db_context.ip)

        self.dbif.process_input(["s"])
        self.assertEqual(self.dbif.db_context.get_stack(), [1])
        self.assertEqual(self.dbif.db_context.ip, 1)

        self.dbif.process_input(["step"])
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 2])
        self.assertEqual(self.dbif.db_context.ip, 2)

        self.dbif.process_input(["reset"])
        self.assertEqual(self.dbif.db_context.ip, 0)

        self.dbif.process_input(["step"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [1])
        self.assertEqual(self.dbif.db_context.ip, 1)

        self.dbif.process_input(["step"])
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 2])
        self.assertEqual(self.dbif.db_context.ip, 2)

    def test_step_and_run(self):
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertIsNone(self.dbif.db_context.ip)

        self.dbif.process_input(["s"])
        self.assertEqual(self.dbif.db_context.get_stack(), [1])
        self.assertEqual(self.dbif.db_context.ip, 1)

        self.dbif.process_input(["run"])
        self.assertEqual(self.dbif.db_context.get_stack(), [3])
        self.assertEqual(self.dbif.db_context.ip, 0)

    def test_file_load_twice(self):
        self.dbif.process_input(["file", EXAMPLE_ADD])
        self.assertIsNone(self.dbif.db_context.ip)

        self.dbif.process_input(["run"])
        self.assertIsNotNone(self.dbif.db_context.ip)
        self.assertEqual(self.dbif.db_context.get_stack(), [3])
        self.assertEqual(self.dbif.db_context.ip, 0)

        self.dbif.process_input(["file", EXAMPLE_SWAP])
        self.assertEqual(self.dbif.db_context.ip, 0)

        self.dbif.process_input(["run"])
        self.assertEqual(self.dbif.db_context.ip, 0)
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 3, 2])

        self.dbif.process_input(["step"])
        self.assertEqual(self.dbif.db_context.ip, 1)
        self.assertEqual(self.dbif.db_context.get_stack(), [1])

    def test_breakpoint(self):
        self.dbif.process_input(["file", EXAMPLE_SWAP])

        self.dbif.process_input(["b", "2"])

        self.dbif.process_input(["run"])
        self.assertEqual(self.dbif.db_context.ip, 2)
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 2])

        # Restarts from the begining
        self.dbif.process_input(["run"])
        self.assertEqual(self.dbif.db_context.ip, 2)
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 2])

        # Continues from current position
        self.dbif.process_input(["c"])
        self.assertEqual(self.dbif.db_context.ip, 0)
        self.assertEqual(self.dbif.db_context.get_stack(), [1, 3, 2])

    def test_interpreter(self):
        self.dbif.process_input(["i", "1", "2", "OP_ADD"])
        self.assertEqual(self.dbif.db_context.get_stack(), [3])


if __name__ == "__main__":
    unittest.main()
