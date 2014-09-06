__author__ = 'XinYu'

import unittest
from Automata import FiniteAutomation, nfa2dfa


class TestAutomata(unittest.TestCase):

    def setUp(self):
        self.fa = FiniteAutomation(set(['0', '1']))
        self.fa.set_start_state('A')
        self.fa.add_transition('A', 'B', FiniteAutomation.epsilon)
        self.fa.add_transition('B', 'C', FiniteAutomation.epsilon)
        self.fa.add_transition('B', 'D', FiniteAutomation.epsilon)
        self.fa.add_transition('C', 'E', '1')
        self.fa.add_transition('D', 'F', '0')
        self.fa.add_transition('E', 'G', FiniteAutomation.epsilon)
        self.fa.add_transition('F', 'G', FiniteAutomation.epsilon)
        self.fa.add_transition('G', 'H', FiniteAutomation.epsilon)
        self.fa.add_transition('H', 'I', FiniteAutomation.epsilon)
        self.fa.add_transition('I', 'J', '1')
        self.fa.add_transition('G', 'A', FiniteAutomation.epsilon)
        self.fa.add_transition('A', 'H', FiniteAutomation.epsilon)

        self.nfa = self.fa

    def test_eclosure(self):
        self.assertEqual(self.fa.get_e_closure('A'), set(['A', 'B', 'C', 'D', 'H', 'I']))

    def test_get_transition(self):
        self.assertEqual(self.fa.get_transition('C', '1'), set(['E', 'G', 'H', 'I', 'A', 'B', 'C', 'D']))

    def test_nfa2dfa(self):
        self.dfa = nfa2dfa(self.nfa)
        self.assertEqual(self.dfa.start_state, set(['A', 'B', 'C', 'D', 'H', 'I']))


if __name__ == '__main__':
    unittest.main()


