import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from collections import Counter
import webbrowser
import json  # Tambahan untuk menyimpan data
import os    # Tambahan untuk mengecek keberadaan file

# --- KONFIGURASI TEMA ---
COLOR_PRIMARY = "#4CAF50"  # Hijau Pertanian
COLOR_SECONDARY = "#FFFFFF" # Putih
COLOR_BG = "#F5F5F5"      # Abu-abu sangat muda untuk background
COLOR_TEXT = "#2E7D32"      # Hijau Tua untuk teks

# ==========================================
# 1. OOP: ENKAPSULASI
# ==========================================
class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password # Private

    def get_username(self):
        return self.__username

    def check_password(self, password_input):
        return self.__password == password_input

    # Method baru untuk mengubah objek menjadi dictionary (untuk JSON)
    def to_dict(self):
        return {"username": self.__username, "password": self.__password}

# ==========================================
# 2. OOP: INHERITANCE & POLYMORPHISM
# ==========================================
class BaseData:
    def __init__(self, tanaman, penyakit):
        self.tanaman = tanaman
        self.penyakit = penyakit

    def get_info(self): # Akan di-override
        pass

class LaporanPenyakit(BaseData):
    def __init__(self, petani, tanaman, penyakit, url):
        super().__init__(tanaman, penyakit)
        self.petani = petani
        self.url = url

    # Polymorphism: Implementasi spesifik untuk laporan
    def get_info(self):
        return (self.petani, self.tanaman, self.penyakit, self.url)

# ==========================================
# 3. LOGIKA SISTEM (Integrasi File JSON)
# ==========================================
class AgricultureSystem:
    def __init__(self):
        self.file_db = "users_db.json"
        self.users = []
        self.daftar_laporan = []
        self.muat_data_user() # Langsung muat data dari JSON saat program jalan

    # Method untuk membaca data dari JSON
    def muat_data_user(self):
        if os.path.exists(self.file_db):
            with open(self.file_db, 'r') as file:
                data = json.load(file)
                for u in data:
                    # Baris di bawah ini WAJIB menjorok ke dalam (1 Tab)
                    self.users.append(User(u['username'], u['password']))
        else:
            self.users.append(User("admin", "admin"))
            self.simpan_data_user()

    # Method untuk menyimpan data list of object ke JSON
    def simpan_data_user(self):
        with open(self.file_db, 'w') as file:
            # Ubah setiap objek User ke bentuk dictionary sebelum disimpan
            data_dict = [u.to_dict() for u in self.users]
            json.dump(data_dict, file, indent=4)

    def register(self, user, pwd):
        if any(u.get_username() == user for u in self.users): return False
        self.users.append(User(user, pwd))
        self.simpan_data_user() # <-- Update JSON setiap kali ada user baru
        return True

    def login(self, user, pwd):
        for u in self.users:
            if u.get_username() == user and u.check_password(pwd): return True
        return False

