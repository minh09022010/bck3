import json
import uuid
import datetime
import os

class Person:
    #khai báo biến
    def __init__(self, pid, name, age, gender, contact=""):
        self.id = pid
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact
    
    #lưu trữ
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

    #
    def add_record(self, record):
        self.medical_records.append(record)

    def to_dict(self):
        d = super().to_dict()
        d["insurance"] = self.insurance
        d["medical_records"] = self.medical_records
        return d


# DOCTOR
class Doctor(Person):
    
    def __init__(self, pid, name, age, gender, contact="", specialty="General", base_fee=100, extra_fee_percent=0):
        super().__init__(pid, name, age, gender, contact)
        self.specialty = specialty #chuyên ngành
        self.base_fee = base_fee #phí khám cơ bản
        self.extra_fee_percent = extra_fee_percent #% phụ phí
        self.schedule = []#lịch

    #tính tiền phí khám bệnh
    def calculate_fee(self, treatment_cost):
        specialty_multiplier = {
            "Cardiology": 1.5,
            "Neurology": 1.6,
            "Pediatrics": 1.1,
            "Orthopedics": 1.3,
            "General": 1.0
        }
        #lấy thông tin
        mult = specialty_multiplier.get(self.specialty, 1.0)

        #tính tiền
        fee = self.base_fee + treatment_cost * mult
        fee += fee * (self.extra_fee_percent / 100)
        return round(fee, 2)



    def to_dict(self):
        d = super().to_dict()
        d["specialty"] = self.specialty
        d["base_fee"] = self.base_fee
        d["extra_fee_percent"] = self.extra_fee_percent
        d["schedule"] = self.schedule
        return d
