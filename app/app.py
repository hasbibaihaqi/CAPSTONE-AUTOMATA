import streamlit as st
import ast
import re

# Mengimpor modul-modul
from modules.fsa import simulate_dfa, convert_nfa_to_dfa, simulate_nfa, simulate_moore, simulate_mealy
from modules.regex import thompson_regex_to_nfa, nfa_to_regular_grammar
from modules.pda_cfg import parse_cfg_input, simulate_derivation_tree, pda_simulator
from modules.chomsky import convert_to_cnf_steps
from utils.visualizer import draw_fsa_graph, draw_moore_graph, draw_mealy_graph, draw_parse_tree, draw_chomsky_hierarchy

# Konfigurasi Halaman Web
st.set_page_config(page_title="Automata Capstone Project", layout="wide", page_icon="⚙️")

# Injeksi CSS Kustom untuk Animasi & Styling Premium
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Header Styling dengan Efek Gradien */
h1 {
    background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.2em;
    animation: fadeInDown 1s ease-out;
}

h2, h3 {
    color: #2b2b2b;
    animation: fadeIn 1.2s ease-in;
}

/* Animasi Fade In */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Styling Tab Content Container (Glassmorphism ringan) */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px 8px 0px 0px;
    padding: 10px 20px;
    border: none;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(78, 205, 196, 0.1);
    border-bottom: 3px solid #4ECDC4 !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(78, 205, 196, 0.2);
    transform: translateY(-2px);
}

