## Biodata
Nama : Fadly Atief

NPM : 2506624940

Kelas : PBP A

## Panduan Setup Local
1. Didalam folder `my portofolio` buat Virtual Environment agar package dan dependencies aplikasi tidak bertrabrakan dengan versi lain dikomputermu

    **Windows:** 
    ``` 
    python -m venv env
    ```

    **Unix (macOS, Linux):** 
    ```
    python3 -m venv env
    ```

2. Aktifkan Virtual Environmentnya dengan perintah ini:

    **Windows:** 
    ```
    env\Scripts\activate
    ```

    **Unix (macOS, Linux):** 
    ```
    env\Scripts\activate
    ```

3. Install semua dependencies
    
    ```
    pip install -r requirements.txt
    ```

4. Buat project Django bernama `myportofolio`:

    ```
    django-admin startproject myportofolio .
    ```

5. Konfigurasi Environment Variables

    Environment variables adalah variabel yang disimpan di luar kode program, dipakai untuk menyimpan informasi konfigurasi (kredensial database, API key, dst) supaya kode yang sama bisa jalan di environment yang berbeda tanpa diubah.

    Buat berkas `.env` di root proyek, isi dengan:

    ```env
    PRODUCTION=False
    ```

    Buat juga berkas `.env.prod` di folder yang sama, untuk konfigurasi production nanti:

    ```env
    DB_NAME=<nama database>
    DB_HOST=<host database>
    DB_PORT=<port database>
    DB_USER=<username database>
    DB_PASSWORD=<password database>
    SCHEMA=tutorial
    PRODUCTION=True
    ```

    **Catatan**
    - `.env`: dipakai untuk development lokal. Karena `PRODUCTION=False`, aplikasi memakai database SQLite yang sederhana untuk testing.
    - `.env.prod`: dipakai saat deployment ke PWS di Tutorial 01. Karena `PRODUCTION=True`, aplikasi memakai database PostgreSQL dengan kredensial yang akan diberikan menyusul.
    - `SCHEMA`: nama schema database, disesuaikan lagi dengan kebutuhan tiap tutorial/tugas.

    Buka berkas `settings.py` yang ada di dalam subfolder `myportofolio`. Di bagian paling atas berkas (setelah `from pathlib import Path`), tambahkan kode untuk mengimpor package `os` dan membaca berkas `.env`:

    ```python
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()
    ```

    Cari variabel `ALLOWED_HOSTS` yang sudah ada di dalam `settings.py` (secara default berisi `ALLOWED_HOSTS = []`), lalu ubah nilainya agar mengizinkan akses dari localhost dan 127.0.0.1:

    ```python
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    ```

    **Penting**
    Pastikan kamu mengubah baris `ALLOWED_HOSTS = []` yang sudah ada, bukannya menambahkan baris baru di bagian atas file.

    Di bawah `ALLOWED_HOSTS`, tambahkan variabel `PRODUCTION` untuk membaca status environment dari berkas `.env`:

    ```python
    PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
    ```

    Cari bagian `DATABASES` di `settings.py`, lalu ganti dengan konfigurasi dinamis berikut yang otomatis memilih SQLite (development) atau PostgreSQL (production):

    ```python
    # Database configuration
    if PRODUCTION:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST'),
                'PORT': os.getenv('DB_PORT'),
                'OPTIONS': {
                    'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
                }
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    ```

6. Menjalankan Server

    Jalankan migrasi database, lalu jalankan servernya.

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

    Perintah `migrate` menerapkan migration bawaan Django untuk app default (`admin`, `auth`, `contenttypes`, `sessions`). Buka `http://localhost:8000/` di browser - kamu akan melihat animasi roket bawaan Django sebagai tanda proyekmu berhasil dibuat.

## Tugas 1

### ❓ Pertanyaan
1. Ya, saya menggunakan <section> untuk sementara ini. elemen ini membantu saya untuk kemudian mengatur layout pada suatu segmen / section tertentu. Contohnya pada section profile dan section skills, saya dapat mengatur layout secara garis besar untuk segmen tersebut. Sedangkan untuk dan, saya belum menggunakannya karena belum menemukan urgensi untuk menambahkan.

