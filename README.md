# 🔄 DNDUPLICATE

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20Mac-lightgrey)
![Size](https://img.shields.io/badge/Size-~15KB-red)
![Stars](https://img.shields.io/github/stars/dokter69/DNDUPLICATE?style=social)

**Tool for Cleaning & Splitting Domain Lists**  
*Tanpa dependency — Pure Python, Fast, and Efficient*

</div>

---

## 📌 **Deskripsi**

**DNDUPLICATE** adalah tools sederhana namun powerful untuk membersihkan dan mengelola file daftar domain.  
Dibuat dengan pure Python — **tanpa perlu install library tambahan**, langsung pakai!

<div align="center">
  <img src="https://i.ibb.co.com/LzHgf747/photo-2026-04-14-03-18-25.jpg" alt="DNDUPLICATE Preview" width="600">
</div>

---

## ✨ **Fitur Utama**

| Opsi | Fungsi | Kecepatan |
|:----:|:-------|:---------:|
| **1** | **Clear Duplicate Domains** — Menghapus domain ganda dalam file list | ✅ O(n) pakai `set()` |
| **2** | **Split Domain List** — Membagi file besar jadi beberapa file kecil | ✅ Progress bar real-time |

### 🎯 **Fitur Umum**

| Fitur | Keterangan |
|:------|:------------|
| ⚡ **Kecepatan** | Algoritma deduplikasi dengan kompleksitas O(n) — cepat bahkan untuk file besar |
| 🌐 **Encoding** | UTF-8 dengan fallback `errors='ignore'` — aman untuk berbagai karakter |
| 📊 **Progress Bar** | Tampil real-time saat proses split berlangsung |
| 🧩 **Tanpa Dependency** | Hanya butuh Python bawaan — **tidak perlu install modules apapun** |
| 🎨 **Colorful Output** | Tampilan terminal dengan warna-warna menarik (ANSI) |
| 💾 **Auto Backup Duplicates** | Opsi untuk menyimpan daftar domain duplikat ke file terpisah |

---

## 🚀 **Cara Penggunaan**

### **1. Clone Repository**

```bash
git clone https://github.com/dokter69/DNDUPLICATE.git
cd DNDUPLICATE