/* Styling Tombol Primary dengan Animasi Hover & Pulse */
button[kind="primary"] {
    background: linear-gradient(135deg, #6e8efb, #a777e3);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    transition: all 0.4s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    background: linear-gradient(135deg, #a777e3, #6e8efb);
}

button[kind="primary"]:active {
    transform: translateY(1px);
}

/* Card efek bayangan untuk input kolom */
div[data-testid="column"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
    animation: fadeIn 1s ease-in-out;
    border: 1px solid #f0f0f0;
}

/* Mode Gelap (Dark Mode) overrides agar tetap bagus */
@media (prefers-color-scheme: dark) {
    h2, h3 { color: #f0f0f0; }
    div[data-testid="column"] {
        background: #1e1e1e;
        border: 1px solid #333;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
}

/* Responsivitas Layar HP (Mobile Responsiveness) */
@media screen and (max-width: 768px) {
    h1 {
        font-size: 1.8rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 12px;
        font-size: 0.9rem;
    }
    
    div[data-testid="column"] {
        padding: 10px;
        margin-bottom: 0.5rem;
    }
    
    /* Buat scroll menyamping untuk diagram graphviz agar tidak kepotong di HP */
    div[data-testid="stGraphVizChart"] > div {
        overflow-x: auto;
        max-width: 100%;
    }
    
    /* Tombol pada HP dibuat full-width (penuh) */
    button[kind="primary"] {
        width: 100%;
        padding: 0.8rem;
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("🎛️ Capstone Project: Teori Bahasa & Otomata")
st.markdown("<p style='text-align: center; color: gray; font-size: 1.1em; margin-bottom: 2rem;'>Aplikasi web terintegrasi untuk simulasi FSA, Regex, PDA/CFG, dan Hierarki Chomsky.</p>", unsafe_allow_html=True)
st.markdown("---")

# Membuat 4 Tab
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Finite State Automata", 
    "2. Regular Expression", 
    "3. PDA & CFG", 
    "4. Chomsky & CNF"
])

# ==========================================
# TAB 1: FSA
# ==========================================
with tab1:
    st.header("Simulator FSA & Mesin Moore/Mealy")
    
    mode = st.radio("Pilih Mode Operasi:", ["Simulasi Mesin (DFA/NFA)", "Konversi NFA ➔ DFA", "Mesin Moore", "Mesin Mealy"], horizontal=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Definisi Mesin")
        states_input = st.text_input("Himpunan State (pisahkan koma)", "q0, q1, q2")
        alphabet_input = st.text_input("Alfabet Input (pisahkan koma)", "0, 1")
        start_state = st.text_input("Start State", "q0")
        
        if mode in ["Simulasi Mesin (DFA/NFA)", "Konversi NFA ➔ DFA"]:
            final_states_input = st.text_input("Final State(s) (pisahkan koma)", "q2")
            st.write("Transisi `('state_asal', 'input'): 'state_tujuan'` atau list `['q1', 'q2']`")
            default_trans = "{('q0', '0'): ['q0', 'q1'], ('q0', '1'): 'q0', ('q1', '1'): 'q2'}"
            transitions_str = st.text_area("Transisi (Dictionary Python)", default_trans, height=150)
            
        else: # Moore or Mealy
            output_alphabet_input = st.text_input("Alfabet Output (pisahkan koma)", "A, B")
            st.write("Transisi `('state_asal', 'input'): 'state_tujuan'`")
            default_trans = "{('q0', '0'): 'q1', ('q0', '1'): 'q0', ('q1', '0'): 'q1', ('q1', '1'): 'q2', ('q2', '0'): 'q2', ('q2', '1'): 'q2'}"
            transitions_str = st.text_area("Transisi (Dictionary Python)", default_trans, height=100)
            
            st.write("Tabel Output")
            if mode == "Mesin Moore":
                st.info("Format: `'state': 'output'`")
                default_out = "{'q0': 'A', 'q1': 'A', 'q2': 'B'}"
            else:
                st.info("Format: `('state_asal', 'input'): 'output'`")
                default_out = "{('q0', '0'): 'A', ('q0', '1'): 'A', ('q1', '0'): 'A', ('q1', '1'): 'B', ('q2', '0'): 'B', ('q2', '1'): 'B'}"
                
            output_table_str = st.text_area("Output (Dictionary Python)", default_out, height=100)

        if mode != "Konversi NFA ➔ DFA":
            test_string = st.text_input("String untuk diuji", "001")
            
        btn_process = st.button("Jalankan Proses", type="primary")

    with col2:
        st.subheader("Visualisasi & Hasil")
        if btn_process:
            try:
                states = [s.strip() for s in states_input.split(',')]
                alphabet = [a.strip() for a in alphabet_input.split(',')]
                transitions = ast.literal_eval(transitions_str)
                
                if mode in ["Simulasi Mesin (DFA/NFA)", "Konversi NFA ➔ DFA"]:
                    final_states = [s.strip() for s in final_states_input.split(',')]
                
                if mode == "Simulasi Mesin (DFA/NFA)":
                    st.write("**Diagram Mesin Input:**")
                    graph = draw_fsa_graph(states, transitions, start_state, final_states)
                    st.graphviz_chart(graph)
                    
                    is_nfa = any(isinstance(v, list) or k[1] in ['ε', 'epsilon'] for k, v in transitions.items())
                    
                    if is_nfa:
                        is_acc, trace = simulate_nfa(transitions, start_state, final_states, test_string)
                    else:
                        is_acc, trace = simulate_dfa(transitions, start_state, final_states, test_string)
                        
                    if is_acc:
                        st.success(f"String '{test_string}' **ACCEPTED**")
                    else:
                        st.error(f"String '{test_string}' **REJECTED**")
                    st.write("**Trace Langkah:**", " ➔ ".join(trace))
                    
                elif mode == "Konversi NFA ➔ DFA":
                    st.write("**1. Diagram NFA Asli:**")
                    nfa_graph = draw_fsa_graph(states, transitions, start_state, final_states)
                    st.graphviz_chart(nfa_graph)
                    
                    n_states, n_trans, n_start, n_final = convert_nfa_to_dfa(
                        alphabet, transitions, start_state, final_states
                    )
                    
                    st.markdown("---")
                    st.write("**2. Diagram DFA Hasil Konversi:**")
                    dfa_graph = draw_fsa_graph(n_states, n_trans, n_start, n_final)
                    st.graphviz_chart(dfa_graph)
                    
                    with st.expander("Lihat Data DFA Baru"):
                        st.json({
                            "States": n_states,
                            "Start State": n_start,
                            "Final States": n_final,
                            "Transitions": {str(k): v for k, v in n_trans.items()}
                        })
                        
                elif mode == "Mesin Moore":
                    out_table = ast.literal_eval(output_table_str)
                    st.write("**Diagram Mesin Moore:**")
                    graph = draw_moore_graph(states, transitions, start_state, out_table)
                    st.graphviz_chart(graph)
                    
                    tr_states, tr_outs = simulate_moore(transitions, out_table, start_state, test_string)
                    st.success("Simulasi Selesai")
                    st.write("**Trace State:**", " ➔ ".join(tr_states))
                    st.write("**Trace Output:**", " ➔ ".join(tr_outs))
                    
                elif mode == "Mesin Mealy":
                    out_table = ast.literal_eval(output_table_str)
                    st.write("**Diagram Mesin Mealy:**")
                    graph = draw_mealy_graph(states, transitions, start_state, out_table)
                    st.graphviz_chart(graph)
                    
                    tr_states, tr_outs = simulate_mealy(transitions, out_table, start_state, test_string)
                    st.success("Simulasi Selesai")
                    st.write("**Trace State:**", " ➔ ".join(tr_states))
                    st.write("**Trace Output:**", " ➔ ".join(tr_outs))

            except Exception as e:
                st.error(f"Terjadi kesalahan format input: {e}")

# ==========================================
# TAB 2: REGULAR EXPRESSION
# ==========================================
with tab2:
    st.header("Regex ➔ NFA ➔ Regular Grammar")
    st.write("Mengonversi Regex ke NFA (Thompson) lalu menampilkan aturan grammar reguler, serta mencocokkan pola.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Input Regex & String")
        regex_input = st.text_input("Masukkan Regex", "a|b*")
        st.info("**Operator yang didukung:** \n* `|` (Union/ATAU)\n* `*` (Kleene Star/Perulangan)\n* `ab` (Konkatenasi implisit)\n* `( )` (Pengelompokan)")
        
        test_str_regex = st.text_input("String untuk dicocokkan", "bb")
        btn_regex = st.button("Generate & Evaluasi", type="primary")
        
    with col2:
        st.subheader("Hasil & Visualisasi")
        if btn_regex:
            try:
                # Generate NFA
                r_states, r_trans, r_start, r_final = thompson_regex_to_nfa(regex_input)
                
                # Visual NFA
                st.write("**Diagram NFA:**")
                graph = draw_fsa_graph(r_states, r_trans, r_start, r_final)
                st.graphviz_chart(graph)
                
                # Evaluasi String
                is_match, tr = simulate_nfa(r_trans, r_start, r_final, test_str_regex)
                if is_match:
                    st.success(f"String '{test_str_regex}' **COCOK (ACCEPTED)** dengan pola '{regex_input}'")
                else:
                    st.error(f"String '{test_str_regex}' **TIDAK COCOK (REJECTED)** dengan pola '{regex_input}'")
                    
                # Generate Regular Grammar
                grammar = nfa_to_regular_grammar(r_states, r_trans, r_start, r_final)
                st.markdown("---")
                st.write("**Aturan Produksi Regular Grammar (Right-Linear):**")
                for state, prods in grammar.items():
                    st.write(f"`{state} -> {' | '.join(prods)}`")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan parsing Regex: {e}")

# ==========================================
# TAB 3: PDA & CFG
# ==========================================
with tab3:
    st.header("Simulator PDA & Parse Tree CFG")
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Definisi Aturan")
        st.write("Gunakan `->` untuk produksi, dan `|` untuk alternatif. Gunakan `epsilon` atau `ε` untuk transisi kosong.")
        cfg_input = st.text_area(
            "Aturan CFG", 
            "S -> aSa | bSb | epsilon"
        )
        cfg_string = st.text_input("String untuk diproses", "abba")
        start_sym_input = st.text_input("Start Symbol", "S")
        
        btn_cfg = st.button("Jalankan Simulasi PDA & Derivasi", type="primary")
        
    with col2:
        if btn_cfg:
            rules_dict = parse_cfg_input(cfg_input)
            
            st.subheader("1. Pushdown Automata Stack Simulator (Top-Down)")
            is_pda_acc, pda_trace = pda_simulator(rules_dict, start_sym_input, cfg_string)
            if is_pda_acc:
                st.success(f"PDA: String '{cfg_string}' DITERIMA")
            else:
                st.error(f"PDA: String '{cfg_string}' DITOLAK (Stack Simulation Gagal/Buntu)")
                
            with st.expander("Lihat Stack Trace (Simulasi Sederhana)"):
                for t in pda_trace:
                    st.text(t)
            
            st.markdown("---")
            st.subheader("2. Leftmost Derivation & Parse Tree")
            is_success, der_trace, tree_struct = simulate_derivation_tree(start_sym_input, rules_dict, cfg_string)
            
            if is_success:
                st.success("Derivasi berhasil ditemukan!")
                st.write("**Jejak Derivasi:**", " ➔ ".join(der_trace))
                
                if tree_struct:
                    st.write("**Parse Tree:**")
                    p_graph = draw_parse_tree(tree_struct)
                    st.graphviz_chart(p_graph)
            else:
                st.error("Gagal melakukan derivasi. (Mungkin string tidak dapat dibentuk oleh grammar atau timeout).")
                with st.expander("Alasan yang mungkin:"):
                    for msg in der_trace:
                        st.write(msg)

# ==========================================
# TAB 4: CHOMSKY & CNF
# ==========================================
with tab4:
    st.header("Hierarki Chomsky & Konversi CNF")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Konversi CFG ➔ CNF")
        cfg_to_cnf_input = st.text_area(
            "Masukkan CFG Sembarang", 
            "S -> aA | B\nA -> aA | epsilon\nB -> bB | c"
        )
        btn_cnf = st.button("Konversi ke CNF", type="primary")
        
        st.markdown("---")
        st.subheader("Visualisasi Hierarki Chomsky")
        btn_chomsky = st.button("Tampilkan Hierarki", type="secondary")
    
    with col2:
        if btn_cnf:
            st.write("### Langkah-langkah Transformasi ke Chomsky Normal Form")
            try:
                rules_dict = parse_cfg_input(cfg_to_cnf_input)
                steps = convert_to_cnf_steps(rules_dict)
                for title, output in steps:
                    st.markdown(f"**{title}**")
                    st.code(output, language="text")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses CFG: {e}")
                
        if btn_chomsky:
            st.write("### Diagram Hierarki Chomsky")
            c_graph = draw_chomsky_hierarchy()
            st.graphviz_chart(c_graph)
            st.info("Bahasa Reguler (Tipe 3) $\subset$ Context-Free (Tipe 2) $\subset$ Context-Sensitive (Tipe 1) $\subset$ Unrestricted (Tipe 0)")