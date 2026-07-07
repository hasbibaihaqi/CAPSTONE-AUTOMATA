import graphviz

def draw_fsa_graph(states, transitions, start_state, final_states):
    """Fungsi untuk menggambar diagram DFA/NFA"""
    dot = graphviz.Digraph(comment='FSA Simulation')
    dot.attr(rankdir='LR') # Kiri ke kanan
    
    # Render final state dengan lingkaran ganda
    for state in states:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')
            
    # Panah penunjuk start state
    dot.node('', shape='none', width='0', height='0')
    dot.edge('', start_state)
    
    # Render transisi
    for (src, symbol), dests in transitions.items():
        if isinstance(dests, list):
            for dest in dests:
                dot.edge(src, dest, label=symbol)
        else:
            dot.edge(src, dests, label=symbol)
            
    return dot

def draw_moore_graph(states, transitions, start_state, output_table):
    """Fungsi untuk menggambar Mesin Moore"""
    dot = graphviz.Digraph(comment='Moore Machine')
    dot.attr(rankdir='LR')
    
    for state in states:
        out_val = output_table.get(state, '')
        dot.node(state, label=f"{state} / {out_val}", shape='circle')
            
    dot.node('', shape='none', width='0', height='0')
    dot.edge('', start_state)
    
    for (src, symbol), dests in transitions.items():
        if isinstance(dests, list):
            for dest in dests:
                dot.edge(src, dest, label=symbol)
        else:
            dot.edge(src, dests, label=symbol)
            
    return dot

def draw_mealy_graph(states, transitions, start_state, output_table):
    """Fungsi untuk menggambar Mesin Mealy"""
    dot = graphviz.Digraph(comment='Mealy Machine')
    dot.attr(rankdir='LR')
    
    for state in states:
        dot.node(state, shape='circle')
            
    dot.node('', shape='none', width='0', height='0')
    dot.edge('', start_state)
    
    for (src, symbol), dests in transitions.items():
        out_val = output_table.get((src, symbol), '')
        edge_label = f"{symbol} / {out_val}"
        if isinstance(dests, list):
            for dest in dests:
                dot.edge(src, dest, label=edge_label)
        else:
            dot.edge(src, dests, label=edge_label)
            
    return dot

def draw_parse_tree(tree_node, counter=[0]):
    """
    Menggambar parse tree CFG. tree_node adalah tuple terstruktur: (Simbol, [Anak-anak...])
    Contoh: ('S', [('a', []), ('S', [('b', [])])])
    """
    dot = graphviz.Digraph(comment='Parse Tree')
    dot.attr(rankdir='TB') # Top to Bottom

    def traverse(node):
        my_id = f"n{counter[0]}"
        counter[0] += 1
        
        symbol = node[0]
        children = node[1]
        
        # Bedakan tampilan terminal dan non-terminal
        if not children: 
            dot.node(my_id, label=symbol, shape='none', fontcolor='blue')
        else:
            dot.node(my_id, label=symbol, shape='none', fontweight='bold')
            
        for child in children:
            child_id = traverse(child)
            dot.edge(my_id, child_id)
            
        return my_id
        
    if tree_node:
        traverse(tree_node)
        
    return dot

def draw_chomsky_hierarchy():
    """Menggambar diagram Venn / Tree Hierarki Chomsky"""
    dot = graphviz.Digraph(comment='Chomsky Hierarchy')
    dot.attr(rankdir='TB')
    
    dot.node('T0', 'Type 0: Unrestricted\n(Turing Machine)', shape='box', style='filled', fillcolor='#ffcccc')
    dot.node('T1', 'Type 1: Context-Sensitive\n(Linear Bounded Automaton)', shape='box', style='filled', fillcolor='#ffebcc')
    dot.node('T2', 'Type 2: Context-Free\n(Pushdown Automaton)', shape='box', style='filled', fillcolor='#ccffcc')
    dot.node('T3', 'Type 3: Regular\n(Finite State Automaton)', shape='box', style='filled', fillcolor='#cceeff')
    
    dot.edge('T0', 'T1', style='dashed', label='Subset')
    dot.edge('T1', 'T2', style='dashed', label='Subset')
    dot.edge('T2', 'T3', style='dashed', label='Subset')
    
    return dot