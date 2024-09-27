transform Data - Nested array Mongodb
==========================================================================

Library ini digunakan untuk memudahkan melakukan transformasi Data
setelah proses extract atau pengambilan data

Penggunaan
----------

Instalasi
~~~~~~~~~

Untuk mendownload dan menginstall library ini, gunakan perintah

.. code:: sh

    pip install StatistikPendidikan

Pemanggilan
~~~~~~~~~~~

Pemanggilan fungsi bisa dilakukan dengan import sederhana terhadap
function yang tersedia

.. code:: python

    import StatistikPendidikan.KemdikbudScrapper
    api = StatistikPendidikan.KemdikbudScrapper("sd","2017")
    api.getGambaranUmumSekolahPerProvinsi()

.. code:: json

    {'Prov. Jambi': {'Pagi': '2454', 'Siang': '5778', 'Kombinasi': '25261', 'Jumlah': '18666'}, 'Prov. Sumatera Selatan': {'Pagi': '4662', 'Siang': '16383', 'Kombinasi': '54676', 'Jumlah': '39405'}, 'Prov. Lampung': {'Pagi': '4660', 'Siang': '11407', 'Kombinasi': '51543', 'Jumlah': '37123'}, 'Prov. Kalimantan Barat': {'Pagi': '4381', 'Siang': '25684', 'Kombinasi': '35340', 'Jumlah': '30687'}, 'Prov. Kalimantan Tengah': {'Pagi': '2625', 'Siang': '6711', 'Kombinasi': '22500', 'Jumlah': '17335'}, 'Prov. Kalimantan Selatan': {'Pagi': '2911', 'Siang': '9364', 'Kombinasi': '27806', 'Jumlah': '20566'}, 'Prov. Kalimantan Timur': {'Pagi': '1869', 'Siang': '6063', 'Kombinasi': '23524', 'Jumlah': '17488'}, 'Prov. Sulawesi Utara': {'Pagi': '2227', 'Siang': '2634', 'Kombinasi': '16434', 'Jumlah': '14311'}, 'Prov. Sulawesi Tengah': {'Pagi': '2889', 'Siang': '7301', 'Kombinasi': '24494', 'Jumlah': '18842'}, 'Prov. Sulawesi Selatan': {'Pagi': '6422', 'Siang': '11446', 'Kombinasi': '65408', 'Jumlah': '45580'}, 'Prov. Sulawesi Tenggara': {'Pagi': '2310', 'Siang': '5794', 'Kombinasi': '21724', 'Jumlah': '16246'}, 'Prov. Maluku': {'Pagi': '1772', 'Siang': '4919', 'Kombinasi': '15506', 'Jumlah': '11765'}, 'Prov. Bali': {'Pagi': '2444', 'Siang': '1985', 'Kombinasi': '24210', 'Jumlah': '17162'}, 'Prov. Nusa Tenggara Barat': {'Pagi': '3174', 'Siang': '7092', 'Kombinasi': '36544', 'Jumlah': '22322'}, 'Prov. Nusa Tenggara Timur': {'Pagi': '5056', 'Siang': '32087', 'Kombinasi': '48856', 'Jumlah': '36857'}, 'Prov. Papua': {'Pagi': '2474', 'Siang': '16431', 'Kombinasi': '16208', 'Jumlah': '17649'}, 'Prov. Bengkulu': {'Pagi': '1375', 'Siang': '4219', 'Kombinasi': '14128', 'Jumlah': '10484'}, 'Prov. Maluku Utara': {'Pagi': '1305', 'Siang': '2781', 'Kombinasi': '9247', 'Jumlah': '8281'}, 'Prov. Banten': {'Pagi': '4562', 'Siang': '9524', 'Kombinasi': '53354', 'Jumlah': '42126'}, 'Prov. Kepulauan Bangka Belitung': {'Pagi': '807', 'Siang': '4657', 'Kombinasi': '8105', 'Jumlah': '6464'}, 'Prov. Gorontalo': {'Pagi': '935', 'Siang': '4859', 'Kombinasi': '7542', 'Jumlah': '6166'}, 'Prov. Kepulauan Riau': {'Pagi': '921', 'Siang': '2724', 'Kombinasi': '12595', 'Jumlah': '9288'}, 'Prov. Papua Barat': {'Pagi': '1016', 'Siang': '5807', 'Kombinasi': '7015', 'Jumlah': '7030'}, 'Prov. Sulawesi Barat': {'Pagi': '1327', 'Siang': '2948', 'Kombinasi': '11939', 'Jumlah': '8887'}, 'Prov. Kalimantan Utara': {'Pagi': '463', 'Siang': '1620', 'Kombinasi': '5327', 'Jumlah': '3884'}}

Fungsi Tersedia
~~~~~~~~~~~~~~~

1. getGambaranUmumSekolahByStatus
2. getGambaranUmumSekolahPerProvinsi
3. getGambaranUmumSekolahPerProvinsiPerWaktuPenyelenggaraan
4. getJumlahSiswaMenurutAgamaTiapProvinsi License ----

MIT License
