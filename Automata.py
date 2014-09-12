__author__ = 'XinYu'

from graphviz import Digraph
from copy import deepcopy


class FiniteAutomation(object):
    epsilon = u"\u03B5"

    def __init__(self):
        self.start_state = None
        self.states = set()
        self.finish_states = set()
        self.language = set()
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

    def get_single_transition(self, state, char):
        if self.transition_fn.has_key(state) and self.transition_fn[state].has_key(char):
            for s in self.transition_fn[state][char]:
                return s
        else:
            return None

    @staticmethod
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
        dfa = FiniteAutomation()
        dfa.set_start_state(nfa.get_e_closure(nfa.start_state))

        states = set([dfa.start_state])
        marked = set()

        while len(states) > 0:
            state = states.pop()
            for s in nfa.language:
                new_state = nfa.get_transition_r(state, s)
                if len(new_state) > 0:
                    dfa.add_transition(state, new_state, s)
                    if new_state not in marked:
                        states.add(new_state)

            marked.add(state)

            if NFA2DFA.is_finish_state(state, nfa):
                dfa.add_finish_state(state)

        return NFA2DFA.minimalDFA(dfa)

    @staticmethod
    def is_finish_state(states, nfa):
        return len(states.intersection(nfa.finish_states)) > 0

    @staticmethod
    def minimalDFA(dfa):
        P = set()
        Q = set([frozenset(dfa.finish_states), frozenset(dfa.states.difference(dfa.finish_states))])

        # 1.get subset combination
        while P != Q:
            P = Q
            Q = set()
            for p in P:
                Q = set.union(NFA2DFA.split(p, P, dfa), Q)
        # 2.build reversed dict
        reversed_dict = {}
        for states in P:
            for state in states:
                reversed_dict[state] = states

        # 3.connect states
        minimal_dfa = FiniteAutomation()

        for from_state in dfa.transition:
            for to_state in dfa.transition[from_state]:
                for c in dfa.transition[from_state][to_state]:
                    minimal_dfa.add_transition(reversed_dict[from_state], reversed_dict[to_state], c)

        # 4.set start and finish states
        minimal_dfa.set_start_state(reversed_dict[dfa.start_state])

        for finish_states in dfa.finish_states:
            minimal_dfa.add_finish_state(reversed_dict[finish_states])

        return minimal_dfa


    @staticmethod
    def split(p, P, dfa):
        subdict = {frozenset(): set()}
        reverse_dict = {}

        # 1.building reverse dict for classify
        for states in P:
            for state in states:
                reverse_dict[state] = frozenset(states)

        # 2.build subdict for get result
        for states in P:
            subdict[frozenset(states)] = set()

        # 3.real split set here
        for c in dfa.language:
            result_state_list = []
            for state in p:
                result_state_list.append(dfa.get_single_transition(state, c))

            for index, item in enumerate(result_state_list):
                if item:
                    result_state_list[index] = reverse_dict[item]
                else:
                    result_state_list[index] = item

            # here we need split
            if len(set(result_state_list)) > 1:
                transition_kv = zip(p, result_state_list)

                for (k, v) in transition_kv:
                    if v:
                        subdict[v].add(k)
                    else:
                        subdict[frozenset()].add(k)
                return set([frozenset(x) for x in subdict.values() if len(x) > 0])

        return set([frozenset(p)])


def char2nfa(c):
    nfa = FiniteAutomation()
    nfa.set_start_state('s0')
    nfa.add_finish_state('s1')
    nfa.add_transition('s0', 's1', c)

    return nfa


