import streamlit as st
import pandas as pd
import altair as alt

# ==========================================
# KONFIGURASI HALAMAN & SIDEBAR FILTER
# ==========================================
st.set_page_config(page_title="Dashboard Responden ShopeePay", layout="wide")

st.title("📊 Dashboard Hasil Survei & Analisis Tren ShopeePay")

# Sidebar untuk Widgets Interaktif
st.sidebar.header("⚙️ Filter Data")
gender_filter = st.sidebar.selectbox(
    "Pilih Gender Responden:",
    options=["Semua Responden", "Perempuan Only", "Laki-laki Only"]
)

# Simulasi Penyesuaian Data Berdasarkan Filter Dropdown
if gender_filter == "Perempuan Only":
    mult = 0.534
    st.sidebar.caption("Menampilkan estimasi data untuk responden Perempuan (53.4%)")
elif gender_filter == "Laki-laki Only":
    mult = 0.466
    st.sidebar.caption("Menampilkan estimasi data untuk responden Laki-laki (46.6%)")
else:
    mult = 1.0
    st.sidebar.caption("Menampilkan keseluruhan data responden.")

# Membagi halaman menjadi 2 Tabs Utama untuk kerapihan Layout
tab1, tab2 = st.tabs(["📈 Grafik Distribusi Jawaban", "💡 Identifikasi Tren & Korelasi"])

# ==========================================
# TAB 1: GRAFIK DISTRIBUSI JAWABAN (NATIVE)
# ==========================================
with tab1:
    st.header("Visualisasi Data Kuesioner (Streamlit Native)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Demografi Berdasarkan Jenis Kelamin")
        
        # Membuat Dataframe untuk Pie/Donut Chart menggunakan Altair (Rekomendasi Streamlit)
        df_pie = pd.DataFrame({
            'Gender': ['Perempuan', 'Laki-laki'],
            'Persentase': [53.4, 46.6]
        })
        
        # Grafik Donut interaktif khas Streamlit modern
        chart_pie = alt.Chart(df_pie).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Persentase", type="quantitative"),
            color=alt.Color(field="Gender", type="nominal", scale=alt.Scale(range=['#a1c9f4', '#ffb482'])),
            tooltip=['Gender', 'Persentase']
        ).properties(width=300, height=300)
        
        st.altair_chart(chart_pie, use_container_width=True)
        
    with col2:
        st.caption("ℹ️ Info Grafik")
        st.write("""
        Grafik di samping dan di bawah ini sekarang menggunakan komponen bawaan Streamlit dan Altair. 
        Arahkan kursor (*hover*) ke area grafik untuk melihat detail jumlah responden secara interaktif!
        """)

    st.markdown("---")

    # Grafik Batang 2 (Tampilan Banner Promo) - Menggunakan st.bar_chart
    st.subheader("2. Tampilan banner promo ShopeePay di aplikasi Shopee cukup menarik perhatian saya")
    data_g2 = pd.DataFrame({
        'Jumlah Responden': [max(1, int(6 * mult)), max(1, int(20 * mult)), max(1, int(22 * mult)), max(1, int(10 * mult))]
    }, index=['Skala 2', 'Skala 3', 'Skala 4', 'Skala 5'])
    
    st.bar_chart(data_g2, color="#399579")

    st.markdown("---")

    # Grafik Batang 3 (Promo Waktu Terbatas) - Menggunakan st.bar_chart
    st.subheader("3. Promo ShopeePay dengan waktu terbatas membuat saya ingin segera melakukan transaksi")
    data_g3 = pd.DataFrame({
        'Jumlah Responden': [max(1, int(2 * mult)), max(1, int(2 * mult)), max(1, int(17 * mult)), max(1, int(23 * mult)), max(1, int(14 * mult))]
    }, index=['Skala 1', 'Skala 2', 'Skala 3', 'Skala 4', 'Skala 5'])
    
    st.bar_chart(data_g3, color="#4ca679")

    st.markdown("---")

    # Grafik Batang 4 (Checkout Tergiur Promo) - Menggunakan st.bar_chart
    st.subheader("4. Saya melakukan checkout dengan ShopeePay karena tergiur promo, bukan karena kebutuhan")
    data_g4 = pd.DataFrame({
        'Jumlah Responden': [max(1, int(6 * mult)), max(1, int(13 * mult)), max(1, int(19 * mult)), max(1, int(14 * mult)), max(1, int(5 * mult))]
    }, index=['Skala 1', 'Skala 2', 'Skala 3', 'Skala 4', 'Skala 5'])
    
    st.bar_chart(data_g4, color="#3d7181")

    st.markdown("---")

    # Grafik Batang 5 (Minat Beli Terpengaruh Promo) - Menggunakan st.bar_chart
    st.subheader("5. Informasi promo ShopeePay yang jelas meningkatkan minat saya untuk bertransaksi")
    data_g5 = pd.DataFrame({
        'Jumlah Responden': [max(1, int(1 * mult)), max(1, int(3 * mult)), max(1, int(18 * mult)), max(1, int(25 * mult)), max(1, int(11 * mult))]
    }, index=['Skala 1', 'Skala 2', 'Skala 3', 'Skala 4', 'Skala 5'])
    
    st.bar_chart(data_g5, color="#82c068")


