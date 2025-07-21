import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import pandas as pd
import datetime
import os
import json

# Excel dosyası yollarını tanımla
KUTUPHANE_DOSYASI = "kutuphane_tablosu.xlsx"
ODUNC_DOSYASI = "odunc_verilen_kitaplar.xlsx"
AYARLAR_DOSYASI = "app_settings.json" # Uygulama ayarları dosyası

# --- Tema Renkleri ve Boyutları (Global değişkenler olarak tanımlandı) ---
# Bu değişkenler, mevcut_temayi_uygula fonksiyonu tarafından güncellenecektir.
# Başlangıçta ayarlar yüklendikten sonra doldurulacak
_ilk_ayarlar = {} 

def varsayilan_ayarlari_olustur():
    """
    Uygulama için varsayılan tema ve boyut ayarlarını döndürür.
    Bu renkler ve boyutlar, platform bağımsız olarak iyi bir başlangıç teması sağlar.
    """
    # Geçici pencere oluşturup ekran boyutlarını al, pencere boyut varsayılanları için
    temp_root = tk.Tk()
    temp_root.withdraw() # Pencereyi gizle
    ekran_genisligi = temp_root.winfo_screenwidth()
    ekran_yuksekligi = temp_root.winfo_screenheight()
    temp_root.destroy()

    return {
        # Renk Ayarları (Koyu tema varsayılanları)
        "ARKA_PLAN_KOYU_GRI": "#2C2C2C", # Koyu gri ana arka plan
        "ARKA_PLAN_ORTA_GRI": "#3C3C3C", # Orta gri ikincil arka plan
        "YAZI_RENGI_BEYAZ": "#E0E0E0", # Açık gri yazı rengi
        "BUTON_AKTIF_ARKA_PLAN": "#555555", # Buton aktifken arka plan
        "GIRIS_KUTUSU_ARKA_PLAN": "#4A4A4A", # Giriş kutusu arka planı
        "GIRIS_KUTUSU_YAZI_RENGI": "#FFFFFF", # Giriş kutusu yazı rengi
        "CERCEVE_BASLIK_YAZI_RENGI": "#E0E0E0", # Çerçeve başlık yazı rengi
        "ACILIR_LISTE_YAZI_RENGI": "#FFFFFF", # Açılır liste metin rengi
        "ACILIR_LISTE_ACILIR_ARKA_PLAN": "#3C3C3C", # Açılır liste menü arka planı
        "ACILIR_LISTE_ACILIR_YAZI_RENGI": "#E0E0E0",    # Açılır liste menü yazı rengi
        "KAYDIRMA_CUBUGU_YOL_ARKA_PLAN": "#3C3C3C",    # Kaydırma çubuğu yolu
        "KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN": "#6A6A6A",    # Kaydırma çubuğu sürgüsü
        "KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN": "#8A8A8A", # Kaydırma çubuğu sürgüsü aktif

        # Boyut Ayarları (Ekran boyutlarına göre dinamik başlangıç varsayılanları)
        "PENCERE_GENISLIGI": ekran_genisligi // 2,
        "PENCERE_YUKSEKLIGI": ekran_yuksekligi,
        "MENU_GENISLIGI": 200
    }

# --- Ayarları Yükleme ve Kaydetme Fonksiyonları ---
def ayarlari_yukle():
    """
    Ayarlar dosyasını yükler. Eğer dosya yoksa veya bozuksa varsayılan ayarları döndürür.
    Varsayılan ayarlar, varsayilan_ayarlari_olustur() fonksiyonundan alınır.
    """
    varsayilan_ayarlar = varsayilan_ayarlari_olustur() # Dinamik varsayılanları al
    yuklenen_ayarlar = {}

    if os.path.exists(AYARLAR_DOSYASI):
        try:
            with open(AYARLAR_DOSYASI, "r") as f:
                yuklenen_ayarlar = json.load(f)
            print(f"'{AYARLAR_DOSYASI}' dosyasından ayarlar yüklendi.")
        except json.JSONDecodeError:
            messagebox.showwarning("Ayarlar Hatası", "Ayarlar dosyası bozuk. Varsayılan ayarlar yüklenecek.")
            print(f"Hata: '{AYARLAR_DOSYASI}' dosyası bozuk. Varsayılanlar kullanılıyor.")
            yuklenen_ayarlar = {} # Bozuksa boş sözlükle devam et
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar dosyası okunurken bir hata oluştu: {e}. Varsayılanlar yüklenecek.")
            print(f"Hata: '{AYARLAR_DOSYASI}' okunurken hata: {e}. Varsayılanlar kullanılıyor.")
            yuklenen_ayarlar = {} # Hata durumunda boş sözlükle devam et
    else:
        print(f"'{AYARLAR_DOSYASI}' dosyası bulunamadı. Varsayılan ayarlar oluşturulacak ve kaydedilecek.")
        # Dosya yoksa, varsayılanları kaydetmeye çalış
        ayarlari_kaydet(varsayilan_ayarlar) # İlk kez çalışıyorsa varsayılanları kaydet
        return varsayilan_ayarlar # Ve varsayılanları döndür

    # Yüklenen ayarlarda eksik anahtar varsa varsayılanı ekle
    # Bu adım, her zaman varsayılanları temel alır ve üzerine yüklenenleri yazar.
    son_ayarlar = varsayilan_ayarlar.copy() # Varsayılanları kopyala
    son_ayarlar.update(yuklenen_ayarlar) # Yüklenenleri üzerine yaz

    print(f"Uygulanan ayarlar: {son_ayarlar}")
    return son_ayarlar

def ayarlari_kaydet(ayarlar):
    """
    Ayarları JSON dosyasına kaydeder.
    """
    try:
        with open(AYARLAR_DOSYASI, "w") as f:
            json.dump(ayarlar, f, indent=4)
        print(f"Ayarlar başarıyla '{AYARLAR_DOSYASI}' dosyasına kaydedildi: {ayarlar}")
        return True
    except Exception as e:
        messagebox.showerror("Kaydetme Hatası", f"Ayarlar kaydedilirken bir hata oluştu: {e}")
        print(f"Hata: Ayarlar kaydedilirken hata oluştu: {e}")
        return False

