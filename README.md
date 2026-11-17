# Kurum analitiği | Demo

**Bu rapordaki tüm iş verileri örnek amaçlı, Python ile sıfırdan üretilmiştir. Gerçek veriler paylaşılmamıştır.** Hastaneler, ödeyiciler, hasta ve protokol anahtarları, faturalar, bütçeler ve tahsilatlar kurgusaldır. Sonuçlar herhangi bir sağlık kuruluşunun performansını temsil etmez.

**[Canlı raporu Power BI’da aç](https://app.powerbi.com/view?r=eyJrIjoiN2U2NTRhNmQtYTFlYS00M2NiLTg0MWEtZTkwNzFlMWI1ZDU2IiwidCI6ImQ5NjQ2ZTQyLTUzMWQtNDBlNC1hMDQ3LTBkOGU3ZDFhNmNlNCIsImMiOjl9)**
## Star Schema
<img width="931" height="707" alt="01 semantic-model" src="https://github.com/user-attachments/assets/cd8264c4-2b0d-4fbd-849e-0d0b7309a421" />

## Rapor görünümleri

<img width="1036" height="583" alt="02 genel-bakis" src="https://github.com/user-attachments/assets/25d87e1c-1a3c-43bb-bbaf-da5b20608b92" />


<details>
<summary>Gelirin Kaynakları</summary>

<img width="919" height="517" alt="03 gelirin-kaynaklari" src="https://github.com/user-attachments/assets/03ced628-8eb3-4180-9ce0-49f00d47ed7d" />


</details>

<details>
<summary>Demografik</summary>
<img width="1036" height="583" alt="04 basvuru-profili" src="https://github.com/user-attachments/assets/cd9ac923-6458-458f-896c-7b91105c3b7a" />
</details>

<details>
<summary>Merkez Karşılaştırması</summary>
<img width="919" height="517" alt="05 merkez-karsilastirmasi" src="https://github.com/user-attachments/assets/8037092d-8087-45a1-9f71-474927e37933" />


</details>

<details>
<summary>Ödeyici Karşılaştırması</summary>
<img width="1036" height="583" alt="06 odeyici-karsilastirmasi" src="https://github.com/user-attachments/assets/98db66f5-f2d2-4a85-8c09-603196723bb9" />


</details>

<details>
<summary>Alacak Takibi</summary>

<img width="1036" height="583" alt="07 alacak-takibi" src="https://github.com/user-attachments/assets/4ffdb93d-07ac-449d-9d0a-3fdbb403dbd8" />


</details>

<details>
<summary>Gidişat</summary>

<img width="907" height="513" alt="08 projeksiyon" src="https://github.com/user-attachments/assets/1efcb897-83f5-4a57-88fe-e7a31a456978" />


</details>

## Raporu keşfetme

Raporu bilgisayarınızda incelemek için [Hastane-Kurum-Analizi.pbix](./Hastane-Kurum-Analizi.pbix) dosyasını indirin ve Power BI Desktop ile açın. Sentetik veriler dosyaya gömülüdür. Raporu görüntülemek için verileri yenilemeniz, Python kurmanız veya bir veri kaynağına bağlanmanız gerekmez.

- **Portföye Genel Bakış ve Gelirin Kaynakları** üzerinden hizmet cirosunu, anlaşmalı kurum payını ve bütçe gerçekleşmesini inceleyin.
- **Başvuru Profili** sayfasında yaş grubu ve cinsiyet kırılımlarında hasta sayısı ile ciro arasında geçiş yapın.
- **Merkez Karşılaştırması ve Ödeyici Karşılaştırması** bölümlerinde aynı dönemi farklı hastaneler ve ödeyiciler için karşılaştırın.
- **Alacak Takibi** bölümünde hastane ve kurum görünümleri arasında geçin. Kısmen ödenmiş dosyalardan kalan alacağa inin.
- **Projeksiyon** bölümünde son veri tarihine göre yıl sonu beklentisini ve gerçekleşen ayları inceleyin.

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

275 ölçünün 123 tanesi rapor tanımlarında doğrudan kullanılır. 59 ölçüye model ifadeleri, sorgular veya ölçü bağımlılıkları üzerinden ulaşılır. Kalan 93 ölçü **Rapor dışında kalanlar** klasöründe konusuna göre gruplandırılmıştır. Bu ayrım proje dosyalarındaki başvurulara dayanır.

## İletişim

Kutay Alaaddin · [k.alaaeddin@outlook.com](mailto:k.alaaeddin@outlook.com)
