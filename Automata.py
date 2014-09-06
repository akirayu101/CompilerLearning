__author__ = 'XinYu'


class FiniteAutomation(object):

    epsilon = ':e:'

    def __init__(self, language=set()):
        self.start_states = None
        self.states = set()
        self.finish_states = []
        self.language = language
        self.transition = dict()
        self.transition_fn = dict()

    def set_start_state(self, state):
        self.start_states = state
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

        return e_closure

    def get_transition(self, state, char):
        return self.transition_fn[state][char]


def test_e_closure():
    fa = FiniteAutomation()
    fa.add_transition(1, 2, FiniteAutomation.epsilon)
    fa.add_transition(1, 3, FiniteAutomation.epsilon)
    fa.add_transition(2, 3, FiniteAutomation.epsilon)
    fa.add_transition(3, 1, FiniteAutomation.epsilon)
    fa.add_transition(3, 2, FiniteAutomation.epsilon)
    assert fa.get_e_closure(1) == set([1, 2, 3])


def test_transition():
    fa = FiniteAutomation()
    fa.add_transition(1, 2, FiniteAutomation.epsilon)
    fa.add_transition(1, 3, FiniteAutomation.epsilon)
    assert fa.get_transition(1, FiniteAutomation.epsilon) == set([3, 2])

