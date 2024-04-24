import sqlite3

# Veritabanı bağlantısını kur ve tabloyu oluştur
conn = sqlite3.connect('texts.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY,
    content TEXT
)
''')

# Mevcut verileri silmek için fonksiyon
def clear_texts():
    cursor.execute('DELETE FROM texts')
    conn.commit()

# Metinleri veritabanına yükleme fonksiyonu
def insert_text(text):
    cursor.execute('INSERT INTO texts (content) VALUES (?)', (text,))
    conn.commit()

# Metinleri SQLite'dan çekme fonksiyonu
def fetch_texts():
    cursor.execute('SELECT content FROM texts')
    return [row[0] for row in cursor.fetchall()]

# Özgün benzerlik hesaplama fonksiyonu
def calculate_similarity(text1, text2):
    words1 = set(text1.split())
    words2 = set(text2.split())
    common_words = words1.intersection(words2)
    total_words = len(words1.union(words2))
    similarity = (len(common_words) / total_words * 100) if total_words > 0 else 0
    return similarity

# Mevcut verileri temizle
clear_texts()

# Metinleri veritabanına yükle
text1 = "Bu bir deneme metnidir, özgün içerikler içermektedir."
text2 = "Bu metin de deneme amaçlıdır ve bazı özgün içerikleri barındırır."
insert_text(text1)
insert_text(text2)

# Veritabanından metinleri çek
texts = fetch_texts()

# Benzerlik hesapla
similarity_percentage = calculate_similarity(texts[0], texts[1])

# Benzerlik oranını bir dosyaya yazdır
with open('benzerlik_durumu.txt', 'w') as file:
    file.write(f'İki metin arasındaki benzerlik yüzdesi: {similarity_percentage:.2f}%\n')

print(f'İki metin arasındaki benzerlik yüzdesi: {similarity_percentage:.2f}%')

# Veritabanı bağlantısını kapat
conn.close()
