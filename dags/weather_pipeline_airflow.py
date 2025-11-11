import requests
import pandas as pd
from datetime import datetime

# GANTI DENGAN KOTA & API KEY ANDA
API_KEY = "d989cf2f89935f0f5e49ed0da6e97496"
KOTA = "Jakarta"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={KOTA}&appid={API_KEY}&units=metric"

# Tentukan nama file output
# Kita tambahkan timestamp agar setiap file unik
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
NAMA_FILE = f"data/cleaned_data_{timestamp}.csv" # Sesuaikan path ini nanti

def get_and_clean_weather_data():
    print(f"Memulai proses pipeline cuaca untuk {KOTA}...")

    # 1. Extract (Mengambil data dari API)
    response = requests.get(URL)
    data = response.json()

    # 2. Transform (Membersihkan data)
    # Ini hanya contoh sederhana. Data aslinya jauh lebih kompleks (nested JSON).
    if 'main' in data and 'weather' in data:
        cuaca_data = {
            'kota': data['name'],
            'suhu_celcius': data['main']['temp'],
            'terasa_seperti': data['main']['feels_like'],
    'cuaca_utama': data['weather'][0]['main'],
            'deskripsi': data['weather'][0]['description'],
            'timestamp_utc': pd.to_datetime(data['dt'], unit='s')
        }

        df = pd.DataFrame([cuaca_data])

        # Membersihkan missing value (jika ada, meski di sini kecil kemungkinan)
        df.dropna(inplace=True)

        # Cek duplikat (untuk satu kali run, pasti tidak ada)
        df.drop_duplicates(inplace=True)

        print("Data berhasil diambil dan dibersihkan.")

        # 3. Load (Menyimpan data)
        # Pastikan folder '/opt/airflow/data' ada di dalam server Airflow Anda
        df.to_csv(NAMA_FILE, index=False)
        print(f"Data bersih berhasil disimpan di {NAMA_FILE}")

    else:
        print("Gagal mengambil data atau format data tidak sesuai.")

# Baris ini untuk menguji di Colab
if __name__ == "__main__":
    # (Anda mungkin perlu menyesuaikan NAMA_FILE saat tes di Colab)
    # NAMA_FILE = "cleaned_data_test.csv" 
    get_and_clean_weather_data()




# ----------------------------------------------------
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import fungsi yang sudah kita buat tadi
# (Dalam project nyata, file logic.py dan dag.py harus bisa diakses oleh Airflow)
# Untuk mini project, kita copy-paste saja fungsinya ke sini agar mudah

import requests
import pandas as pd

def get_and_clean_weather_data():
    API_KEY = "d989cf2f89935f0f5e49ed0da6e97496"
    KOTA = "Jakarta"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={KOTA}&appid={API_KEY}&units=metric"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    NAMA_FILE = f"data/cleaned_data_{timestamp}.csv"

    print(f"Memulai proses pipeline cuaca untuk {KOTA}...")
    response = requests.get(URL)
    data = response.json()

    if 'main' in data and 'weather' in data:
        cuaca_data = {
            'kota': data['name'],
            'suhu_celcius': data['main']['temp'],
            'terasa_seperti': data['main']['feels_like'],
            'cuaca_utama': data['weather'][0]['main'],
            'deskripsi': data['weather'][0]['description'],
            'timestamp_utc': pd.to_datetime(data['dt'], unit='s')
        }
        df = pd.DataFrame([cuaca_data])
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("Data berhasil diambil dan dibersihkan.")


        df.to_csv(NAMA_FILE, index=False)
        print(f"Data bersih berhasil disimpan di {NAMA_FILE}")
    else:
        print("Gagal mengambil data atau format data tidak sesuai.")

# ----------------------------------------------------
# Definisi DAG (Ini adalah "Mandor"nya)
# ----------------------------------------------------

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_hourly_pipeline',
    default_args=default_args,
    description='Pipeline ETL cuaca setiap jam',
    schedule_interval=timedelta(hours=0.5),  # <-- Ini menjawab langkah 4 Anda
    # atau gunakan '0 * * * *' (cron expression)
    start_date=datetime(2025, 10, 10), # Ganti dengan tanggal kemarin
    catchup=False,
    tags=['weather', 'mini-project'],
) as dag:

    # Ini adalah "Pekerja" nya (langkah 4 Anda)
    run_etl_task = PythonOperator(
        task_id='get_clean_and_save_weather_data',
        python_callable=get_and_clean_weather_data, # Fungsi yang akan dipanggil
    )

    # Mengatur urutan (meski hanya 1 task, ini adalah best practice)
    run_etl_task