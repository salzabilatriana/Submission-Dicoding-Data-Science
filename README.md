# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

**Nama:** Salzabila Triana Said
**Email:** strianasaid@gmail.com
**Id Dicoding:** zalana9

## Business Understanding
Jaya Jaya Institut adalah institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi baik. Namun, institusi ini menghadapi masalah tingkat **dropout** (siswa tidak menyelesaikan pendidikan) yang cukup tinggi, sekitar **32% dari 4.424 siswa** pada data historis yang dianalisis. Angka dropout yang tinggi berdampak pada reputasi institusi, efisiensi biaya operasional pendidikan, dan tingkat kelulusan yang menjadi salah satu indikator kualitas institusi.

Agar dapat memberikan bimbingan khusus secara tepat waktu, Jaya Jaya Institut membutuhkan cara untuk **mendeteksi sedini mungkin** siswa yang berisiko dropout, berdasarkan data yang sudah mereka miliki sejak pendaftaran hingga performa akademik semester berjalan.

### Permasalahan Bisnis
1. Tingginya angka dropout siswa (32%) yang belum diketahui pemicu utamanya secara data-driven.
2. Belum adanya sistem yang dapat mendeteksi secara dini siswa-siswa yang berisiko dropout, sehingga bimbingan konseling/akademik seringkali diberikan terlambat (setelah siswa sudah berhenti kuliah).
3. Belum ada visibilitas yang jelas bagi manajemen mengenai faktor-faktor apa saja (akademik, finansial, maupun demografis) yang paling berkontribusi terhadap dropout.

### Cakupan Proyek
1. **Data Understanding & Exploratory Data Analysis (EDA)** terhadap data siswa (`data.csv`) mencakup 4.424 baris dan 37 atribut (data pendaftaran, latar belakang keluarga, kondisi finansial, performa akademik semester 1 & 2, serta indikator makroekonomi).
2. **Data Preparation**, pemeriksaan kualitas data, encoding target, split data latih/uji, dan standarisasi fitur.
3. **Modeling**, membangun model klasifikasi (Logistic Regression sebagai baseline dan Random Forest yang dituning) untuk memprediksi status siswa: `Dropout`, `Enrolled`, atau `Graduate`.
4. **Evaluation**, mengukur performa model dan menganalisis fitur-fitur yang paling berpengaruh terhadap dropout.
5. **Prototype sistem machine learning** berbasis Streamlit yang dapat digunakan tim akademik untuk memprediksi status siswa secara individual maupun massal (batch via CSV).
6. **Rekomendasi action items** bagi manajemen berdasarkan insight yang ditemukan.

### Persiapan

