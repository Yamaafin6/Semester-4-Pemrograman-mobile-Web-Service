# Impor modul yang diperlukan
from typing import Union  # Mengimpor modul Union dari modul typing untuk mendukung tipe data gabungan
from fastapi import FastAPI, Response, Request, HTTPException  # Mengimpor kelas FastAPI, Response, Request, dan HTTPException dari modul fastapi
from fastapi.middleware.cors import CORSMiddleware  # Mengimpor kelas CORSMiddleware dari modul fastapi.middleware.cors untuk menangani masalah CORS
import sqlite3


# Inisialisasi aplikasi FastAPI
app = FastAPI()  # Membuat objek aplikasi FastAPI

# Menambahkan middleware CORSMiddleware untuk mengatasi masalah CORS (Cross-Origin Resource Sharing)
app.add_middleware(  # Menggunakan metode add_middleware() untuk menambahkan middleware
    CORSMiddleware,  # Menggunakan CORSMiddleware sebagai middleware
    allow_origins=["*"],  # Mengizinkan semua origin untuk CORS
    allow_credentials=True,  # Mengizinkan credentials untuk CORS
    allow_methods=["*"],  # Mengizinkan semua metode HTTP untuk CORS
    allow_headers=["*"],  # Mengizinkan semua header untuk CORS
)

# Routing dan handler untuk endpoint "/"
@app.get("/")  # Menentukan endpoint untuk HTTP GET request ke root path ("/")
def read_root():  # Definisi handler untuk endpoint root
    return {"Hello": "World"}  # Mengembalikan respons JSON dengan pesan "Hello World"

# Routing dan handler untuk endpoint "/mahasiswa/{nim}"
@app.get("/mahasiswa/{nim}")  # Menentukan endpoint untuk HTTP GET request ke path "/mahasiswa/{nim}"
def ambil_mhs(nim:str):  # Definisi handler untuk endpoint "/mahasiswa/{nim}"
    return {"nama": "Budi Martami"}  # Mengembalikan respons JSON dengan nama "Budi Martami"

# Routing dan handler untuk endpoint "/mahasiswa2/"
@app.get("/mahasiswa2/")  # Menentukan endpoint untuk HTTP GET request ke path "/mahasiswa2/"
def ambil_mhs2(nim:str):  # Definisi handler untuk endpoint "/mahasiswa2/"
    return {"nama": "Budi Martami 2"}  # Mengembalikan respons JSON dengan nama "Budi Martami 2"

# Routing dan handler untuk endpoint "/daftar_mhs/"
@app.get("/daftar_mhs/")  # Menentukan endpoint untuk HTTP GET request ke path "/daftar_mhs/"
def daftar_mhs(id_prov:str, angkatan:str):  # Definisi handler untuk endpoint "/daftar_mhs/"
    return {"query": " idprov: {}  ; angkatan: {} ".format(id_prov, angkatan),  # Mengembalikan respons JSON dengan pesan yang berisi data query
            "data": [{"nim": "1234"}, {"nim": "1235"}]}  # Mengembalikan data dalam bentuk list JSON dengan nim 1234 dan 1235

# Routing dan handler untuk endpoint "/init/"
@app.get("/init/")  # Menentukan endpoint untuk HTTP GET request ke path "/init/"
def init_db():  # Definisi handler untuk endpoint "/init/"
    try:
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuat koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        create_table = """ CREATE TABLE mahasiswa(  # Membuat tabel 'mahasiswa' dalam database
            ID      	INTEGER PRIMARY KEY 	AUTOINCREMENT,  # Kolom ID dengan tipe data INTEGER dan AUTOINCREMENT
            nim     	TEXT            	NOT NULL,  # Kolom nim dengan tipe data TEXT dan wajib diisi (NOT NULL)
            nama    	TEXT            	NOT NULL,  # Kolom nama dengan tipe data TEXT dan wajib diisi (NOT NULL)
            id_prov 	TEXT            	NOT NULL,  # Kolom id_prov dengan tipe data TEXT dan wajib diisi (NOT NULL)
            angkatan	TEXT            	NOT NULL,  # Kolom angkatan dengan tipe data TEXT dan wajib diisi (NOT NULL)
            tinggi_badan  INTEGER  # Kolom tinggi_badan dengan tipe data INTEGER
        )  
        """
        cur.execute(create_table)  # Membuat tabel mahasiswa dengan perintah SQL
        con.commit()  # Melakukan commit perubahan ke database
    except:
        return ({"status":"terjadi error"})  # Mengembalikan pesan error jika terjadi exception
    finally:
        con.close()  # Menutup koneksi ke database
    
    return ({"status":"ok, db dan tabel berhasil dicreate"})  # Mengembalikan pesan sukses jika tabel berhasil dibuat


# Impor BaseModel dari modul pydantic untuk digunakan dalam mendefinisikan model data
from pydantic import BaseModel
from typing import Optional  # Impor tipe Optional dari modul typing untuk mendukung nilai opsional

