import streamlit as st
import pandas as pd
import altair as alt
import os

# ==========================================
# KONFIGURASI HALAMAN & PEMBACAAN DATA ASLI
# ==========================================
st.set_page_config(page_title="Dashboard Responden ShopeePay", layout="wide")

file_path = "Analisis Peran Visual Promo dan Batas Waktu dalam Mendorong Impulse Buying pada Pengguna ShopeePay (Jawaban).xlsx"

@st.cache_data
def load_data():
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        # Menghapus spasi liar di nama kolom
        df.columns = df.columns.str.strip()
        return df
    else:
        st.error(f"File '{file_path}' tidak ditemukan! Pastikan file sudah diunggah ke runtime Colab.")
        return None

df_raw = load_data()

if df_raw is not None:
    total_responden_asli = len(df_raw)

    # Identifikasi kolom secara dinamis berdasarkan indeks urutan untuk menghindari KeyError string
    col_usia = df_raw.columns[2]      # Kolom Usia
    col_instansi = df_raw.columns[3]  # Kolom Sekolah/Universitas
    col_gender = df_raw.columns[4]    # Kolom Jenis Kelamin
    col_freq = df_raw.columns[5]      # Kolom Frekuensi Penggunaan
    
    # Kolom Pertanyaan Grafik Batang
    col_g2 = df_raw.columns[6]   # Tampilan banner promo
    col_g3 = df_raw.columns[11]  # Promo waktu terbatas
    col_g4 = df_raw.columns[23]  # Checkout karena tergiur promo
    col_g5 = df_raw.columns[8]   # Informasi diskon/promo yang jelas

    # Standardisasi nama UNJ dan UI untuk mempermudah filterisasi data yang seragam
    def benerin_unj(x):
        x_str = str(x).strip().lower()
        if 'negeri jakarta' in x_str or x_str == 'unj':
            return 'Universitas Negeri Jakarta (UNJ)'
        elif 'indonesia' in x_str or x_str == 'ui':
            return 'Universitas Indonesia (UI)'
        return str(x).strip()

    df_raw['Instansi_Clean'] = df_raw[col_instansi].apply(benerin_unj)

    # ==========================================
    # WIDGETS SIDEBAR INTERAKTIF (4 FILTER)
    # ==========================================
    st.sidebar.header("⚙️ Filterisasi Demografi Responden")
    
    # 1. Filter Jenis Kelamin
    list_gender = ["Semua"] + sorted(df_raw[col_gender].dropna().unique().tolist())
    gender_select = st.sidebar.selectbox("Jenis Kelamin:", list_gender)
    
    # 2. Filter Usia
    list_usia = ["Semua"] + sorted(df_raw[col_usia].dropna().unique().tolist())
    usia_select = st.sidebar.selectbox("Kategori Usia:", list_usia)
    
    # 3. Filter Frekuensi Penggunaan
    list_freq = ["Semua"] + sorted(df_raw[col_freq].dropna().unique().tolist())
    freq_select = st.sidebar.selectbox("Frekuensi Penggunaan:", list_freq)

    # 4. BARU: Filter Asal Instansi Sekolah / Universitas
    list_instansi = ["Semua"] + sorted(df_raw['Instansi_Clean'].dropna().unique().tolist())
    instansi_select = st.sidebar.selectbox("Asal Sekolah / Universitas:", list_instansi)

    # Proses Filtering Data Aktual (Saling Silang)
    df_filtered = df_raw.copy()
    if gender_select != "Semua":
        df_filtered = df_filtered[df_filtered[col_gender] == gender_select]
    if usia_select != "Semua":
        df_filtered = df_filtered[df_filtered[col_usia] == usia_select]
    if freq_select != "Semua":
        df_filtered = df_filtered[df_filtered[col_freq] == freq_select]
    if instansi_select != "Semua":
        df_filtered = df_filtered[df_filtered['Instansi_Clean'] == instansi_select]

    # Info Jumlah Data yang Tersaring
    st.sidebar.markdown("---")
    st.sidebar.metric(label="Sampel Terfilter / Total", value=f"{len(df_filtered)} / {total_responden_asli} Responden")

    st.title("📊 Dashboard Hasil Survei & Analisis Tren ShopeePay")
    
    tab1, tab2 = st.tabs(["📈 Grafik Distribusi Jawaban", "💡 Identifikasi Tren & Korelasi"])

    # ==========================================
    # TAB 1: GRAFIK DISTRIBUSI JAWABAN (NATIVE)
    # ==========================================
    with tab1:
        st.header("Karakteristik & Distribusi Data Kuesioner (Real-time)")
        
        if len(df_filtered) == 0:
            st.warning("Tidak ada data responden yang cocok dengan kombinasi filter demografi di sidebar.")
        else:
            # --- DEMOGRAFI USIA ---
            st.subheader("1. Demografi Responden Berdasarkan Usia")
            usia_counts = df_filtered[col_usia].value_counts(normalize=True) * 100
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Usia 18-22 Tahun", value=f"{usia_counts.get('18-22 Tahun', 0.0):.1f}%")
            with m2:
                st.metric(label="Usia < 18 Tahun", value=f"{usia_counts.get('< 18 Tahun', 0.0):.1f}%")
            with m3:
                st.metric(label="Usia > 27 Tahun", value=f"{usia_counts.get('> 27 Tahun', 0.0):.1f}%")
                
            st.markdown("---")

            # --- FREKUENSI PENGGUNAAN SHOPEEPAY ---
            st.subheader("2. Frekuensi Penggunaan Aplikasi ShopeePay")
            freq_counts = df_filtered[col_freq].value_counts(normalize=True).reset_index()
            freq_counts.columns = ['Kategori Frekuensi', 'Persentase']
            freq_counts['Persentase'] = freq_counts['Persentase'] * 100
            
            chart_frekuensi = alt.Chart(freq_counts).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Persentase", type="quantitative"),
                color=alt.Color(field="Kategori Frekuensi", type="nominal", 
                                scale=alt.Scale(range=['#221150', '#601a80', '#953280', '#d34873'])),
                tooltip=['Kategori Frekuensi', alt.Tooltip('Persentase', format='.1f', title='Persentase (%)')]
            ).properties(width=300, height=220)
            
            st.altair_chart(chart_frekuensi, use_container_width=True)

            st.markdown("---")
                
            # --- DEMOGRAFI SEKOLAH/UNIVERSITAS ---
            st.subheader("3. Demografi Responden Berdasarkan Asal Instansi")
            instansi_counts = df_filtered['Instansi_Clean'].value_counts(normalize=True) * 100
            
            mu1, mu2, mu3 = st.columns(3)
            with mu1:
                val_unj = instansi_counts.get('Universitas Negeri Jakarta (UNJ)', 0.0)
                st.metric(label="Universitas Negeri Jakarta (UNJ)", value=f"{val_unj:.1f}%")
            with mu2:
                val_ui = instansi_counts.get('Universitas Indonesia (UI)', 0.0)
                st.metric(label="Universitas Indonesia (UI)", value=f"{val_ui:.1f}%")
            with mu3:
                val_lain = 100.0 - val_unj - val_ui
                st.metric(label="Gabungan Instansi Lain", value=f"{max(0.0, val_lain):.1f}%")
            
            with st.expander("🔍 Tampilkan Rincian Lengkap Instansi Lain"):
                df_lainnya = df_filtered[~df_filtered['Instansi_Clean'].isin(['Universitas Negeri Jakarta (UNJ)', 'Universitas Indonesia (UI)'])]
                if len(df_lainnya) > 0:
                    counts_lainnya = df_lainnya['Instansi_Clean'].value_counts(normalize=True) * val_lain
                    c_list1, c_list2 = st.columns(2)
                    list_items = [(idx, row) for idx, row in counts_lainnya.items()]
                    half = (len(list_items) + 1) // 2
                    
                    with c_list1:
                        for inst, prs in list_items[:half]:
                            st.write(f"* {inst} — **{prs:.1f}%**")
                    with c_list2:
                        for inst, prs in list_items[half:]:
                            st.write(f"* {inst} — **{prs:.1f}%**")
                else:
                    st.write("*Tidak ada instansi lain dalam filter ini.*")
                    
            st.markdown("---")
            
            # --- DEMOGRAFI JENIS KELAMIN ---
            st.subheader("4. Demografi Responden Berdasarkan Gender")
            gender_counts = df_filtered[col_gender].value_counts(normalize=True).reset_index()
            gender_counts.columns = ['Gender', 'Persentase']
            gender_counts['Persentase'] = gender_counts['Persentase'] * 100
            
            chart_pie = alt.Chart(gender_counts).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Persentase", type="quantitative"),
                color=alt.Color(field="Gender", type="nominal", scale=alt.Scale(range=['#a1c9f4', '#ffb482'])),
                tooltip=['Gender', alt.Tooltip('Persentase', format='.1f', title='Persentase (%)')]
            ).properties(width=260, height=200)
            
            st.altair_chart(chart_pie, use_container_width=True)
                
            st.markdown("---")

            # FUNGSI MEMBUAT BAR CHART BERDASARKAN OBJEK KOLOM ASLI
            def buat_bar_chart(kolom_obj, judul_grafik, warna_bar):
                counts = df_filtered[kolom_obj].value_counts()
                counts = counts.reindex([1, 2, 3, 4, 5], fill_value=0)
                df_bar = pd.DataFrame({'Jumlah Responden': counts.values}, index=['Skala 1', 'Skala 2', 'Skala 3', 'Skala 4', 'Skala 5'])
                st.subheader(judul_grafik)
                st.bar_chart(df_bar, color=warna_bar)

            # Render semua grafik batang
            buat_bar_chart(col_g2, f"5. {col_g2}", "#399579")
            st.markdown("---")
            buat_bar_chart(col_g3, f"6. {col_g3}", "#4ca679")
            st.markdown("---")
            buat_bar_chart(col_g4, f"7. {col_g4}", "#3d7181")
            st.markdown("---")
            buat_bar_chart(col_g5, f"8. {col_g5}", "#82c068")

    # ==========================================
    # TAB 2: IDENTIFIKASI TREN DAN KORELASI
    # ==========================================
    with tab2:
        st.header("💡 Identifikasi Tren & Analisis Korelasi")
        
        st.markdown("""
        Analisis ini bertujuan untuk melihat keterkaitan antara desain visual (banner), faktor psikologis (waktu terbatas & kejelasan informasi), terhadap perilaku nyata konsumen (minat beli & *impulsive checkout*) pada penggunaan ShopeePay.
        """)

        st.subheader("1. Hubungan Desain Visual (Banner) dengan Minat Transaksi")
        st.info("""
        **Analisis Korelasi:** Terdapat korelasi positif yang kuat antara aspek visual banner dan kejelasan informasi promo. Responden menilai bahwa banner ShopeePay tidak hanya menarik perhatian secara visual, tetapi juga berhasil menyampaikan informasi promo dengan jelas. Gabungan antara visual yang menarik dan informasi yang mudah dipahami ini menjadi stimulus utama yang berhasil menggerakkan minat beli konsumen.
        """)

        st.subheader("2. Strategi Scarcity (Waktu Terbatas) vs Perilaku Impulsive Buying")
        st.warning("""
        **Analisis Korelasi:** Ada kecenderungan korelasi psikologis yang menarik di sini. Strategi *limitation* atau promo batas waktu menciptakan efek *Fear of Missing Out* (FOMO). Efek mendesak ini berbanding lurus dengan tingginya angka *impulsive checkout*. Konsumen merasa harus segera bertransaksi demi mengejar promo, meskipun produk tersebut sebenarnya tidak terlalu mereka butuhkan.
        """)

        st.subheader("3. Karakteristik Responden Berdasarkan Demografi")
        st.success("""
        **Analisis Korelasi:** Profil demografi responden sangat terfokus pada segmen mahasiswa aktif berumur **18-22 tahun** dengan basis sebaran utama berasal dari **Universitas Negeri Jakarta (UNJ)**. Sebagai bagian dari Gen Z yang tumbuh di lingkungan serbadigital, kelompok ini terbukti sangat peka terhadap elemen visual aplikasi dan penawaran instan (*voucher/cashback*). Dominasi kelompok mahasiswa ini menjelaskan mengapa variabel psikologis seperti ketakutan kehilangan promo (*scarcity*) memiliki pengaruh yang begitu kuat terhadap pola konsumsi mereka yang cenderung impulsif.
        """)

        st.subheader("📌 Kesimpulan Tren Utama (Summary)")
        st.markdown("""
        Dari keseluruhan data, dapat ditarik kesimpulan alur perilaku konsumen (*consumer journey*) sebagai berikut:

        1. **Daya Tarik Awal:** `Banner Menarik` + `Informasi Jelas` ➡️ **Memicu Minat Transaksi**
        2. **Dorongan Transaksi:** `Didesak Waktu Terbatas` ➡️ **Mendorong Checkout Impulsif / Non-Kebutuhan**

        Secara keseluruhan, responden dalam survei ini memiliki karakteristik **'Promo-Driven Consumers'** (konsumen yang sangat digerakkan oleh insentif promo). Penjualan/transaksi ShopeePay berhasil didongkrak bukan karena kebutuhan riil konsumen, melainkan karena efektivitas komunikasi visual banner dan manipulasi urgensi waktu promo.
        """)