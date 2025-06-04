import tkinter as tk
from tkinter import messagebox, ttk

class AplikasiToko:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Toko Sederhana")
        self.root.geometry("600x400")  # Ukuran window diperbesar

        # Data barang (list of dict)
        self.data_barang = []

        # Frame Input
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Nama Barang:").grid(row=0, column=0, padx=5, pady=5)
        self.nama_barang_entry = tk.Entry(frame_input)
        self.nama_barang_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Harga Barang (Rp):").grid(row=1, column=0, padx=5, pady=5)
        self.harga_entry = tk.Entry(frame_input)
        self.harga_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Uang Pembeli (Rp):").grid(row=2, column=0, padx=5, pady=5)
        self.uang_entry = tk.Entry(frame_input)
        self.uang_entry.grid(row=2, column=1, padx=5, pady=5)

        # Tombol CRUD
        frame_button = tk.Frame(root)
        frame_button.pack()

        self.tambah_button = tk.Button(frame_button, text="Tambah Barang", width=15, command=self.tambah_barang)
        self.tambah_button.grid(row=0, column=0, padx=5, pady=5)

        self.ubah_button = tk.Button(frame_button, text="Ubah Barang", width=15, command=self.ubah_barang)
        self.ubah_button.grid(row=0, column=1, padx=5, pady=5)

        self.hapus_button = tk.Button(frame_button, text="Hapus Barang", width=15, command=self.hapus_barang)
        self.hapus_button.grid(row=0, column=2, padx=5, pady=5)

        self.proses_button = tk.Button(frame_button, text="Proses Pembayaran", width=20, command=self.proses_pembayaran)
        self.proses_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.kembalian_button = tk.Button(frame_button, text="Kembalikan Barang Rusak", width=20, command=self.kembalikan_barang)
        self.kembalian_button.grid(row=1, column=2, pady=5)

        # Treeview untuk menampilkan data barang
        self.tree = ttk.Treeview(root, columns=("Nama", "Harga"), show="headings", height=8)
        self.tree.heading("Nama", text="Nama Barang")
        self.tree.heading("Harga", text="Harga (Rp)")
        self.tree.pack(pady=10, fill="x", padx=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def tambah_barang(self):
        nama = self.nama_barang_entry.get().strip()
        harga = self.harga_entry.get().strip()
        if not nama or not harga:
            messagebox.showwarning("Input Kosong", "Nama dan harga barang harus diisi!")
            return
        try:
            harga = int(harga)
        except ValueError:
            messagebox.showerror("Input Salah", "Harga barang harus berupa angka!")
            return
        # Tambah ke data dan treeview
        self.data_barang.append({"nama": nama, "harga": harga})
        self.refresh_treeview()
        self.clear_entry()

    def ubah_barang(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih barang yang ingin diubah!")
            return
        nama = self.nama_barang_entry.get().strip()
        harga = self.harga_entry.get().strip()
        if not nama or not harga:
            messagebox.showwarning("Input Kosong", "Nama dan harga barang harus diisi!")
            return
        try:
            harga = int(harga)
        except ValueError:
            messagebox.showerror("Input Salah", "Harga barang harus berupa angka!")
            return
        idx = int(selected[0])  # Treeview iid = index data_barang
        self.data_barang[idx] = {"nama": nama, "harga": harga}
        self.refresh_treeview()
        self.clear_entry()

    def hapus_barang(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih barang yang ingin dihapus!")
            return
        idx = int(selected[0])
        del self.data_barang[idx]
        self.refresh_treeview()
        self.clear_entry()

    def proses_pembayaran(self):
        try:
            harga = int(self.harga_entry.get())
            uang = int(self.uang_entry.get())
            nama_barang = self.nama_barang_entry.get()
            if uang < harga:
                kekurangan = harga - uang
                messagebox.showwarning("Uang Kurang", f"Uang Anda kurang sebesar Rp{kekurangan}")
            else:
                kembalian = uang - harga
                messagebox.showinfo("Pembayaran Berhasil", f"Terima kasih telah membeli {nama_barang}\nKembalian Anda: Rp{kembalian}")
        except ValueError:
            messagebox.showerror("Input Salah", "Pastikan harga dan uang diisi dengan angka!")

    def kembalikan_barang(self):
        nama_barang = self.nama_barang_entry.get()
        if nama_barang.strip() == "":
            messagebox.showerror("Data Kosong", "Masukkan nama barang yang ingin dikembalikan!")
        else:
            messagebox.showinfo("Pengembalian", f"Barang '{nama_barang}' telah ditandai sebagai rusak dan dikembalikan.")

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for idx, barang in enumerate(self.data_barang):
            self.tree.insert("", "end", iid=idx, values=(barang["nama"], barang["harga"]))

    def clear_entry(self):
        self.nama_barang_entry.delete(0, tk.END)
        self.harga_entry.delete(0, tk.END)
        self.uang_entry.delete(0, tk.END)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            barang = self.data_barang[idx]
            self.nama_barang_entry.delete(0, tk.END)
            self.nama_barang_entry.insert(0, barang["nama"])
            self.harga_entry.delete(0, tk.END)
            self.harga_entry.insert(0, barang["harga"])
            # uang_entry tetap kosong

# Menjalankan Aplikasi
root = tk.Tk()
app = AplikasiToko(root)
root.mainloop()