# ==========================================
# 4. GUI MODERN
# ==========================================
class ModernAgriApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agri Clima Care - Sistem Informasi Penyakit Tanaman")
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_BG)
        self.system = AgricultureSystem()
        
        self.style = ttk.Style()
        self.setup_styles()
        
        self.main_container = tk.Frame(self.root, bg=COLOR_BG)
        self.main_container.pack(fill="both", expand=True)
        
        self.show_login()

    def setup_styles(self):
        # Mengatur gaya Treeview (Tabel)
        self.style.theme_use("clam")
        self.style.configure("Treeview", 
            background=COLOR_SECONDARY, 
            foreground="#333", 
            rowheight=30, 
            fieldbackground=COLOR_SECONDARY,
            font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", 
            background=COLOR_PRIMARY, 
            foreground="white", 
            font=("Segoe UI", 11, "bold"))
        self.style.map("Treeview", background=[('selected', '#81C784')])

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- HALAMAN LOGIN ---
    def show_login(self):
        self.clear_screen()
        # Card Login
        card = tk.Frame(self.main_container, bg=COLOR_SECONDARY, padx=40, pady=40, highlightbackground="#DDD", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Agri Clima Care", font=("Segoe UI", 24, "bold"), bg=COLOR_SECONDARY, fg=COLOR_PRIMARY).pack(pady=(0, 10))
        tk.Label(card, text="Silakan masuk ke akun Anda", font=("Segoe UI", 10), bg=COLOR_SECONDARY, fg="gray").pack(pady=(0, 20))

        tk.Label(card, text="Username", bg=COLOR_SECONDARY, fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        u_entry = tk.Entry(card, font=("Segoe UI", 12), width=30, bd=0, bg="#F0F0F0")
        u_entry.pack(pady=(5, 15), ipady=8)

        tk.Label(card, text="Password", bg=COLOR_SECONDARY, fg=COLOR_TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        p_entry = tk.Entry(card, font=("Segoe UI", 12), width=30, bd=0, bg="#F0F0F0", show="•")
        p_entry.pack(pady=(5, 25), ipady=8)

        btn_login = tk.Button(card, text="LOGIN", command=lambda: self.do_login(u_entry.get(), p_entry.get()), 
                              bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 12, "bold"), 
                              activebackground="#45a049", cursor="hand2", bd=0, width=28)
        btn_login.pack(ipady=10)

        tk.Button(card, text="Belum punya akun? Daftar", command=self.show_register, bg=COLOR_SECONDARY, 
                  fg=COLOR_PRIMARY, bd=0, cursor="hand2", font=("Segoe UI", 9)).pack(pady=(15, 0))

    def do_login(self, u, p):
        if self.system.login(u, p):
            messagebox.showinfo("Berhasil", f"Selamat datang, {u}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Gagal", "Username atau Password salah")

    def show_register(self):
        self.clear_screen()
        card = tk.Frame(self.main_container, bg=COLOR_SECONDARY, padx=40, pady=40, highlightbackground="#DDD", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Registrasi Petani", font=("Segoe UI", 20, "bold"), bg=COLOR_SECONDARY, fg=COLOR_PRIMARY).pack(pady=(0, 20))

        tk.Label(card, text="Username Baru", bg=COLOR_SECONDARY, font=("Segoe UI", 10)).pack(anchor="w")
        u_entry = tk.Entry(card, font=("Segoe UI", 12), width=30, bg="#F0F0F0", bd=0)
        u_entry.pack(pady=5, ipady=8)

        tk.Label(card, text="Password Baru", bg=COLOR_SECONDARY, font=("Segoe UI", 10)).pack(anchor="w")
        p_entry = tk.Entry(card, font=("Segoe UI", 12), width=30, bg="#F0F0F0", bd=0, show="•")
        p_entry.pack(pady=5, ipady=8)

        tk.Button(card, text="DAFTAR SEKARANG", command=lambda: self.do_reg(u_entry.get(), p_entry.get()), 
                  bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 11, "bold"), bd=0, width=30).pack(pady=20, ipady=10)
        
        tk.Button(card, text="Kembali ke Login", command=self.show_login, bg=COLOR_SECONDARY, fg="gray", bd=0).pack()

    def do_reg(self, u, p):
        if u == "" or p == "":
            messagebox.showwarning("Input Kosong", "Isi semua bidang!")
            return
        if self.system.register(u, p):
            messagebox.showinfo("Sukses", "Akun berhasil dibuat!")
            self.show_login()
        else:
            messagebox.showerror("Gagal", "Username sudah ada")

    # --- HALAMAN DASHBOARD ---
    def show_dashboard(self):
        self.clear_screen()
        
        # Header Navigasi
        header = tk.Frame(self.main_container, bg=COLOR_PRIMARY, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Agri Clima Care Dashboard", font=("Segoe UI", 16, "bold"), bg=COLOR_PRIMARY, fg="white").pack(side="left", padx=30)
        tk.Button(header, text="Logout", command=self.show_login, bg="#e53935", fg="white", bd=0, padx=15).pack(side="right", padx=30)

        # Konten Utama
        content = tk.Frame(self.main_container, bg=COLOR_BG, padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # Bagian Atas: Form Input (Card Style)
        form_card = tk.Frame(content, bg=COLOR_SECONDARY, padx=20, pady=20, highlightbackground="#DDD", highlightthickness=1)
        form_card.pack(fill="x", pady=(0, 20))

        tk.Label(form_card, text="Tambah Laporan Penyakit", font=("Segoe UI", 12, "bold"), bg=COLOR_SECONDARY, fg=COLOR_PRIMARY).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        labels = ["Nama Petani", "Nama Tanaman", "Jenis Penyakit", "URL Informasi"]
        self.entries = []
        for i, text in enumerate(labels):
            tk.Label(form_card, text=text, bg=COLOR_SECONDARY, font=("Segoe UI", 9, "bold")).grid(row=1, column=i, sticky="w", padx=5)
            e = tk.Entry(form_card, font=("Segoe UI", 10), bg="#F0F0F0", bd=0)
            e.grid(row=2, column=i, padx=5, pady=5, ipady=5, sticky="ew")
            self.entries.append(e)

        tk.Button(form_card, text="SIMPAN DATA", command=self.add_report, bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=20).grid(row=2, column=4, padx=10, ipady=4)

        # Bagian Tengah: Tabel
        table_frame = tk.Frame(content, bg=COLOR_SECONDARY)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("P1", "T1", "J1", "U1"), show="headings")
        self.tree.heading("P1", text="Petani")
        self.tree.heading("T1", text="Tanaman")
        self.tree.heading("J1", text="Penyakit")
        self.tree.heading("U1", text="Link Informasi")
        self.tree.pack(fill="both", expand=True, side="left")
        
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind("<Double-1>", self.open_link)

        # Bagian Bawah: Tombol Grafik
        btn_frame = tk.Frame(content, bg=COLOR_BG)
        btn_frame.pack(fill="x", pady=20)

        tk.Button(btn_frame, text="📊 Grafik Penyakit", command=self.plot_disease, bg=COLOR_SECONDARY, fg=COLOR_PRIMARY, font=("Segoe UI", 10, "bold"), bd=1, padx=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🌿 Grafik Tanaman", command=self.plot_plant, bg=COLOR_SECONDARY, fg=COLOR_PRIMARY, font=("Segoe UI", 10, "bold"), bd=1, padx=20).pack(side="left", padx=5)
        tk.Label(btn_frame, text="*Klik ganda pada baris tabel untuk buka link informasi", font=("Segoe UI", 9, "italic"), bg=COLOR_BG, fg="gray").pack(side="right")

    def add_report(self):
        data = [e.get() for e in self.entries]
        if "" in data:
            messagebox.showwarning("Peringatan", "Mohon lengkapi semua data laporan!")
            return
        
        new_rep = LaporanPenyakit(data[0], data[1], data[2], data[3])
        self.system.daftar_laporan.append(new_rep)
        self.tree.insert("", "end", values=new_rep.get_info())
        
        for e in self.entries: e.delete(0, tk.END)
        messagebox.showinfo("Berhasil", "Data penyakit berhasil disimpan")

    def open_link(self, event):
        item = self.tree.selection()[0]
        url = self.tree.item(item, "values")[3]
        if url.startswith("http"):
            webbrowser.open(url)
        else:
            messagebox.showwarning("URL Tidak Valid", "Pastikan URL diawali dengan http:// atau https://")

    def plot_disease(self):
        if not self.system.daftar_laporan: return messagebox.showwarning("Data Kosong", "Belum ada data untuk grafik")
        counts = Counter([rep.penyakit for rep in self.system.daftar_laporan])
        self.create_chart(counts, "Statistik Jenis Penyakit", COLOR_PRIMARY)

    def plot_plant(self):
        if not self.system.daftar_laporan: return messagebox.showwarning("Data Kosong", "Belum ada data untuk grafik")
        counts = Counter([rep.tanaman for rep in self.system.daftar_laporan])
        self.create_chart(counts, "Statistik Tanaman Terdampak", "#8BC34A")

    def create_chart(self, data_dict, title, color):
        plt.figure(figsize=(8, 5))
        plt.bar(data_dict.keys(), data_dict.values(), color=color)
        plt.title(title, fontsize=14, fontweight='bold', color='#2E7D32')
        plt.xlabel("Kategori", fontweight='bold')
        plt.ylabel("Jumlah Kasus", fontweight='bold')
        plt.tight_layout()
        plt.show()

# --- RUN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAgriApp(root)
    root.mainloop()