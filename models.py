from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Kota(Base):
    __tablename__ = "kota"

    id_kota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_kota = Column(String(100), nullable=False)
    provinsi = Column(String(100), nullable=False)
    status_aktif = Column(Boolean, default=True)


class Bus(Base):
    __tablename__ = "bus"

    id_bus = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_travel = Column(String(100), nullable=False)
    plat_nomor = Column(String(20), nullable=False)
    kapasitas = Column(Integer, nullable=False)
    tipe_kendaraan = Column(String(50), nullable=False)


class Rute(Base):
    __tablename__ = "rute"

    id_rute = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_kota_asal = Column(Integer, ForeignKey("kota.id_kota"), nullable=False)
    id_kota_tujuan = Column(Integer, ForeignKey("kota.id_kota"), nullable=False)
    estimasi_waktu = Column(String(50), nullable=False)

    kota_asal = relationship("Kota", foreign_keys=[id_kota_asal])
    kota_tujuan = relationship("Kota", foreign_keys=[id_kota_tujuan])


class Jadwal(Base):
    __tablename__ = "jadwal"

    id_jadwal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_bus = Column(Integer, ForeignKey("bus.id_bus"), nullable=False)
    id_rute = Column(Integer, ForeignKey("rute.id_rute"), nullable=False)
    tanggal_berangkat = Column(Date, nullable=False)
    jam_berangkat = Column(Time, nullable=False)
    harga_tiket = Column(Numeric(10, 2), nullable=False)

    bus = relationship("Bus")
    rute = relationship("Rute")


class Penumpang(Base):
    __tablename__ = "penumpang"

    id_penumpang = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_lengkap = Column(String(100), nullable=False)
    umur = Column(Integer, nullable=False)
    no_hp = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)


class Pemesanan(Base):
    __tablename__ = "pemesanan"

    id_pemesanan = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_penumpang = Column(Integer, ForeignKey("penumpang.id_penumpang"), nullable=False)
    id_jadwal = Column(Integer, ForeignKey("jadwal.id_jadwal"), nullable=False)
    nomor_kursi = Column(String(100), nullable=False)
    jumlah_kursi = Column(Integer, nullable=False)
    total_harga = Column(Numeric(10, 2), nullable=False)
    status_pemesanan = Column(String(50), default="Pending")
    tanggal_pemesanan = Column(DateTime, default=datetime.now)

    penumpang = relationship("Penumpang")
    jadwal = relationship("Jadwal")

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)