import unittest
from unittest.mock import patch

from bdmc.modules.controller import CloseLoopController, MotorInfo

from mentabotix.modules.botix import MovingTransition, MovingState, Botix


# Define a mock MovingState class for testing purposes


class TestMovingTransition(unittest.TestCase):

    def setUp(self):
        self.default_duration = 1.5

        def breker() -> bool:
            return True

        self.default_breaker = breker
        self.default_check_interval = 0.2
        self.default_from_state = MovingState(0)
        self.default_to_state = MovingState(0)

    def test_init_valid_input(self):
        # Test valid input with all parameters provided
        transition = MovingTransition(
            self.default_duration,
            self.default_breaker,
            self.default_check_interval,
            self.default_from_state,
            self.default_to_state,
        )
        self.assertEqual(transition.duration, self.default_duration)
        self.assertEqual(transition.breaker, self.default_breaker)
        self.assertEqual(transition.check_interval, self.default_check_interval)
        self.assertIsInstance(transition.from_states, list)
        self.assertIsInstance(transition.to_states, dict)

    def test_init_duration_not_positive(self):
        with self.assertRaises(ValueError):
            MovingTransition(-1, None, None, None, None)

    def test_init_from_states_valid_types(self):
        # Test valid from_states types
        transition = MovingTransition(self.default_duration, None, None, self.default_from_state, None)
        self.assertEqual(len(transition.from_states), 1)
        self.assertEqual(transition.from_states[0], self.default_from_state)

        from_states_iterable = [MovingState(0), MovingState(0)]
        transition = MovingTransition(self.default_duration, None, None, from_states_iterable, None)
        self.assertEqual(len(transition.from_states), len(from_states_iterable))
        self.assertEqual(transition.from_states, list(from_states_iterable))

    def test_init_from_states_invalid_type(self):
        with self.assertRaises(ValueError):
            MovingTransition(self.default_duration, None, None, "invalid", None)

    def test_init_to_states_valid_types(self):
        # Test valid to_states types
        transition = MovingTransition(self.default_duration, None, None, None, self.default_to_state)
        self.assertEqual(len(transition.to_states), 1)
        self.assertEqual(list(transition.to_states.values())[0], self.default_to_state)

        to_states_dict = {1: MovingState(0), 2: MovingState(1)}
        transition = MovingTransition(self.default_duration, None, None, None, to_states_dict)
        self.assertEqual(len(transition.to_states), len(to_states_dict))
        self.assertEqual(transition.to_states, to_states_dict)

    def test_init_to_states_invalid_type(self):
        with self.assertRaises(ValueError):
            MovingTransition(self.default_duration, None, None, None, "invalid")

    def test_add_from_state(self):
        transition = MovingTransition(self.default_duration, None, None, None, None)
        transition.add_from_state(self.default_from_state)
        self.assertEqual(len(transition.from_states), 1)
        self.assertEqual(transition.from_states[0], self.default_from_state)

    def test_add_to_state(self):
        transition = MovingTransition(self.default_duration, None, None, None, None)
        key = 1
        transition.add_to_state(key, self.default_to_state)
        self.assertEqual(len(transition.to_states), 1)
        self.assertEqual(transition.to_states[key], self.default_to_state)

    @patch("mentabotix.MovingTransition.tokenize")
    def test_tokenize_called(self, mock_tokenize):
        transition = MovingTransition(self.default_duration, None, None, None, None)
        transition.tokenize()
        mock_tokenize.assert_called_once_with()

    @patch("mentabotix.MovingTransition.clone")
    def test_clone_called(self, mock_clone):
        transition = MovingTransition(self.default_duration, None, None, None, None)
        transition.clone()
        mock_clone.assert_called_once_with()

    def test_clone_behavior(self):
        transition1 = MovingTransition(self.default_duration)
        transition2 = transition1.clone()
        self.assertEqual(transition1, transition2)
        self.assertNotEqual(id(transition1), id(transition2))
        self.assertNotEqual(id(transition1.to_states), id(transition2.to_states))
        self.assertNotEqual(id(transition1.from_states), id(transition2.from_states))

    def test_identifier(self):
        transition1 = MovingTransition(self.default_duration, None, None, None, None)
        transition2 = MovingTransition(self.default_duration, None, None, None, None)
        self.assertNotEqual(transition1.transition_id, transition2.transition_id)

    def test_str(self):
        MovingState.__state_id_counter__ = 0
        MovingTransition.__transition_id_counter__ = 0
        from_states = [MovingState(100), MovingState(0)]
        to_states = {1: MovingState(4100), 2: MovingState(2000), 3: MovingState(0)}
        transition = MovingTransition(self.default_duration, None, None, from_states, to_states)

        self.assertEqual(
            str(transition),
            (
                "┌0-MovingTransition──┬─────────────────────┐\n"
                "│ From               │ To                  │\n"
                "├────────────────────┼─────────────────────┤\n"
                "│ 0-MovingState(100) │ 2-MovingState(4100) │\n"
                "│ 1-MovingState(0)   │ 3-MovingState(2000) │\n"
                "│                    │ 4-MovingState(0)    │\n"
                "├────────────────────┼─────────────────────┤\n"
                "│ Duration: 1.500s   │ Breaker: None       │\n"
                "└────────────────────┴─────────────────────┘"
            ),
        )

    def test_hash(self):
        transition1 = MovingTransition(self.default_duration, None, None, None, None)
        transition2 = MovingTransition(self.default_duration, None, None, None, None)
        self.assertNotEqual(hash(transition1), hash(transition2))

    def test_som(self):
        state_a = MovingState(100, -100)

        end_state = MovingState(0)

        state_b = MovingState(5000)

        state_c = MovingState(
            speed_expressions=("var1", "var2"),
            used_context_variables=["var1", "var2"],
        )

        import random

        con = CloseLoopController(
            [MotorInfo(1), MotorInfo(2), MotorInfo(3), MotorInfo(4)], port="COM10", context={"var1": 10, "var2": 20}
        )

        def breaker() -> int:
            return random.randint(0, 2)

        trans = MovingTransition(
            2.0,
            to_states={0: end_state, 1: state_b, 2: state_c},
            from_states=state_a,
            breaker=breaker,
        )
        botix = Botix(con)
        botix.token_pool.append(trans)
        func = botix.compile(False)

        print(f"is callable {callable(func)}")


if __name__ == "__main__":
    unittest.main()
