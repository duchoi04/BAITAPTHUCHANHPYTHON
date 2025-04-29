import json
import os

# Lớp Student
class Student:
    def __init__(self, name, mssv, student_class, phone, birthday, address):
        self.name = name
        self.mssv = mssv
        self.student_class = student_class
        self.phone = phone
        self.birthday = birthday
        self.address = address

    def to_dict(self):
        return {
            "Họ tên": self.name,
            "MSSV": self.mssv,
            "Lớp": self.student_class,
            "SĐT": self.phone,
            "Ngày sinh": self.birthday,
            "Địa chỉ hiện tại": self.address
        }

# Lớp Family kế thừa Student
class Family(Student):
    def __init__(self, name, mssv, student_class, phone, birthday, address, family_address, father_name, mother_name):
        super().__init__(name, mssv, student_class, phone, birthday, address)
        self.family_address = family_address
        self.father_name = father_name
        self.mother_name = mother_name

    def to_dict(self):
        return {
            "Thông tin sinh viên": super().to_dict(),
            "Thông tin gia đình": {
                "Địa chỉ gia đình": self.family_address,
                "Họ tên bố": self.father_name,
                "Họ tên mẹ": self.mother_name
            }
        }

# Lớp quản lý danh sách sinh viên
class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.students, f, ensure_ascii=False, indent=4)

    def add_student(self, student: Family):
        new_id = 1 if not self.students else self.students[-1]["id"] + 1
        self.students.append({
            "id": new_id,
            **student.to_dict()
        })
        self.save()

    def update_student(self, student_id, new_student: Family):
        for i, student in enumerate(self.students):
            if student["id"] == student_id:
                self.students[i] = {
                    "id": student_id,
                    **new_student.to_dict()
                }
                self.save()
                return True
        return False

    def delete_student(self, student_id):
        initial_len = len(self.students)
        self.students = [s for s in self.students if s["id"] != student_id]
        if len(self.students) < initial_len:
            self.save()
            return True
        return False

    def show_students(self):
        for s in self.students:
            print(json.dumps(s, ensure_ascii=False, indent=4))


# ================================
# PHẦN THỬ NGHIỆM
# ================================
if __name__ == "__main__":
    manager = StudentManager()# Thêm sinh viên
    sv1 = Family(
        name="Nguyễn Văn A",
        mssv="12345678",
        student_class="DHTH17A",
        phone="0123456789",
        birthday="2002-05-10",
        address="KTX ĐHQG",
        family_address="Hà Nội",
        father_name="Nguyễn Văn B",
        mother_name="Trần Thị Hoa"
    )

    manager.add_student(sv1)
    manager.show_students()

    # Cập nhật
    sv1_update = Family(
        name="Nguyễn Văn A (updated)",
        mssv="12345678",
        student_class="DHTH17A",
        phone="0987654321",
        birthday="2002-05-10",
        address="KTX ĐHQG mới",
        family_address="Hà Nội",
        father_name="Nguyễn Văn B",
        mother_name="Trần Thị C"
    )
    manager.update_student(student_id=1, new_student=sv1_update)
    manager.show_students()

    # Xoá
    manager.delete_student(student_id=1)
    manager.show_students()