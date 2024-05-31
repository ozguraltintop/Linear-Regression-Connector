import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# MySQL veritabanına bağlanın
connection = mysql.connector.connect(
    host='localhost',  # MySQL sunucunuzun adresi
    user='root',  # MySQL kullanıcı adı
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


# Özellikler ve hedef değişkeni belirleyin
X = df[['bir', 'iki', 'uc']]
y = df['fon']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Test seti üzerinde tahminler yapın
y_pred = model.predict(X_test)

# Model performansını değerlendirin
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Yeni veriler üzerinde tahmin yapın
new_data = pd.DataFrame({'bir': [10], 'iki': [2], 'uc': [1]})
predicted_time = model.predict(new_data)
print(f'Predicted Delivery Time: {predicted_time[0]}')