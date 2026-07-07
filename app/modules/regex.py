class State:
    _id = 0
    @classmethod
    def reset_id(cls):
        cls._id = 0
    def __init__(self):
        self.name = f"q{State._id}"
        State._id += 1

class NFA:
    def __init__(self, start_state, final_state):
        self.start = start_state
        self.final = final_state
        self.transitions = [] # list of (src, symbol, dest)

def insert_explicit_concat(regex):
    """Menambahkan operator titik (.) untuk konkatensi eksplisit agar mudah di-parsing."""
    res = []
    for i in range(len(regex)):
        c1 = regex[i]
        res.append(c1)
        if i + 1 < len(regex):
            c2 = regex[i+1]
            if c1 not in '(|' and c2 not in ')|*':
                res.append('.')
    return "".join(res)

def infix_to_postfix(regex):
    """Mengubah format infix (a.b) ke postfix (ab.) menggunakan shunting-yard."""
    precedence = {'*': 3, '.': 2, '|': 1}
    output = []
    stack = []
    for char in regex:
        if char.isalnum() or char == 'ε':
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() # hapus '('
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return "".join(output)

def thompson_regex_to_nfa(regex_input):
    """Fungsi utama: Mengubah Regex string menjadi dictionary NFA."""
    State.reset_id()
    if not regex_input:
        return [], {}, "", []
        
    regex_concat = insert_explicit_concat(regex_input)
    postfix = infix_to_postfix(regex_concat)
    stack = []

    for char in postfix:
        if char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            # Sambungkan final state NFA1 ke start state NFA2 dengan epsilon
            transitions = nfa1.transitions + nfa2.transitions
            transitions.append((nfa1.final.name, 'ε', nfa2.start.name))
            stack.append(NFA(nfa1.start, nfa2.final))
            
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            final = State()
            transitions = nfa1.transitions + nfa2.transitions
            transitions.append((start.name, 'ε', nfa1.start.name))
            transitions.append((start.name, 'ε', nfa2.start.name))
            transitions.append((nfa1.final.name, 'ε', final.name))
            transitions.append((nfa2.final.name, 'ε', final.name))
            nfa = NFA(start, final)
            nfa.transitions = transitions
            stack.append(nfa)
            
        elif char == '*':
            nfa1 = stack.pop()
            start = State()
            final = State()
            transitions = nfa1.transitions
            transitions.append((start.name, 'ε', nfa1.start.name))
            transitions.append((start.name, 'ε', final.name))
            transitions.append((nfa1.final.name, 'ε', nfa1.start.name))
            transitions.append((nfa1.final.name, 'ε', final.name))
            nfa = NFA(start, final)
            nfa.transitions = transitions
            stack.append(nfa)
            
        else: # Karakter biasa (alfabet)
            start = State()
            final = State()
            nfa = NFA(start, final)
            nfa.transitions = [(start.name, char, final.name)]
            stack.append(nfa)

    final_nfa = stack.pop()
    
    # Format output agar sesuai dengan fungsi visualizer Graphviz
    states_set = set()
    trans_dict = {}
    for src, sym, dest in final_nfa.transitions:
        states_set.add(src)
        states_set.add(dest)
        key = (src, sym)
        if key not in trans_dict:
            trans_dict[key] = []
        trans_dict[key].append(dest)

    states = sorted(list(states_set), key=lambda x: int(x[1:]))
    start_state = final_nfa.start.name
    final_states = [final_nfa.final.name]
    
    return states, trans_dict, start_state, final_states

def nfa_to_regular_grammar(states, transitions, start_state, final_states):
    """Mengubah NFA menjadi Right-Linear Regular Grammar."""
    grammar = {}
    
    for state in states:
        grammar[state] = []
        
    for (src, sym), dests in transitions.items():
        if isinstance(dests, str):
            dests = [dests]
            
        for dest in dests:
            # A -> aB
            grammar[src].append(f"{sym} {dest}")
            
    # Tambahkan epsilon untuk state final (A -> ε)
    for state in final_states:
        if state in grammar:
            grammar[state].append("ε")
        else:
            grammar[state] = ["ε"]
            
    # Hapus array kosong
    grammar = {k: v for k, v in grammar.items() if v}
    return grammar