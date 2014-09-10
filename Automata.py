__author__ = 'XinYu'

from graphviz import Digraph


class FiniteAutomation(object):
    epsilon = u"\u03B5"

    def __init__(self, language=set()):
        self.start_state = None
        self.states = set()
        self.finish_states = set()
        self.language = language
        self.transition = dict()
        self.transition_fn = dict()

    def set_start_state(self, state):
        self.start_state = state
        self.states.add(state)

    def add_finish_state(self, state):
        self.finish_states.add(state)
        self.states.add(state)

    def add_transition(self, from_state, to_state, char):
        if char != FiniteAutomation.epsilon:
            self.language.add(char)
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state not in self.transition:
            self.transition[from_state] = dict()
            self.transition[from_state][to_state] = set([char])
        else:
            if to_state in self.transition[from_state]:
                self.transition[from_state][to_state].add(char)
            else:
                self.transition[from_state][to_state] = set([char])

        if from_state not in self.transition_fn:
            self.transition_fn[from_state] = dict()
            self.transition_fn[from_state][char] = set([to_state])
        else:
            if char not in self.transition_fn[from_state]:
                self.transition_fn[from_state][char] = set([to_state])
            else:
                self.transition_fn[from_state][char].add(to_state)

    def get_e_closure(self, find_state):

        e_closure = set()
        states = set([find_state])
        marked = set()

        while len(states) != 0:
            from_state = states.pop()
            e_closure.add(from_state)

            if from_state in self.transition:
                for to_state in self.transition[from_state]:
                    if FiniteAutomation.epsilon in self.transition[from_state][to_state] and to_state not in marked:
                        states.add(to_state)
                        marked.add(to_state)

        return frozenset(e_closure)

    def get_transition(self, state, char):
        if self.transition_fn.has_key(state) and self.transition_fn[state].has_key(char):
            states = []
            for s in self.transition_fn[state][char]:
                states.append(self.get_e_closure(s))
            return frozenset.union(*states)
        else:
            return frozenset([])

    def get_transition_r(self, states, char):
        ret_states = []
        for state in states:
            ret_states.append(self.get_transition(state, char))
        if len(ret_states) > 0:
            return frozenset.union(*ret_states)
        else:
            return frozenset([])

    def sava_graph(self, filename):

        node_dict = {}
        node_reverse_dict = {}

        node_dict['s0'] = self.start_state
        node_reverse_dict[self.start_state] = 's0'

        states = self.states.difference(set([self.start_state]))

        for (state, state_index) in zip(states, xrange(1, len(states) + 1)):
            identifier = 's' + str(state_index)
            node_dict[identifier] = state
            node_reverse_dict[state] = identifier

        dot = Digraph(comment='FiniteAutomation', graph_attr={'rankdir': 'LR'})

        for state_x in self.transition:
            for state_y in self.transition[state_x]:
                for label in self.transition[state_x][state_y]:
                    dot.edge(node_reverse_dict[state_x],
                             node_reverse_dict[state_y],
                             label)

        for s in self.finish_states:
            dot.node(node_reverse_dict[s], _attributes={'shape': 'doublecircle'})
        dot.render(filename, view=True)


class NFA2DFA(object):
    def __call__(self, nfa):
        dfa = FiniteAutomation(nfa.language)
        dfa.set_start_state(nfa.get_e_closure(nfa.start_state))

        states = set([dfa.start_state])
        marked = set()

        while len(states) > 0:
            state = states.pop()
            for s in dfa.language:
                new_state = nfa.get_transition_r(state, s)
                if len(new_state) > 0:
                    dfa.add_transition(state, new_state, s)
                    if new_state not in marked:
                        states.add(new_state)

            marked.add(state)

            if NFA2DFA.is_finish_state(state, nfa):
                dfa.add_finish_state(state)

        return dfa

    @staticmethod
    def is_finish_state(states, nfa):
        return len(states.intersection(nfa.finish_states)) > 0

    @staticmethod
    def minimalDFA(dfa):
        P = set()
        Q = set([dfa.finish_states, dfa.states.difference(dfa.finish_states)])


