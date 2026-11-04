import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# =========================================================
st.set_page_config(
    page_title="Bike Sharing Interactive Dashboard",
    page_icon="🚲",
    layout="wide"
)

# =========================================================
# 2. FUNGSI HELPER AGREGASI DATA
# =========================================================
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "instant": "count",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    
    daily_rentals_df.rename(columns={
        "instant": "day_count",
        "cnt": "total_rentals",
        "casual": "casual_rentals",
        "registered": "registered_rentals"
    }, inplace=True)
    
    return daily_rentals_df

def create_byhour_df(df):
    byhour_df = df.groupby("hr").agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    }).reset_index().sort_values(by="cnt", ascending=False)
    
    return byhour_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").agg({
        "cnt": "sum",
        "casual": "mean",
        "registered": "mean"
    }).reset_index()
    
    byweather_df.rename(columns={
        "cnt": "total_rentals",
        "casual": "avg_casual",
        "registered": "avg_registered"
    }, inplace=True)
    
    return byweather_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    }).reset_index()
    
    season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    byseason_df['season'] = byseason_df['season'].map(season_names)
    byseason_df['season'] = pd.Categorical(
        byseason_df['season'], 
        categories=["Spring", "Summer", "Fall", "Winter"], 
        ordered=True
    )
    
    return byseason_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday").agg({
        "cnt": ["sum", "mean"],
        "casual": "sum",
        "registered": "sum"
    }).reset_index()
    
    byworkingday_df.columns = ["workingday", "total_rentals", "avg_rentals", "total_casual", "total_registered"]
    byworkingday_df['day_type'] = byworkingday_df['workingday'].map({0: "Weekend/Holiday", 1: "Workingday"})
    
    return byworkingday_df

def create_daily_summary_df(df):
    daily_summary_df = df.groupby(by="dteday", as_index=False).agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum",
        "temp": "mean"
    })
    
    daily_summary_df.columns = ["dteday", "total_rentals", "total_casual", "total_registered", "avg_temp"]
    
    recent_date = df["dteday"].dt.date.max()
    daily_summary_df["dteday_date"] = daily_summary_df["dteday"].dt.date
    daily_summary_df["recency"] = daily_summary_df["dteday_date"].apply(lambda x: (recent_date - x).days)
    daily_summary_df.drop("dteday_date", axis=1, inplace=True)
    
    return daily_summary_df

# =========================================================
# 3. MEMUAT & MEMERIKSA DATASET
# =========================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("all_data.csv")
    except FileNotFoundError:
        df = pd.read_csv("all_data.csv")
        
    df["dteday"] = pd.to_datetime(df["dteday"])
    df.sort_values(by="dteday", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

all_df = load_data()

# =========================================================
# 4. SIDEBAR FILTER RENTANG WAKTU
# =========================================================
min_date = all_df["dteday"].min().date()
max_date = all_df["dteday"].max().date()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Dataframe Utama Berdasarkan Tanggal
main_df = all_df[(all_df["dteday"].dt.date >= start_date) & 
                 (all_df["dteday"].dt.date <= end_date)]

# =========================================================
# 5. MENJALANKAN FUNGSI HELPER UNTUK AGREGASI DATA
# =========================================================
daily_rentals_df = create_daily_rentals_df(main_df)
byhour_df = create_byhour_df(main_df)
byweather_df = create_byweather_df(main_df)
byseason_df = create_byseason_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
daily_summary_df = create_daily_summary_df(main_df)

# =========================================================
# 6. HEADER & METRIK UTAMA DASHBOARD
# =========================================================
st.header('Bike Sharing Analytics Dashboard :sparkles:')
st.caption('Analisis Tren dan Pola Penyewaan Sepeda (2011-2012)')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,}")

with col2:
    total_registered = main_df['registered'].sum()
    st.metric(label="Pengguna Terdaftar (Registered)", value=f"{total_registered:,}")

with col3:
    total_casual = main_df['casual'].sum()
    st.metric(label="Pengguna Biasa (Casual)", value=f"{total_casual:,}")

st.divider()

# =========================================================
# 7. VISUALISASI PERTANYAAN 1: POLA JAM (HARI KERJA VS LIBUR)
# =========================================================
st.subheader("1. Pola Penyewaan Sepeda per Jam: Hari Kerja vs Akhir Pekan / Libur")

