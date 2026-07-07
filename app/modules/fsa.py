def simulate_dfa(transitions, start_state, final_states, input_string):
    """Simulasi DFA dasar."""
    current_state = start_state
    trace = [current_state]
    
    for symbol in input_string:
        key = (current_state, symbol)
        if key in transitions:
            current_state = transitions[key]
            trace.append(current_state)
        else:
            trace.append("REJECT (Dead State)")
            return False, trace
            
    is_accepted = current_state in final_states
    return is_accepted, trace

def convert_nfa_to_dfa(alphabet, transitions, start_state, final_states):
    """
    Algoritma Subset Construction untuk mengubah NFA menjadi DFA.
    Mengelompokkan state NFA ke dalam himpunan (frozenset) untuk membuat state DFA baru.
    """
    # Gunakan frozenset agar himpunan state bisa dijadikan key dictionary
    start_subset = frozenset([start_state])
    unprocessed = [start_subset]
    dfa_states = set([start_subset])
    
    dfa_transitions_raw = {}
    dfa_final_states_raw = set()

    while unprocessed:
        current_subset = unprocessed.pop(0)
        
        # Jika subset mengandung salah satu final state NFA, maka subset ini adalah final state DFA
        if any(state in final_states for state in current_subset):
            dfa_final_states_raw.add(current_subset)

        for symbol in alphabet:
            next_subset = set()
            for state in current_subset:
                dests = transitions.get((state, symbol), [])
                if isinstance(dests, list):
                    next_subset.update(dests)
                else:
                    next_subset.add(dests)

            if next_subset:
                next_subset_frozen = frozenset(next_subset)
                dfa_transitions_raw[(current_subset, symbol)] = next_subset_frozen
                
                if next_subset_frozen not in dfa_states:
                    dfa_states.add(next_subset_frozen)
                    unprocessed.append(next_subset_frozen)

    # Merapikan output (Mengubah frozenset menjadi string agar mudah dibaca UI)
    def subset_to_str(subset):
        return "{" + ",".join(sorted(list(subset))) + "}"

    new_states = [subset_to_str(s) for s in dfa_states]
    new_start_state = subset_to_str(start_subset)
    new_final_states = [subset_to_str(s) for s in dfa_final_states_raw]
    
    new_transitions = {}
    for (src_subset, symbol), dest_subset in dfa_transitions_raw.items():
        new_transitions[(subset_to_str(src_subset), symbol)] = subset_to_str(dest_subset)

    return new_states, new_transitions, new_start_state, new_final_states

def get_epsilon_closure(states, transitions):
    """Menghitung epsilon closure untuk sekumpulan state NFA."""
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        dests = transitions.get((state, 'ε'), []) + transitions.get((state, 'epsilon'), [])
        if isinstance(dests, str):
            dests = [dests]
            
        for dest in dests:
            if dest not in closure:
                closure.add(dest)
                stack.append(dest)
                
    return closure

def simulate_nfa(transitions, start_state, final_states, input_string):
    """Simulasi NFA (mendukung epsilon dan multi-branching)."""
    current_states = get_epsilon_closure([start_state], transitions)
    trace = [", ".join(sorted(list(current_states))) if current_states else "Dead State"]
    
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            dests = transitions.get((state, symbol), [])
            if isinstance(dests, str):
                dests = [dests]
            next_states.update(dests)
            
        current_states = get_epsilon_closure(next_states, transitions)
        if not current_states:
            trace.append("REJECT (Dead State)")
            return False, trace
        trace.append(", ".join(sorted(list(current_states))))
        
    is_accepted = any(state in final_states for state in current_states)
    return is_accepted, trace

def simulate_moore(transitions, output_table, start_state, input_string):
    """Simulasi Mesin Moore."""
    current_state = start_state
    trace_states = [current_state]
    trace_outputs = [output_table.get(current_state, '')]
    
    for symbol in input_string:
        key = (current_state, symbol)
        if key in transitions:
            current_state = transitions[key]
            # Handle if transitions returns a list (should be a string for Moore but just in case)
            if isinstance(current_state, list):
                current_state = current_state[0]
                
            trace_states.append(current_state)
            trace_outputs.append(output_table.get(current_state, ''))
        else:
            trace_states.append("HALT")
            trace_outputs.append("-")
            break
            
    return trace_states, trace_outputs

def simulate_mealy(transitions, output_table, start_state, input_string):
    """Simulasi Mesin Mealy."""
    current_state = start_state
    trace_states = [current_state]
    trace_outputs = []
    
    for symbol in input_string:
        key = (current_state, symbol)
        if key in transitions:
            current_state = transitions[key]
            if isinstance(current_state, list):
                current_state = current_state[0]
                
            out_val = output_table.get(key, '')
            trace_states.append(current_state)
            trace_outputs.append(out_val)
        else:
            trace_states.append("HALT")
            trace_outputs.append("-")
            break
            
    return trace_states, trace_outputs