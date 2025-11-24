import json
import uuid
import datetime
import os

class Person:
    #khai báo biến
    def __init__(self, pid, name, age, gender, contact=""):
        self.id = pid               # mã định danh
        self.name = name            # tên
        self.age = age              # tuổi
        self.gender = gender        # giới tính
        self.contact = contact      # liên hệ (email/sđt)

    #lưu trữ thông tin thành dict để đưa vào JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact
        }
class Patient(Person):
    #kế thừa
    def __init__(self, pid, name, age, gender, contact="", insurance=None):
        super().__init__(pid, name, age, gender, contact)
        self.insurance = insurance
        self.medical_records = []
    #thêm bản ghi bệnh án
    def add_record(self, record):
        self.medical_records.append(record)

    #chuyển dữ liệu thành dict để lưu file
    def to_dict(self):
        d = super().to_dict()               # lấy dict từ Person
        d["insurance"] = self.insurance
        d["medical_records"] = self.medical_records
        return d

# DOCTOR
class Doctor(Person):
    
    def __init__(self, pid, name, age, gender, contact="", specialty="General", base_fee=100, extra_fee_percent=0):
        super().__init__(pid, name, age, gender, contact)
        self.specialty = specialty           # chuyên ngành
        self.base_fee = base_fee             # phí khám cơ bản
        self.extra_fee_percent = extra_fee_percent  # phần trăm phụ thu
        self.schedule = []                   # danh sách lịch làm việc


    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "datetime": self.datetime,
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "invoice_id": self.invoice_id
        }

    #cập nhật
    def to_dict(self):
        d = super().to_dict()
        d["specialty"] = self.specialty
        d["base_fee"] = self.base_fee
        d["extra_fee_percent"] = self.extra_fee_percent
        d["schedule"] = self.schedule
        return d
class Appointment:
    def __init__(self, aid, patient_id, doctor_id, date_str, reason="", status="Pending"):
        self.id = aid                      # mã cuộc hẹn
        self.patient_id = patient_id       # bệnh nhân
        self.doctor_id = doctor_id         # bác sĩ
        self.datetime = date_str           # thời gian cuộc hẹn
        self.reason = reason               # lý do khám
        self.status = status               # trạng thái (Pending, Completed, Cancelled…)
        self.notes = []                    # ghi chú thêm
        self.invoice_id = None             # hóa đơn sau khi khám

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "datetime": self.datetime,
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "invoice_id": self.invoice_id
        }
