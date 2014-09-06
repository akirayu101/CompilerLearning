__author__ = 'XinYu'


class FiniteAutomation(object):

    epsilon = ':e:'

    def __init__(self, language=set()):
        self.start_state = None
        self.states = set()
        self.finish_states = []
        self.language = language
        self.transition = dict()
        self.transition_fn = dict()

    def set_start_state(self, state):
        self.start_state = state
        self.states.add(state)

    def add_final_state(self, state):
        self.finish_states.append(state)
        self.states.add(state)

    def add_transition(self, from_state, to_state, char):
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state not in self.transition:
            self.transition[from_state] = dict()
            self.transition[from_state][to_state] = set([char])
        else:
            if to_state in self.transition[from_state]:
                self.transition[from_state][to_state] = self.transition[from_state][to_state].add(char)
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


def nfa2dfa(nfa):
    dfa = FiniteAutomation(nfa.language)
    dfa.set_start_state(nfa.get_e_closure(nfa.start_state))

    return dfa