# Definisikan model Mhs (Mahasiswa) yang merupakan subkelas dari BaseModel
class Mhs(BaseModel):
   nim: str  # Field nim dengan tipe data string (wajib diisi)
   nama: str  # Field nama dengan tipe data string (wajib diisi)
   id_prov: str  # Field id_prov dengan tipe data string (wajib diisi)
   angkatan: str  # Field angkatan dengan tipe data string (wajib diisi)
   tinggi_badan: Optional[int] | None = None  # Field tinggi_badan dengan tipe data int (opsional, boleh null)

# Routing dan handler untuk endpoint "/tambah_mhs/"
@app.post("/tambah_mhs/", response_model=Mhs, status_code=201)  
def tambah_mhs(m: Mhs, response: Response, request: Request):
    try:
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        # Menjalankan perintah SQL untuk memasukkan data mahasiswa ke dalam tabel mahasiswa
        cur.execute("""insert into mahasiswa (nim, nama, id_prov, angkatan, tinggi_badan) 
                        values ("{}", "{}", "{}", "{}", {})""".format(m.nim, m.nama, m.id_prov, m.angkatan, m.tinggi_badan))
        con.commit()  # Melakukan commit perubahan ke database
    except:
        print("oioi error")  # Menampilkan pesan kesalahan jika terjadi exception
        return ({"status": "terjadi error"})  # Mengembalikan respons JSON dengan status error
    finally:  	 
        con.close()  # Menutup koneksi ke database
    response.headers["Location"] = "/mahasiswa/{}".format(m.nim)  # Menambahkan header Location pada respons dengan lokasi endpoint mahasiswa
    print(m.nim)  # Mencetak nim mahasiswa yang ditambahkan
    print(m.nama)  # Mencetak nama mahasiswa yang ditambahkan
    print(m.angkatan)  # Mencetak angkatan mahasiswa yang ditambahkan
  
    return m  # Mengembalikan data mahasiswa yang ditambahkan sebagai respons

# Routing dan handler untuk endpoint "/tampilkan_semua_mhs/"
@app.get("/tampilkan_semua_mhs/")  # Menentukan endpoint untuk HTTP GET request ke path "/tampilkan_semua_mhs/"
def tampil_semua_mhs():  # Definisi handler untuk endpoint "/tampilkan_semua_mhs/"
    try:
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        recs = []  # Inisialisasi list untuk menyimpan hasil query
        for row in cur.execute("select * from mahasiswa"):  # Melakukan query untuk menampilkan semua data mahasiswa
            recs.append(row)  # Menambahkan setiap baris hasil query ke dalam list recs
    except:
        return ({"status": "terjadi error"})  # Mengembalikan respons JSON dengan status error jika terjadi exception
    finally:  	 
        con.close()  # Menutup koneksi ke database
    return {"data": recs}  # Mengembalikan respons JSON berisi data mahasiswa

# Impor jsonable_encoder dari fastapi.encoders
from fastapi.encoders import jsonable_encoder

# Routing dan handler untuk endpoint "/update_mhs_put/{nim}"
@app.put("/update_mhs_put/{nim}", response_model=Mhs)  # Menentukan endpoint untuk HTTP PUT request ke path "/update_mhs_put/{nim}"
def update_mhs_put(response: Response, nim: str, m: Mhs):  # Definisi handler untuk endpoint "/update_mhs_put/{nim}"
    try:
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        cur.execute("select * from mahasiswa where nim = ?", (nim,))  # Melakukan query untuk mencari data mahasiswa dengan nim tertentu
        existing_item = cur.fetchone()  # Mengambil hasil query pertama
    except Exception as e:
        raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  # Mengembalikan respons error jika terjadi exception
    
    if existing_item:  # Jika data ditemukan
        print(m.tinggi_badan)  # Mencetak tinggi_badan mahasiswa yang diupdate
        cur.execute("update mahasiswa set nama = ?, id_prov = ?, angkatan = ?, tinggi_badan = ? where nim = ?",  # Melakukan perintah SQL untuk mengupdate data mahasiswa
                    (m.nama, m.id_prov, m.angkatan, m.tinggi_badan, nim))
        con.commit()  # Melakukan commit perubahan ke database
        response.headers["location"] = "/mahasiswa/{}".format(m.nim)  # Menambahkan header Location pada respons dengan lokasi endpoint mahasiswa
    else:  # Jika data tidak ditemukan
        print("item not found")  # Mencetak pesan bahwa data tidak ditemukan
        raise HTTPException(status_code=404, detail="Item Not Found")  # Mengembalikan respons error dengan status code 404
      
    con.close()  # Menutup koneksi ke database
    return m  # Mengembalikan data mahasiswa yang diupdate sebagai respons

# Definisikan model MhsPatch (Patch Mahasiswa)
class MhsPatch(BaseModel):
   nama: str | None = "kosong"  # Nama mahasiswa yang akan diupdate, defaultnya "kosong"
   id_prov: str | None = "kosong"  # ID provinsi mahasiswa yang akan diupdate, defaultnya "kosong"
   angkatan: str | None = "kosong"  # Tahun angkatan mahasiswa yang akan diupdate, defaultnya "kosong"
   tinggi_badan: Optional[int] | None = -9999  # Tinggi badan mahasiswa yang akan diupdate, defaultnya -9999 (boleh null)

