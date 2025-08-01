# Python 3.10 tabanlı resmi image
FROM python:3.10-slim

# Uygulama dizinine geç
WORKDIR /app

# Tüm dosyaları konteynıra kopyala
COPY . .

# Gerekli kütüphaneleri kur
RUN pip install --no-cache-dir -r requirements.txt

# Flask uygulaması için port ayarı
ENV PORT=10000

# Uygulamayı başlat
CMD ["python", "app.py"]