2. Untuk mengatur CSS tetap responsive, terdapat beberapa tantangan untuk mengaturnya, seperti widthnya sudah saya atur 100% namun tidak full, atau posisinya tidak sesuai dengan yang aku mau, bahkan sampai sering terjadi layoutnya bagus di mobile tapi kurang di desktop, vice versa. Untuk mengevaluasinya, saya mencoba memaksakannya sampai mengatur elemen html dan body di cssnya, namun karena masih belum ketemu sumber permasalahannya, saya akhirnya meminta AI untuk mengecek dan memberikan rekomendasi perbaikan. Untuk prioritas, saya prioritaskan desktop, namun layout mobile juga saya terus tingkatkan even tho tidak sebagus website

3. Batasan dari website static ini tentunya adalah bagaimana elemen - elemen didalamnya harus di **hardcode**, Apabila sudah dideploy, dan ada perubahan di skills saya, atau kedepannya di halaman project dll. Saya butuh untuk mengubahnya dan menambahkannya di htmlnya langsung, setelah itu harus redeploy lagi. Tentu sangat tidak efisien dan sangat terbatas. Lalu karena juga ini merupakan static web murni dengan html dan css murni, saya menemukan kesulitan dimana saya harus membuat semua hal secara manual dan dari nol, tidak seperti apabila saya menggunakan CSS Framework yang akan mempercepat proses pengerjaan web staticnya.

### 📶 Progress Mingguan
**Untuk Full *Commit History*, bisa lihat di branch tugas-1**
- 1 September 2026: Melakukan Inisialisasi Project Django dengan penambahan HTML, CSS, dan PWS Setup
- 2 September 2026: Melakukan trigger rebuild agar PWS dapat melakukan rebuild (karena error sebelum informasi DB diberikan)
- 3 September 2026: 
    1. Menambahkan Skill Page
    2. Mengubah arah visual design dengan pure CSS
    3. Melakukan perbaikan pada tampilan mobile
    4. Menambahkan dokumentasi pada README.md
    5. Update tampilan skills-card pada mobile agar lebih nyaman dibaca dan melakukan refining layout
    6. Mengubah keseluruhan text pada Skills section agar sesuai dengan konteks section
    7. Membuat elemen navbar menjadi `position: fixed` sehingga ketika user scroll, navbar akan selalu mengikuti diatasnya
- 5 September 2026:
    1. Menambahkan Progress Mingguan, Tutorial set-up local, dan AI Disclosure Tugas 1

### 🤖 AI Disclosure

#### AI Tools yang Digunakan

- **Claude**: digunakan untuk membantu permasalahan proses git.
    
    **Link:** https://claude.ai/share/f14bd50f-a4b4-4984-9f18-428623e0f963
- **ChatGPT**: digunakan untuk menanyakan penyebab layout Grid/Flexbox yang tidak sesuai ekspektasi, dengan cara mencari kesalahan pada kode yang sudah saya tulis serta menanyakan copywriting yang baik untuk konten section portofolio.
    
    **Link:**: https://chatgpt.com/share/6a9983b6-6020-83ec-a2bb-ec0f40bb849e
- **Gemini**: digunakan untuk membantu copywriting, baik untuk konten portofolio maupun pesan commit yang professional
    
    **Link:** https://share.gemini.google/qSBgxFbT12dv

#### Pembagian Kontribusi

Hampir seluruh bagian HTML dan CSS saya kerjakan sendiri, termasuk:
- Pengisian section **About Me** dengan data asli (nama, NPM, foto, bio).
- Pembuatan section baru beserta minimal 3 item konten di dalamnya.
- Penulisan aturan CSS khusus (Flexbox/Grid, styling, warna, efek hover) untuk section tersebut.

AI hanya dilibatkan pada bagian tertentu ketika saya mengalami kebuntuan, terutama:
- Masalah responsivitas mobile, di mana beberapa elemen sudah diberi `width: 100%` hingga ke parent element-nya, namun tidak tampil selebar yang diharapkan.
- Saran copywriting untuk isi konten section portofolio.

#### Keterbatasan AI

Selama proses debugging layout, ditemukan keterbatasan AI dalam **image and context recognition**. AI tidak dapat sepenuhnya memahami konteks visual dari layout yang sedang saya kerjakan, sehingga solusi yang diberikan terkadang tidak sesuai dengan kondisi nyata halaman.

Contohnya saat memperbaiki tampilan **skills-card** untuk versi mobile, solusi layout Grid yang disarankan AI justru membuat susunan card menjadi lebih sulit dibaca dan tidak rapi, alih-alih memperbaiki masalah width yang saya keluhkan.

#### Perbaikan Manual