class NFABuilder(object):
    @staticmethod
    def concatentation(nfa_a, nfa_b):
        nfa = FiniteAutomation()
        uniq_dict = NFABuilder.gen_uniq_dict(nfa_a, nfa_b)
        NFABuilder.init_states(nfa_a, nfa_b, uniq_dict, nfa)

        nfa.set_start_state(uniq_dict['a'][nfa_a.start_state])

        for finish_state in nfa_b.finish_states:
            nfa.add_finish_state(uniq_dict['b'][finish_state])

        for finish_state in nfa_a.finish_states:
            nfa.add_transition(uniq_dict['a'][finish_state], uniq_dict['b'][nfa_b.start_state], FiniteAutomation.epsilon)

        return nfa


    @staticmethod
    def alternation(nfa_a, nfa_b):
        nfa = FiniteAutomation()
        uniq_dict = NFABuilder.gen_uniq_dict(nfa_a, nfa_b)
        NFABuilder.init_states(nfa_a, nfa_b, uniq_dict, nfa)

        new_start_state = len(nfa.states) + 1
        new_finish_state = len(nfa.states) + 2

        nfa.set_start_state(new_start_state)
        nfa.add_finish_state(new_finish_state)

        nfa.add_transition(new_start_state, uniq_dict['a'][nfa_a.start_state], FiniteAutomation.epsilon)
        nfa.add_transition(new_start_state, uniq_dict['b'][nfa_b.start_state], FiniteAutomation.epsilon)

        for finish_state in nfa_a.finish_states:
            nfa.add_transition(uniq_dict['a'][finish_state], new_finish_state, FiniteAutomation.epsilon)

        for finish_state in nfa_b.finish_states:
            nfa.add_transition(uniq_dict['b'][finish_state], new_finish_state, FiniteAutomation.epsilon)

        return nfa

    @staticmethod
    def closure(nfa_a):
        nfa = deepcopy(nfa_a)

        new_start_state = len(nfa.states) + 1
        new_finish_state = len(nfa.states) + 2

        nfa.add_transition(new_start_state, nfa_a.start_state, FiniteAutomation.epsilon)
        for finish_state in nfa.finish_states:
            nfa.add_transition(finish_state, new_finish_state, FiniteAutomation.epsilon)
            nfa.add_transition(finish_state, nfa.start_state, FiniteAutomation.epsilon)

        nfa.add_transition(new_start_state, new_finish_state, FiniteAutomation.epsilon)

        nfa.start_state = set()
        nfa.finish_states = set()

        nfa.set_start_state(new_start_state)
        nfa.add_finish_state(new_finish_state)

        return nfa




    @staticmethod
    def gen_uniq_dict(nfa_a, nfa_b):
        return_dict = {'a': {},'b': {} }

        for state in nfa_a.states:
            return_dict['a'][state] = len(return_dict['a'])

        for state in nfa_b.states:
            return_dict['b'][state] = len(return_dict['a']) + len(return_dict['b'])


        return return_dict

    @staticmethod
    def init_states(nfa_a, nfa_b, uniq_dict, nfa):
        for from_state in nfa_a.transition:
            for to_state in nfa_a.transition[from_state]:
                for c in nfa_a.transition[from_state][to_state]:
                    nfa.add_transition(uniq_dict['a'][from_state], uniq_dict['a'][to_state], c)

        for from_state in nfa_b.transition:
            for to_state in nfa_b.transition[from_state]:
                for c in nfa_b.transition[from_state][to_state]:
                    nfa.add_transition(uniq_dict['b'][from_state], uniq_dict['b'][to_state], c)



class Lexer(object):
    def __init__(self, dfa, stream):
        self.dfa = dfa
        self.stream = stream
        self.buf = ""
        self.input_pos = 0
        self.fail_dict = {}
        for state in self.dfa.states:
            if state not in self.fail_dict:
                self.fail_dict[state] = {}
            for pos in xrange(1,len(self.stream)+1):
                self.fail_dict[state][pos] = False


    def get_char_from_buffer(self):
        c = self.buf[-1]
        self.buf = self.buf[:-1]
        return c, not (len(self.stream) + len(self.buf))

    def get_char_from_stream(self):
        c = self.stream[0]
        self.stream = self.stream[1:]
        return c, not (len(self.stream) + len(self.buf))

    def get_char(self):
        if len(self.buf) > 0:
            return self.get_char_from_buffer()
        else:
            return self.get_char_from_stream()

    def get_token(self):

        # 1.init state, stack, lexeme
        state_stack = []
        lexeme = ""
        state = self.dfa.start_state
        bad_state = frozenset([])
        state_stack.append(bad_state)

        is_last = not (len(self.stream) + len(self.buf))
        # 2.loop and transition until error
        while state != None and not is_last:
            c, is_last = self.get_char()
            lexeme += c
            if state in self.dfa.finish_states:
                state_stack = []
            state_stack.append(state)

            state = self.dfa.get_single_transition(state, c)

        # 3.rollback until a finish state
        while state not in self.dfa.finish_states and state != bad_state:
            state = state_stack.pop()
            if len(lexeme) > 0 :
                self.buf += lexeme[-1]
                lexeme = lexeme[:-1]

        # 4.return lexeme and token
        if state in self.dfa.finish_states:
            return (lexeme, True)
        else:
            return (None, False)

    def get_token_optimazed(self):
        stack = []
        lexeme = ""
        state = self.dfa.start_state
        bad_state = frozenset([])
        stack.append((bad_state, self.input_pos))

        is_last = not (len(self.stream) + len(self.buf))

        while state != None and not is_last:
            c, is_last = self.get_char()
            self.input_pos += 1
            lexeme += c
            if self.fail_dict[state][self.input_pos]:
                break
            if state in self.dfa.finish_states:
                stack = []
            stack.append((state, self.input_pos))
            state = self.dfa.get_single_transition(state, c)

        while state not in self.dfa.finish_states and state != bad_state:
            if state:
                self.fail_dict[state][self.input_pos] = True
            (state, _) = stack.pop()
            self.input_pos -= 1

            if len(lexeme) > 0 :
                self.buf += lexeme[-1]
                lexeme = lexeme[:-1]

        if state in self.dfa.finish_states:
            return (lexeme, True)
        else:
            return (None, False)

