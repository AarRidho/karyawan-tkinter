from dotenv import load_dotenv
from tkinter import *
import tkinter.messagebox as messagebox
# import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import mysql.connector
import os

class Student:
    def __init__(self, name, age, gender, jumlah_anak):
        self.name = name
        self.age = age
        self.gender = gender

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASS"),
            database=os.getenv("DATABASE_NAME"),
            port=os.getenv("DATABASE_PORT")
        )
        self.cursor = self.connection.cursor()
        # self.Membuat_Table()

    # def Membuat_Table(self):
    #     self.cursor.execute("CREATE TABLE IF NOT EXISTS pegawai (id int NOT NULL, name VARCHAR(255), age INTEGER, gender VARCHAR(255), pangkat VARCHAR(255), jumlah_anak INTEGER, CONSTRAINT )")

    def memasukan_karyawan(self, karyawan):
        self.cursor.execute("INSERT INTO pegawai (nama, umur, gender, jumlah_anak) VALUES (?, ?, ?, ?)",
                            (karyawan.name, karyawan.age, karyawan.gender, karyawan.jumlah_anak))
                            # print(self.connection.info_query(query))
        # self.cursor.execute("INSERT INTO pegawai VALUES (?, ?, ?, ?)",
        #                     (Karyawan.nip, Karyawan.name, Karyawan.gender, Karyawan.jumlah_anak, Karyawan.tanggal_lahir, Karyawan.tempat_lahir, Karyawan.alamat))
        self.connection.commit()

    def get_all_karyawan(self):    
        self.cursor.execute("SELECT * FROM pegawai")
        return self.cursor.fetchall()

    def update_karyawan(self, name, new_major):
        self.cursor.execute("UPDATE pegawai SET pangkat=? WHERE name=?", (new_major, name))
        self.connection.commit()

    def delete_karyawan(self, name):
        self.cursor.execute("DELETE FROM pegawai WHERE name=?", (name,))
        self.connection.commit()

    def search_karyawan(self, name):
        self.cursor.execute("SELECT * FROM pegawai WHERE name=?", (name,))
        return self.cursor.fetchall() 

    def close_connection(self):
        self.connection.close()

