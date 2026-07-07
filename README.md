---
title: Capstone Automata
emoji: ⚙️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app/app.py
pinned: false
---

# Capstone Project: Teori Bahasa & Otomata

Aplikasi web terintegrasi untuk menyimulasikan berbagai konsep utama dalam **Teori Bahasa dan Otomata**. Proyek ini dibangun sebagai syarat pemenuhan tugas Capstone Automata.

## Deskripsi Proyek
Proyek ini berisi implementasi langsung dari empat konsep utama Otomata ke dalam sebuah antarmuka aplikasi web interaktif yang modern, responsif, dan mudah digunakan. Pengguna dapat merancang mesin otomata, memasukkan ekspresi reguler, mendefinisikan grammar (CFG), hingga melihat transformasi struktural ke *Chomsky Normal Form*.

## Tech Stack
- **Bahasa Pemrograman**: Python 3
- **Framework Web**: [Streamlit](https://streamlit.io/)
- **Visualisasi Grafis**: [Graphviz](https://graphviz.org/)

## Daftar Fitur Modul
Aplikasi ini terbagi menjadi 4 modul (tab) utama:

1. **Finite State Automata (FSA)**
   - Mendukung definisi State, Alphabet, dan Transisi untuk *Deterministic* maupun *Non-Deterministic* (DFA/NFA).
   - Fitur konversi algoritma struktural dari NFA menjadi DFA yang setara.
   - Simulasi *Acceptance/Rejection* string dengan visualisasi node *Trace*.
   - Menyertakan dukungan Mesin Moore dan Mesin Mealy (Visualisasi + Output Simulator).

2. **Regular Expression (Regex)**
   - Algoritma konstruksi **Thompson** untuk mengubah ekspresi reguler menjadi mesin NFA.
   - Pencocokan string langsung terhadap *Regex Pattern*.
   - Ekstraksi dan pembentukan aturan produksi **Regular Grammar** (Right-Linear).

3. **Pushdown Automata (PDA) & Context-Free Grammar (CFG)**
   - Simulator stack PDA berbasis *Top-Down Parsing*.
   - Pencarian rute derivasi *Leftmost Derivation*.
   - Penggambaran struktur pohon sintaksis (*Parse Tree*) secara hierarkis.

4. **Hierarki Chomsky & Chomsky Normal Form (CNF)**
   - Modul transformasi langkah demi langkah (Step-by-Step) dari CFG sembarang menjadi format baku CNF.
   - Menghilangkan *Epsilon/Nullable production*, *Unit production*, dan menyederhanakan produksi campuran/panjang.
   - Diagram grafis perbandingan kelas bahasa dalam bentuk *Chomsky Hierarchy*.

## Cara Instalasi Lokal
1. *Clone* repositori ini:
   ```bash
   git clone https://github.com/hasbibaihaqi/CAPSTONE-AUTOMATA.git
   cd CAPSTONE-AUTOMATA
   ```
2. Pastikan Python 3 dan Graphviz telah terinstall di OS Anda.
3. Install semua *dependencies*:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app/app.py
   ```

## Tautan / Referensi
- **Live Domain App**: [https://nama-domain-anda.my.id](https://nama-domain-anda.my.id) *(Contoh)*
- **Video Presentasi Demo (YouTube)**: [Tonton di Sini](https://youtube.com) *(Contoh)*
