# Mini-Project: Pipeline Data Cuaca dengan Apache Airflow

Proyek ini adalah pipeline data sederhana yang dibuat untuk *challenge* data engineering. Tujuannya adalah mengambil data cuaca setiap jam dari API publik, membersihkannya, dan menyimpannya. Seluruh proses ini diatur dan dijadwalked menggunakan Apache Airflow.

## 🚀 Fitur Utama

* **Ekstraksi Data:** Mengambil data cuaca *real-time* (per kota) dari API [OpenWeatherMap](https://openweathermap.org/api).
* **Transformasi Data:** Membersihkan data JSON mentah, memilih kolom yang relevan, dan mengubahnya menjadi format tabular (DataFrame Pandas).
* **Pemuatan Data (Load):** Menyimpan data bersih ke file `.csv` baru setiap jam.
* **Penjadwalan:** Pipeline dijadwalkan untuk berjalan secara otomatis **setiap 1 jam** menggunakan penjadwal Airflow.
* **Orkestrasi:** Dikelola dan dimonitor sepenuhnya menggunakan Apache Airflow, yang berjalan di atas Docker.

## 🛠️ Teknologi yang Digunakan

* **Apache Airflow:** Untuk orkestrasi dan penjadwalan *workflow*.
* **Docker & Docker Compose:** Untuk menjalankan lingkungan Airflow secara terisolasi dan mudah.
* **Python:** Bahasa utama untuk skrip pipeline.
* **Pandas:** Digunakan untuk transformasi dan pembersihan data.
* **Requests:** Digunakan untuk mengambil data dari API eksternal.

## 📂 Struktur Proyek

Berikut adalah struktur folder yang digunakan dalam proyek ini:



## ⚙️ Cara Menjalankan Proyek

### 1. Prasyarat

* Pastikan **Docker Desktop** telah ter-install dan berjalan di komputer Anda.

### 2. Dapatkan API Key

* Daftar akun di [OpenWeatherMap](https://openweathermap.org/api) untuk mendapatkan API Key gratis.
* Tunggu sekitar 30 menit hingga 2 jam agar API Key Anda aktif.

### 3. Konfigurasi Proyek

1.  **Struktur Folder:** Buat struktur folder seperti yang ditunjukkan di atas.
2.  **Dapatkan `docker-compose.yaml`:** Unduh file `docker-compose.yaml` resmi dari Airflow ke dalam folder `mini_project_airflow/`:
    ```bash
    curl -LfO "[https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml)"
    ```
3.  **Inisialisasi Folder:** Buat folder yang diperlukan dan file `.env`:
    ```bash
    mkdir -p ./dags ./logs ./plugins ./data
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
4.  **Edit File DAG:**
    * Salin file `weather_pipeline_dag.py` ke dalam folder `dags/`.
    * Buka file tersebut dan ganti nilai `API_KEY = "dummy_api_key_anda"` dengan API Key Anda yang asli.
5.  **Edit `docker-compose.yaml`:**
    * Buka file `docker-compose.yaml`.
    * Di bawah `volumes:` untuk layanan `airflow-scheduler`, `airflow-webserver`, dan `airflow-worker`, tambahkan pemetaan untuk folder `data`:
        ```yaml
        volumes:
          - ./dags:/opt/airflow/dags
          - ./logs:/opt/airflow/logs
          - ./plugins:/opt/airflow/plugins
          - ./data:/opt/airflow/data   # <-- TAMBAHKAN BARIS INI
        ```

### 4. Jalankan Airflow

1.  Buka terminal di folder `mini_project_airflow/` dan jalankan:
    ```bash
    docker-compose up -d
    ```
2.  Tunggu beberapa menit hingga semua layanan menyala.

### 5. Akses Airflow UI

1.  Buka browser Anda dan kunjungi: `http://localhost:8080`
2.  Login dengan username: `airflow` dan password: `airflow`.
3.  Cari DAG bernama `weather_hourly_pipeline` dan nyalakan *toggle* (dari Off ke On).
4.  Anda bisa memicunya secara manual (klik tombol ▶️) untuk tes pertama.

## 📊 Hasil

Pipeline akan berjalan sesuai jadwal (`schedule_interval`) setiap satu jam. Setiap kali berjalan, sebuah file CSV baru akan dibuat di dalam folder `data/` dengan data cuaca pada jam tersebut.

## 🛑 Cara Menghentikan

Untuk mematikan semua layanan Airflow dengan bersih, jalankan perintah berikut di terminal:

```bash
docker-compose down