Karena solusi AI belum menyelesaikan masalah dengan tepat, saya melakukan penelusuran manual terhadap struktur CSS untuk menemukan akar permasalahan layout (seperti box-sizing, padding/margin yang tidak diperhitungkan, atau parent container yang membatasi width). Proses ini tetap dibantu AI sebagai alat diskusi ketika mengalami kebuntuan, namun keputusan akhir dan penyesuaian struktur CSS dilakukan secara manual berdasarkan pemahaman saya sendiri terhadap penyebab masalahnya, bukan sekadar menerapkan solusi Grid yang disarankan sebelumnya.


## Tugas 2

### ❓ Pertanyaan
1. Alur yang terjadi ketika pengguna membuka url portofolio dari browser (user melakukan *request*), lalu Django akan mengecek prefix pathnya pada `urls.py` project. Setelah itu, akan dilemparnya ke `urls.py` app yang cocok. Setelah ditemukan yang cocok, Django akan memanggil fungsi `views.py` . `views.py` akan melakukan pengambilan dan pemrosesan data dari model apabila dibutuhkan, sekaligus mengirim contextnya ke template portofolio. Setelah itu, templatenya dirender menjadi HTML dan dikembalikan sebagai response kepada user.

2. Alasan mengapa data untuk portofolio disimpan dalam model adalah kemudahan untuk mengedit dan untuk melakukan *scale up* apabila terdapat hal - hal baru yang ingin ditambahkan yang tentunya mempermudah dalam hal pemeliharaan dan pengembangan aplikasi

3. Perbedaan makemigrations dan migrate adalah makemigrations hanya membuat sebuah berkas yang berisi perubahan model yang **belum** diaplikasikan dalam basis data. Sedangkan migrate adalah mengaplikasikan perubahan modelnya yang sudah ada di berkas perubahan model hasil makemigrations ke dalam basis data.

### 📶 Progress Mingguan
**Untuk Full *Commit History*, bisa lihat di branch tugas-2**
- 9 September 2026: 
    1. Menyelesaikan setup MVT untuk halaman `experience.html` (Tutorial 2)
    2. Mengubah bio dari awalnya hardcoded di template menjadi ada di `views.py`
    3. Fix Django Version
    4. Membuat model `Project` dan melakukan migrasi model
    5. Menambahkan section `Project` di halaman utama (`index.html`)
- 10 September 2026:
    1. Melakukan redesign pada section skills - project
    2. Melakukan integrasi model ke admin page
    3. Memperbaiki error saat adminpage tidak dapat diakses pada versi deploy pws (csrf error)
    4. Membuat test untuk model Project

### 🤖 AI Disclosure

#### AI Tools yang Digunakan

- **Claude**: digunakan untuk membantu permasalahan layouting pada bagian project-card, git error dan git commit message, dan kode untuk mengecek data apa saja yang sudah tersimpan dan cara menghapusnya, serta mengatasi csrf & admin page error
    
    **Link:** https://claude.ai/share/b65a48f1-d5a3-48c5-95a1-56875299a35d
    **Link:** https://claude.ai/share/8fe37de8-1b6b-42b0-9143-b3866c4a9f72

#### Pembagian Kontribusi

Hampir seluruh bagian saya kerjakan sendiri, termasuk:
- Pembuatan Model Project, dan integrasinya juga pada `views.py`, `index.html`.
- Melakukan perubahan di bagian - bagian yang sebelumnya hardcoded pada template
- Pembuatan tampilan baru section skill-project
- Penulisan CSS untuk section baru

AI hanya dilibatkan pada bagian tertentu ketika saya mengalami kebuntuan, terutama:
- Masalah responsivitas tampilan, tampilan belum sesuai harapan sehingga menanyakan inti permasalahan dari kode yang saya buat
- Saran copywriting untuk isi konten section portofolio & commit message.
- Error - error yang saya kurang mengerti, seperti csrf error dan error pada halaman admin

#### Keterbatasan AI

(Masih sama dengan Tugas-1)
Selama proses debugging layout, ditemukan keterbatasan AI dalam **image and context recognition**. AI tidak dapat sepenuhnya memahami konteks visual dari layout yang sedang saya kerjakan, sehingga solusi yang diberikan terkadang tidak sesuai dengan kondisi nyata halaman. Terutama dalam membuat design project-card


#### Perbaikan Manual
Karena terkadang AI masih belum tepat, terutama pada bagian thumbnail untuk project-card, saya melakukan penyesuaian lebih lanjut untuk bagian tersebut agar terlihat lebih responsif