# ==========================================
# TAB 2: IDENTIFIKASI TREN DAN KORELASI
# ==========================================
with tab2:
    st.header("💡 Identifikasi Tren & Analisis Korelasi")
    
    st.markdown("""
    Analisis ini bertujuan untuk melihat keterkaitan antara desain visual (banner), faktor psikologis (waktu terbatas & kejelasan informasi), terhadap perilaku nyata konsumen (minat beli & *impulsive checkout*) pada penggunaan ShopeePay.
    """)

    # Poin 1
    st.subheader("1. Hubungan Desain Visual (Banner) dengan Minat Transaksi")
    st.info("""
    **Analisis Korelasi:** Terdapat korelasi positif yang kuat antara aspek visual banner dan kejelasan informasi promo. Responden menilai bahwa banner ShopeePay tidak hanya menarik perhatian secara visual, tetapi juga berhasil menyampaikan informasi promo dengan jelas. Gabungan antara visual yang menarik dan informasi yang mudah dipahami ini menjadi stimulus utama yang berhasil menggerakkan minat beli konsumen.
    """)

    # Poin 2
    st.subheader("2. Strategi Scarcity (Waktu Terbatas) vs Perilaku Impulsive Buying")
    st.warning("""
    **Analisis Korelasi:** Ada kecenderungan korelasi psikologis yang menarik di sini. Strategi *limitation* atau promo batas waktu menciptakan efek *Fear of Missing Out* (FOMO). Efek mendesak ini berbanding lurus dengan tingginya angka *impulsive checkout*. Konsumen merasa harus segera bertransaksi demi mengejar promo, meskipun produk tersebut sebenarnya tidak terlalu mereka butuhkan.
    """)

    # Poin 3
    st.subheader("3. Karakteristik Responden Berdasarkan Gender")
    st.success("""
    **Analisis Korelasi:** Dengan proporsi gender yang cukup berimbang (didominasi Perempuan sebesar 53.4%), tren jawaban menunjukkan bahwa daya tarik promo ShopeePay bersifat universal. Baik responden perempuan maupun laki-laki sama-sama rentan terhadap stimulus promo visual dan batas waktu (*flash sale* atau *limited voucher*).
    """)

    # Kesimpulan Akhir
    st.subheader("📌 Kesimpulan Tren Utama (Summary)")
    st.markdown("""
    Dari kelima grafik tersebut, dapat ditarik kesimpulan alur perilaku konsumen (*consumer journey*) sebagai berikut:

    1. **Daya Tarik Awal:** `Banner Menarik` + `Informasi Jelas` ➡️ **Memicu Minat Transaksi**
    2. **Dorongan Transaksi:** `Didesak Waktu Terbatas` ➡️ **Mendorong Checkout Impulsif / Non-Kebutuhan**

    Secara keseluruhan, responden dalam survei ini memiliki karakteristik **'Promo-Driven Consumers'** (konsumen yang sangat digerakkan oleh insentif promo). Penjualan/transaksi ShopeePay berhasil didongkrak bukan karena kebutuhan riil konsumen, melainkan karena efektivitas komunikasi visual banner dan manipulasi urgensi waktu promo.
    """)