# Uygulama başladığında ayarları yükle ve global değişkenleri güncelle
_ilk_ayarlar = ayarlari_yukle()
ARKA_PLAN_KOYU_GRI = _ilk_ayarlar["ARKA_PLAN_KOYU_GRI"]
ARKA_PLAN_ORTA_GRI = _ilk_ayarlar["ARKA_PLAN_ORTA_GRI"]
YAZI_RENGI_BEYAZ = _ilk_ayarlar["YAZI_RENGI_BEYAZ"]
BUTON_AKTIF_ARKA_PLAN = _ilk_ayarlar["BUTON_AKTIF_ARKA_PLAN"]
GIRIS_KUTUSU_ARKA_PLAN = _ilk_ayarlar["GIRIS_KUTUSU_ARKA_PLAN"]
GIRIS_KUTUSU_YAZI_RENGI = _ilk_ayarlar["GIRIS_KUTUSU_YAZI_RENGI"]
CERCEVE_BASLIK_YAZI_RENGI = _ilk_ayarlar["CERCEVE_BASLIK_YAZI_RENGI"]
ACILIR_LISTE_YAZI_RENGI = _ilk_ayarlar["ACILIR_LISTE_YAZI_RENGI"]
ACILIR_LISTE_ACILIR_ARKA_PLAN = _ilk_ayarlar["ACILIR_LISTE_ACILIR_ARKA_PLAN"]
ACILIR_LISTE_ACILIR_YAZI_RENGI = _ilk_ayarlar["ACILIR_LISTE_ACILIR_YAZI_RENGI"]
KAYDIRMA_CUBUGU_YOL_ARKA_PLAN = _ilk_ayarlar["KAYDIRMA_CUBUGU_YOL_ARKA_PLAN"]
KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN = _ilk_ayarlar["KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN"]
KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN = _ilk_ayarlar["KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN"]
# Yeni boyut değişkenlerini global olarak tanımla
PENCERE_GENISLIGI = _ilk_ayarlar["PENCERE_GENISLIGI"]
PENCERE_YUKSEKLIGI = _ilk_ayarlar["PENCERE_YUKSEKLIGI"]
MENU_GENISLIGI = _ilk_ayarlar["MENU_GENISLIGI"]


