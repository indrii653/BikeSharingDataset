# Bike Sharing Analysis Dashboard

Proyek ini merupakan proyek analisis data menggunakan dataset **Bike Sharing Dataset**. Analisis dilakukan menggunakan Python dan Jupyter Notebook, sedangkan visualisasi interaktif dibuat menggunakan Streamlit.

## 1. Struktur Direktori Proyek

Berikut struktur direktori repositori:

```text
BikeSharingDataset/
│
├── Bike-sharing-dataset/
│   ├── Readme.txt
│   ├── day.csv
│   └── hour.csv
│
├── dashboard/
│   ├── all_data.csv
│   └── dashboard.py
│
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md
```

**Keterangan:**
- `Bike-sharing-dataset/`: Dataset mentah yang digunakan dalam proses analisis.
- `dashboard/`: Folder aplikasi dashboard Streamlit.
- `all_data.csv`: Dataset yang telah dipersiapkan untuk visualisasi dashboard.
- `dashboard.py`: Script utama untuk menjalankan aplikasi Streamlit.
- `Proyek_Analisis_Data.ipynb`: Notebook yang berisi proses analisis data dan Exploratory Data Analysis (EDA).
- `requirements.txt`: Daftar dependensi Python yang dibutuhkan.
- `README.md`: Dokumentasi dan panduan penggunaan proyek.

## 2. Persyaratan Sistem

Pastikan perangkat telah memiliki:
- Python 3.11
- pip
- Git

## 3. Setup Environment

### A. Clone Repository

Buka Terminal atau PowerShell, kemudian jalankan:

```bash
git clone https://github.com/indrii653/BikeSharingDataset.git
```

Masuk ke direktori proyek:

```bash
cd BikeSharingDataset
```

### B. Membuat Virtual Environment

Buat lingkungan virtual Python:

```bash
py -3.11 -m venv .venv
```

### C. Instalasi Dependensi

Instal seluruh library yang dibutuhkan menggunakan perintah:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Menjalankan Dashboard Streamlit

Pastikan terminal berada di direktori utama proyek `BikeSharingDataset`.

Jalankan aplikasi dengan perintah:

```bash
.venv\Scripts\python.exe -m streamlit run dashboard/dashboard.py
```

Setelah aplikasi berjalan, Streamlit akan menampilkan alamat lokal dashboard pada terminal, biasanya:

```text
http://localhost:8501
```

Buka alamat tersebut melalui browser untuk melihat dashboard interaktif.

**Catatan:** Jalankan perintah dari direktori utama proyek agar struktur direktori dan lokasi file dapat dikenali dengan benar. File dataset dashboard berada di dalam folder `dashboard/` dan dibaca berdasarkan lokasi script `dashboard.py`.

## 5. Menutup Aplikasi

Untuk menghentikan aplikasi Streamlit, tekan:

```text
Ctrl + C
```

pada terminal yang sedang menjalankan aplikasi.

## 6. Teknologi yang Digunakan

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook
