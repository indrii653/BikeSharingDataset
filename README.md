# Dicoding Collection Dashboard ✨

## Setup Environment - Terminal / Shell (Menggunakan `uv`)

Proyek ini dijalankan menggunakan **Python 3.14** yang dikelola melalui package manager `uv`.

1. **Clone Repositori**
   ```bash
   git clone [https://github.com/indrii653/BikeSharingDataset.git](https://github.com/indrii653/BikeSharingDataset.git)
   cd BikeSharingDataset
   
Jalankan Aplikasi Streamlit
Jalankan Streamlit langsung menggunakan uv tanpa perlu menginstal dependensi secara global:
uv run --with streamlit --with babel --with seaborn --with pandas --with matplotlib streamlit run dashboard/dashboard.py

Setup Environment - Python Lokal (Alternatif)
Jika Anda ingin menjalankan proyek menggunakan Python lokal (Python 3.11):
pip install -r requirements.txt

Jalankan Aplikasi Streamlit
streamlit run dashboard/dashboard.py

---

### Cara Mengunggah Perubahan `README.md` ke GitHub

Jika Anda menyimpan atau memperbarui file `README.md` tersebut di folder proyek Anda, jalankan 3 perintah ini di Git Bash untuk menyinkronkannya ke GitHub:

```bash
git add .
git commit -m "Update README.md dengan petunjuk jalannya aplikasi"
git push
