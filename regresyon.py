import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime


# MySQL veritabanı bağlantısı
mydb = mysql.connector.connect(
    host='',  # MySQL sunucunuzun adresi
    user='',  # MySQL kullanıcı adı
    password='%Dt4w?[G',  # MySQL kullanıcı şifresi
    database=''  # MySQL veritabanı adı
)

# Veritabanı bağlantısı başarılıysa
if mydb.is_connected():
    # Veritabanı üzerinde işlem yapabilmek için cursor oluşturulur
    mycursor = mydb.cursor()

    # MySQL sorgusu
    mycursor.execute("SELECT kg, tarih, para FROM musteri")

    # Sonuçları al
    veriler = mycursor.fetchall()
    print(veriler)
    # Verileri DataFrame'e dönüştür
    df = pd.DataFrame(veriler, columns=['kg', 'tarih', 'para'])

    # Tarihi sayısal bir formata dönüştür
    df['tarih'] = pd.to_datetime(df['tarih']).dt.month
    df.dropna(inplace=True)

    # Bağımsız değişkenleri (X) ve bağımlı değişkeni (y) ayıralım
    X = df[['kg', 'tarih']]
    y = df['para']

    # Veri setini eğitim ve test setlerine ayıralım
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Lineer regresyon modelini oluşturalım ve eğitelim
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Modelin performansını değerlendirelim
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    train_rmse = mean_squared_error(y_train, train_predictions, squared=False)
    test_rmse = mean_squared_error(y_test, test_predictions, squared=False)

    # Gelecek ayın tahmini kazancını bulalım (örneğin, ayın son gününü alabiliriz)
    gelecek_ay_tarih = df['tarih'].max() + 1
    gelecek_ay_kg = 10  # Örnek olarak 10 kg kabul edelim
    tahmin_kazanc = model.predict([[gelecek_ay_kg, gelecek_ay_tarih]])

    print(f"Gelecek ayın tahmini kazancı: ${tahmin_kazanc[0]:.2f}")
    print(f"Eğitim RMSE: {train_rmse:.2f}")
    print(f"Test RMSE: {test_rmse:.2f}")


    # Tahmin edilen kazancı rapor tablosuna ekleyelim
    bugunun_tarihi = datetime.today().strftime('%Y-%m-%d')
    insert_sorgusu = "INSERT INTO rapor (date, rapor) VALUES (%s, %s)"
    degerler = (bugunun_tarihi, tahmin_kazanc[0])

    # Veriyi veritabanına ekle
    mycursor.execute(insert_sorgusu, degerler)
    mydb.commit()

    mycursor.close()
    mydb.close()
