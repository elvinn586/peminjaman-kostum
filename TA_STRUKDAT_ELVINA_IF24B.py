# Nama  : Elvina Farissa Budiputri
# NIM   : 24416255201034
# Kelas : IF-24B
# Tugas : Aplikasi Peminjaman Kostum

import csv
import os
from collections import deque

PEMINJAMAN_FILE = "peminjaman.csv"
KOSTUM_FILE = "kostum.csv"

FIELD_PEMINJAMAN = ["ID", "Nama Penyewa", "Nama Kostum", "Ukuran", "Tanggal Pinjam", "Tanggal Kembali", "Status"]
FIELD_KOSTUM = ["ID", "Nama Kostum", "Ukuran", "Stok"]

antrian_pengembalian = deque()

def inisialisasi_file():
    if not os.path.exists(PEMINJAMAN_FILE):
        with open(PEMINJAMAN_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_PEMINJAMAN)
            writer.writeheader()
    
    if not os.path.exists(KOSTUM_FILE):
        with open(KOSTUM_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_KOSTUM)
            writer.writeheader()
            kostum_list = ["Naruto", "Mikasa", "Luffy", "Sailor Moon", "Nezuko", "Inuyasha"]
            id_counter = 1
            for kostum in kostum_list:
                for ukuran in ["M", "L"]:
                    writer.writerow({"ID": str(id_counter), "Nama Kostum": kostum, "Ukuran": ukuran, "Stok": "1"})
                    id_counter += 1

def load_csv(filename):
    with open(filename, 'r') as file:
        return list(csv.DictReader(file))

def save_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def tampilkan_kostum():
    data = load_csv(KOSTUM_FILE)
    print("\n=== DAFTAR KOSTUM TERSEDIA ===")
    for row in data:
        print(f"{row['Nama Kostum']} - Ukuran {row['Ukuran']} | Stok: {row['Stok']}")

def cek_ketersediaan(kostum, ukuran):
    data = load_csv(KOSTUM_FILE)
    for row in data:
        if row["Nama Kostum"].lower() == kostum.lower() and row["Ukuran"].upper() == ukuran.upper():
            return int(row["Stok"]) > 0
    return False

def kurangi_stok(kostum, ukuran):
    data = load_csv(KOSTUM_FILE)
    for row in data:
        if row["Nama Kostum"].lower() == kostum.lower() and row["Ukuran"].upper() == ukuran.upper():
            row["Stok"] = str(int(row["Stok"]) - 1)
    save_csv(KOSTUM_FILE, data, FIELD_KOSTUM)

def tampilkan_kostum_kosong():
    data = load_csv(KOSTUM_FILE)
    print("\n=== KOSTUM HABIS ===")
    kosong = [row for row in data if int(row['Stok']) == 0]
    if kosong:
        for row in kosong:
            print(f"{row['Nama Kostum']} (Ukuran {row['Ukuran']}) ❌")
    else:
        print("Semua kostum tersedia ✔️")

def tampilkan_data():
    data = load_csv(PEMINJAMAN_FILE)
    if not data:
        print("❌ Belum ada data peminjaman.")
        return
    print("\n=== DATA PEMINJAMAN ===")
    for item in data:
        print(item)

def tambah_data():
    data = load_csv(PEMINJAMAN_FILE)
    id_baru = str(len(data) + 1)
    nama = input("Nama penyewa: ")
    tampilkan_kostum()
    kostum = input("Nama kostum: ")
    ukuran = input("Ukuran (M/L): ").upper()

    if not cek_ketersediaan(kostum, ukuran):
        print("❌ Kostum tidak tersedia.")
        return

    tgl_pinjam = input("Tanggal Pinjam (YYYY-MM-DD): ")
    tgl_kembali = input("Tanggal Kembali (YYYY-MM-DD): ")
    status = "Dipinjam"

    new_data = {
        "ID": id_baru,
        "Nama Penyewa": nama,
        "Nama Kostum": kostum,
        "Ukuran": ukuran,
        "Tanggal Pinjam": tgl_pinjam,
        "Tanggal Kembali": tgl_kembali,
        "Status": status
    }
    data.append(new_data)
    save_csv(PEMINJAMAN_FILE, data, FIELD_PEMINJAMAN)
    kurangi_stok(kostum, ukuran)

    antrian_pengembalian.append(nama)

    print("✅ Data berhasil ditambahkan!")

def ubah_data():
    data = load_csv(PEMINJAMAN_FILE)
    id_target = input("Masukkan ID yang ingin diubah: ")
    ditemukan = False
    for item in data:
        if item["ID"] == id_target:
            item["Nama Penyewa"] = input("Nama baru: ")
            item["Nama Kostum"] = input("Kostum baru: ")
            item["Ukuran"] = input("Ukuran baru (M/L): ").upper()
            item["Tanggal Pinjam"] = input("Tanggal pinjam baru: ")
            item["Tanggal Kembali"] = input("Tanggal kembali baru: ")
            item["Status"] = input("Status (Dipinjam/Kembali): ")
            ditemukan = True
            break
    if ditemukan:
        save_csv(PEMINJAMAN_FILE, data, FIELD_PEMINJAMAN)
        print("✅ Data berhasil diubah.")
    else:
        print("❌ ID tidak ditemukan.")

def hapus_data():
    data = load_csv(PEMINJAMAN_FILE)
    id_target = input("Masukkan ID yang ingin dihapus: ")
    data_baru = [item for item in data if item["ID"] != id_target]
    if len(data_baru) < len(data):
        save_csv(PEMINJAMAN_FILE, data_baru, FIELD_PEMINJAMAN)
        print("✅ Data berhasil dihapus.")
    else:
        print("❌ ID tidak ditemukan.")

def proses_antrian_pengembalian():
    if antrian_pengembalian:
        nama = antrian_pengembalian.popleft()
        print(f"🔄 Pengembalian oleh {nama} sedang diproses...")
    else:
        print("✔️ Tidak ada antrian pengembalian.")

def menu():
    inisialisasi_file()
    while True:
        print("\n=== MENU PEMINJAMAN KOSTUM ===")
        print("1. Lihat Data Peminjaman")
        print("2. Tambah Data Peminjaman")
        print("3. Ubah Data Peminjaman")
        print("4. Hapus Data Peminjaman")
        print("5. Lihat Kostum Tersedia")
        print("6. Lihat Kostum yang Habis")
        print("7. Proses Pengembalian (Queue)")
        print("8. Keluar")
        pilihan = input("Pilih menu (1-8): ")

        if pilihan == '1':
            tampilkan_data()
        elif pilihan == '2':
            tambah_data()
        elif pilihan == '3':
            ubah_data()
        elif pilihan == '4':
            hapus_data()
        elif pilihan == '5':
            tampilkan_kostum()
        elif pilihan == '6':
            tampilkan_kostum_kosong()
        elif pilihan == '7':
            proses_antrian_pengembalian()
        elif pilihan == '8':
            print("🙏 Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid!")

menu()