# Routing dan handler untuk endpoint "/update_mhs_patch/{nim}"
@app.patch("/update_mhs_patch/{nim}", response_model=MhsPatch)  # Menentukan endpoint untuk HTTP PATCH request ke path "/update_mhs_patch/{nim}"
def update_mhs_patch(response: Response, nim: str, m: MhsPatch):  # Definisi handler untuk endpoint "/update_mhs_patch/{nim}"
    try:
        print(str(m))  # Mencetak data MhsPatch yang diterima
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        cur.execute("select * from mahasiswa where nim = ?", (nim,))  # Melakukan query untuk mencari data mahasiswa dengan nim tertentu
        existing_item = cur.fetchone()  # Mengambil hasil query pertama
    except Exception as e:
        raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  # Mengembalikan respons error jika terjadi exception
    
    if existing_item:  # Jika data ditemukan
        sqlstr = "update mahasiswa set "  # Membuat string SQL untuk melakukan update data mahasiswa
        # Todo: bisa direfaktor dan dirapikan
        if m.nama != "kosong":  # Jika nama tidak "kosong"
            if m.nama is not None:  # Jika nama tidak null
                sqlstr = sqlstr + " nama = '{}' ,".format(m.nama)  # Menambahkan perintah update nama ke string SQL
            else:     
                sqlstr = sqlstr + " nama = null ,"  # Jika nama null, set nama menjadi null
        
        if m.angkatan != "kosong":  # Jika angkatan tidak "kosong"
            if m.angkatan is not None:  # Jika angkatan tidak null
                sqlstr = sqlstr + " angkatan = '{}' ,".format(m.angkatan)  # Menambahkan perintah update angkatan ke string SQL
            else:
                sqlstr = sqlstr + " angkatan = null ,"  # Jika angkatan null, set angkatan menjadi null
        
        if m.id_prov != "kosong":  # Jika id_prov tidak "kosong"
            if m.id_prov is not None:  # Jika id_prov tidak null
                sqlstr = sqlstr + " id_prov = '{}' ,".format(m.id_prov)   # Menambahkan perintah update id_prov ke string SQL
            else:
                sqlstr = sqlstr + " id_prov = null, "   # Jika id_prov null, set id_prov menjadi null     

        if m.tinggi_badan != -9999:  # Jika tinggi_badan bukan -9999
            if m.tinggi_badan is not None:  # Jika tinggi_badan tidak null
                sqlstr = sqlstr + " tinggi_badan = {} ,".format(m.tinggi_badan)  # Menambahkan perintah update tinggi_badan ke string SQL
            else:    
                sqlstr = sqlstr + " tinggi_badan = null ,"  # Jika tinggi_badan null, set tinggi_badan menjadi null

        sqlstr = sqlstr[:-1] + " where nim = '{}' ".format(nim)  # Menghapus koma terakhir dan menambahkan kondisi WHERE ke string SQL
        print(sqlstr)  # Mencetak string SQL yang akan dieksekusi
        try:
            cur.execute(sqlstr)  # Mengeksekusi perintah SQL untuk update data mahasiswa
            con.commit()  # Melakukan commit perubahan ke database         
            response.headers["location"] = "/mahasixswa/{}".format(nim)  # Menambahkan header Location pada respons dengan lokasi endpoint mahasiswa
        except Exception as e:
            raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  # Mengembalikan respons error jika terjadi exception   
        

    else:  # Jika data tidak ditemukan
        raise HTTPException(status_code=404, detail="Item Not Found")  # Mengembalikan respons error dengan status code 404
   
    con.close()  # Menutup koneksi ke database
    return m  # Mengembalikan data MhsPatch sebagai respons


# Routing dan handler untuk endpoint "/delete_mhs/{nim}"
@app.delete("/delete_mhs/{nim}")  # Menentukan endpoint untuk HTTP DELETE request ke path "/delete_mhs/{nim}"
def delete_mhs(nim: str):  # Definisi handler untuk endpoint "/delete_mhs/{nim}"
    try:
        DB_NAME = "upi.db"  # Nama file database
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor
        sqlstr = "delete from mahasiswa where nim = '{}'".format(nim)  # Membuat string SQL untuk menghapus data mahasiswa dengan nim tertentu
        print(sqlstr)  # Mencetak string SQL untuk debug
        cur.execute(sqlstr)  # Mengeksekusi perintah SQL untuk menghapus data mahasiswa
        con.commit()  # Melakukan commit perubahan ke database
    except:
        return ({"status": "terjadi error"})  # Mengembalikan respons error jika terjadi exception   
    finally:  	 
        con.close()  # Menutup koneksi ke database
    
    return {"status": "ok"}  # Mengembalikan respons sukses setelah menghapus data mahasiswa