hourly_pattern = main_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=hourly_pattern,
    x='hr',
    y='cnt',
    hue='workingday',
    palette=['#E74C3C', '#2ECC71'],
    marker='o',
    ax=ax1
)

ax1.set_title('Rata-Rata Penyewaan Sepeda per Jam', fontsize=12, fontweight='bold')
ax1.set_xlabel('Jam dalam Sehari (00.00 - 23.00)', fontsize=10)
ax1.set_ylabel('Rata-Rata Penyewaan (cnt)', fontsize=10)
ax1.set_xticks(range(0, 24))
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(title='Jenis Hari', labels=['Akhir Pekan / Libur (0)', 'Hari Kerja (1)'])

st.pyplot(fig1)

with st.expander("📌 Lihat Insight Pola Jam"):
    st.write("""
    * **Hari Kerja (`workingday = 1`)**: Memiliki dua jam puncak utama (*peak hours*), yaitu **pukul 08.00 pagi** (jam berangkat kerja/sekolah) dan **pukul 17.00 - 18.00 sore** (jam pulang kerja).
    * **Akhir Pekan / Libur (`workingday = 0`)**: Permintaan terdistribusi melengkung dari siang hingga sore hari, dengan puncak pada **pukul 12.00 - 16.00**.
    """)

st.divider()

# =========================================================
# 8. VISUALISASI PERTANYAAN 2: DUKUNGAN KONDISI CUACA
# =========================================================
st.subheader("2. Rata-Rata Penyewaan Sepeda per Jam Berdasarkan Kondisi Cuaca")

weather_avg = main_df.groupby('weathersit')['cnt'].mean().reset_index()

weather_labels = {
    1: '1: Cerah / Berawan Sedikit',
    2: '2: Kabut / Mendung',
    3: '3: Hujan Ringan / Salju Ringan',
    4: '4: Hujan Lebat / Badai'
}
weather_avg['weather_label'] = weather_avg['weathersit'].map(weather_labels)

fig2, ax2 = plt.subplots(figsize=(10, 5))
colors = ['#2ECC71', '#F1C40F', '#E67E22', '#E74C3C']

barplot = sns.barplot(
    data=weather_avg,
    x='weather_label',
    y='cnt',
    palette=colors,
    ax=ax2
)

ax2.set_title('Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda', fontsize=12, fontweight='bold')
ax2.set_xlabel('Kondisi Cuaca', fontsize=10)
ax2.set_ylabel('Rata-Rata Penyewaan (cnt)', fontsize=10)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for p in barplot.patches:
    if p.get_height() > 0:
        barplot.annotate(f'{p.get_height():.2f}',
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom',
                         fontsize=9, fontweight='bold',
                         xytext=(0, 4), textcoords='offset points')

st.pyplot(fig2)

with st.expander("📌 Lihat Insight Kondisi Cuaca"):
    st.write("""
    * **Permintaan Tertinggi**: Terjadi pada **Cuaca 1 (Cerah / Berawan Sedikit)**.
    * **Permintaan Terendah**: Terjadi pada **Cuaca 4 (Hujan Lebat / Badai / Salju)**.
    * Terdapat penurunan drastis secara linear seiring memburuknya kondisi cuaca.
    """)

st.caption("Proyek Analisis Data Bike Sharing - Dicoding")

# =========================================================
# 1. DAILY RENTALS SUMMARY & TREND
# =========================================================
st.subheader('Daily Rentals Overview')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df.total_rentals.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    total_registered = daily_rentals_df.registered_rentals.sum()
    st.metric("Total Registered", value=f"{total_registered:,}")

with col3:
    total_casual = daily_rentals_df.casual_rentals.sum()
    st.metric("Total Casual", value=f"{total_casual:,}")

