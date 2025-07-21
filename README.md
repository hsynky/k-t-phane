# Kütüphane Yönetim Sistemi

Bu uygulama, küçük bir kütüphane veya kişisel kitap koleksiyonunu yönetmek için tasarlanmış basit bir masaüstü uygulamasıdır. Kitapları ekleyebilir, düzenleyebilir, silebilir, ödünç durumlarını takip edebilir ve teslim hatırlatıcıları alabilirsiniz. Ayrıca uygulamanın tema renklerini ve pencere boyutlarını da özelleştirebilirsiniz.

## Özellikler

* **Kitap Yönetimi:** Kitapları ID, Ad, Yazar, Sayfa Sayısı, Basım Markası, Kayıt Tarihi ve Durumu (Mevcut/Ödünç Verildi) ile ekleme, düzenleme ve silme.
* **Ödünç Takibi:** Kitapların ödünç verilme durumunu yönetme, kimin ödünç aldığını ve teslim tarihini kaydetme.
* **Hatırlatıcılar:** Ödünç verilen kitapların teslim tarihlerine göre kalan günleri veya gecikmeleri görme. Gecikmiş kitaplar görsel olarak vurgulanır.
* **Özelleştirilebilir Tema:** Uygulamanın arka plan, yazı, buton ve giriş kutusu renklerini ayarlardan değiştirme ve kaydetme.
* **Özelleştirilebilir Boyutlar:** Uygulama penceresinin ve menü çubuğunun başlangıç boyutlarını ayarlardan belirleme.
* **Veri Kalıcılığı:** Tüm kitap verileri ve uygulama ayarları Excel ve JSON dosyalarında saklanır, böylece uygulama kapatılıp açıldığında verileriniz kaybolmaz.
* **Kullanıcı Dostu Arayüz:** Tkinter ile oluşturulmuş basit ve anlaşılır bir grafik arayüzü.

## Kurulum

Uygulamayı çalıştırmak için aşağıdaki adımları izleyin:

1.  **Python Kurulumu:** Bilgisayarınızda Python 3.x yüklü olduğundan emin olun. Python'ı [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.

2.  **Gerekli Kütüphaneleri Yükleme:** Uygulamanın çalışması için gerekli Python kütüphanelerini yükleyin. Komut istemcinizi (Terminal veya CMD) açın ve aşağıdaki komutu çalıştırın:
    ```bash
    pip install pandas openpyxl
    ```
    * `pandas`: Veri yönetimi (Excel dosyaları için)
    * `openpyxl`: Pandas'ın Excel dosyalarını okuyup yazması için gerekli bir bağımlılık

3.  **Uygulama Dosyalarını İndirme:** `anaekran.py` ve varsa diğer uygulama dosyalarını (örn. `girisekran.py`) bilgisayarınıza indirin veya kopyalayın.

## Kullanım

1.  **Uygulamayı Başlatma:**
    * Eğer projenizde `girisekran.py` gibi bir başlangıç dosyası varsa, onu çalıştırın:
        ```bash
        python girisekran.py
        ```
    * Eğer doğrudan ana uygulamayı başlatmak istiyorsanız:
        ```bash
        python anaekran.py
        ```

2.  **Ana Ekran:**
    * Uygulama açıldığında "Ana Ekran" ile karşılaşacaksınız. Burada kütüphanenizdeki tüm kitapların bir listesi bulunur.

3.  **Menü Navigasyonu:**
    * Sol üstteki "☰ Menü" butonuna tıklayarak yan menüyü açıp kapatabilirsiniz.
    * Menüde aşağıdaki seçenekler bulunur:
        * **Ana Sayfa:** Kütüphanedeki tüm kitapları gösterir.
        * **Kitap Listesi:** Kitap ekleme, düzenleme, silme ve durum değiştirme işlemlerini yapabileceğiniz yönetim ekranıdır.
        * **Ödünç Kitaplar:** Sadece ödünç verilmiş kitapları listeler.
        * **Hatırlatıcılar:** Ödünç verilen kitapların teslim tarihlerine göre kalan günlerini/gecikmelerini gösterir.
        * **Ayarlar:** Uygulamanın tema renklerini ve pencere boyutlarını özelleştirebileceğiniz bölümdür.

4.  **Kitap Ekleme/Düzenleme/Silme (Kitap Listesi Ekranı):**
    * **Kitap Ekle:** Formu doldurun ve "Kitap Ekle" butonuna tıklayın.
    * **Kitabı Düzenle:** Listeden bir kitap seçin, formda bilgileri belirecektir. Bilgileri değiştirin ve "Değişiklikleri Kaydet" butonuna tıklayın.
    * **Kitabı Sil:** Listeden bir kitap seçin ve "Kitabı Sil" butonuna tıklayın.
    * **Durumu Değiştir (Ödünç/Mevcut):** Bir kitap seçin. Eğer kitap "Mevcut" ise, bu butona tıkladığınızda ödünç alan ve teslim tarihi sorulur. Eğer kitap "Ödünç Verildi" ise, butona tıkladığınızda iade onayı istenir ve ödünç bilgileri temizlenir.

5.  **Ayarlar Ekranı:**
    * Burada uygulamanın renklerini (hex kodları ile) ve pencere/menü boyutlarını değiştirebilirsiniz.
    * Değişiklikleri yaptıktan sonra "Ayarları Kaydet ve Uygula" butonuna tıklayarak anında görünümü güncelleyebilirsiniz.
    * "Varsayılan Ayarları Yükle" butonu, uygulamanın başlangıçtaki varsayılan tema ve boyut ayarlarına geri dönmenizi sağlar.

## Dosya Yapısı

* `anaekran.py`: Uygulamanın ana kodunu ve tüm GUI (grafik kullanıcı arayüzü) mantığını içerir.
* `kutuphane_tablosu.xlsx`: Kitap verilerinin saklandığı Excel dosyası.
* `app_settings.json`: Uygulamanın tema ve boyut ayarlarının saklandığı JSON dosyası.
* `girisekran.py` (varsa): Uygulamanın başlangıç ekranını yöneten dosya.

## Teknolojiler

* **Python:** Programlama dili.
* **Tkinter:** Python'ın standart GUI kütüphanesi.
* **Pandas:** Veri analizi ve manipülasyonu için kullanılır, özellikle Excel dosyalarıyla etkileşimde.
* **openpyxl:** Pandas'ın Excel dosyalarını okuma/yazma yeteneği için arka uç kütüphanesi.
