def format_rules(r_dict):
    res = []
    for k, v in r_dict.items():
        if v:
            res.append(f"{k} -> {' | '.join(v)}")
    return "\n".join(res) if res else "(Kosong)"

def get_nullables(rules):
    nullables = set()
    changed = True
    while changed:
        changed = False
        for k, prods in rules.items():
            if k in nullables:
                continue
            for p in prods:
                if p in ['epsilon', 'ε'] or all(c in nullables for c in p):
                    nullables.add(k)
                    changed = True
                    break
    return nullables

def remove_epsilon_productions(rules):
    nullables = get_nullables(rules)
    new_rules = {}
    
    def get_combinations(prod, nullables):
        from itertools import combinations
        # Find indices of nullable symbols
        indices = [i for i, char in enumerate(prod) if char in nullables]
        res = set([prod])
        
        for r in range(1, len(indices) + 1):
            for combo in combinations(indices, r):
                temp = list(prod)
                for idx in sorted(combo, reverse=True):
                    temp.pop(idx)
                if temp:
                    res.add("".join(temp))
        return list(res)

    for k, prods in rules.items():
        new_prods = set()
        for p in prods:
            if p not in ['epsilon', 'ε']:
                combos = get_combinations(p, nullables)
                new_prods.update(combos)
        if new_prods:
            new_rules[k] = list(new_prods)
            
    return new_rules, nullables

def remove_unit_productions(rules):
    new_rules = {k: list(v) for k, v in rules.items()}
    
    # Kumpulkan pasangan unit (A -> B)
    unit_pairs = []
    for k, prods in rules.items():
        for p in prods:
            if len(p) == 1 and p.isupper():
                unit_pairs.append((k, p))
                
    changed = True
    while changed:
        changed = False
        temp_pairs = list(unit_pairs)
        for (A, B) in temp_pairs:
            # Tambahkan produksi B ke A
            for b_prod in new_rules.get(B, []):
                if b_prod not in new_rules[A] and not (len(b_prod) == 1 and b_prod.isupper()):
                    new_rules[A].append(b_prod)
                    changed = True
            # Hapus unit production A -> B
            if B in new_rules[A]:
                new_rules[A].remove(B)
                changed = True
                
    # Bersihkan yang masih tertinggal (A -> A)
    for k in new_rules:
        new_rules[k] = [p for p in new_rules[k] if not (len(p) == 1 and p == k) and not (len(p) == 1 and p.isupper())]
        
    return new_rules

def convert_to_cnf(rules):
    """Konversi beneran ke CNF"""
    steps = []
    steps.append(("1. CFG Awal", format_rules(rules)))
    
    # 2. Hapus Epsilon
    rules, nullables = remove_epsilon_productions(rules)
    steps.append((f"2. Menghapus ε-production (Nullable: {', '.join(nullables)})", format_rules(rules)))
    
    # 3. Hapus Unit
    rules = remove_unit_productions(rules)
    steps.append(("3. Menghapus Unit Production", format_rules(rules)))
    
    # 4. Ganti terminal campur & pecah string panjang
    new_rules = {k: list(v) for k, v in rules.items()}
    var_counter = 1
    term_dict = {} # terminal -> Variable baru
    
    final_rules = {}
    
    for k, prods in new_rules.items():
        final_rules[k] = []
        for p in prods:
            if len(p) == 1:
                final_rules[k].append(p)
            else:
                # Ganti semua huruf kecil dengan variabel baru
                new_p = []
                for char in p:
                    if char.islower():
                        if char not in term_dict:
                            new_var = f"X{char.upper()}"
                            term_dict[char] = new_var
                            final_rules[new_var] = [char]
                        new_p.append(term_dict[char])
                    else:
                        new_p.append(char)
                
                # Pecah jadi biner (Chomsky Form: A -> BC)
                while len(new_p) > 2:
                    first = new_p.pop(0)
                    new_var = f"Y{var_counter}"
                    var_counter += 1
                    # Sisa ditaruh di variabel baru
                    final_rules[new_var] = ["".join(new_p)]
                    new_p = [new_var]
                    final_rules[k].append(f"{first}{new_var}")
                    
                if len(new_p) == 2:
                    final_rules[k].append(f"{new_p[0]}{new_p[1]}")
                elif len(new_p) == 1:
                    final_rules[k].append(new_p[0])
                    
    # Clean up duplikat
    for k in final_rules:
        final_rules[k] = list(set(final_rules[k]))

    steps.append(("4. Hasil Akhir CNF (Chomsky Normal Form)", format_rules(final_rules)))
    return steps

def convert_to_cnf_steps(rules):
    return convert_to_cnf(rules)