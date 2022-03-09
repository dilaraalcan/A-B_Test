
# PROJE
##################
# Facebook kısa süre önce mevcut maximum bidding adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan average bidding’i tanıttı.
# Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi ve averagebidding’in, maximumbidding’den daha fazla dönüşüm getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.

# Veri Seti Hikayesi
######################
# bombabomba.com’un web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.
# Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır.

# Değişkenler
######################
# Impression – Reklam görüntüleme sayısı Click – Tıklama
#Görüntülenen reklama tıklanma sayısını belirtir.
# Purchase – Satın alım
#Tıklanan reklamlar sonrası satın alınan ürün sayısını belirtir.
# Earning – Kazanç
#Satın alınan ürünler sonrası elde edilen kazanç

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

from google.colab import files
df_= files.upload()
#veri dosyası yükleme

test = pd.read_excel("ab_testing.xlsx",sheet_name='Test Group')
test.head()

control = pd.read_excel("ab_testing.xlsx",sheet_name='Control Group')
control.head()

control["Click"].sum()

test["Click"].sum()

control["Purchase"].sum()

test["Purchase"].sum()

test["Earning"].sum()

control["Earning"].sum()

test
# 40 günlük veri

control
# 40 günlük veri

# GÖREV1 HİPOTEZLERİ TANIMLAYINIZ.
#
# H0: control ve test arasında istatistiki olarak anlamlı bir fark yoktur.
# H1: control ve test arasında istatistiki olarak anlamlı bir fark vardır.

# Birbirinden bagımsız iki grup arasında karsılastırma yapabilmek için Bagımsız Orneklem T Testi kullanılır.

# A/B Testi aşamaları:
#
# ADIM1:  Hipotez kurulur.
#
# ADIM2: Varsayım kontrolleri yapılır.
#         Normallik varsayımı.(shapiro)
#          H0: Normal dagılım varsayımı saglanır.
#          H1: Normal dagılım varsayımı saglanmaz.
#         Homojenlik varsayımı (levene)
#          H0: Homojenlik varsayımı saglanır.
#          H1: Homojenlik varsayımı saglanmaz.
#
# ADIM3: Hipotez uygulanır.
#       Varsayımlar saglanıyorsa: A/B Testi
#       Normallik saglanmıyorsa: non-parametrik test
#       Normallik sagllanıyor, homojenlik saglanmıyorsa: welch test uygulanır.

# Normallik Varsayımı (control)
#          H0: Normal dagılım varsayımı saglanır.
#          H1: Normal dagılım varsayımı saglanmaz.
test_stat, pvalue = shapiro(control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# control normallik varsayımı: 0.58   p>0.05
# H0 rededilemez.
# Normal dagılım saglanır.

# Normallik Varsayımı (test)
#          H0: Normal dagılım varsayımı saglanır.
#          H1: Normal dagılım varsayımı saglanmaz.
test_stat, pvalue = shapiro(test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# control normallik varsayımı: 0.15   p>0.05
# H0 rededilemez.
# Normal dagılım saglanır.

#Homojenlik varsayımı (control)
#          H0: Homojenlik varsayımı saglanır.
#          H1: Homojenlik varsayımı saglanmaz.
test_stat, pvalue = levene(control["Purchase"],
                           test["Purchase"] )
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1083 
# H0 reddedilemez.
# Homojenlik varsayımı saglanır.

# Hipotezin uygulanması:
#
# Normallik ve Homojenlik varsayımı saglandıgı için T Testi uygulanır.

# T Test:
test_stat, pvalue = ttest_ind(control["Purchase"] ,
                              test["Purchase"] ,
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# T Test value : 0.3493
# p> 0.05
# H0 reddedilemez.
# control ve test arasında istatistiki olarak anlamlı bir fark yoktur.

# Kullanılan Testler
#
# Normallik varsayımı için shapiro
# Homojenlik varsayımı için levene
# İki örneklem arasında karsılastırma yapabilmek için ve
# Normallik ve homojenlik saglandıgı için A/B testi.

# Tavsiyeler
#
# Test sonucunda iki durum arasında istatistiki acıdan anlamlı bir fark olmadıgı sonucunu aldık.
# İki durumun degerlendirilmesinde etkileyen daha farklı faktörler de bulunur. mesela zaman, mevsimsel farklılıklar.
# bu sebeple daha uzun bir zaman aralıgına bakmak daha fazla yorum yapılabilme imkanı sunabilir.
#