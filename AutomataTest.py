__author__ = 'XinYu'

import unittest
from Automata import FiniteAutomation, NFA2DFA, char2nfa, NFABuilder


class TestAutomata(unittest.TestCase):

    def setUp(self):
        self.fa = FiniteAutomation()
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
        self.dfa = NFA2DFA()(self.nfa)
        FiniteAutomation.sava_graph(self.dfa, 'dfa_graph')

    def test_minimalDFA(self):
        self.dfa = FiniteAutomation()
        self.dfa.set_start_state('s0')
        self.dfa.add_transition('s0', 's1', 'f')
        self.dfa.add_transition('s1', 's2', 'e')
        self.dfa.add_transition('s1', 's4', 'i')
        self.dfa.add_transition('s2', 's3', 'e')
        self.dfa.add_transition('s4', 's5', 'e')

        self.dfa.add_finish_state('s3')
        self.dfa.add_finish_state('s5')

        minimal_dfa = NFA2DFA.minimalDFA(self.dfa)

        FiniteAutomation.sava_graph(self.dfa, 'beforeMinimal')
        FiniteAutomation.sava_graph(minimal_dfa, 'afterMinimal')

    def test_char2nfa(self):
        nfa = char2nfa('h')
        nfa.sava_graph('char2nfa')

    def test_NFABuilder(self):
        nfa_a = char2nfa('a')
        nfa_b = char2nfa('b')

        nfa_builder = NFABuilder()
        nfa_builder.gen_uniq_dict(nfa_a, nfa_b)

        nfa = nfa_builder.alternation(nfa_a, nfa_b)
        FiniteAutomation.sava_graph(nfa, 'alternation')

        dfa = NFA2DFA()(nfa)
        FiniteAutomation.sava_graph(dfa, 'minimal_alternation')

        nfa = nfa_builder.concatentation(nfa_a, nfa_b)
        FiniteAutomation.sava_graph(nfa, 'concatentation')

        dfa = NFA2DFA()(nfa)
        FiniteAutomation.sava_graph(dfa, 'minimal_concatentation')

        nfa = nfa_builder.closure(nfa_a)
        FiniteAutomation.sava_graph(nfa, 'closure')

        dfa = NFA2DFA()(nfa)
        FiniteAutomation.sava_graph(dfa, 'minimal_closure')




if __name__ == '__main__':
    unittest.main()