# Tren Peminjaman Sepeda Harian
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rentals"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Daily Bike Rentals Trend", fontsize=20, pad=15)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# =========================================================
# 2. PEAK & LOWEST RENTAL HOURS (Menggantikan Best/Worst Product)
# =========================================================
st.subheader("Peak & Lowest Rental Hours")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 8))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Jam dengan Peminjaman Tertinggi
sns.barplot(
    x="cnt", 
    y="hr", 
    data=byhour_df.head(5), 
    palette=colors, 
    orient='h',
    ax=ax[0]
)
ax[0].set_ylabel("Hour (00.00 - 23.00)", fontsize=18)
ax[0].set_xlabel("Total Rentals", fontsize=18)
ax[0].set_title("Most Active Hours", loc="center", fontsize=22)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Jam dengan Peminjaman Terendah
sns.barplot(
    x="cnt", 
    y="hr", 
    data=byhour_df.sort_values(by="cnt", ascending=True).head(5), 
    palette=colors, 
    orient='h',
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Rentals", fontsize=18)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Active Hours", loc="center", fontsize=22)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# =========================================================
# 3. DEMOGRAPHICS & ENVIRONMENTAL FACTORS (Menggantikan Customer Demographics)
# =========================================================
st.subheader("Environmental Factors & Day Categories")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors_weather = ["#2ECC71", "#F1C40F", "#E67E22", "#E74C3C"]
    
    sns.barplot(
        y="total_rentals", 
        x="weathersit",
        data=byweather_df.sort_values(by="total_rentals", ascending=False),
        palette=colors_weather,
        ax=ax
    )
    ax.set_title("Rentals by Weather Situation", loc="center", fontsize=18)
    ax.set_ylabel("Total Rentals", fontsize=14)
    ax.set_xlabel("Weather Situation", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors_season = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="cnt", 
        x="season",
        data=byseason_df.sort_values(by="cnt", ascending=False),
        palette=colors_season,
        ax=ax
    )
    ax.set_title("Rentals by Season", loc="center", fontsize=18)
    ax.set_ylabel("Total Rentals", fontsize=14)
    ax.set_xlabel("Season", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

# Peminjaman berdasarkan Workingday
fig, ax = plt.subplots(figsize=(12, 5))
colors_workingday = ["#E74C3C", "#2ECC71"]

sns.barplot(
    x="total_rentals", 
    y="day_type",
    data=byworkingday_df.sort_values(by="total_rentals", ascending=False),
    palette=colors_workingday,
    ax=ax
)
ax.set_title("Rentals by Day Type (Workingday vs Weekend/Holiday)", loc="center", fontsize=18)
ax.set_ylabel(None)
ax.set_xlabel("Total Rentals", fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# =========================================================
# 4. DAILY SUMMARY PARAMETERS (Menggantikan RFM Parameters)
# =========================================================
st.subheader("Daily Rental Parameters Summary")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(daily_summary_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_rentals = round(daily_summary_df.total_rentals.mean(), 1)
    st.metric("Average Daily Rentals", value=f"{avg_rentals:,}")

with col3:
    avg_temp = round(daily_summary_df.avg_temp.mean(), 2)
    st.metric("Average Temperature", value=f"{avg_temp}")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))
colors_rfm = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

# Top 5 Days by Recency
sns.barplot(
    y="recency", 
    x="dteday", 
    data=daily_summary_df.sort_values(by="recency", ascending=True).head(5), 
    palette=colors_rfm, 
    ax=ax[0]
)
ax[0].set_ylabel("Recency (days)", fontsize=14)
ax[0].set_xlabel("Date", fontsize=14)
ax[0].set_title("Most Recent Recorded Days", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=12)
ax[0].tick_params(axis='x', labelsize=10, rotation=45)

# Top 5 Days by Total Rentals
sns.barplot(
    y="total_rentals", 
    x="dteday", 
    data=daily_summary_df.sort_values(by="total_rentals", ascending=False).head(5), 
    palette=colors_rfm, 
    ax=ax[1]
)
ax[1].set_ylabel("Total Rentals", fontsize=14)
ax[1].set_xlabel("Date", fontsize=14)
ax[1].set_title("Top 5 Days by Highest Rentals", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=10, rotation=45)

# Top 5 Days by Registered Rentals
sns.barplot(
    y="total_registered", 
    x="dteday", 
    data=daily_summary_df.sort_values(by="total_registered", ascending=False).head(5), 
    palette=colors_rfm, 
    ax=ax[2]
)
ax[2].set_ylabel("Registered Rentals", fontsize=14)
ax[2].set_xlabel("Date", fontsize=14)
ax[2].set_title("Top 5 Days by Registered Rentals", loc="center", fontsize=18)
ax[2].tick_params(axis='y', labelsize=12)
ax[2].tick_params(axis='x', labelsize=10, rotation=45)

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023 - Bike Sharing Dashboard')