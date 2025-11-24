import json
import datetime
import os


# ===============================
# CLASS PERSON (LỚP CHA)
# ===============================
class Person:
    """
    Lớp cơ sở cho mọi thực thể con người trong hệ thống:
    - Patient (BN), Doctor (BS), Nurse (YT) sẽ kế thừa từ lớp này.
    """
    def __init__(self, pid, name, age, gender, contact=""):
        # id: mã định danh (vd: "BN001", "BS002")
        self.id = pid
        # name: tên đầy đủ
        self.name = name
        # age: tuổi (số nguyên)
        self.age = age
        # gender: giới tính (string)
        self.gender = gender
        # contact: thông tin liên lạc (sđt/email)
        self.contact = contact

    def to_dict(self):
        """
        Chuyển object thành dict để dễ lưu JSON.
        Lưu ý: subclasses có thể override và bổ sung trường riêng.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact
        }


# ===============================
# PATIENT (BỆNH NHÂN)
# ===============================
class Patient(Person):
    """
    Lớp đại diện bệnh nhân, kế thừa Person.
    Lưu thông tin bảo hiểm và danh sách hồ sơ y tế (medical_records).
    """
    def __init__(self, pid, name, age, gender, contact="", insurance=None):
        # gọi constructor lớp cha để khởi tạo các thuộc tính chung
        super().__init__(pid, name, age, gender, contact)
        # insurance: chuỗi hoặc dict thông tin bảo hiểm, None nếu không có
        self.insurance = insurance
        # medical_records: danh sách các bản ghi khám bệnh (mỗi bản ghi là dict)
        self.medical_records = []

    def add_record(self, record):
        """
        Thêm một bản ghi bệnh án vào patient.medical_records.
        record nên là dict có các khóa như: date, doctor, diagnosis, procedures, doctor_fee...
        """
        self.medical_records.append(record)

    def to_dict(self):
        """
        Ghi đè to_dict để bao gồm thông tin riêng của Patient.
        Trả về dict sẵn sàng để json.dump.
        """
        data = super().to_dict()
        data["insurance"] = self.insurance
        data["medical_records"] = self.medical_records
        return data


# ===============================
# DOCTOR (BÁC SĨ)
# ===============================
class Doctor(Person):
    """
    Lớp bác sĩ: có chuyên ngành (specialty), phí cơ bản (base_fee),
    và phần trăm phụ thu (extra_fee_percent). Có thể mở rộng thêm schedule.
    """

    def __init__(self, pid, name, age, gender, contact="", specialty="General",
                 base_fee=100, extra_fee_percent=0):
        super().__init__(pid, name, age, gender, contact)
        # specialty: chuyên môn của bác sĩ (chuỗi)
        self.specialty = specialty
        # base_fee: phí khám cơ bản (số)
        self.base_fee = base_fee
        # extra_fee_percent: phần trăm phụ thu trên tổng (VD: 10 => +10%)
        self.extra_fee_percent = extra_fee_percent
        # schedule: có thể lưu danh sách ca/khung giờ thực tế (hiện chưa sử dụng nhiều)
        self.schedule = []

    def calculate_fee(self, treatment_cost):
        """
        Tính phí khám dựa trên:
        - base_fee: phí cố định
        - treatment_cost: tổng chi phí điều trị (tiền thuốc, thủ thuật...)
        - specialty_multiplier: nhân thêm nếu chuyên ngành đắt hơn
        - extra_fee_percent: phần trăm phụ thu (ví dụ dịch vụ ngoài giờ)
        
        Trả về fee đã làm tròn 2 chữ số thập phân.
        """
        specialty_multiplier = {
            "Cardiology": 1.5,
            "Neurology": 1.6,
            "Pediatrics": 1.1,
            "Orthopedics": 1.3,
            "General": 1.0
        }

        # lấy hệ số theo chuyên ngành, mặc định 1.0 nếu không có trong dict
        mult = specialty_multiplier.get(self.specialty, 1.0)

        # fee cơ bản cộng với phần trị giá của treatment_cost nhân hệ số chuyên ngành
        fee = self.base_fee + treatment_cost * mult

        # thêm phụ phí theo phần trăm (nếu extra_fee_percent = 10 => tăng 10%)
        fee += fee * (self.extra_fee_percent / 100)

        # round để tránh float quá dài
        return round(fee, 2)

    def to_dict(self):
        """
        Chuyển Doctor thành dict; dùng khi lưu file.
        """
        d = super().to_dict()
        d["specialty"] = self.specialty
        d["base_fee"] = self.base_fee
        d["extra_fee_percent"] = self.extra_fee_percent
        d["schedule"] = self.schedule
        return d


# ===============================
# NURSE (Y TÁ)
# ===============================
class Nurse(Person):
    """
    Lớp Y tá; hiện tại chỉ có thêm thuộc tính ward (khoa/ban phụ trách).
    """

    def __init__(self, pid, name, age, gender, contact="", ward=None):
        super().__init__(pid, name, age, gender, contact)
        # ward: tên khoa hoặc mã phòng y tá phụ trách
        self.ward = ward

    def to_dict(self):
        d = super().to_dict()
        d["ward"] = self.ward
        return d


# ===============================
# LỊCH HẸN
# ===============================
class Appointment:
    """
    Lưu thông tin một cuộc hẹn:
    - aid: id cuộc hẹn
    - patient_id, doctor_id: tham chiếu đến persons dict của Hospital
    - date: chuỗi thời gian (hiện đang để date_str như chuỗi)
    - reason: lý do khám
    - status: trạng thái (Pending, Completed, Cancelled,...)
    - invoice_id: id hóa đơn nếu đã có
    """
    def __init__(self, aid, patient_id, doctor_id, date_str, reason="", status="Pending"):
        self.id = aid
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        # date lưu chuỗi, nhưng bạn có thể đổi sang datetime nếu muốn validate/so sánh
        self.date = date_str
        self.reason = reason
        self.status = status
        self.invoice_id = None

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "reason": self.reason,
            "status": self.status,
            "invoice_id": self.invoice_id
        }
