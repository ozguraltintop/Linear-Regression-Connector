import mysql.connector
import pandas as pd

# MySQL veritabanına bağlanın
connection = mysql.connector.connect(
    host='',  # MySQL sunucunuzun adresi
    user='devialtcomtr_turkeyca_yapilacaklar_db',  # MySQL kullanıcı adı
    password='',  # MySQL kullanıcı şifresi
    database='devialtcomtr_turkeyca_yapilacaklar_db'  # MySQL veritabanı adı
)
# SQL sorgusu
query = "SELECT * FROM upsfiyat"
# Veriyi çekin ve bir DataFrame'e dönüştürün
df = pd.read_sql(query, connection)
# Bağlantıyı kapatın
connection.close()

print(df.head())