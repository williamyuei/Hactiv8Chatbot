# ==============================================================================
# ASISTEN BELAJAR KOMPUTER & PERSIAPAN SERTIFIKASI OFFICE OPERATOR (BNSP)
# ------------------------------------------------------------------------------
# Use case      : Education bot
# Domain        : Microsoft Office 2021 & kompetensi BNSP Junior Office Operator
# Gaya bahasa   : Ramah, tapi tetap sopan (campuran)
# Fitur kreatif :
#   1. Persona & domain knowledge lewat system_instruction ke model
#   2. Memory persisten antar sesi (disimpan ke file JSON, bukan cuma session_state)
#   3. Fitur rekomendasi modul belajar otomatis berdasarkan topik yang dibahas
# ==============================================================================

import streamlit as st
from google import genai
import json
import os
from datetime import datetime

# ── 0. Konfigurasi Dasar ─────────────────────────────────────────────────────
MEMORY_DIR = "chat_memory"          # folder penyimpanan riwayat chat per pengguna
os.makedirs(MEMORY_DIR, exist_ok=True)

# Basis pengetahuan modul belajar sederhana untuk fitur rekomendasi.
# Setiap entri berisi kata kunci pemicu -> nama modul yang direkomendasikan.
MODUL_REKOMENDASI = {
    "word": "📄 Modul 1: Pengolah Kata (Microsoft Word) - format dokumen, mail merge, TOC",
    "excel": "📊 Modul 2: Pengolah Angka (Microsoft Excel) - rumus, fungsi, pivot table",
    "powerpoint": "📽️ Modul 3: Presentasi (Microsoft PowerPoint) - slide, animasi, desain",
    "internet": "🌐 Modul 4: Aplikasi Internet & Email - browsing aman, etika email",
    "sosial media": "📱 Modul 5: Aplikasi Media Sosial untuk Kerja - etika digital, personal branding",
    "sertifikasi": "🎓 Modul 6: Simulasi Uji Kompetensi BNSP Junior Office Operator",
    "bnsp": "🎓 Modul 6: Simulasi Uji Kompetensi BNSP Junior Office Operator",
}

SYSTEM_INSTRUCTION = """
Kamu adalah "Bu Ari", asisten belajar virtual yang membantu peserta pelatihan
mempersiapkan diri untuk sertifikasi kompetensi Junior Office Operator (BNSP)
dan meningkatkan kemampuan komputer dasar (Microsoft Word, Excel, PowerPoint,
internet, dan media sosial untuk keperluan kerja).

Gaya bicaramu ramah dan suportif, seperti trainer yang sabar, tapi tetap sopan
dan profesional (gunakan sapaan "Kak" ke pengguna). Jawab dengan bahasa
Indonesia yang mudah dipahami, beri contoh praktis, dan jika relevan, tawarkan
langkah-langkah singkat bernomor.

Jika pengguna bertanya di luar topik komputer/office/sertifikasi BNSP, tetap
jawab dengan sopan namun arahkan kembali secara halus ke topik pelatihan.
"""

# ── 1. Konfigurasi Halaman ───────────────────────────────────────────────────
st.set_page_config(page_title="Asisten Belajar Office & BNSP", page_icon="🎓")
st.title("🎓 Asisten Belajar Komputer & Sertifikasi BNSP")
st.caption("Ditenagai oleh Google Gemini — teman belajar Microsoft Office & persiapan uji kompetensi")

# ── 2. Sidebar: Pengaturan & Identitas Pengguna ─────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Pengaturan")

    google_api_key = st.text_input("Google AI API Key", type="password")

    # Nama pengguna dipakai sebagai ID untuk menyimpan memory antar sesi
    username = st.text_input("Nama kamu", value="peserta", help="Dipakai untuk menyimpan riwayat belajarmu")
    memory_file = os.path.join(MEMORY_DIR, f"{username.strip().lower().replace(' ', '_')}.json")

    reset_button = st.button("🔄 Reset Percakapan", help="Hapus riwayat belajar untuk pengguna ini")

    st.divider()
    st.caption("💡 Fitur:")
    st.caption("- Memory tersimpan antar sesi\n- Rekomendasi modul otomatis\n- Persona trainer BNSP")

# ── 3. Validasi API Key ──────────────────────────────────────────────────────
if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk mulai belajar bersama Bu Ari.", icon="🗝️")
    st.stop()

# ── 4. Fungsi Bantu: Load & Save Memory Persisten ───────────────────────────
def load_memory(path):
    """Muat riwayat chat dari file JSON, kalau ada."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_memory(path, messages):
    """Simpan riwayat chat ke file JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# ── 5. Reset Percakapan ──────────────────────────────────────────────────────
if reset_button:
    if os.path.exists(memory_file):
        os.remove(memory_file)
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ── 6. Inisialisasi Gemini Client ────────────────────────────────────────────
if ("genai_client" not in st.session_state) or (
    getattr(st.session_state, "_last_key", None) != google_api_key
):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat", None)
    except Exception as e:
        st.error(f"API Key tidak valid: {e}")
        st.stop()

# ── 7. Muat Riwayat dari File (Memory Persisten) ────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = load_memory(memory_file)

# ── 8. Inisialisasi Chat Session dengan Persona + Riwayat Sebelumnya ───────
if "chat" not in st.session_state:
    # Bangun ulang histori percakapan dalam format yang dipahami Gemini,
    # supaya konteks belajar sebelumnya "diingat" walau sesi Streamlit baru.
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})

    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION},
        history=history,
    )

# ── 9. Fungsi Rekomendasi Modul ─────────────────────────────────────────────
def cari_rekomendasi(teks):
    """Cek apakah teks mengandung kata kunci topik tertentu, lalu kembalikan
    rekomendasi modul belajar yang relevan (fitur kreatif tambahan)."""
    teks_lower = teks.lower()
    hasil = []
    for kata_kunci, modul in MODUL_REKOMENDASI.items():
        if kata_kunci in teks_lower and modul not in hasil:
            hasil.append(modul)
    return hasil

# ── 10. Tampilkan Riwayat Percakapan ────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 11. Input & Respons ──────────────────────────────────────────────────────
prompt = st.chat_input("Tanya apa saja seputar Office & persiapan sertifikasi BNSP...")

if prompt:
    # Tampilkan & simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim ke Gemini
    try:
        response = st.session_state.chat.send_message(prompt)
        answer = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        answer = f"Maaf Kak, ada kendala teknis: {e}"

    # Tampilkan respons
    with st.chat_message("assistant"):
        st.markdown(answer)

        # Fitur rekomendasi: cek topik dari pesan user + jawaban bot
        rekomendasi = cari_rekomendasi(prompt + " " + answer)
        if rekomendasi:
            st.info(
                "**📚 Rekomendasi modul belajar terkait:**\n\n"
                + "\n\n".join(f"- {r}" for r in rekomendasi)
            )

    # Simpan respons ke riwayat & simpan seluruh riwayat ke file (persisten)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_memory(memory_file, st.session_state.messages)

# ── 12. Info Kaki Halaman ───────────────────────────────────────────────────
st.caption(f"Sesi belajar untuk: **{username}** • Riwayat tersimpan otomatis di `{memory_file}`")
