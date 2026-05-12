import os
from dotenv import load_dotenv
from fastapi import Header
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Travel API")

load_dotenv()

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key tidak valid")
    return True

@app.get("/")
def home():
    return {"message": "API Booking Travel berjalan"}


# ===================== KOTA =====================

@app.get("/kota", response_model=list[schemas.KotaResponse])
def get_kota(
    db: Session = Depends(get_db),
    auth: bool = Depends(verify_api_key)
):
    return db.query(models.Kota).all()

@app.get("/kota/search", response_model=list[schemas.KotaResponse])
def search_kota(nama: str, db: Session = Depends(get_db)):
    return db.query(models.Kota).filter(models.Kota.nama_kota.like(f"%{nama}%")).all()


@app.post("/kota", response_model=schemas.KotaResponse)
def create_kota(kota: schemas.KotaCreate, db: Session = Depends(get_db)):
    data = models.Kota(**kota.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/kota/{id}", response_model=schemas.KotaResponse)
def update_kota(id: int, kota: schemas.KotaCreate, db: Session = Depends(get_db)):
    data = db.query(models.Kota).filter(models.Kota.id_kota == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Kota tidak ditemukan")

    for key, value in kota.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data

@app.post("/kota/bulk", response_model=list[schemas.KotaResponse])
def create_kota_bulk(kota_list: list[schemas.KotaCreate], db: Session = Depends(get_db)):
    data_list = []

    for kota in kota_list:
        data = models.Kota(**kota.model_dump())
        db.add(data)
        data_list.append(data)

    db.commit()

    for data in data_list:
        db.refresh(data)

    return data_list

@app.delete("/kota/{id}")
def delete_kota(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Kota).filter(models.Kota.id_kota == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Kota tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Kota berhasil dihapus"}


# ===================== BUS =====================

@app.get("/bus", response_model=list[schemas.BusResponse])
def get_bus(db: Session = Depends(get_db)):
    return db.query(models.Bus).all()


@app.post("/bus", response_model=schemas.BusResponse)
def create_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    data = models.Bus(**bus.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/bus/{id}", response_model=schemas.BusResponse)
def update_bus(id: int, bus: schemas.BusCreate, db: Session = Depends(get_db)):
    data = db.query(models.Bus).filter(models.Bus.id_bus == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Bus tidak ditemukan")

    for key, value in bus.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data


@app.delete("/bus/{id}")
def delete_bus(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Bus).filter(models.Bus.id_bus == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Bus tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Bus berhasil dihapus"}


# ===================== RUTE =====================

@app.get("/rute", response_model=list[schemas.RuteResponse])
def get_rute(db: Session = Depends(get_db)):
    return db.query(models.Rute).all()


@app.get("/rute/search", response_model=list[schemas.RuteResponse])
def search_rute(asal: int, tujuan: int, db: Session = Depends(get_db)):
    return db.query(models.Rute).filter(
        models.Rute.id_kota_asal == asal,
        models.Rute.id_kota_tujuan == tujuan
    ).all()


@app.post("/rute", response_model=schemas.RuteResponse)
def create_rute(rute: schemas.RuteCreate, db: Session = Depends(get_db)):
    data = models.Rute(**rute.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/rute/{id}", response_model=schemas.RuteResponse)
def update_rute(id: int, rute: schemas.RuteCreate, db: Session = Depends(get_db)):
    data = db.query(models.Rute).filter(models.Rute.id_rute == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Rute tidak ditemukan")

    for key, value in rute.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data


@app.delete("/rute/{id}")
def delete_rute(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Rute).filter(models.Rute.id_rute == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Rute tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Rute berhasil dihapus"}


# ===================== JADWAL =====================

@app.get("/jadwal", response_model=list[schemas.JadwalResponse])
def get_jadwal(db: Session = Depends(get_db)):
    return db.query(models.Jadwal).all()


@app.get("/jadwal/search", response_model=list[schemas.JadwalResponse])
def search_jadwal(rute: int, tanggal: date, db: Session = Depends(get_db)):
    return db.query(models.Jadwal).filter(
        models.Jadwal.id_rute == rute,
        models.Jadwal.tanggal_berangkat == tanggal
    ).all()


@app.post("/jadwal", response_model=schemas.JadwalResponse)
def create_jadwal(jadwal: schemas.JadwalCreate, db: Session = Depends(get_db)):
    data = models.Jadwal(**jadwal.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/jadwal/{id}", response_model=schemas.JadwalResponse)
def update_jadwal(id: int, jadwal: schemas.JadwalCreate, db: Session = Depends(get_db)):
    data = db.query(models.Jadwal).filter(models.Jadwal.id_jadwal == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")

    for key, value in jadwal.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data


@app.delete("/jadwal/{id}")
def delete_jadwal(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Jadwal).filter(models.Jadwal.id_jadwal == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Jadwal tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Jadwal berhasil dihapus"}


# ===================== PENUMPANG =====================

@app.get("/penumpang", response_model=list[schemas.PenumpangResponse])
def get_penumpang(db: Session = Depends(get_db)):
    return db.query(models.Penumpang).all()


@app.post("/penumpang", response_model=schemas.PenumpangResponse)
def create_penumpang(penumpang: schemas.PenumpangCreate, db: Session = Depends(get_db)):
    data = models.Penumpang(**penumpang.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/penumpang/{id}", response_model=schemas.PenumpangResponse)
def update_penumpang(id: int, penumpang: schemas.PenumpangCreate, db: Session = Depends(get_db)):
    data = db.query(models.Penumpang).filter(models.Penumpang.id_penumpang == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Penumpang tidak ditemukan")

    for key, value in penumpang.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data


@app.delete("/penumpang/{id}")
def delete_penumpang(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Penumpang).filter(models.Penumpang.id_penumpang == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Penumpang tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Penumpang berhasil dihapus"}


# ===================== PEMESANAN =====================

@app.get("/pemesanan", response_model=list[schemas.PemesananResponse])
def get_pemesanan(db: Session = Depends(get_db)):
    return db.query(models.Pemesanan).all()


@app.get("/pemesanan/riwayat", response_model=list[schemas.PemesananResponse])
def riwayat_pemesanan(db: Session = Depends(get_db)):
    return db.query(models.Pemesanan).order_by(models.Pemesanan.tanggal_pemesanan.desc()).all()


@app.get("/pemesanan/{id}", response_model=schemas.PemesananResponse)
def detail_pemesanan(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Pemesanan).filter(models.Pemesanan.id_pemesanan == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")
    return data


@app.post("/pemesanan", response_model=schemas.PemesananResponse)
def create_pemesanan(pemesanan: schemas.PemesananCreate, db: Session = Depends(get_db)):
    data = models.Pemesanan(
        **pemesanan.model_dump(),
        status_pemesanan="Berhasil"
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.put("/pemesanan/{id}", response_model=schemas.PemesananResponse)
def update_pemesanan(id: int, pemesanan: schemas.PemesananCreate, db: Session = Depends(get_db)):
    data = db.query(models.Pemesanan).filter(models.Pemesanan.id_pemesanan == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")

    for key, value in pemesanan.model_dump().items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return data


@app.put("/pemesanan/{id}/batal", response_model=schemas.PemesananResponse)
def batal_pemesanan(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Pemesanan).filter(models.Pemesanan.id_pemesanan == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")

    data.status_pemesanan = "Dibatalkan"
    db.commit()
    db.refresh(data)
    return data


@app.delete("/pemesanan/{id}")
def delete_pemesanan(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Pemesanan).filter(models.Pemesanan.id_pemesanan == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemesanan tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Pemesanan berhasil dihapus"}