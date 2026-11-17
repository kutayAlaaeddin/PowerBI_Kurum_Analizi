# Kurum Analitiği | Power BI Demo Proje

**Bu rapordaki tüm iş verileri örnek amaçlı, Python ile sıfırdan üretilmiştir. Gerçek veriler paylaşılmamıştır.** Hastaneler, ödeyiciler, hasta ve protokol anahtarları, faturalar, bütçeler ve tahsilatlar kurgusaldır. Sonuçlar herhangi bir sağlık kuruluşunun performansını temsil etmez.

**[Canlı raporu Power BI’da aç](https://app.powerbi.com/view?r=eyJrIjoiN2U2NTRhNmQtYTFlYS00M2NiLTg0MWEtZTkwNzFlMWI1ZDU2IiwidCI6ImQ5NjQ2ZTQyLTUzMWQtNDBlNC1hMDQ3LTBkOGU3ZDFhNmNlNCIsImMiOjl9)**

## Raporu keşfetme

Raporu tarayıcıda incelemek için yukarıdaki canlı rapor bağlantısını kullanın. Power BI Desktop’ta incelemek için depodaki `Hastane-Kurum-Analizi.pbix` dosyasını indirin ve açın. Örnek veriler dosyaya gömülüdür. Raporu görüntülemek için yenileme veya Python kurulumu gerekmez.

- **Portföye Genel Bakış ve Gelirin Kaynakları** üzerinden hizmet cirosunu, anlaşmalı kurum payını ve bütçe gerçekleşmesini inceleyin.
- **Başvuru Profili** sayfasında yaş grubu ve cinsiyet kırılımlarında hasta sayısı ile ciro arasında geçiş yapın.
- **Merkez Karşılaştırması ve Ödeyici Karşılaştırması** bölümlerinde aynı dönemi farklı hastaneler ve ödeyiciler için karşılaştırın.
- **Alacak Takibi** bölümünde hastane ve kurum görünümleri arasında geçin. Kısmen ödenmiş dosyalardan kalan alacağa inin.
- **Projeksiyon** bölümünde son veri tarihine göre yıl sonu beklentisini ve gerçekleşen ayları inceleyin.

## Model ve örnek senaryo

Proje 11 rapor sayfası, 180 görsel kapsayıcısı (grafikler, kartlar, düğmeler ve diğer öğeler), 13 yer imi, 23 model tablosu, 18 ilişki ve 275 DAX ölçüsü içerir. Gezinme düğmeleri ve yer imleri, aynı sayfada farklı inceleme görünümlerine geçiş sağlar. Kurumsal logo yerine “Hastane / Ödeyici Kurum Analizi” etiketi kullanılmıştır.

Beş kurgusal hastane, 32 ödeyici ve altı klinik bölüm için 8.522 örnek protokol üretilmiştir. İşlem dönemi Ocak 2025–19 Ekim 2026 arasındadır. Takvim ve aylık bütçeler 2026 sonuna kadar uzanır. Böylece tamamlanan ayları, kısmi ayı ve tahmin dönemini aynı raporda inceleyebilirsiniz. Örnek senaryo tam ödeme, kısmi ödeme, açık alacak ve henüz faturası bulunmayan protokoller içerir.

## Veriyi yeniden üretme

`data/` klasöründe 11 tablonun okunabilir UTF-8 CSV dosyaları bulunur. Tarih boyutu ve hesaplanan tablolar Power BI içinde oluşturulur. Python 3 ile proje klasöründe aşağıdaki komutu çalıştırabilirsiniz.

~~~sh
python generate_data.py
~~~

Betik aynı rastgelelik tohumu ile CSV dosyalarını ve bunların Power Query içindeki sıkıştırılmış kopyalarını birlikte yeniden oluşturur. Yeni bir senaryo için betikteki üretim kurallarını değiştirip tekrar çalıştırın ve Power BI Desktop’ta projeyi yeniden açarak yenileyin.

## Programlar ve göstergeler

Pusula, Prizma, Yörünge ve Açık Ağ sentetik sözleşme programlarıdır. Grafiklerdeki dağılımlar üretilen işlem kayıtlarından hesaplanır.

275 ölçünün 123 tanesi rapor tanımlarında doğrudan kullanılır. 59 ölçüye model ifadeleri, sorgular veya ölçü bağımlılıkları üzerinden ulaşılır. Kalan 93 ölçü, ilerideki analizlerde kullanılmak üzere **Rapor dışında kalanlar** klasöründe konularına göre gruplandırılmıştır. Bu ayrım proje dosyalarındaki başvurulara dayanır.
