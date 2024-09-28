# import inspect


# def ij():
#     frame = inspect.currentframe().f_back
#     info = inspect.getframeinfo(frame)
#     print(f'{info.filename}')
#     return info.filename
import os
import inspect

# รับกรอบของฟังก์ชันที่เรียก
frame = inspect.currentframe().f_back

# รับข้อมูลเกี่ยวกับกรอบนั้น
info = inspect.getframeinfo(frame)

# รับชื่อไฟล์ที่เรียก
caller_file = os.path.basename(info.filename)

# พิมพ์ชื่อไฟล์ที่เรียก
print(f"โมดูลนี้ถูกนำเข้าในไฟล์: {caller_file}")

