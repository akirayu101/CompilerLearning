__author__ = 'XinYu'

import unittest
from Automata import FiniteAutomation, NFA2DFA


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
        self.fa.add_finish_state('J')

        self.nfa = self.fa

    def test_eclosure(self):
        self.assertEqual(self.fa.get_e_closure('A'),
                         set(['A', 'B', 'C', 'D', 'H', 'I']))
        self.assertEqual(self.fa.get_e_closure('G'),
                         set(['A', 'B', 'C', 'D', 'H', 'I', 'G']))
        self.assertEqual(self.fa.get_e_closure('B'),
                         set(['B', 'C', 'D']))

    def test_get_transition(self):
        self.assertEqual(self.fa.get_transition('C', '1'),
                         set(['E', 'G', 'H', 'I', 'A', 'B', 'C', 'D']))

    def test_get_transition_r(self):
        self.assertEqual(
            self.fa.get_transition_r(set(['A', 'B', 'C', 'D', 'H', 'I']), '0'),
            set(['F', 'G', 'H', 'I', 'A', 'B', 'C', 'D']))

    def test_nfa2dfa(self):
        self.nfa.sava_graph('nfa_graph')
        self.dfa = NFA2DFA()(self.nfa)
        self.assertEqual(self.dfa.start_state,
                         set(['A', 'B', 'C', 'D', 'H', 'I']))

        self.dfa.sava_graph('dfa_graph')


if __name__ == '__main__':
    unittest.main()


