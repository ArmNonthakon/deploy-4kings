# 4kings

เป็นเว็บไซต์คัดสรรสถาบัน 4kings โดยคำนวณการคัดสรรสถาบันด้วย NLP(Natural Language Processing) มาช่วยในการคำนวณ ซึ่งจะใช้เป็น PyThaiNLP ของคนไทยเพื่อคำนวณข้อมูลภาษาไทย และการรับส่งข้อมูลก็จะใช้ websocket ทำให้สามารถส่งและรับข้อมูลได้แบบ real time ได้ ภายในเว็บไซต์ก็จะมีการตรวจจับ error ก่อนส่งข้อมูลไป

# วิธีติดตั้ง
เข้าโฟลเดอร์ที่จะเก็บไฟล์ และ clone ไฟล์จาก git ลงเครื่อง
```bash
git clone https://github.com/ArmNonthakon/4kings.git
```
เข้าไปในไฟล์โฟลเดอร์
```bash
cd 4kings
```
ติดตั้ง dependency ต่างๆ
```bash
pip install requirements.txt
```
run คำสั่ง
```bash
uvicorn main:app --reload
```

## เครดิต

 - [PyThaiNLP](https://pythainlp.github.io/)


