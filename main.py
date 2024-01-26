import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Notebook Sunumu
pd.options.display.float_format = '{:,.2f}'.format

# Veriyi Yükle
df_veri = pd.read_csv('mission_launches.csv')

# Ön Veri Keşfi
print("df_veri'nin Şekli:", df_veri.shape)
print("Sütunlar:", df_veri.columns)

print(df_veri.columns)

print("NaN Değerleri:", df_veri.isnull().any().any())
print("Yinelenenler:", df_veri.duplicated().sum())

# Veri Temizleme - Eksik Değer ve Tekrarları Kontrol Et
# Gereksiz veri içeren sütunları kaldırmayı düşünün.

# Tanımlayıcı İstatistikler

# Şirket Başına Yapılan Fırlatma Sayısı
fırlatmalar_sirket = df_veri['Organisation'].value_counts()

plt.figure(figsize=(15, 6))
sns.barplot(x=fırlatmalar_sirket.index, y=fırlatmalar_sirket.values)
plt.xticks(rotation=90)
plt.title('Kuruluş Başına Yapılan Uzay Görevi Fırlatma Sayısı')
plt.xlabel('Kuruluş')
plt.ylabel('Fırlatma Sayısı')
plt.show()

# Aktif ve Emekli Roketlerin Sayısı
aktif_vs_emekli = df_veri['Rocket_Status'].value_counts()
print(df_veri.columns)

plt.figure(figsize=(8, 6))
sns.barplot(x=aktif_vs_emekli.index, y=aktif_vs_emekli.values)
plt.title('Aktif ve Emekli Roketlerin Sayısı')
plt.xlabel('Durum')
plt.ylabel('Sayı')
plt.show()

# Görev Durumu Dağılımı
gorev_durumu_dagilimi = df_veri['Mission_Status'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=gorev_durumu_dagilimi.index, y=gorev_durumu_dagilimi.values)
plt.title('Görev Durumu Dağılımı')
plt.xlabel('Görev Durumu')
plt.ylabel('Sayı')
plt.show()

# Fırlatmalar Ne Kadar Maliyetli?
plt.figure(figsize=(12, 6))
sns.histplot(df_veri['Price'], bins=30, kde=True)
plt.title('Fırlatma Maliyeti Dağılımı')
plt.xlabel('Maliyet (USD Milyon)')
plt.ylabel('Sayı')
plt.show()

# Ülkelere Göre Fırlatma Sayısını Gösteren Bir Choropleth Haritası Kullanın
df_veri['Ülke'] = df_veri['Location'].apply(lambda x: x.split(',')[-1].strip())
df_veri['Ülke'] = df_veri['Ülke'].replace({
    'Russia': 'Rusya Federasyonu',
    'New Mexico': 'ABD',
    'Yellow Sea': 'Çin',
    'Shahrud Missile Test Site': 'İran',
    'Pacific Missile Range Facility': 'ABD',
    'Barents Sea': 'Rusya Federasyonu',
    'Gran Canaria': 'ABD'
})

fırlatmalar_ülke = df_veri['Ülke'].value_counts().reset_index()
fırlatmalar_ülke.columns = ['Ülke', 'Fırlatma Sayısı']

fig = px.choropleth(fırlatmalar_ülke,
                    locations='Ülke',
                    locationmode='country names',
                    color='Fırlatma Sayısı',
                    color_continuous_scale='matter',
                    title='Ülkelere Göre Fırlatma Sayısı')
fig.show()

# Bir Choropleth Haritası Kullanarak Ülkelere Göre Başarısızlık Sayısını Gösterin
başarısızlık_ülke = df_veri[df_veri['Mission_Status'] == 'Failure']['Ülke'].value_counts().reset_index()
başarısızlık_ülke.columns = ['Ülke', 'Başarısızlık Sayısı']

fig_başarısızlık = px.choropleth(başarısızlık_ülke,
                                  locations='Ülke',
                                  locationmode='country names',
                                  color='Başarısızlık Sayısı',
                                  color_continuous_scale='matter',
                                  title='Ülkelere Göre Başarısızlık Sayısı')
fig_başarısızlık.show()

# Ülkeler, kuruluşlar ve görev durumu üzerine bir Plotly Sunburst Grafiği oluşturun.
fig_sunburst = px.sunburst(df_veri, path=['Ülke', 'Organisation', 'Mission_Status'],
                           title='Ülkeler, Kuruluşlar ve Görev Durumu Sunburst Grafiği')
fig_sunburst.show()

# 'Price' sütununu sayısal bir formata dönüştürme
df_veri['Price'] = pd.to_numeric(df_veri['Price'], errors='coerce')

# Kuruluşların Uzay Görevlerine Ne Kadar Para Harcadığını Analiz Edin
toplam_harcama = df_veri.groupby('Organisation')['Price'].sum().sort_values(ascending=False).reset_index()
toplam_harcama.columns = ['Kuruluş', 'Toplam Harcama (USD Milyar)']

plt.figure(figsize=(15, 6))
sns.barplot(x='Kuruluş', y='Toplam Harcama (USD Milyar)', data=toplam_harcama)
plt.xticks(rotation=90)
plt.title('Kuruluşların Uzay Görevlerine Toplam Harcaması')
plt.xlabel('Kuruluş')
plt.ylabel('Toplam Harcama (USD Milyar)')
plt.show()

# Kuruluş Başına Harcanan Para Miktarını Analiz Edin
harcanan_para_fırlatma_başı = df_veri.groupby('Organisation')['Price'].mean().sort_values(ascending=False).reset_index()
harcanan_para_fırlatma_başı.columns = ['Kuruluş', 'Ortalama Harcama Fırlatma Başı (USD Milyon)']

plt.figure(figsize=(15, 6))
sns.barplot(x='Kuruluş', y='Ortalama Harcama Fırlatma Başı (USD Milyon)', data=harcanan_para_fırlatma_başı)
plt.xticks(rotation=90)
plt.title('Kuruluş Başına Harcanan Para Miktarı')
plt.xlabel('Kuruluş')
plt.ylabel('Ortalama Harcama Fırlatma Başı (USD Milyon)')
plt.show()

# Zaman İçinde İlk 10 Kuruluş Tarafından Yapılan Fırlatmaların Sayısı
top_10_kuruluşlar = df_veri['Organisation'].value_counts().nlargest(10).index
df_top_10 = df_veri[df_veri['Organisation'].isin(top_10_kuruluşlar)]

plt.figure(figsize=(12, 6))
sns.lineplot(x='Date', y='Unnamed: 0', hue='Organisation', data=df_top_10)
plt.title('Zaman İçinde İlk 10 Kuruluş Tarafından Yapılan Fırlatmaların Sayısı')
plt.xlabel('Yıl')
plt.ylabel('Fırlatma Sayısı')
plt.legend(title='Kuruluş')
plt.show()