class Application:
    def __init__(self, window):
        self.window = window
        self.window.title("Aplikasi Penghitung gaji karyawan")
        
        self.database = Database()
        
        self.membuat_widget()
    
    def membuat_widget(self):
        self.label_name = Label(self.window, text="Nama:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = Entry(self.window)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_age = Label(self.window, text="Umur:")
        self.label_age.grid(row=1, column=0, padx=10, pady=5)
        self.entry_age = Entry(self.window)
        self.entry_age.grid(row=1, column=1, padx=10, pady=5)

        self.label_gender = Label(self.window, text="Gender:")
        self.label_gender.grid(row=2, column=0, padx=10, pady=5)
        self.entry_gender = Entry(self.window)
        self.entry_gender.grid(row=2, column=1, padx=10, pady=5)

        self.label_major = Label(self.window, text="Jabatan:")
        self.label_major.grid(row=3, column=0, padx=10, pady=5)
        self.entry_major = Entry(self.window)
        self.entry_major.grid(row=3, column=1, padx=10, pady=5)

        
        self.label_child = Label(self.window, text="jumlah_anak:")
        self.label_child.grid(row=3, column=0, padx=10, pady=5)
        self.entry_child = Entry(self.window)
        self.entry_child.grid(row=3, column=1, padx=10, pady=5)


        self.button_add = Button(self.window, text="Tambahkan Karyawan", command=self.Menambahkan_Karyawan)
        self.button_add.grid(row=5, column=0, padx=10, pady=5)
        self.button_show = Button(self.window, text="Data Karyawan", command=self.show_karyawan)
        self.button_show.grid(row=5, column=1, padx=10, pady=5)

        self.label_statistics = Label(self.window, text="Karyawan:")
        self.label_statistics.grid(row=4, column=0, padx=10, pady=5)


        self.label_statistics = Label(self.window, text="Statistics:")
        self.label_statistics.grid(row=4, column=1, padx=10, pady=5)

        self.button_statistics = Button(self.window, text="Tampilkan Statistics", command=self.show_statistics)
        self.button_statistics.grid(row=6, column=1, padx=10, pady=5)
        
        self.button_delete = Button(self.window, text="Hapus Karyawan", command=self.delete_karyawan)
        self.button_delete.grid(row=6, column=0, padx=10, pady=5)


    def Menambahkan_Karyawan(self):
        # try:
            name = self.entry_name.get()
            age = int(self.entry_age.get())
            gender = self.entry_gender.get()
            # pangkat = self.entry_major.get()
            jumlah_anak = int(self.entry_child.get())
            
            karyawan = self.database.get_all_karyawan()
            status = False
            for karyawan in karyawan:
                print(name,karyawan[0])
                if name == karyawan[0]:
                    status = True
                    self.entry_name.configure(background='red')
                    messagebox.showinfo("Gagal",f"'Gagal' Nama ' {name} ' sudah ada di DataBase, Coba Masukan Nama Yang Lain.")
                    self.clear_TextBox()
                    return

            if status == False:
                karyawan = Student(name, age, gender, jumlah_anak)
                self.database.memasukan_karyawan(karyawan)
                messagebox.showinfo("Berhasil", "Student Berhasil Di Tambahkan.")
                self.clear_TextBox()
        # except:
            # messagebox.showinfo("Gagal", "Tolong Lengkapi Box Diatas")
            # self.clear_TextBox()

    def show_karyawan(self):
        karyawan = self.database.get_all_karyawan()
        print(karyawan)
        if karyawan:
            karyawan_list = "Student List:\n\n"
            for i,Karyawan in enumerate(karyawan):
                print(karyawan[i])
                karyawan_list += f"Nama: {Karyawan[0]}\nUmur: {Karyawan[1]}\nGender: {Karyawan[2]}\nJumlah Anak: {Karyawan[4]}\n\n"
            messagebox.showinfo("Students", karyawan_list)
        else:
            messagebox.showinfo("Students", "Tidak Ada Data Karyawan Yang Disimpan.")

    def show_statistics(self):
        karyawan = self.database.get_all_karyawan()
        if karyawan:
            ages = [Karyawan[1] for Karyawan in karyawan]

            mean_age = np.mean(ages)
            median_age = np.median(ages)
            max_age = np.max(ages)
            min_age = np.min(ages)
            
            plt.hist(ages, bins=10, color='yellow', edgecolor='black')
            plt.title('Distribution Umur')
            plt.xlabel('Umur')
            plt.ylabel('Frekuensi')
            plt.show()

            statistics = f"Statistics:\n\nMean UMUR: {mean_age}\nMedian UMUR: {median_age}\nMaximum UMUR: {max_age}\nMinimum UMUR: {min_age}"

            messagebox.showinfo("Statistics", statistics)
            

        
        else:
            messagebox.showinfo("Statistics", "Tidak Ada Static Tentang karyawan.")

    def delete_karyawan(self):
        name = self.entry_name.get()

        
        Karyawan = self.database.search_karyawan(name)
        if Karyawan:
            karyawan = self.database.get_all_karyawan()

            dell_list = f"'Berhasil' Nama '{name}' Berhasil di Deleted.\n\n"
            for i,Karyawan in enumerate(karyawan):
                print(karyawan[i])
                if Karyawan[i][0] == name:
                    dell_list += f"Nama: {Karyawan[i][0]}\nUmur: {Karyawan[1]}\nGender: {Karyawan[i][0]}\nJumlah Anak: {Karyawan[i][0]}\n\n"
                    self.entry_name.configure(background='green')
                    self.database.delete_karyawan(name)
                    messagebox.showinfo("Delete Student", dell_list)
                    self.clear_TextBox()
                    return
                else:
                    messagebox.showinfo("Mencari", "Mencari nama...")
        elif name == "":
            self.entry_name.configure(background='red')
            messagebox.showinfo("Delete Student", f"'Gagal'  Tolong Masukan Nama Yang Ingin Dihapus di Kolum Nama.")
        else:
            self.entry_name.configure(background='red')
            messagebox.showinfo("Delete Student", f"'Gagal'  Nama '{name}' Tidak Ditemukan Di DataBase.")
        
        
        self.clear_TextBox()

    def clear_TextBox(self):
        self.entry_name.delete(0, END)
        self.entry_age.delete(0, END)
        self.entry_gender.delete(0, END)
        self.entry_major.delete(0, END)
        self.entry_child.delete(0, END)
        self.entry_name.configure(background='white')
        self.entry_age.configure(background='white')
        self.entry_gender.configure(background='white')
        self.entry_major.configure(background='white')
        self.entry_child.configure(background='white')

    def close_application(self):
        self.database.close_connection()
        self.window.destroy()


if __name__ == "__main__":
    load_dotenv()

    main = Tk()
    app = Application(main)
    main.protocol("WM_DELETE_WINDOW", app.close_application)
    main.mainloop()