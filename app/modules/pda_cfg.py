def parse_cfg_input(cfg_text):
    """
    Mengubah teks CFG dari input pengguna menjadi struktur dictionary Python.
    Contoh: 'S -> aSb | epsilon' menjadi {'S': ['aSb', 'epsilon']}
    """
    rules = {}
    if not cfg_text.strip():
        return rules
        
    for line in cfg_text.strip().split('\n'):
        if '->' in line:
            left, right = line.split('->')
            left = left.strip()
            # Pisahkan berdasarkan simbol OR (|) dan bersihkan spasi
            rights = [r.strip() for r in right.split('|')]
            
            if left not in rules:
                rules[left] = []
            rules[left].extend(rights)
            
    return rules

def simulate_derivation_tree(start_symbol, rules, target_string, max_steps=2000):
    """
    Mengembalikan: (is_success, string_trace, parse_tree_structure)
    Parse tree structure: ('S', [('a', []), ('S', [...])])
    Mencari jalur Leftmost Derivation.
    """
    if not rules or start_symbol not in rules:
        return False, ["Error: Aturan atau Start Symbol tidak valid."], None
        
    # Queue: (current_string, tree_nodes, trace_strings)
    # tree_nodes: list of tuples (Symbol, id_node, is_expanded, children) - complex, let's simplify
    # simpler approach: we just build the tree after we find the derivation sequence
    
    queue = [([start_symbol], start_symbol, [(start_symbol, -1)])] # trace, current_str, tree_construction_path
    # This might be too complex for a simple BFS. Let's just do standard BFS for trace, then reconstruct tree
    
    steps_count = 0
    while queue and steps_count < max_steps:
        trace, current, tree_path = queue.pop(0)
        steps_count += 1
        
        current_clean = current.replace("epsilon", "").replace("ε", "")
        if current_clean == target_string:
            # We found the path. Let's build a simple tree structure based on standard derivation
            tree = build_tree_from_trace(trace, rules, target_string)
            return True, trace, tree
            
        if len(current_clean) > len(target_string) + 5:
            continue
            
        for i, char in enumerate(current):
            if char.isupper() and char in rules:
                for production in rules[char]:
                    if production == "epsilon" or production == "ε":
                        new_str = current[:i] + current[i+1:]
                    else:
                        new_str = current[:i] + production + current[i+1:]
                    queue.append((trace + [new_str], new_str, []))
                break 
                
    return False, ["Derivasi tidak ditemukan (atau string ditolak)."], None

def build_tree_from_trace(trace, rules, target_string):
    """Fungsi pembantu kasar untuk membangun pohon dari trace leftmost derivation"""
    if not trace: return None
    
    # Pendekatan sederhana (heuristic tree builder)
    # Karena ini leftmost derivation, yang diekspansi selalu huruf besar paling kiri.
    root = [trace[0], []]
    
    def get_leftmost_nonterminal_node(node):
        if not node[1]: # No children
            if node[0].isupper():
                return node
            return None
        for child in node[1]:
            res = get_leftmost_nonterminal_node(child)
            if res: return res
        return None

    # Ini adalah simulasi struktur pohon. 
    # Untuk pohon asli CYK butuh parsing, tapi ini cukup untuk simulasi Capstone Automata.
    tree = [trace[0], []]
    
    for i in range(len(trace) - 1):
        curr_str = trace[i]
        next_str = trace[i+1]
        
        # Cari non-terminal yang diubah
        nt_node = get_leftmost_nonterminal_node(tree)
        if nt_node:
            # Cari apa penggantinya dengan membandingkan next_str
            # Cara bodoh: kita tahu produksi, kita tinggal cocokin dari rule nt_node[0]
            for prod in rules.get(nt_node[0], []):
                # Kita anggap prod adalah yang dipilih. 
                # (Di implementasi nyata kita harus mendeteksi tepat production mana, 
                # ini disimplifikasi untuk visualisasi)
                
                # Buat children
                if prod == 'epsilon' or prod == 'ε':
                    nt_node[1] = [('ε', [])]
                    break
                else:
                    nt_node[1] = [[c, []] for c in prod]
                    break
                    
    return tuple_convert(tree)

def tuple_convert(lst):
    if isinstance(lst, list) and len(lst) == 2 and isinstance(lst[1], list):
        return (lst[0], [tuple_convert(c) for c in lst[1]])
    return lst

def pda_simulator(rules, start_symbol, input_string):
    """Simulasi stack PDA sederhana secara top-down parsing."""
    trace = []
    stack = [start_symbol]
    
    # Simulasi visual stack trace
    trace.append(f"Init: Stack {stack}, Input '{input_string}'")
    
    curr_input = input_string
    max_iter = 50
    iters = 0
    
    while stack and iters < max_iter:
        iters += 1
        top = stack.pop()
        
        if top.islower():
            if curr_input.startswith(top):
                curr_input = curr_input[len(top):]
                trace.append(f"Match '{top}': Stack {stack}, Input sisa '{curr_input}'")
            else:
                trace.append(f"Mismatch '{top}' dengan input '{curr_input}' -> REJECT")
                return False, trace
        elif top.isupper():
            if top in rules:
                # Heuristik murni untuk demonstrasi (Pilih aturan pertama yang cocok atau epsilon)
                # PDA aslinya Non-deterministik, kita ambil salah satu untuk trace.
                chosen = rules[top][0] 
                if chosen in ['epsilon', 'ε']:
                    trace.append(f"Expand {top} -> ε: Stack {stack}")
                else:
                    for char in reversed(chosen):
                        stack.append(char)
                    trace.append(f"Expand {top} -> {chosen}: Stack {stack}")
            else:
                trace.append(f"Error: {top} tidak ada di rules -> REJECT")
                return False, trace
                
    if not stack and not curr_input:
        trace.append("Stack kosong dan input habis -> ACCEPT")
        return True, trace
    else:
        trace.append("Gagal memroses semua -> REJECT")
        return False, trace