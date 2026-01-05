import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import os
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="PNS Activity Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk UI menarik
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #4a5568;
    }
    
    h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 10px !important;
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 20px !important;
    }
    
    h3 {
        color: #4a5568 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
        border-radius: 12px;
        font-weight: 600;
        color: #2d3748;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateX(5px);
    }
    
    .stDateInput > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 12px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 12px;
    }
    
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 12px;
        padding: 15px;
        font-weight: 600;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 30px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Sidebar navigation buttons */
    .nav-button {
        width: 100%;
        padding: 15px;
        margin: 10px 0;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        text-align: left;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# File untuk menyimpan data
DATA_FILE = "kegiatan_pns.csv"
IMAGE_FOLDER = "bukti_kegiatan"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # Konversi DataFrame ke list of dictionaries
            return df.to_dict('records')
        except:
            return []
    return []

def save_data(data):
    if not data:
        # Buat CSV kosong dengan header
        df = pd.DataFrame(columns=['id', 'tanggal', 'kegiatan', 'deskripsi', 'status', 'kategori', 'bukti'])
    else:
        df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')  # utf-8-sig agar bisa dibuka di Excel

def save_image(image, activity_id):
    filename = f"{activity_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    filepath = os.path.join(IMAGE_FOLDER, filename)
    image.save(filepath)
    return filename

def export_to_csv(data, start_date=None, end_date=None):
    if not data:
        # Return empty CSV with headers
        return pd.DataFrame(columns=['tanggal', 'kegiatan', 'kategori', 'status', 'deskripsi']).to_csv(index=False).encode('utf-8')
    
    df = pd.DataFrame(data)
    if start_date and end_date:
        df = df[(df['tanggal'] >= start_date) & (df['tanggal'] <= end_date)]
    df_export = df[['tanggal', 'kegiatan', 'kategori', 'status', 'deskripsi']]
    return df_export.to_csv(index=False).encode('utf-8')

# Initialize session state
if 'activities' not in st.session_state:
    st.session_state.activities = load_data()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
    st.session_state.edit_id = None

# Sidebar Navigation
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🎯 Navigasi")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📊 DASHBOARD", use_container_width=True, type="primary" if st.session_state.current_page == 'Dashboard' else "secondary"):
        st.session_state.current_page = 'Dashboard'
        st.session_state.edit_mode = False
        st.rerun()
    
    if st.button("➕ TAMBAH KEGIATAN", use_container_width=True, type="primary" if st.session_state.current_page == 'Tambah' else "secondary"):
        st.session_state.current_page = 'Tambah'
        st.session_state.edit_mode = False
        st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Statistik Cepat")
    total = len(st.session_state.activities)
    selesai = sum(1 for a in st.session_state.activities if a['status'] == 'Selesai')
    st.metric("Total Kegiatan", total)
    st.metric("Selesai", selesai, f"{(selesai/total*100):.0f}%" if total > 0 else "0%")

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🎯 PNS Activity Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem; margin-top: -10px;'>Kelola Kegiatan Harian Anda dengan Mudah</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== HALAMAN TAMBAH/EDIT KEGIATAN ====================
if st.session_state.current_page == 'Tambah':
    if st.session_state.edit_mode:
        st.markdown("## ✏️ Edit Kegiatan")
        # Cari data yang akan diedit
        edit_data = next((a for a in st.session_state.activities if a['id'] == st.session_state.edit_id), None)
    else:
        st.markdown("## ➕ Tambah Kegiatan Baru")
        edit_data = None
    
    with st.form("activity_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal = st.date_input(
                "📅 Tanggal", 
                value=datetime.strptime(edit_data['tanggal'], "%Y-%m-%d").date() if edit_data else date.today()
            )
            kegiatan = st.text_input(
                "📝 Nama Kegiatan", 
                value=edit_data['kegiatan'] if edit_data else "",
                placeholder="Masukkan nama kegiatan..."
            )
            kategori = st.selectbox(
                "🏷️ Kategori", 
                ["Pengolahan", "IT", "Hardware", "Software", "Diseminasi", "SE 2026", "Pojok Statistik"],
                index=["Pengolahan", "IT", "Hardware", "Software", "Diseminasi", "SE 2026", "Pojok Statistik"].index(edit_data['kategori']) if edit_data else 0
            )
        
        with col2:
            status = st.selectbox(
                "✅ Status", 
                ["Selesai", "Dalam Proses", "Tertunda"],
                index=["Selesai", "Dalam Proses", "Tertunda"].index(edit_data['status']) if edit_data else 0
            )
            deskripsi = st.text_area(
                "📄 Deskripsi", 
                value=edit_data['deskripsi'] if edit_data else "",
                placeholder="Jelaskan detail kegiatan...", 
                height=150
            )
        
        st.markdown("---")
        st.markdown("### 📸 Bukti Kegiatan (Opsional)")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_image = st.file_uploader("📁 Upload File Gambar", type=['jpg', 'jpeg', 'png'])
        with col2:
            camera_image = st.camera_input("📷 Ambil Foto Langsung")
        
        # Tampilkan gambar lama jika edit mode
        if edit_data and edit_data.get('bukti'):
            st.markdown("**Bukti Kegiatan Saat Ini:**")
            image_path = os.path.join(IMAGE_FOLDER, edit_data['bukti'])
            if os.path.exists(image_path):
                st.image(image_path, width=300)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button(
                "💾 SIMPAN KEGIATAN" if not st.session_state.edit_mode else "✅ UPDATE KEGIATAN", 
                use_container_width=True
            )
        
        if submit:
            if kegiatan:
                # Pilih gambar yang akan digunakan
                image_to_save = camera_image if camera_image else uploaded_image
                image_filename = edit_data.get('bukti') if edit_data else None
                
                if image_to_save:
                    # Hapus gambar lama jika ada dan ada gambar baru
                    if edit_data and edit_data.get('bukti'):
                        old_image_path = os.path.join(IMAGE_FOLDER, edit_data['bukti'])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    
                    # Simpan gambar baru
                    image = Image.open(image_to_save)
                    activity_id = st.session_state.edit_id if st.session_state.edit_mode else (len(st.session_state.activities) + 1)
                    image_filename = save_image(image, activity_id)
                
                if st.session_state.edit_mode:
                    # Update kegiatan yang ada
                    for i, activity in enumerate(st.session_state.activities):
                        if activity['id'] == st.session_state.edit_id:
                            st.session_state.activities[i] = {
                                "id": st.session_state.edit_id,
                                "tanggal": tanggal.strftime("%Y-%m-%d"),
                                "kegiatan": kegiatan,
                                "deskripsi": deskripsi,
                                "status": status,
                                "kategori": kategori,
                                "bukti": image_filename
                            }
                            break
                    save_data(st.session_state.activities)
                    st.success("✅ Kegiatan berhasil diupdate!")
                    st.session_state.edit_mode = False
                    st.session_state.edit_id = None
                else:
                    # Tambah kegiatan baru
                    new_activity = {
                        "id": len(st.session_state.activities) + 1,
                        "tanggal": tanggal.strftime("%Y-%m-%d"),
                        "kegiatan": kegiatan,
                        "deskripsi": deskripsi,
                        "status": status,
                        "kategori": kategori,
                        "bukti": image_filename
                    }
                    st.session_state.activities.append(new_activity)
                    save_data(st.session_state.activities)
                    st.success("✅ Kegiatan berhasil ditambahkan!")
                
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Nama kegiatan harus diisi!")
    
    # Tombol batal edit
    if st.session_state.edit_mode:
        if st.button("❌ Batal Edit"):
            st.session_state.edit_mode = False
            st.session_state.edit_id = None
            st.rerun()

# ==================== HALAMAN DASHBOARD ====================
elif st.session_state.current_page == 'Dashboard':
    tab1, tab2, tab3 = st.tabs(["📊 OVERVIEW", "📝 DAFTAR KEGIATAN", "📈 STATISTIK & ANALISIS"])
    
    with tab1:
        # Metrics
        st.markdown("### 📊 Ringkasan Kegiatan")
        col1, col2, col3, col4 = st.columns(4)
        
        total_kegiatan = len(st.session_state.activities)
        selesai = sum(1 for a in st.session_state.activities if a['status'] == 'Selesai')
        proses = sum(1 for a in st.session_state.activities if a['status'] == 'Dalam Proses')
        tertunda = sum(1 for a in st.session_state.activities if a['status'] == 'Tertunda')
        
        with col1:
            st.metric("📋 Total Kegiatan", total_kegiatan)
        with col2:
            st.metric("✅ Selesai", selesai, delta=f"{(selesai/total_kegiatan*100):.0f}%" if total_kegiatan > 0 else "0%")
        with col3:
            st.metric("⏳ Proses", proses)
        with col4:
            st.metric("⚠️ Tertunda", tertunda)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filter periode
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📅 Pilih Periode")
        with col2:
            bulan_options = ["Bulan Ini"] + sorted(list(set([a['tanggal'][:7] for a in st.session_state.activities])), reverse=True)
            selected_month = st.selectbox("", bulan_options, label_visibility="collapsed")
        
        if selected_month == "Bulan Ini":
            current_month = date.today().strftime("%Y-%m")
            filtered_activities = [a for a in st.session_state.activities if a['tanggal'].startswith(current_month)]
        else:
            filtered_activities = [a for a in st.session_state.activities if a['tanggal'].startswith(selected_month)]
        
        if filtered_activities:
            df_month = pd.DataFrame(filtered_activities)
            kategori_count = df_month['kategori'].value_counts().reset_index()
            kategori_count.columns = ['Kategori', 'Jumlah']
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140']
                fig_pie = go.Figure(data=[go.Pie(
                    labels=kategori_count['Kategori'],
                    values=kategori_count['Jumlah'],
                    hole=.5,
                    marker=dict(colors=colors, line=dict(color='white', width=3)),
                    textinfo='label+percent',
                    textfont=dict(size=14, color='white', family='Poppins'),
                    hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
                )])
                
                fig_pie.update_layout(
                    title=dict(text=f'🎯 Distribusi Kegiatan - {selected_month}', 
                              font=dict(size=20, color='#2d3748', family='Poppins', weight=600)),
                    showlegend=True,
                    legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1),
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Detail Kategori")
                for _, row in kategori_count.iterrows():
                    persen = (row['Jumlah'] / len(filtered_activities) * 100)
                    st.metric(f"{row['Kategori']}", row['Jumlah'], f"{persen:.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📋 Kegiatan Terkini")
            
            for activity in sorted(filtered_activities, key=lambda x: x['tanggal'], reverse=True)[:5]:
                with st.expander(f"📅 {activity['tanggal']} • {activity['kegiatan']} • [{activity['kategori']}]"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Status:** `{activity['status']}`")
                        st.markdown(f"**Deskripsi:** {activity['deskripsi']}")
                    with col2:
                        if activity.get('bukti'):
                            image_path = os.path.join(IMAGE_FOLDER, activity['bukti'])
                            if os.path.exists(image_path):
                                st.image(image_path, caption="📸 Bukti", width=200)
        else:
            st.info(f"📭 Belum ada kegiatan untuk periode {selected_month}")
    
    with tab2:
        st.markdown("### 📝 Daftar Semua Kegiatan")
        
        # Filter
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_kategori = st.selectbox("🏷️ Kategori", 
                ["Semua", "Pengolahan", "IT", "Hardware", "Software", "Diseminasi", "SE 2026", "Pojok Statistik"])
        with col2:
            filter_status = st.selectbox("✅ Status", ["Semua", "Selesai", "Dalam Proses", "Tertunda"])
        with col3:
            filter_bulan = st.selectbox("📅 Bulan",
                ["Semua"] + sorted(list(set([a['tanggal'][:7] for a in st.session_state.activities])), reverse=True))
        
        filtered_data = st.session_state.activities
        if filter_bulan != "Semua":
            filtered_data = [a for a in filtered_data if a['tanggal'].startswith(filter_bulan)]
        if filter_status != "Semua":
            filtered_data = [a for a in filtered_data if a['status'] == filter_status]
        if filter_kategori != "Semua":
            filtered_data = [a for a in filtered_data if a['kategori'] == filter_kategori]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Export section
        st.markdown("### 📥 Export Data ke CSV")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("📆 Tanggal Mulai", date.today().replace(day=1))
        with col2:
            end_date = st.date_input("📆 Tanggal Akhir", date.today())
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            csv = export_to_csv(st.session_state.activities, 
                               start_date.strftime("%Y-%m-%d"), 
                               end_date.strftime("%Y-%m-%d"))
            st.download_button(
                label="📥 DOWNLOAD CSV",
                data=csv,
                file_name=f"rekap_{start_date}_{end_date}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if filtered_data:
            st.markdown(f"### 🔍 Ditemukan {len(filtered_data)} kegiatan")
            
            for activity in sorted(filtered_data, key=lambda x: x['tanggal'], reverse=True):
                with st.expander(f"📅 {activity['tanggal']} • {activity['kegiatan']} • [{activity['kategori']}]"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Status:** `{activity['status']}`")
                        st.markdown(f"**Deskripsi:** {activity['deskripsi']}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(f"✏️ Edit", key=f"edit_{activity['id']}"):
                                st.session_state.edit_mode = True
                                st.session_state.edit_id = activity['id']
                                st.session_state.current_page = 'Tambah'
                                st.rerun()
                        
                        with col_b:
                            if st.button(f"🗑️ Hapus", key=f"delete_{activity['id']}"):
                                if activity.get('bukti'):
                                    image_path = os.path.join(IMAGE_FOLDER, activity['bukti'])
                                    if os.path.exists(image_path):
                                        os.remove(image_path)
                                
                                st.session_state.activities = [a for a in st.session_state.activities if a['id'] != activity['id']]
                                save_data(st.session_state.activities)
                                st.success("✅ Kegiatan berhasil dihapus!")
                                st.rerun()
                    
                    with col2:
                        if activity.get('bukti'):
                            image_path = os.path.join(IMAGE_FOLDER, activity['bukti'])
                            if os.path.exists(image_path):
                                st.image(image_path, caption="📸 Bukti", width=200)
        else:
            st.info("📭 Tidak ada data kegiatan yang sesuai filter")
    
    with tab3:
        st.markdown("### 📈 Statistik & Analisis Mendalam")
        
        if st.session_state.activities:
            df = pd.DataFrame(st.session_state.activities)
            df['tanggal'] = pd.to_datetime(df['tanggal'])
            df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)
            df['tahun'] = df['tanggal'].dt.year
            
            tahun_options = sorted(df['tahun'].unique(), reverse=True)
            selected_year = st.selectbox("📅 Pilih Tahun", tahun_options)
            
            df_year = df[df['tahun'] == selected_year]
            
            st.markdown(f"### 🎯 Akumulasi Tahun {selected_year}")
            
            col1, col2, col3, col4 = st.columns(4)
            total_tahun = len(df_year)
            selesai_tahun = len(df_year[df_year['status'] == 'Selesai'])
            
            with col1:
                st.metric("📋 Total Kegiatan", total_tahun)
            with col2:
                st.metric("✅ Selesai", selesai_tahun)
            with col3:
                st.metric("📊 Rata-rata/Bulan", f"{total_tahun/12:.1f}")
            with col4:
                st.metric("🎯 Completion Rate", f"{(selesai_tahun/total_tahun*100):.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tren bulanan dengan gradient colors
            st.markdown("### 📊 Tren Kegiatan Bulanan")
            monthly_kategori = df_year.groupby(['bulan', 'kategori']).size().reset_index(name='jumlah')
            
            colors_map = {
                'Pengolahan': '#667eea',
                'IT': '#764ba2',
                'Hardware': '#f093fb',
                'Software': '#4facfe',
                'Diseminasi': '#43e97b',
                'SE 2026': '#fa709a',
                'Pojok Statistik': '#fee140'
            }
            
            fig_trend = px.bar(monthly_kategori, x='bulan', y='jumlah', color='kategori',
                              color_discrete_map=colors_map,
                              labels={'jumlah': 'Jumlah Kegiatan', 'bulan': 'Bulan'},
                              barmode='stack')
            
            fig_trend.update_layout(
                title=dict(text='', font=dict(size=20)),
                xaxis_title="Bulan",
                yaxis_title="Jumlah Kegiatan",
                legend_title="Kategori",
                height=450,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.95)',
                font=dict(family='Poppins', size=12),
                hovermode='x unified'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Total per Kategori")
                kategori_year = df_year['kategori'].value_counts().reset_index()
                kategori_year.columns = ['Kategori', 'Jumlah']
                
                fig_bar = go.Figure(data=[
                    go.Bar(x=kategori_year['Kategori'], y=kategori_year['Jumlah'],
                          marker=dict(
                              color=kategori_year['Jumlah'],
                              colorscale=[[0, '#667eea'], [1, '#764ba2']],
                              line=dict(color='white', width=2)
                          ),
                          text=kategori_year['Jumlah'],
                          textposition='outside')
                ])
                
                fig_bar.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.95)',
                    xaxis_title="Kategori",
                    yaxis_title="Jumlah",
                    font=dict(family='Poppins', size=12)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
                top_kategori = kategori_year.iloc[0]
                st.info(f"💡 **Insight:** Kategori terbanyak adalah **{top_kategori['Kategori']}** dengan **{top_kategori['Jumlah']}** kegiatan ({top_kategori['Jumlah']/total_tahun*100:.1f}%)")
            
            with col2:
                st.markdown("### ✅ Status Penyelesaian")
                status_year = df_year['status'].value_counts().reset_index()
                status_year.columns = ['Status', 'Jumlah']
                
                status_colors = {'Selesai': '#48bb78', 'Dalam Proses': '#f6ad55', 'Tertunda': '#fc8181'}
                
                fig_donut = go.Figure(data=[go.Pie(
                    labels=status_year['Status'],
                    values=status_year['Jumlah'],
                    hole=.6,
                    marker=dict(colors=[status_colors.get(s, '#667eea') for s in status_year['Status']],
                               line=dict(color='white', width=3)),
                    textinfo='label+percent',
                    textfont=dict(size=13, color='white', family='Poppins')
                )])
                
                fig_donut.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    annotations=[dict(text=f'{selesai_tahun}<br>Selesai', x=0.5, y=0.5, font_size=20, showarrow=False)]
                )
                st.plotly_chart(fig_donut, use_container_width=True)
                
                st.info(f"💡 **Insight:** Tingkat penyelesaian mencapai **{(selesai_tahun/total_tahun*100):.1f}%**")
            
            # Heatmap
            st.markdown("### 🔥 Heatmap Intensitas Kegiatan")
            heatmap_data = df_year.groupby(['bulan', 'kategori']).size().reset_index(name='jumlah')
            heatmap_pivot = heatmap_data.pivot(index='kategori', columns='bulan', values='jumlah').fillna(0)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                colorscale='Viridis',
                text=heatmap_pivot.values,
                texttemplate='%{text}',
                textfont={"size": 12},
                colorbar=dict(title="Jumlah")
            ))
            
            fig_heatmap.update_layout(
                xaxis_title="Bulan",
                yaxis_title="Kategori",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.95)',
                font=dict(family='Poppins', size=12)
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Line chart kumulatif
            st.markdown("### 📈 Tren Kumulatif Kegiatan")
            df_year_sorted = df_year.sort_values('tanggal')
            df_year_sorted['kumulatif'] = range(1, len(df_year_sorted) + 1)
            
            fig_cumulative = go.Figure()
            fig_cumulative.add_trace(go.Scatter(
                x=df_year_sorted['tanggal'],
                y=df_year_sorted['kumulatif'],
                mode='lines+markers',
                name='Kumulatif',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6, color='#764ba2'),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            
            fig_cumulative.update_layout(
                xaxis_title="Tanggal",
                yaxis_title="Total Kumulatif",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.95)',
                font=dict(family='Poppins', size=12),
                hovermode='x unified'
            )
            st.plotly_chart(fig_cumulative, use_container_width=True)
            
            # Tabel ringkasan
            st.markdown("### 📋 Ringkasan Bulanan")
            monthly_summary = df_year.groupby('bulan').agg({
                'kegiatan': 'count',
                'kategori': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
            }).reset_index()
            monthly_summary.columns = ['Bulan', 'Total Kegiatan', 'Kategori Terbanyak']
            
            st.dataframe(
                monthly_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Bulan": st.column_config.TextColumn("📅 Bulan", width="small"),
                    "Total Kegiatan": st.column_config.NumberColumn("📊 Total Kegiatan", width="small"),
                    "Kategori Terbanyak": st.column_config.TextColumn("🏷️ Kategori Terbanyak", width="medium")
                }
            )
            
        else:
            st.info("📭 Belum ada data untuk ditampilkan")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px);'>
    <p style='color: white; font-size: 0.9rem; margin: 0;'>
        💼 <b>PNS Activity Tracker</b> | Dibuat dengan ❤️ menggunakan Streamlit
    </p>
    <p style='color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 5px 0 0 0;'>
        © 2026 | Version 2.0
    </p>
</div>
""", unsafe_allow_html=True)