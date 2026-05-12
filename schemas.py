
from pydantic import BaseModel
from datetime import date, time, datetime
from decimal import Decimal


class KotaBase(BaseModel):
    nama_kota: str
    provinsi: str
    status_aktif: bool = True


class KotaCreate(KotaBase):
    pass


class KotaResponse(KotaBase):
    id_kota: int

    class Config:
        from_attributes = True


class BusBase(BaseModel):
    nama_travel: str
    plat_nomor: str
    kapasitas: int
    tipe_kendaraan: str


class BusCreate(BusBase):
    pass


class BusResponse(BusBase):
    id_bus: int

    class Config:
        from_attributes = True


class RuteBase(BaseModel):
    id_kota_asal: int
    id_kota_tujuan: int
    estimasi_waktu: str


class RuteCreate(RuteBase):
    pass


class RuteResponse(RuteBase):
    id_rute: int

    class Config:
        from_attributes = True


class JadwalBase(BaseModel):
    id_bus: int
    id_rute: int
    tanggal_berangkat: date
    jam_berangkat: time
    harga_tiket: Decimal


class JadwalCreate(JadwalBase):
    pass


class JadwalResponse(JadwalBase):
    id_jadwal: int

    class Config:
        from_attributes = True


class PenumpangBase(BaseModel):
    nama_lengkap: str
    umur: int
    no_hp: str
    email: str


class PenumpangCreate(PenumpangBase):
    pass


class PenumpangResponse(PenumpangBase):
    id_penumpang: int

    class Config:
        from_attributes = True


class PemesananBase(BaseModel):
    id_penumpang: int
    id_jadwal: int
    nomor_kursi: str
    jumlah_kursi: int
    total_harga: Decimal


class PemesananCreate(PemesananBase):
    pass


class PemesananResponse(PemesananBase):
    id_pemesanan: int
    status_pemesanan: str
    tanggal_pemesanan: datetime

    class Config:
        from_attributes = True