Sumber data: [Students' Performance Dataset](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance) — `data.csv` (4.424 baris, 37 kolom, disertakan dalam folder proyek ini).

Setup environment:
```bash
# 1. Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install seluruh dependency yang dibutuhkan
pip install -r requirements.txt

# 3. Jalankan notebook untuk melihat proses analisis end-to-end
jupyter notebook notebook.ipynb
```

## Business Dashboard
Dashboard ini dibuat menggunakan **Google Looker Studio** untuk menganalisis performa dan status mahasiswa berdasarkan data akademik, demografi, serta faktor risiko yang berkaitan dengan dropout.

Dashboard menyajikan beberapa indikator utama, seperti:
1. Total mahasiswa
2. Graduation Rate
3. Dropout Rate
4. Course Pass Rate
5. Distribusi status mahasiswa (Graduate, Dropout, dan Enrolled)
6. Status mahasiswa berdasarkan Financial Risk
7. Dropout Rate berdasarkan Financial Risk
8. Rata-rata nilai akademik Semester 1 dan Semester 2 berdasarkan status mahasiswa
9. Dropout Rate berdasarkan kelompok usia
10. Dropout Rate berdasarkan gender
11. Top 10 program studi berdasarkan Dropout Rate

Dashboard juga dilengkapi dengan beberapa filter interaktif, seperti **Status, Age Group, Gender, dan Financial Risk**, sehingga pengguna dapat melakukan eksplorasi data berdasarkan kategori tertentu.

### 🔗 Dashboard
[**View Interactive Dashboard — Looker Studio**](https://datastudio.google.com/s/gj4mVvoa6pc)

## Menjalankan Sistem Machine Learning
Prototype sistem machine learning dibangun menggunakan **Streamlit** dan memanfaatkan model Random Forest (`model/rf_dropout_model.pkl`) beserta scaler (`model/scaler.pkl`) yang telah disimpan dari hasil notebook.

**Menjalankan secara lokal:**
```bash
pip install -r requirements.txt
streamlit run app.py
```
Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`. Terdapat dua mode:
- **Input Manual**, mengisi data satu siswa lewat form, lalu mendapatkan prediksi status beserta probabilitas tiap kelas.
- **Upload CSV (Batch)**, mengunggah file CSV berisi banyak siswa (format sama seperti `data.csv`, tanpa kolom `Status`) untuk memprediksi seluruhnya sekaligus dan mengunduh hasilnya.

**Menjalankan di Streamlit Community Cloud:**
1. Push seluruh isi folder submission ini (termasuk folder `model/`) ke sebuah repository GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun GitHub.
3. Klik **New app**, pilih repository tersebut, branch `main`, dan file utama `app.py`.
4. Klik **Deploy**, Streamlit Cloud akan otomatis menginstall dependency dari `requirements.txt`.
5. Setelah deploy selesai, tautan publik aplikasi dapat dibagikan (contoh format: `https://<nama-app>.streamlit.app`).

### 🔗 Streamlit
[**View Streamlit Cloud**](https://submission-dicoding-data-science-tsajgkzu33f5tqta9fikoi.streamlit.app)

## Conclusion
Berdasarkan hasil analisis data dan pemodelan machine learning terhadap 4.424 data siswa Jaya Jaya Institut:

- Sekitar **32% siswa berstatus Dropout**, **50% Graduate**, dan **18% masih Enrolled**. Angka dropout ini cukup signifikan dan menjadi perhatian utama institusi.
- **Performa akademik semester 1 dan 2** (jumlah mata kuliah yang disetujui/lulus dan nilai rata-rata) merupakan faktor **paling prediktif** terhadap status dropout siswa, jauh lebih prediktif dibanding nilai admission grade saat pendaftaran.
- **Faktor finansial** juga berperan penting: siswa dengan status **debtor** (memiliki tunggakan) dan pembayaran SPP yang **tidak up to date** menunjukkan proporsi dropout yang jauh lebih tinggi, sedangkan penerima **scholarship** menunjukkan proporsi dropout yang jauh lebih rendah.
- Model **Random Forest (tuned)** yang dikembangkan mencapai akurasi sekitar **75%** dan F1-score (macro) sekitar **0,71** pada data uji, dengan performa yang baik dalam mengenali kelas Dropout (precision 0,83; recall 0,69) dan Graduate (precision 0,83; recall 0,86). Model ini sudah cukup layak digunakan sebagai alat bantu deteksi dini, meskipun masih ada ruang untuk perbaikan pada pengenalan kelas Enrolled.
- Model beserta seluruh dependency yang diperlukan telah disimpan pada folder `model/` dan diintegrasikan ke dalam prototype `app.py`, sehingga tim akademik dapat langsung menggunakannya untuk memprediksi status siswa baru.

Dengan sistem deteksi dini ini, Jaya Jaya Institut dapat mengidentifikasi siswa berisiko dropout **sejak awal semester**, sehingga intervensi (bimbingan akademik maupun bantuan finansial) dapat diberikan lebih cepat dan tepat sasaran, alih-alih menunggu siswa benar-benar berhenti kuliah.

### Rekomendasi Action Items
- **Bangun sistem monitoring performa akademik semester berjalan** yang secara otomatis menjalankan model prediksi ini di setiap akhir semester, lalu memberi flag pada siswa dengan probabilitas dropout tinggi untuk ditindaklanjuti oleh dosen wali/konselor akademik.
- **Prioritaskan program bimbingan konseling dan akademik intensif** bagi siswa dengan jumlah mata kuliah yang disetujui/lulus rendah pada semester 1, karena ini merupakan sinyal risiko dropout paling kuat dan dapat dideteksi lebih awal dari nilai akhir semester.
- **Perluas atau permudah akses program beasiswa dan skema keringanan/cicilan SPP** bagi siswa dengan status debtor atau pembayaran SPP yang tertunggak, mengingat faktor finansial terbukti berkontribusi besar terhadap dropout.
- **Lakukan evaluasi berkala terhadap siswa berusia lebih tua saat pendaftaran (non-tradisional)**, karena kelompok ini menunjukkan pola risiko yang berbeda dan mungkin membutuhkan dukungan tambahan seperti fleksibilitas jadwal kuliah.
- **Integrasikan prototype machine learning ini ke dalam sistem akademik (SIAKAD)** yang sudah ada agar prediksi dapat diakses langsung oleh staf akademik tanpa perlu berpindah aplikasi, dan lakukan retraining model secara berkala (misalnya tiap tahun ajaran) menggunakan data terbaru agar akurasi model tetap terjaga.
