import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import pandas as pd
import datetime
import os
import json

# Excel dosyası yollarını tanımla
KUTUPHANE_DOSYASI = "kutuphane_tablosu.xlsx"
ODUNC_DOSYASI = "odunc_verilen_kitaplar.xlsx" # Bu dosya artık kullanılmıyor, tüm veriler KUTUPHANE_DOSYASI içinde.
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
    Yeni sütunlar: "Ödünç Alan", "Teslim Tarihi"
    """
    gerekli_sutunlar = ["ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "durumu", "Ödünç Alan", "Teslim Tarihi"]
    
    if not os.path.exists(KUTUPHANE_DOSYASI):
        df = pd.DataFrame(columns=gerekli_sutunlar)
        try:
            df.to_excel(KUTUPHANE_DOSYASI, index=False)
            print(f"'{KUTUPHANE_DOSYASI}' dosyası oluşturuldu.")
        except Exception as e:
            messagebox.showerror("Hata", f"Excel dosyası oluşturulurken bir hata oluştu: {e}")
            return pd.DataFrame()
    
    try:
        df = pd.read_excel(KUTUPHANE_DOSYASI)
        
        # Eksik sütunları kontrol et ve ekle
        for sutun in gerekli_sutunlar:
            if sutun not in df.columns:
                df[sutun] = "" # Varsayılan boş değer
        
        # ID sütunu yoksa veya boşsa yeniden oluştur
        if 'ID' not in df.columns or df['ID'].isnull().all():
            df['ID'] = range(1, len(df) + 1)
            df.to_excel(KUTUPHANE_DOSYASI, index=False) # ID'yi güncelledikten sonra kaydet
            
        return df
    except Exception as e:
        messagebox.showerror("Hata", f"'{KUTUPHANE_DOSYASI}' okunurken bir hata oluştu: {e}\nDosya bozuk olabilir veya açık olabilir.")
        return pd.DataFrame(columns=gerekli_sutunlar) # Hata durumunda boş DataFrame döndür

def kutuphane_verisi_kaydet(df):
    """
    Kütüphane DataFrame'ini Excel dosyasına kaydeder.
    """
    try:
        df.to_excel(KUTUPHANE_DOSYASI, index=False)
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
        for oge in [menu_oge1, menu_oge2, menu_oge3, menu_oge4, menu_oge5]: # menu_oge5 eklendi
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

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu", "Ödünç Alan", "Teslim Tarihi")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=120) # Genişlik ayarlandı
        agac_gorunumu.column("Yazar", width=100) # Genişlik ayarlandı
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=100)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")
        agac_gorunumu.column("Ödünç Alan", width=120)
        agac_gorunumu.column("Teslim Tarihi", width=100, anchor="center")

        df_kutuphane_verisi = kutuphane_verisi_yukle()
        if not df_kutuphane_verisi.empty:
            for index, satir in df_kutuphane_verisi.iterrows():
                agac_gorunumu.insert("", "end", values=(
                    satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], 
                    satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"],
                    satir.get("Ödünç Alan", ""), satir.get("Teslim Tarihi", "") # Yeni sütunları güvenli al
                ))
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

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu", "Ödünç Alan", "Teslim Tarihi")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=120) # Genişlik ayarlandı
        agac_gorunumu.column("Yazar", width=100) # Genişlik ayarlandı
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=100)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")
        agac_gorunumu.column("Ödünç Alan", width=120)
        agac_gorunumu.column("Teslim Tarihi", width=100, anchor="center")

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
                    agac_gorunumu.insert("", "end", values=(
                        satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], 
                        satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"],
                        satir.get("Ödünç Alan", ""), satir.get("Teslim Tarihi", "") # Yeni sütunları güvenli al
                    ))
            else:
                pass 
        
        agac_gorunumunu_yenile()

        form_cercevesi = tk.LabelFrame(ust_cerceve, text="Kitap Bilgileri", bg=ARKA_PLAN_KOYU_GRI, fg=CERCEVE_BASLIK_YAZI_RENGI, padx=10, pady=10) 
        form_cercevesi.pack(fill="x", padx=20, pady=10)

        etiketler = ["Kitap Adı:", "Yazar:", "Sayfa Sayısı:", "Basım Markası:", "Durumu:", "Ödünç Alan:", "Teslim Tarihi:"]
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
        
        button_frame = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        button_frame.pack(fill="x", padx=20, pady=10)

        def clear_form():
            for key in giris_kutulari:
                if isinstance(giris_kutulari[key], ttk.Combobox):
                    giris_kutulari[key].set("Mevcut")
                else:
                    giris_kutulari[key].delete(0, tk.END)

        def add_book():
            df_kutuphane = kutuphane_verisi_yukle()
            next_id = 1 if df_kutuphane.empty else df_kutuphane["ID"].max() + 1

            kitap_adi = giris_kutulari["Kitap Adı"].get().strip()
            yazar = giris_kutulari["Yazar"].get().strip()
            sayfa_sayisi = giris_kutulari["Sayfa Sayısı"].get().strip()
            basim_markasi = giris_kutulari["Basım Markası"].get().strip()
            durumu = giris_kutulari["Durumu"].get().strip()
            odunc_alan = giris_kutulari["Ödünç Alan"].get().strip()
            teslim_tarihi = giris_kutulari["Teslim Tarihi"].get().strip()
            kayit_tarihi = datetime.date.today().strftime("%Y-%m-%d")

            if not kitap_adi or not yazar or not sayfa_sayisi or not basim_markasi:
                messagebox.showwarning("Eksik Bilgi", "Lütfen tüm zorunlu alanları doldurun.")
                return
            
            if durumu == "Ödünç Verildi" and (not odunc_alan or not teslim_tarihi):
                messagebox.showwarning("Eksik Bilgi", "Ödünç verilen kitap için 'Ödünç Alan' ve 'Teslim Tarihi' alanları zorunludur.")
                return
            
            if teslim_tarihi and not validate_date_format(teslim_tarihi):
                messagebox.showwarning("Geçersiz Tarih Formatı", "Teslim Tarihi formatı YYYY-MM-DD olmalıdır.")
                return

            try:
                sayfa_sayisi = int(sayfa_sayisi)
                if sayfa_sayisi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Geçersiz Sayfa Sayısı", "Sayfa sayısı pozitif bir sayı olmalıdır.")
                return

            new_book = pd.DataFrame([{
                "ID": next_id,
                "Kitap Adı": kitap_adi,
                "Yazar": yazar,
                "Sayfa Sayısı": sayfa_sayisi,
                "Basım Markası": basim_markasi,
                "Kayıt Tarihi": kayit_tarihi,
                "durumu": durumu,
                "Ödünç Alan": odunc_alan if durumu == "Ödünç Verildi" else "",
                "Teslim Tarihi": teslim_tarihi if durumu == "Ödünç Verildi" else ""
            }])
            
            updated_df = pd.concat([df_kutuphane, new_book], ignore_index=True)
            if kutuphane_verisi_kaydet(updated_df):
                messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi.")
                agac_gorunumunu_yenile()
                clear_form()
            else:
                messagebox.showerror("Hata", "Kitap eklenirken bir sorun oluştu.")

        def delete_book():
            selected_item = agac_gorunumu.focus()
            if not selected_item:
                messagebox.showwarning("Seçim Yok", "Lütfen silmek istediğiniz kitabı seçin.")
                return

            confirm = messagebox.askyesno("Silme Onayı", "Seçilen kitabı silmek istediğinizden emin misiniz?")
            if confirm:
                # selected_id'yi int'e dönüştür
                selected_id = int(agac_gorunumu.item(selected_item, "values")[0])
                df_kutuphane = kutuphane_verisi_yukle()
                updated_df = df_kutuphane[df_kutuphane["ID"] != selected_id]
                if kutuphane_verisi_kaydet(updated_df):
                    messagebox.showinfo("Başarılı", "Kitap başarıyla silindi.")
                    agac_gorunumunu_yenile()
                else:
                    messagebox.showerror("Hata", "Kitap silinirken bir sorun oluştu.")

        def edit_book_form():
            selected_item = agac_gorunumu.focus()
            if not selected_item:
                messagebox.showwarning("Seçim Yok", "Lütfen düzenlemek istediğiniz kitabı seçin.")
                return
            
            values = agac_gorunumu.item(selected_item, "values")
            giris_kutulari["Kitap Adı"].delete(0, tk.END)
            giris_kutulari["Kitap Adı"].insert(0, values[1])
            giris_kutulari["Yazar"].delete(0, tk.END)
            giris_kutulari["Yazar"].insert(0, values[2])
            giris_kutulari["Sayfa Sayısı"].delete(0, tk.END)
            giris_kutulari["Sayfa Sayısı"].insert(0, values[3])
            giris_kutulari["Basım Markası"].delete(0, tk.END)
            giris_kutulari["Basım Markası"].insert(0, values[4])
            giris_kutulari["Durumu"].set(values[6])
            giris_kutulari["Ödünç Alan"].delete(0, tk.END)
            giris_kutulari["Ödünç Alan"].insert(0, values[7] if len(values) > 7 else "") # Güvenli erişim
            giris_kutulari["Teslim Tarihi"].delete(0, tk.END)
            giris_kutulari["Teslim Tarihi"].insert(0, values[8] if len(values) > 8 else "") # Güvenli erişim

            edit_book_button.config(text="Değişiklikleri Kaydet", command=lambda: save_edited_book(selected_item))
            add_book_button.config(state="disabled")
            delete_book_button.config(state="disabled")

        def save_edited_book(selected_item):
            # selected_id'yi int'e dönüştür
            selected_id = int(agac_gorunumu.item(selected_item, "values")[0])
            df_kutuphane = kutuphane_verisi_yukle()

            kitap_adi = giris_kutulari["Kitap Adı"].get().strip()
            yazar = giris_kutulari["Yazar"].get().strip()
            sayfa_sayisi = giris_kutulari["Sayfa Sayısı"].get().strip()
            basim_markasi = giris_kutulari["Basım Markası"].get().strip()
            durumu = giris_kutulari["Durumu"].get().strip()
            odunc_alan = giris_kutulari["Ödünç Alan"].get().strip()
            teslim_tarihi = giris_kutulari["Teslim Tarihi"].get().strip()

            if not kitap_adi or not yazar or not sayfa_sayisi or not basim_markasi:
                messagebox.showwarning("Eksik Bilgi", "Lütfen tüm zorunlu alanları doldurun.")
                return
            
            if durumu == "Ödünç Verildi" and (not odunc_alan or not teslim_tarihi):
                messagebox.showwarning("Eksik Bilgi", "Ödünç verilen kitap için 'Ödünç Alan' ve 'Teslim Tarihi' alanları zorunludur.")
                return

            if teslim_tarihi and not validate_date_format(teslim_tarihi):
                messagebox.showwarning("Geçersiz Tarih Formatı", "Teslim Tarihi formatı YYYY-MM-DD olmalıdır.")
                return

            try:
                sayfa_sayisi = int(sayfa_sayisi)
                if sayfa_sayisi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Geçersiz Sayfa Sayısı", "Sayfa sayısı pozitif bir sayı olmalıdır.")
                return

            idx_to_update = df_kutuphane[df_kutuphane["ID"] == selected_id].index
            if not idx_to_update.empty:
                df_kutuphane.loc[idx_to_update, "Kitap Adı"] = kitap_adi
                df_kutuphane.loc[idx_to_update, "Yazar"] = yazar
                df_kutuphane.loc[idx_to_update, "Sayfa Sayısı"] = sayfa_sayisi
                df_kutuphane.loc[idx_to_update, "Basım Markası"] = basim_markasi
                df_kutuphane.loc[idx_to_update, "durumu"] = durumu
                df_kutuphane.loc[idx_to_update, "Ödünç Alan"] = odunc_alan if durumu == "Ödünç Verildi" else ""
                df_kutuphane.loc[idx_to_update, "Teslim Tarihi"] = teslim_tarihi if durumu == "Ödünç Verildi" else ""

                if kutuphane_verisi_kaydet(df_kutuphane):
                    messagebox.showinfo("Başarılı", "Kitap başarıyla güncellendi.")
                    agac_gorunumunu_yenile()
                    clear_form()
                    edit_book_button.config(text="Kitabı Düzenle", command=edit_book_form)
                    add_book_button.config(state="normal")
                    delete_book_button.config(state="normal")
                else:
                    messagebox.showerror("Hata", "Kitap güncellenirken bir sorun oluştu.")
            else:
                messagebox.showerror("Hata", "Düzenlenecek kitap bulunamadı.")

        def validate_date_format(date_str):
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False

        def toggle_borrow_status():
            selected_item = agac_gorunumu.focus()
            if not selected_item:
                messagebox.showwarning("Seçim Yok", "Lütfen durumunu değiştirmek istediğiniz kitabı seçin.")
                return

            # selected_id'yi int'e dönüştür
            selected_id = int(agac_gorunumu.item(selected_item, "values")[0])
            df_kutuphane = kutuphane_verisi_yukle()

            idx_to_update = df_kutuphane[df_kutuphane["ID"] == selected_id].index
            if not idx_to_update.empty:
                current_status = df_kutuphane.loc[idx_to_update, "durumu"].iloc[0]
                
                if current_status == "Mevcut":
                    # Kitap ödünç verilecek, bilgi al
                    borrow_dialog = tk.Toplevel(ust_cerceve)
                    borrow_dialog.title("Ödünç Bilgileri Girin")
                    borrow_dialog.transient(ust_cerceve.winfo_toplevel()) # Ana pencereye bağla
                    borrow_dialog.grab_set() # Pencereyi modal yap
                    
                    tk.Label(borrow_dialog, text="Ödünç Alan:").grid(row=0, column=0, padx=5, pady=5)
                    borrower_entry = tk.Entry(borrow_dialog)
                    borrower_entry.grid(row=0, column=1, padx=5, pady=5)

                    tk.Label(borrow_dialog, text="Teslim Tarihi (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
                    return_date_entry = tk.Entry(borrow_dialog)
                    return_date_entry.grid(row=1, column=1, padx=5, pady=5)

                    def save_borrow_info():
                        borrower_name = borrower_entry.get().strip()
                        return_date = return_date_entry.get().strip()

                        if not borrower_name or not return_date:
                            messagebox.showwarning("Eksik Bilgi", "Lütfen ödünç alan ve teslim tarihi bilgilerini doldurun.", parent=borrow_dialog)
                            return
                        
                        if not validate_date_format(return_date):
                            messagebox.showwarning("Geçersiz Tarih Formatı", "Teslim Tarihi formatı YYYY-MM-DD olmalıdır.", parent=borrow_dialog)
                            return
                        
                        df_kutuphane.loc[idx_to_update, "durumu"] = "Ödünç Verildi"
                        df_kutuphane.loc[idx_to_update, "Ödünç Alan"] = borrower_name
                        df_kutuphane.loc[idx_to_update, "Teslim Tarihi"] = return_date

                        if kutuphane_verisi_kaydet(df_kutuphane):
                            messagebox.showinfo("Başarılı", "Kitap başarıyla ödünç verildi.")
                            borrow_dialog.destroy()
                            icerigi_goster("Kitap Listesi") # Kitap listesini yenile
                            icerigi_goster("Ödünç Kitaplar") # Ödünç kitaplar listesini yenile
                            icerigi_goster("Hatırlatıcılar") # Hatırlatıcılar listesini yenile
                        else:
                            messagebox.showerror("Hata", "Kitap ödünç verilirken bir sorun oluştu.")
                            borrow_dialog.destroy()

                    def cancel_borrow_info():
                        borrow_dialog.destroy()

                    tk.Button(borrow_dialog, text="Kaydet", command=save_borrow_info).grid(row=2, column=0, pady=10)
                    tk.Button(borrow_dialog, text="İptal", command=cancel_borrow_info).grid(row=2, column=1, pady=10)

                else: # current_status == "Ödünç Verildi" (Kitap iade edilecek)
                    confirm_return = messagebox.askyesno("İade Onayı", "Kitabı iade etmek istediğinizden emin misiniz? Ödünç bilgileri temizlenecektir.")
                    if confirm_return:
                        df_kutuphane.loc[idx_to_update, "durumu"] = "Mevcut"
                        df_kutuphane.loc[idx_to_update, "Ödünç Alan"] = ""
                        df_kutuphane.loc[idx_to_update, "Teslim Tarihi"] = ""
                        
                        if kutuphane_verisi_kaydet(df_kutuphane):
                            messagebox.showinfo("Başarılı", "Kitap başarıyla iade alındı.")
                            icerigi_goster("Kitap Listesi") # Kitap listesini yenile
                            icerigi_goster("Ödünç Kitaplar") # Ödünç kitaplar listesini yenile
                            icerigi_goster("Hatırlatıcılar") # Hatırlatıcılar listesini yenile
                        else:
                            messagebox.showerror("Hata", "Kitap iade edilirken bir sorun oluştu.")
            else:
                messagebox.showerror("Hata", "Kitap bulunamadı.")

        add_book_button = tk.Button(button_frame, text="Kitap Ekle", command=add_book,
                                    bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        add_book_button.pack(side="left", padx=5, pady=5)

        edit_book_button = tk.Button(button_frame, text="Kitabı Düzenle", command=edit_book_form,
                                     bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        edit_book_button.pack(side="left", padx=5, pady=5)

        delete_book_button = tk.Button(button_frame, text="Kitabı Sil", command=delete_book,
                                       bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        delete_book_button.pack(side="left", padx=5, pady=5)

        borrow_return_button = tk.Button(button_frame, text="Durumu Değiştir (Ödünç/Mevcut)", command=toggle_borrow_status,
                                         bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        borrow_return_button.pack(side="left", padx=5, pady=5)

        clear_button = tk.Button(button_frame, text="Formu Temizle", command=clear_form,
                                 bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
        clear_button.pack(side="left", padx=5, pady=5)

    # --- Ödünç Kitaplar İçeriği Oluşturma Fonksiyonu ---
    def odunc_kitaplar_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Ödünç Verilen Kitaplar", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        agac_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        agac_cercevesi.pack(fill="both", expand=True, padx=20, pady=10)

        sutunlar = ("ID", "Kitap Adı", "Yazar", "Sayfa Sayısı", "Basım Markası", "Kayıt Tarihi", "Durumu", "Ödünç Alan", "Teslim Tarihi")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=120)
        agac_gorunumu.column("Yazar", width=100)
        agac_gorunumu.column("Sayfa Sayısı", width=80, anchor="center")
        agac_gorunumu.column("Basım Markası", width=100)
        agac_gorunumu.column("Kayıt Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Durumu", width=80, anchor="center")
        agac_gorunumu.column("Ödünç Alan", width=120)
        agac_gorunumu.column("Teslim Tarihi", width=100, anchor="center")

        df_kutuphane_verisi = kutuphane_verisi_yukle()
        odunc_kitaplar_verisi = df_kutuphane_verisi[df_kutuphane_verisi["durumu"] == "Ödünç Verildi"]

        if not odunc_kitaplar_verisi.empty:
            for index, satir in odunc_kitaplar_verisi.iterrows():
                agac_gorunumu.insert("", "end", values=(
                    satir["ID"], satir["Kitap Adı"], satir["Yazar"], satir["Sayfa Sayısı"], 
                    satir["Basım Markası"], satir["Kayıt Tarihi"], satir["durumu"],
                    satir.get("Ödünç Alan", ""), satir.get("Teslim Tarihi", "")
                ))
        else:
            tk.Label(agac_cercevesi, text="Henüz ödünç verilmiş kitap bulunmamaktadır.", bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).pack(pady=20) 

        kaydirma_cubugu = ttk.Scrollbar(agac_cercevesi, orient="vertical", command=agac_gorunumu.yview)
        agac_gorunumu.configure(yscrollcommand=kaydirma_cubugu.set)

        kaydirma_cubugu.pack(side="right", fill="y")
        agac_gorunumu.pack(side="left", fill="both", expand=True)

    # --- Hatırlatıcılar İçeriği Oluşturma Fonksiyonu ---
    def hatirlaticilar_icerigi_olustur(ust_cerceve):
        for widget in ust_cerceve.winfo_children():
            widget.destroy()

        tk.Label(ust_cerceve, text="Kitap Teslim Hatırlatıcıları", font=("Arial", 16, "bold"), bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, pady=10).pack(pady=(20, 10))

        agac_cercevesi = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        agac_cercevesi.pack(fill="both", expand=True, padx=20, pady=10)

        sutunlar = ("ID", "Kitap Adı", "Ödünç Alan", "Teslim Tarihi", "Kalan Gün/Durum")
        agac_gorunumu = ttk.Treeview(agac_cercevesi, columns=sutunlar, show="headings")

        for sutun in sutunlar:
            agac_gorunumu.heading(sutun, text=sutun, anchor="w")
            agac_gorunumu.column(sutun, width=100, anchor="w")

        agac_gorunumu.column("ID", width=50, anchor="center")
        agac_gorunumu.column("Kitap Adı", width=150)
        agac_gorunumu.column("Ödünç Alan", width=120)
        agac_gorunumu.column("Teslim Tarihi", width=100, anchor="center")
        agac_gorunumu.column("Kalan Gün/Durum", width=150, anchor="center")

        def hatirlatici_listesini_yenile():
            for oge in agac_gorunumu.get_children():
                agac_gorunumu.delete(oge)
            
            df_kutuphane_verisi = kutuphane_verisi_yukle()
            odunc_kitaplar_verisi = df_kutuphane_verisi[df_kutuphane_verisi["durumu"] == "Ödünç Verildi"]
            
            bugun = datetime.date.today()

            if not odunc_kitaplar_verisi.empty:
                for index, satir in odunc_kitaplar_verisi.iterrows():
                    teslim_tarihi_str = satir.get("Teslim Tarihi", "")
                    kalan_gun_durum = ""
                    if teslim_tarihi_str:
                        try:
                            teslim_tarihi_obj = datetime.datetime.strptime(str(teslim_tarihi_str), "%Y-%m-%d").date()
                            gun_farki = (teslim_tarihi_obj - bugun).days

                            if gun_farki < 0:
                                kalan_gun_durum = f"{-gun_farki} gün gecikmiş"
                                tag = 'gecikmis' # Gecikmiş kitaplar için tag
                            elif gun_farki == 0:
                                kalan_gun_durum = "Bugün teslim"
                                tag = 'bugun' # Bugün teslim edilecekler için tag
                            else:
                                kalan_gun_durum = f"{gun_farki} gün kaldı"
                                tag = 'normal'
                        except ValueError:
                            kalan_gun_durum = "Geçersiz Tarih"
                            tag = 'normal'
                    else:
                        kalan_gun_durum = "Tarih Belirtilmemiş"
                        tag = 'normal'

                    agac_gorunumu.insert("", "end", values=(
                        satir["ID"], satir["Kitap Adı"], satir.get("Ödünç Alan", ""), 
                        teslim_tarihi_str, kalan_gun_durum
                    ), tags=(tag,))
            else:
                tk.Label(agac_cercevesi, text="Henüz ödünç verilmiş kitap bulunmamaktadır.", bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ).pack(pady=20)
        
        # Gecikmiş kitaplar için stil (kırmızı yazı) - Düzeltildi: stil.tag_configure yerine agac_gorunumu.tag_configure
        agac_gorunumu.tag_configure('gecikmis', foreground='red', font=('Arial', 10, 'bold'))
        agac_gorunumu.tag_configure('bugun', foreground='orange', font=('Arial', 10, 'bold'))
        agac_gorunumu.tag_configure('normal', foreground=YAZI_RENGI_BEYAZ)

        hatirlatici_listesini_yenile()

        kaydirma_cubugu = ttk.Scrollbar(agac_cercevesi, orient="vertical", command=agac_gorunumu.yview)
        agac_gorunumu.configure(yscrollcommand=kaydirma_cubugu.set)

        kaydirma_cubugu.pack(side="right", fill="y")
        agac_gorunumu.pack(side="left", fill="both", expand=True)

        # Listeyi yenile butonu
        refresh_button_frame = tk.Frame(ust_cerceve, bg=ARKA_PLAN_KOYU_GRI)
        refresh_button_frame.pack(pady=10)
        tk.Button(refresh_button_frame, text="Listeyi Yenile", command=hatirlatici_listesini_yenile,
                  bg=ARKA_PLAN_ORTA_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat").pack()


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
            if color_code[1]: # Eğer bir renk seçildyse (None değilse)
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
            odunc_kitaplar_icerigi_olustur(ana_icerik_cercevesi)
        elif icerik_adi == "Hatırlatıcılar": # Yeni hatırlatıcılar içeriği
            hatirlaticilar_icerigi_olustur(ana_icerik_cercevesi)
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

    menu_oge5 = tk.Button(menu_cercevesi, text="Hatırlatıcılar", command=lambda: icerigi_goster("Hatırlatıcılar"), anchor="w", padx=10, pady=5,
                           bg=ARKA_PLAN_KOYU_GRI, fg=YAZI_RENGI_BEYAZ, activebackground=BUTON_AKTIF_ARKA_PLAN, activeforeground=YAZI_RENGI_BEYAZ, relief="flat")
    menu_oge5.pack(fill="x", pady=5)

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