# --- Yardımcı Fonksiyonlar ---
def kutuphane_verisi_yukle():
    """
    Kütüphane Excel dosyasını yükler. Eğer dosya yoksa, boş bir DataFrame ile oluşturur.
    """
    if not os.path.exists(KUTUPHANE_DOSYASI):
        df_kutuphane = pd.DataFrame(columns=["ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "durumu"])
        try:
            df_kutuphane.to_excel(KUTUPHANE_DOSYASI, index=False)
            print(f"'{KUTUPHANE_DOSYASI}' dosyası oluşturuldu.")
        except Exception as e:
            messagebox.showerror("Hata", f"Excel dosyası oluşturulurken bir hata oluştu: {e}")
            return pd.DataFrame()
    
    try:
        df_kutuphane = pd.read_excel(KUTUPHANE_DOSYASI)
        if 'ID' not in df_kutuphane.columns or df_kutuphane['ID'].isnull().all():
            df_kutuphane['ID'] = range(1, len(df_kutuphane) + 1)
            df_kutuphane.to_excel(KUTUPHANE_DOSYASI, index=False)
        return df_kutuphane
    except Exception as e:
        messagebox.showerror("Hata", f"'{KUTUPHANE_DOSYASI}' okunurken bir hata oluştu: {e}\nDosya bozuk olabilir veya açık olabilir.")
        return pd.DataFrame()

def kutuphane_verisi_kaydet(df_kutuphane):
    """
    Kütüphane DataFrame'ini Excel dosyasına kaydeder.
    """
    try:
        df_kutuphane.to_excel(KUTUPHANE_DOSYASI, index=False)
        return True
    except Exception as e:
        messagebox.showerror("Hata", f"Excel dosyasına kaydedilirken bir hata oluştu: {e}\nDosya açık olabilir veya yazma izni olmayabilir.")
        return False

def ana_ekran_penceresi_ac():
    ana_pencere = tk.Tk()
    ana_pencere.title("Ana Ekran")
    
    # Uygulama başladığında veya tema yenilendiğinde güncel ayarları yükle
    guncel_ayarlar = ayarlari_yukle()

    # Ekran boyutlarına göre pencere konumunu hesapla
    ekran_genisligi = ana_pencere.winfo_screenwidth()
    ekran_yuksekligi = ana_pencere.winfo_screenheight()
    x_konumu = ekran_genisligi // 2
    y_konumu = 0
    
    # Yüklü ayarlara göre pencere boyutunu ayarla
    pencere_genisligi_ayari = guncel_ayarlar.get("PENCERE_GENISLIGI", ekran_genisligi // 2)
    pencere_yuksekligi_ayari = guncel_ayarlar.get("PENCERE_YUKSEKLIGI", ekran_yuksekligi)

    ana_pencere.geometry(f"{pencere_genisligi_ayari}x{pencere_yuksekligi_ayari}+{x_konumu}+{y_konumu}")
    print("Ana ekran açıldı")

    # --- Tema Ayarları (ttk.Style ile) ---
    stil = ttk.Style()
    stil.theme_use("clam") # Daha fazla özelleştirme için "clam" temasını kullanıyoruz

    # Pencere üzerinde o an hangi içeriğin gösterildiğini takip etmek için
    ana_pencere._mevcut_icerik_adi = "Ana Sayfa" 

    # Menü durumu (açık/kapalı) ve genişliği için nonlocal değişkenler
    # Bu değişkenler, ana_ekran_penceresi_ac fonksiyonunun scope'unda tanımlanır
    # ve iç fonksiyonlar (toggle_menu, mevcut_temayi_uygula) tarafından erişilir ve değiştirilir.
    menu_acik_mi = False
    
    # menu_genisligi_ayari'nı başlangıçta ayarlar dosyasından al
    # toggle_menu içindeki menu_genisligi değişkeni bu değeri kullanacak
    menu_genisligi_icerden = guncel_ayarlar.get("MENU_GENISLIGI", 200)

    # --- Dinamik Tema Uygulama Fonksiyonu ---
    def mevcut_temayi_uygula():
        # Global renk değişkenlerini güncelle
        global ARKA_PLAN_KOYU_GRI, ARKA_PLAN_ORTA_GRI, YAZI_RENGI_BEYAZ, BUTON_AKTIF_ARKA_PLAN, \
               GIRIS_KUTUSU_ARKA_PLAN, GIRIS_KUTUSU_YAZI_RENGI, CERCEVE_BASLIK_YAZI_RENGI, ACILIR_LISTE_YAZI_RENGI, \
               ACILIR_LISTE_ACILIR_ARKA_PLAN, ACILIR_LISTE_ACILIR_YAZI_RENGI, \
               KAYDIRMA_CUBUGU_YOL_ARKA_PLAN, KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN, KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN, \
               PENCERE_GENISLIGI, PENCERE_YUKSEKLIGI, MENU_GENISLIGI

        yuklenen_ayarlar = ayarlari_yukle()
        ARKA_PLAN_KOYU_GRI = yuklenen_ayarlar["ARKA_PLAN_KOYU_GRI"]
        ARKA_PLAN_ORTA_GRI = yuklenen_ayarlar["ARKA_PLAN_ORTA_GRI"]
        YAZI_RENGI_BEYAZ = yuklenen_ayarlar["YAZI_RENGI_BEYAZ"]
        BUTON_AKTIF_ARKA_PLAN = yuklenen_ayarlar["BUTON_AKTIF_ARKA_PLAN"]
        GIRIS_KUTUSU_ARKA_PLAN = yuklenen_ayarlar["GIRIS_KUTUSU_ARKA_PLAN"]
        GIRIS_KUTUSU_YAZI_RENGI = yuklenen_ayarlar["GIRIS_KUTUSU_YAZI_RENGI"]
        CERCEVE_BASLIK_YAZI_RENGI = yuklenen_ayarlar["CERCEVE_BASLIK_YAZI_RENGI"]
        ACILIR_LISTE_YAZI_RENGI = yuklenen_ayarlar["ACILIR_LISTE_YAZI_RENGI"]
        ACILIR_LISTE_ACILIR_ARKA_PLAN = yuklenen_ayarlar["ACILIR_LISTE_ACILIR_ARKA_PLAN"]
        ACILIR_LISTE_ACILIR_YAZI_RENGI = yuklenen_ayarlar["ACILIR_LISTE_ACILIR_YAZI_RENGI"]
        KAYDIRMA_CUBUGU_YOL_ARKA_PLAN = yuklenen_ayarlar["KAYDIRMA_CUBUGU_YOL_ARKA_PLAN"]
        KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN = yuklenen_ayarlar["KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN"]
        KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN = yuklenen_ayarlar["KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN"]
        
        # Boyut ayarlarını güncelle
        nonlocal menu_genisligi_icerden # menu_genisligi_icerden'i güncelle
        PENCERE_GENISLIGI = yuklenen_ayarlar.get("PENCERE_GENISLIGI", ana_pencere.winfo_screenwidth() // 2)
        PENCERE_YUKSEKLIGI = yuklenen_ayarlar.get("PENCERE_YUKSEKLIGI", ana_pencere.winfo_screenheight())
        MENU_GENISLIGI = yuklenen_ayarlar.get("MENU_GENISLIGI", 200) # Global menü genişliğini güncelle
        menu_genisligi_icerden = MENU_GENISLIGI # nonlocal değişkeni de güncelle

        # Pencere boyutunu güncelle (konumu sabit tut)
        ana_pencere.geometry(f"{PENCERE_GENISLIGI}x{PENCERE_YUKSEKLIGI}+{ana_pencere.winfo_screenwidth() // 2}+{0}")
        
        # ttk.Style ayarlarını güncelle
        stil.configure("Treeview",
                        background=ARKA_PLAN_ORTA_GRI,
                        foreground=YAZI_RENGI_BEYAZ,
                        rowheight=25,
                        fieldbackground=ARKA_PLAN_ORTA_GRI)
        stil.map("Treeview",
                  background=[('selected', BUTON_AKTIF_ARKA_PLAN)],
                  foreground=[('selected', YAZI_RENGI_BEYAZ)]) # Seçili satır yazı rengi

        stil.configure("Treeview.Heading",
                        background=ARKA_PLAN_KOYU_GRI,
                        foreground=YAZI_RENGI_BEYAZ,
                        font=('Arial', 10, 'bold'))
        stil.map("Treeview.Heading",
                  background=[('active', ARKA_PLAN_ORTA_GRI)])

        stil.configure("TCombobox",
                        fieldbackground=GIRIS_KUTUSU_ARKA_PLAN, # Combobox giriş alanı arka planı
                        background=ARKA_PLAN_KOYU_GRI, # Combobox genel arka planı (açılır menü çerçevesi)
                        foreground=ACILIR_LISTE_YAZI_RENGI) # Combobox metin rengi
        stil.map("TCombobox",
                  fieldbackground=[('readonly', GIRIS_KUTUSU_ARKA_PLAN)],
                  selectbackground=[('readonly', ACILIR_LISTE_ACILIR_ARKA_PLAN)], # Açılır menü seçili öğe arka planı
                  selectforeground=[('readonly', ACILIR_LISTE_ACILIR_YAZI_RENGI)]) # Açılır menü seçili öğe yazı rengi
        
        # Combobox açılır menü listesi stili
        stil.configure("TCombobox.Listbox",
                        background=ACILIR_LISTE_ACILIR_ARKA_PLAN,
                        foreground=ACILIR_LISTE_ACILIR_YAZI_RENGI,
                        selectbackground=BUTON_AKTIF_ARKA_PLAN,
                        selectforeground=YAZI_RENGI_BEYAZ)


        # Kaydırma Çubuğu Stili
        stil.configure("TScrollbar",
                        background=KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN, # Sürgü rengi
                        troughcolor=KAYDIRMA_CUBUGU_YOL_ARKA_PLAN, # Yol rengi
                        bordercolor=KAYDIRMA_CUBUGU_YOL_ARKA_PLAN,
                        arrowcolor=YAZI_RENGI_BEYAZ)
        stil.map("TScrollbar",
                  background=[('active', KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN)])

        # Tkinter widget renklerini doğrudan güncelle (ana çerçeveler ve menü butonları)
        ana_pencere.config(bg=ARKA_PLAN_KOYU_GRI)
        menu_cubugu.config(bg=ARKA_PLAN_KOYU_GRI)
        menu_butonu.config(bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ)
        menu_cercevesi.config(bg=ARKA_PLAN_KOYU_GRI)
        ana_icerik_cercevesi.config(bg=ARKA_PLAN_KOYU_GRI)

        # Menü öğesi butonlarını güncelle
        for oge in [menu_oge1, menu_oge2, menu_oge3, menu_oge4]:
            oge.config(bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ)

        # Menü açıkken genişliğini güncelle, kapalıysa 0 tut
        if menu_acik_mi:
             menu_cercevesi.config(width=menu_genisligi_icerden)
        else:
             menu_cercevesi.config(width=0)


        # Mevcut içeriği yeniden oluşturarak tüm widget'ların renklerini güncelle
        # Bu, her bir içeriğin kendi içinde widget'larını güncelleyecek
        icerigi_goster(ana_pencere._mevcut_icerik_adi)


    # --- Menü Çubuğu ve Buton ---
    menu_cubugu = tk.Frame(ana_pencere, bg=ARKA_PLAN_KOYU_GRI, height=40)
    menu_cubugu.pack(side="top", fill="x")

    menu_butonu = tk.Button(menu_cubugu, text="☰ Menü", command=lambda: menuyu_ac_kapa(),
                            bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ,
                            relief="flat", padx=10, pady=5)
    menu_butonu.pack(side="left", padx=10, pady=5)

    # --- Sol Menü Çerçevesi ---
    menu_cercevesi = tk.Frame(ana_pencere, bg=ARKA_PLAN_KOYU_GRI, width=0)
    menu_cercevesi.pack(side="left", fill="y", expand=False)
    menu_cercevesi.pack_propagate(False)

    def menuyu_ac_kapa():
        nonlocal menu_acik_mi
        # menu_genisligi_icerden, bu scope'ta zaten ayarlar dosyasından gelen değerle güncellenmiş durumda.
        if menu_acik_mi:
            for i in range(menu_genisligi_icerden, -1, -11):
                menu_cercevesi.config(width=i)
                ana_pencere.update_idletasks()
                ana_pencere.after(5)
            menu_acik_mi = False
        else:
            for i in range(0, menu_genisligi_icerden + 1, 10):
                menu_cercevesi.config(width=i)
                ana_pencere.update_idletasks()
                ana_pencere.after(5)
            menu_acik_mi = True

    # --- Ana Sayfa İçeriği Oluşturma Fonksiyonu ---
    def ana_sayfa_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Kütüphanedeki Kitaplar", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        agac_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        agac_cercevesi.pack(fill="both", expand=True, padx=20, pady=10)

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=200)
        agac_gorunumu.column("Yazar", width=150)
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=120)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")

        df_kutuphane_verisi = kutuphane_verisi_yukle()
        if not df_kutuphane_verisi.empty:
            for index, satir in df_kutuphane_verisi.iterrows():
                agac_gorunumu.insert("", "end", values=(satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"]))
        else:
            tk.Label(agac_cercevesi, text="Kütüphanede henüz kitap bulunmamaktadır.", bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).pack(pady=20) 

        kaydirma_cubugu = ttk.Scrollbar(agac_cercevesi, orient="vertical", command=agac_gorunumu.yview)
        agac_gorunumu.configure(yscrollcommand=kaydirma_cubugu.set)

        kaydirma_cubugu.pack(side="right", fill="y")
        agac_gorunumu.pack(side="left", fill="both", expand=True)

    # --- Kitap Yönetimi İçeriği Oluşturma Fonksiyonu ---
    def kitap_yonetimi_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Kitap Yönetimi", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        agac_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        agac_cercevesi.pack(fill="both", expand=True, padx=20, pady=10)

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=180)
        agac_gorunumu.column("Yazar", width=120)
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=100)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")

        kaydirma_cubugu = ttk.Scrollbar(agac_cercevesi, orient="vertical", command=agac_gorunumu.yview)
        agac_gorunumu.configure(yscrollcommand=kaydirma_cubugu.set)

        kaydirma_cubugu.pack(side="right", fill="y")
        agac_gorunumu.pack(side="left", fill="both", expand=True)

        def agac_gorunumunu_yenile():
            for oge in agac_gorunumu.get_children():
                agac_gorunumu.delete(oge)
            df_kutuphane_verisi = kutuphane_verisi_yukle()
            if not df_kutuphane_verisi.empty:
                for index, satir in df_kutuphane_verisi.iterrows():
                    agac_gorunumu.insert("", "end", values=(satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"]))
            else:
                pass 
        
        agac_gorunumunu_yenile()

        form_cercevesi = tk.LabelFrame(ust_cerceve, text="Kitap Bilgileri", bg=ARKA_PLAN_KOYU_GRI, fg=CERCEVE_BASLIK_YAZI_RENGI, padx=10, pady=10) 
        form_cercevesi.pack(fill="x", padx=20, pady=10)

        etiketler = ["Kitap Adı:", "Yazar:", "Sayfa Sayısı:", "Basım Markası:", "Durumu:"]
        giris_kutulari = {}
        for i, etiket_metni in enumerate(etiketler):
            tk.Label(form_cercevesi, text=etiket_metni, bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).grid(row=i, column=0, sticky="w", pady=2)
            if etiket_metni == "Durumu:":
                durum_secenekleri = ["Mevcut", "Ödünç Verildi"]
                durum_degiskeni = tk.StringVar(value=durum_secenekleri[0])
                durum_acilir_liste = ttk.Combobox(form_cercevesi, textvariable=durum_degiskeni, values=durum_secenekleri, state="readonly")
                durum_acilir_liste.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
                giris_kutulari["Durumu"] = durum_acilir_liste
            else:
                giris_kutusu = tk.Entry(form_cercevesi, width=40, bg=GIRIS_KUTUSU_ARKA_PLAN, fg=GIRIS_KUTUSU_YAZI_RENGI) 
                giris_kutusu.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
                giris_kutulari[etiket_metni.replace(":", "")] = giris_kutusu
        
        buton_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        buton_cercevesi.pack(fill="x", padx=20, pady=10)

        def formu_temizle():
            for anahtar in giris_kutulari:
                if isinstance(giris_kutulari[anahtar], ttk.Combobox):
                    giris_kutulari[anahtar].set("Mevcut")
                else:
                    giris_kutulari[anahtar].delete(0, tk.END)

        def kitap_ekle():
            df_kutuphane_verisi = kutuphane_verisi_yukle()
            sonraki_id = 1 if df_kutuphane_verisi.empty else df_kutuphane_verisi["ID"].max() + 1

            kitap_adi_girisi = giris_kutulari["Kitap Adı"].get().strip()
            yazar_girisi = giris_kutulari["Yazar"].get().strip()
            sayfa_sayisi_girisi = giris_kutulari["Sayfa Sayısı"].get().strip()
            basim_markasi_girisi = giris_kutulari["Basım Markası"].get().strip()
            durum_girisi = giris_kutulari["Durumu"].get().strip()
            kayit_tarihi_girisi = datetime.date.today().strftime("%Y-%m-%d")

            if not kitap_adi_girisi or not yazar_girisi or not sayfa_sayisi_girisi or not basim_markasi_girisi:
                messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
                return

            try:
                sayfa_sayisi_girisi = int(sayfa_sayisi_girisi)
                if sayfa_sayisi_girisi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Geçersiz Sayfa Sayısı", "Sayfa sayısı pozitif bir sayı olmalıdır.")
                return

            yeni_kitap_verisi = pd.DataFrame([{
                "ID": sonraki_id,
                "Kitap Adı": kitap_adi_girisi,
                "Yazar": yazar_girisi,
                "Sayfa Sayısı": sayfa_sayisi_girisi,
                "Basım Markası": basim_markasi_girisi,
                "Kayıt Tarihi": kayit_tarihi_girisi,
                "durumu": durum_girisi
            }])
            
            guncellenmis_df = pd.concat([df_kutuphane_verisi, yeni_kitap_verisi], ignore_index=True)
            if kutuphane_verisi_kaydet(guncellenmis_df):
                messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi.")
                agac_gorunumunu_yenile()
                formu_temizle()
            else:
                messagebox.showerror("Hata", "Kitap eklenirken bir sorun oluştu.")

        def kitap_sil():
            secili_oge = agac_gorunumu.focus()
            if not secili_oge:
                messagebox.showwarning("Seçim Yok", "Lütfen silmek istediğiniz kitabı seçin.")
                return

            onay = messagebox.askyesno("Silme Onayı", "Seçilen kitabı silmek istediğinizden emin misiniz?")
            if onay:
                selected_id = agac_gorunumu.item(secili_oge, "values")[0]
                df_kutuphane_verisi = kutuphane_verisi_yukle()
                guncellenmis_df = df_kutuphane_verisi[df_kutuphane_verisi["ID"] != selected_id]
                if kutuphane_verisi_kaydet(guncellenmis_df):
                    messagebox.showinfo("Başarılı", "Kitap başarıyla silindi.")
                    agac_gorunumunu_yenile()
                else:
                    messagebox.showerror("Hata", "Kitap silinirken bir sorun oluştu.")

        def kitap_duzenleme_formu():
            secili_oge = agac_gorunumu.focus()
            if not secili_oge:
                messagebox.showwarning("Seçim Yok", "Lütfen düzenlemek istediğiniz kitabı seçin.")
                return
            
            degerler = agac_gorunumu.item(secili_oge, "values")
            giris_kutulari["Kitap Adı"].delete(0, tk.END)
            giris_kutulari["Kitap Adı"].insert(0, degerler[1])
            giris_kutulari["Yazar"].delete(0, tk.END)
            giris_kutulari["Yazar"].insert(0, degerler[2])
            giris_kutulari["Sayfa Sayısı"].delete(0, tk.END)
            giris_kutulari["Sayfa Sayısı"].insert(0, degerler[3])
            giris_kutulari["Basım Markası"].delete(0, tk.END)
            giris_kutulari["Basım Markası"].insert(0, degerler[4])
            giris_kutulari["Durumu"].set(degerler[6])

            kitap_duzenle_butonu.config(text="Değişiklikleri Kaydet", command=lambda: duzenlenen_kitabi_kaydet(secili_oge))
            kitap_ekle_butonu.config(state="disabled")
            kitap_sil_butonu.config(state="disabled")

        def duzenlenen_kitabi_kaydet(secili_oge):
            secili_id = agac_gorunumu.item(secili_oge, "values")[0]
            df_kutuphane_verisi = kutuphane_verisi_yukle()

            kitap_adi_girisi = giris_kutulari["Kitap Adı"].get().strip()
            yazar_girisi = giris_kutulari["Yazar"].get().strip()
            sayfa_sayisi_girisi = giris_kutulari["Sayfa Sayısı"].get().strip()
            basim_markasi_girisi = giris_kutulari["Basım Markası"].get().strip()
            durum_girisi = giris_kutulari["Durumu"].get().strip()

            if not kitap_adi_girisi or not yazar_girisi or not sayfa_sayisi_girisi or not basim_markasi_girisi:
                messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
                return

            try:
                sayfa_sayisi_girisi = int(sayfa_sayisi_girisi)
                if sayfa_sayisi_girisi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Geçersiz Sayfa Sayısı", "Sayfa sayısı pozitif bir sayı olmalıdır.")
                return

            guncellenecek_indeks = df_kutuphane_verisi[df_kutuphane_verisi["ID"] == secili_id].index
            if not guncellenecek_indeks.empty:
                df_kutuphane_verisi.loc[guncellenecek_indeks, "Kitap Adı"] = kitap_adi_girisi
                df_kutuphane_verisi.loc[guncellenecek_indeks, "Yazar"] = yazar_girisi
                df_kutuphane_verisi.loc[guncellenecek_indeks, "Sayfa Sayısı"] = sayfa_sayisi_girisi
                df_kutuphane_verisi.loc[guncellenecek_indeks, "Basım Markası"] = basim_markasi_girisi
                df_kutuphane_verisi.loc[guncellenecek_indeks, "durumu"] = durum_girisi

                if kutuphane_verisi_kaydet(df_kutuphane_verisi):
                    messagebox.showinfo("Başarılı", "Kitap başarıyla güncellendi.")
                    agac_gorunumunu_yenile()
                    formu_temizle()
                    kitap_duzenle_butonu.config(text="Kitabı Düzenle", command=kitap_duzenleme_formu)
                    kitap_ekle_butonu.config(state="normal")
                    kitap_sil_butonu.config(state="normal")
                else:
                    messagebox.showerror("Hata", "Kitap güncellenirken bir sorun oluştu.")
            else:
                messagebox.showerror("Hata", "Düzenlenecek kitap bulunamadı.")

        def odunc_durumunu_degistir():
            secili_oge = agac_gorunumu.focus()
            if not secili_oge:
                messagebox.showwarning("Seçim Yok", "Lütfen durumunu değiştirmek istediğiniz kitabı seçin.")
                return

            secili_id = agac_gorunumu.item(secili_oge, "values")[0]
            df_kutuphane_verisi = kutuphane_verisi_yukle()

            guncellenecek_indeks = df_kutuphane_verisi[df_kutuphane_verisi["ID"] == secili_id].index
            if not guncellenecek_indeks.empty:
                mevcut_durum = df_kutuphane_verisi.loc[guncellenecek_indeks, "durumu"].iloc[0]
                yeni_durum = "Ödünç Verildi" if mevcut_durum == "Mevcut" else "Mevcut"
                
                df_kutuphane_verisi.loc[guncellenecek_indeks, "durumu"] = yeni_durum
                
                if kutuphane_verisi_kaydet(df_kutuphane_verisi):
                    messagebox.showinfo("Başarılı", f"Kitap durumu '{yeni_durum}' olarak güncellendi.")
                    agac_gorunumunu_yenile()
                else:
                    messagebox.showerror("Hata", "Kitap durumu güncellenirken bir sorun oluştu.")
            else:
                messagebox.showerror("Hata", "Kitap bulunamadı.")

        kitap_ekle_butonu = tk.Button(buton_cercevesi, text="Kitap Ekle", command=kitap_ekle,
                                    bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        kitap_ekle_butonu.pack(side="left", padx=5, pady=5)

        kitap_duzenle_butonu = tk.Button(buton_cercevesi, text="Kitabı Düzenle", command=kitap_duzenleme_formu,
                                     bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        kitap_duzenle_butonu.pack(side="left", padx=5, pady=5)

        kitap_sil_butonu = tk.Button(buton_cercevesi, text="Kitabı Sil", command=kitap_sil,
                                       bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        kitap_sil_butonu.pack(side="left", padx=5, pady=5)

        odunc_iade_butonu = tk.Button(buton_cercevesi, text="Durumu Değiştir (Ödünç/Mevcut)", command=odunc_durumunu_degistir,
                                         bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        odunc_iade_butonu.pack(side="left", padx=5, pady=5)

        temizle_butonu = tk.Button(buton_cercevesi, text="Formu Temizle", command=formu_temizle,
                                 bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        temizle_butonu.pack(side="left", padx=5, pady=5)

    # --- Ödünç Kitaplar İçeriği Oluşturma Fonksiyonu ---
    def odunc_kitaplar_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Ödünç Verilen Kitaplar", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        agac_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        agac_cercevesi.pack(fill="both", expand=True, padx=20, pady=10)

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=200)
        agac_gorunumu.column("Yazar", width=150)
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=120)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")

        df_kutuphane_verisi = kutuphane_verisi_yukle()
        odunc_kitaplar_verisi = df_kutuphane_verisi[df_kutuphane_verisi["durumu"] == "Ödünç Verildi"]

        if not odunc_kitaplar_verisi.empty:
            for index, satir in odunc_kitaplar_verisi.iterrows():
                agac_gorunumu.insert("", "end", values=(satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"]))
        else:
            tk.Label(agac_cercevesi, text="Henüz ödünç verilmiş kitap bulunmamaktadır.", bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).pack(pady=20) 

        kaydirma_cubugu = ttk.Scrollbar(agac_cercevesi, orient="vertical", command=agac_gorunumu.yview)
        agac_gorunumu.configure(yscrollcommand=kaydirma_cubugu.set)

        kaydirma_cubugu.pack(side="right", fill="y")
        agac_gorunumu.pack(side="left", fill="both", expand=True)

    # --- Ayarlar İçeriği Oluşturma Fonksiyonu ---
    def ayarlar_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Uygulama Ayarları", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        # Renk Ayarları Çerçevesi
        renk_ayarlari_form_cercevesi = tk.LabelFrame(ust_cerceve, text="Tema Renkleri", bg=ARKA_PLAN_KOYU_GRI, fg=CERCEVE_BASLIK_YAZI_RENGI, padx=10, pady=10)
        renk_ayarlari_form_cercevesi.pack(fill="x", padx=20, pady=10)

        renk_giris_kutulari = {} # Giriş alanlarını tutmak için
        renk_onizlemeleri = {} # Renk önizleme çerçevelerini tutmak için
        
        renk_etiketleri = {
            "ARKA_PLAN_KOYU_GRI": "Ana Arka Plan Rengi:",
            "ARKA_PLAN_ORTA_GRI": "İkincil Arka Plan Rengi:",
            "YAZI_RENGI_BEYAZ": "Genel Yazı Rengi:",
            "BUTON_AKTIF_ARKA_PLAN": "Buton Aktif Arka Plan:",
            "GIRIS_KUTUSU_ARKA_PLAN": "Giriş Kutusu Arka Planı:",
            "GIRIS_KUTUSU_YAZI_RENGI": "Giriş Kutusu Yazı Rengi:",
            "CERCEVE_BASLIK_YAZI_RENGI": "Çerçeve Başlık Yazı Rengi:",
            "ACILIR_LISTE_YAZI_RENGI": "Açılır Liste Yazı Rengi:",
            "ACILIR_LISTE_ACILIR_ARKA_PLAN": "Açılır Liste Arka Planı:",
            "ACILIR_LISTE_ACILIR_YAZI_RENGI": "Açılır Liste Öğesi Yazı Rengi:",
            "KAYDIRMA_CUBUGU_YOL_ARKA_PLAN": "Kaydırma Çubuğu Yolu Rengi:",
            "KAYDIRMA_CUBUGU_SURGU_ARKA_PLAN": "Kaydırma Çubuğu Sürgü Rengi:",
            "KAYDIRMA_CUBUGU_SURGU_AKTIF_ARKA_PLAN": "Kaydırma Çubuğu Sürgü Aktif Rengi:"
        }

        mevcut_ayarlar = ayarlari_yukle() # Mevcut ayarları yükle

        for i, (anahtar, etiket_metni) in enumerate(renk_etiketleri.items()):
            tk.Label(renk_ayarlari_form_cercevesi, text=etiket_metni, bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).grid(row=i, column=0, sticky="w", pady=2)
            
            giris_kutusu = tk.Entry(renk_ayarlari_form_cercevesi, width=15, bg=GIRIS_KUTUSU_ARKA_PLAN, fg=GIRIS_KUTUSU_YAZI_RENGI) 
            giris_kutusu.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            giris_kutusu.insert(0, mevcut_ayarlar.get(anahtar, ""))
            renk_giris_kutulari[anahtar] = giris_kutusu
            
            # Renk seçici butonu
            renk_sec_butonu = tk.Button(renk_ayarlari_form_cercevesi, text="Seç",
                                            command=lambda k=anahtar, e=giris_kutusu, p=None: renk_sec(k, e, p), 
                                            bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
            renk_sec_butonu.grid(row=i, column=2, padx=2)

            # Renk önizleme
            onizleme_cercevesi = tk.Frame(renk_ayarlari_form_cercevesi, width=20, height=20, bg=mevcut_ayarlar.get(anahtar, "#FFFFFF5F"), bd=1, relief="solid")
            onizleme_cercevesi.grid(row=i, column=3, padx=5)
            renk_onizlemeleri[anahtar] = onizleme_cercevesi
            # Renk seçici butonunun command'ini güncelleyelim, onizleme_cercevesi'ni de alsın
            renk_sec_butonu.config(command=lambda k=anahtar, e=giris_kutusu, p=onizleme_cercevesi: renk_sec(k, e, p))


        def renk_sec(anahtar, giris_kutusu_widgeti, onizleme_widgeti):
            color_code = colorchooser.askcolor(title=f"{renk_etiketleri[anahtar]} Seç")
            if color_code[1]: # Eğer bir renk seçildiyse (None değilse)
                giris_kutusu_widgeti.delete(0, tk.END)
                giris_kutusu_widgeti.insert(0, color_code[1])
                if onizleme_widgeti: # Eğer önizleme widget'ı varsa güncelle
                    onizleme_widgeti.config(bg=color_code[1])

        def onizlemeleri_guncelle():
            for anahtar, giris_kutusu in renk_giris_kutulari.items():
                hex_renk_kodu = giris_kutusu.get()
                try:
                    if len(hex_renk_kodu) == 7 and hex_renk_kodu.startswith("#"):
                        # Renk kodu geçerli ise önizlemeyi güncelle
                        renk_onizlemeleri[anahtar].config(bg=hex_renk_kodu)
                    else:
                        # Geçersiz renk kodu ise kırmızı göster
                        renk_onizlemeleri[anahtar].config(bg="red")
                except tk.TclError:
                    renk_onizlemeleri[anahtar].config(bg="red")

        # Giriş alanlarına her tuş bırakıldığında önizlemeyi güncelle
        for giris_kutusu in renk_giris_kutulari.values():
            giris_kutusu.bind("<KeyRelease>", lambda event=None: onizlemeleri_guncelle())

        # Boyut Ayarları Çerçevesi
        boyut_ayarlari_form_cercevesi = tk.LabelFrame(ust_cerceve, text="Pencere ve Menü Boyutları", bg=ARKA_PLAN_KOYU_GRI, fg=CERCEVE_BASLIK_YAZI_RENGI, padx=10, pady=10)
        boyut_ayarlari_form_cercevesi.pack(fill="x", padx=20, pady=10)

        boyut_etiketleri = {
            "PENCERE_GENISLIGI": "Pencere Genişliği:",
            "PENCERE_YUKSEKLIGI": "Pencere Yüksekliği:",
            "MENU_GENISLIGI": "Menü Genişliği:"
        }
        boyut_giris_kutulari = {} # Giriş alanlarını tutmak için

        for i, (key, label_text) in enumerate(boyut_etiketleri.items()):
            tk.Label(boyut_ayarlari_form_cercevesi, text=label_text, bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(boyut_ayarlari_form_cercevesi, width=15, bg=GIRIS_KUTUSU_ARKA_PLAN, fg=GIRIS_KUTUSU_YAZI_RENGI)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            entry.insert(0, str(mevcut_ayarlar.get(key, ""))) # Sayısal değerleri string olarak ekle
            boyut_giris_kutulari[key] = entry


        def ayarlari_kaydet_ve_uygula_islemi():
            new_settings = {}
            
            # Renkleri kaydet
            for key, entry in renk_giris_kutulari.items():
                hex_color = entry.get().strip()
                if not (len(hex_color) == 7 and hex_color.startswith("#")):
                    messagebox.showwarning("Geçersiz Renk Kodu", f"'{renk_etiketleri[key]}' için geçerli bir hex renk kodu girin (örn: #RRGGBB).")
                    return
                new_settings[key] = hex_color

            # Boyutları kaydet
            for key, entry in boyut_giris_kutulari.items():
                try:
                    boyut_degeri = int(entry.get().strip())
                    if boyut_degeri <= 0:
                        messagebox.showwarning("Geçersiz Boyut", f"'{boyut_etiketleri[key]}' için pozitif bir sayı girin.")
                        return
                    new_settings[key] = boyut_degeri
                except ValueError:
                    messagebox.showwarning("Geçersiz Boyut", f"'{boyut_etiketleri[key]}' için sayısal bir değer girin.")
                    return

            if ayarlari_kaydet(new_settings):
                messagebox.showinfo("Başarılı", "Ayarlar kaydedildi ve uygulandı.")
                mevcut_temayi_uygula() # Yeni temayı hemen uygula
            else:
                messagebox.showerror("Hata", "Ayarlar kaydedilirken bir sorun oluştu.")

        def sistem_varsayilan_renklerini_yukle_action():
            # Tüm varsayılan ayarları al (hem renk hem boyut)
            varsayilan_ayarlar = varsayilan_ayarlari_olustur() 
            if ayarlari_kaydet(varsayilan_ayarlar):
                messagebox.showinfo("Başarılı", "Varsayılan ayarlar yüklendi ve uygulandı.")
                
                # Renk giriş kutularını güncelle
                for key, entry in renk_giris_kutulari.items():
                    entry.delete(0, tk.END)
                    entry.insert(0, varsayilan_ayarlar.get(key, ""))
                onizlemeleri_guncelle() # Renk önizlemelerini de güncelle

                # Boyut giriş kutularını güncelle
                for key, entry in boyut_giris_kutulari.items():
                    entry.delete(0, tk.END)
                    entry.insert(0, str(varsayilan_ayarlar.get(key, ""))) # Sayısal değerleri string olarak ekle

                mevcut_temayi_uygula() # Temayı hemen uygula
            else:
                messagebox.showerror("Hata", "Varsayılan ayarlar yüklenirken bir sorun oluştu.")


        # Butonlar ayrı bir çerçevede toplanabilir, kolay yönetim için
        ayarlar_buton_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        ayarlar_buton_cercevesi.pack(fill="x", padx=20, pady=10)

        kaydet_butonu = tk.Button(ayarlar_buton_cercevesi, text="Ayarları Kaydet ve Uygula", command=ayarlari_kaydet_ve_uygula_islemi,
                                bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        kaydet_butonu.pack(side="left", padx=5, pady=5)

        sistem_varsayilan_butonu = tk.Button(ayarlar_buton_cercevesi, text="Varsayılan Ayarları Yükle", command=sistem_varsayilan_renklerini_yukle_action,
                                             bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        sistem_varsayilan_butonu.pack(side="left", padx=5, pady=5)

        # İlk önizlemeleri güncelle
        onizlemeleri_guncelle()


    # --- Menü Öğeleri ---
    def icerigi_goster(icerik_adi):
        # Pencere üzerinde o an hangi içeriğin gösterildiğini güncelle
        ana_pencere._mevcut_icerik_adi = icerik_adi 

        print(f"'{icerik_adi}' seçildi.")
        
        ana_icerik_cercevesi.config(bg=ARKA_PLAN_KOYU_GRI) 
        for widget in ana_icerik_cercevesi.winfo_children():
            widget.destroy() # Mevcut içeriği temizle
        
        if icerik_adi == "Ana Sayfa":
            ana_sayfa_icerigi_olustur(ana_icerik_cercevesi)
        elif icerik_adi == "Kitap Listesi":
            kitap_yonetimi_icerigi_olustur(ana_icerik_cercevesi)
        elif icerik_adi == "Ödünç Kitaplar":
            # Düzeltme: 'ana_icerceivesi' yerine 'ana_icerik_cercevesi' kullanılmalı
            odunc_kitaplar_icerigi_olustur(ana_icerik_cercevesi)
        elif icerik_adi == "Ayarlar":
            ayarlar_icerigi_olustur(ana_icerik_cercevesi)

    menu_oge1 = tk.Button(menu_cercevesi, text="Ana Sayfa", command=lambda: icerigi_goster("Ana Sayfa"), anchor="w", padx=10, pady=5,
                           bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
    menu_oge1.pack(fill="x", pady=5)

    menu_oge2 = tk.Button(menu_cercevesi, text="Kitap Listesi", command=lambda: icerigi_goster("Kitap Listesi"), anchor="w", padx=10, pady=5,
                           bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
    menu_oge2.pack(fill="x", pady=5)

    menu_oge3 = tk.Button(menu_cercevesi, text="Ödünç Kitaplar", command=lambda: icerigi_goster("Ödünç Kitaplar"), anchor="w", padx=10, pady=5,
                           bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
    menu_oge3.pack(fill="x", pady=5)

    menu_oge4 = tk.Button(menu_cercevesi, text="Ayarlar", command=lambda: icerigi_goster("Ayarlar"), anchor="w", padx=10, pady=5,
                           bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
    menu_oge4.pack(fill="x", pady=5)

    # --- Ana İçerik Çerçevesi ---
    ana_icerik_cercevesi = tk.Frame(ana_pencere, bg=ARKA_PLAN_KOYU_GRI)
    ana_icerik_cercevesi.pack(side="right", fill="both", expand=True)
    
    # Uygulama başladığında temayı uygula ve Ana Sayfayı göster
    mevcut_temayi_uygula()
    icerigi_goster("Ana Sayfa") # Bu, yüklenen temayı kullanacaktır

    ana_pencere.mainloop()

# Uygulamayı başlat
if __name__ == "__main__":
    ana_ekran_penceresi_ac()