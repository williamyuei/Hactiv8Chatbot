# 🎓 Asisten Belajar Komputer & Sertifikasi BNSP

Chatbot berbasis AI (Google Gemini) yang berperan sebagai asisten belajar virtual
untuk membantu peserta pelatihan mempersiapkan diri menghadapi **Uji Kompetensi
BNSP Junior Office Operator** dan meningkatkan kemampuan komputer dasar
(Microsoft Word, Excel, PowerPoint, internet, dan media sosial untuk kerja).

Dibangun sebagai final project untuk mata kuliah dengan kriteria: chatbot AI
berbasis NLP/LLM dengan use case dan parameter kreatif tertentu.

## ✨ Fitur

- **Use case**: Education bot — persiapan sertifikasi BNSP & literasi komputer
- **Persona & domain knowledge**: "Bu Ari", trainer virtual dengan gaya bahasa
  ramah namun tetap sopan, difokuskan ke domain Microsoft Office & BNSP
- **Memory persisten**: riwayat percakapan disimpan ke file JSON per pengguna,
  sehingga konteks belajar tetap ada meski sesi Streamlit di-restart
- **Rekomendasi modul otomatis**: bot mendeteksi topik yang dibahas (Word,
  Excel, PowerPoint, internet, sertifikasi, dll) dan menyarankan modul belajar
  terkait
- **Reset percakapan**: opsi untuk menghapus riwayat belajar dan memulai ulang

## 🖥️ System Requirements

| Komponen | Versi Minimum |
|---|---|
| Python | 3.9 atau lebih baru |
| Sistem Operasi | Windows, macOS, atau Linux |
| Koneksi Internet | Diperlukan (memanggil Google Gemini API) |
| Google AI API Key | Wajib — dapatkan gratis di [Google AI Studio](https://aistudio.google.com/app/apikey) |

### Dependencies (Python packages)

```
streamlit>=1.38.0
google-genai>=0.3.0
```

## 📦 Instalasi

1. **Clone repository ini**
   ```bash
   git clone https://github.com/<username-kamu>/<nama-repo>.git
   cd <nama-repo>
   ```

2. **(Opsional tapi disarankan) Buat virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit google-genai
   ```

## 🚀 Menjalankan Aplikasi

```bash
streamlit run streamlit_chat_app.py
```

Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`.

1. Masukkan **Google AI API Key** kamu di sidebar (klik ikon 🗝️ untuk info cara mendapatkannya)
2. Isi **nama kamu** di sidebar — dipakai untuk menyimpan riwayat belajar
3. Mulai bertanya seputar Microsoft Office & persiapan sertifikasi BNSP di kotak chat

## 📁 Struktur Proyek

```
.
├── streamlit_chat_app.py    # Kode utama aplikasi chatbot
├── chat_memory/             # Folder otomatis untuk menyimpan riwayat chat (JSON)
└── README.md                # Dokumentasi proyek
```

> Catatan: folder `chat_memory/` dibuat otomatis saat aplikasi pertama kali
> dijalankan dan berisi data pribadi riwayat percakapan pengguna — disarankan
> menambahkannya ke `.gitignore` agar tidak ikut ter-commit ke repository publik.

## 🔒 Keamanan API Key

Jangan pernah menaruh API key langsung di dalam kode atau meng-commit-nya ke
GitHub. Aplikasi ini meminta API key melalui input sidebar (`type="password"`)
setiap kali dijalankan, sehingga key tidak pernah tersimpan di dalam kode.

## 🛠️ Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/) — framework antarmuka web
- [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash`) — model NLP/LLM
- Python `json` & `os` — penyimpanan memory persisten

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik (final project).
