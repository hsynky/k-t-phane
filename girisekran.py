import tkinter as tk
from tkinter import Button
import os
import datetime
import pandas as pd
import anaekran

pencere = tk.Tk();pencere.title("Kütüphane Giriş Sayfa")
ekran_genislik = pencere.winfo_screenwidth();ekran_yukseklik = pencere.winfo_screenheight()
yarim_genislik = ekran_genislik // 2 ;tam_yukseklik = ekran_yukseklik
x_konum = ekran_genislik // 2 ;y_konum = 0
pencere.geometry(f"{yarim_genislik}x{tam_yukseklik}+{x_konum}+{y_konum}")
dosya_yolu = "kutuphane_tablosu.xlsx"

if os.path.exists(dosya_yolu):
    print("Dosya mevcut.");print("tanıtım ekranı atlanıyor")
    def gecis():
        pencere.destroy(),anaekran.ana_ekran_penceresi_ac()
    pencere.after(100, gecis)
else:
    print("Dosya bulunamadı.")
    tanıtım = tk.Label(pencere, text="Hoş geldiniz", font=("Arial", 24));tanıtım.pack(pady=200)
    def ikinci_mesaj():
        tanıtım.config(text="Hadi kitaplarınızı kayıt altına alalım")
        def devam_et():
            if not os.path.exists(dosya_yolu):
                kolonlar = ["ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi","durumu"]
                df = pd.DataFrame(columns=kolonlar)
                df.to_excel(dosya_yolu, index=False)
                print("Excel dosyası oluşturuldu.")
            pencere.destroy();anaekran.ana_ekran_penceresi_ac()

        devam_dugmesi = Button(
            pencere,text="Devam",
            font=("Helvetica", 16, "bold"),bg="#4CAF50",fg="orange",bd=3,relief="raised",padx=20,pady=10,command=devam_et)
        devam_dugmesi.pack(pady=20)
        # Renk değiştirme olayları
        devam_dugmesi.bind("<Enter>", lambda e: devam_dugmesi.config(bg="#45a049"));devam_dugmesi.bind("<Leave>", lambda e: devam_dugmesi.config(bg="#4CAF50"))
    pencere.after(3000, ikinci_mesaj)  # 3 saniye sonra ikinci mesaj
pencere.mainloop()