from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pythainlp.classify import GzipModel
import json
import pythainlp.util
import math
import random
app = FastAPI()

def isThaiText(txt):#ฟังชั่นตรวจสอบ text ว่าเป็นภาษาไทยไหม
    if pythainlp.util.isthai(txt):
        return True
    else:
        return False
def classify4King(inputNameMember):#ฟังชั่นรับค่า array ชื่อคน และทำการจัดสรรสมาชิกให้เท่ากัน ซึ่งจัดสรรด้วยการใช้ machine learning
    num = 0
    isCase = 0
    if len(inputNameMember)%4 == 0 or len(inputNameMember)/4 <= 0.5 or math.fmod(len(inputNameMember),4) == 3:#ตรวจสอบจำนวนที่รับเข้ามา แยกเคสและหาจำนวนที่เหมาะสมที่จะรับคนจำนวนนี้
        num = math.ceil(len(inputNameMember)/4)
        isCase = 1
    else :
        num = math.floor(len(inputNameMember)/4)
        isCase = 2
    training_data =  [#ข้อมูลที่ใช้ในการ train machine learning 
        ("บ่าง", "กนก"),("เคใหญ่", "กนก"),("ตุ้มเม้ง", "กนก"),("หนุ่ย", "กนก"),
        ("ราษฎร์", "อินทร"),("บิลลี่", "อินทร"),("ดา", "อินทร"),("รูแปง", "อินทร"),("หรั่ง", "อินทร"),
        ("มด", "ประชาชล"),("สุวิชชา", "ประชาชล"),("โอ๋", "ประชาชล"),("เอ็กซ์", "ประชาชล"),
        ("เอก", "บุรณพนธ์"),("รก", "บุรณพนธ์"),("เจี๊ยบ", "บุรณพนธ์")
    ]
    school = ["กนก","อินทร","ประชาชล","บุรณพนธ์"]
    result = {"กนก" : [],"อินทร" : [],"ประชาชล" : [],"บุรณพนธ์" : [],}
    model = GzipModel(training_data)#นำ dataset มาเทรนผ่าน model GzipModel และจะทำนายผ่านคำสั่ง model.predict(name, k=2)
    

    if isCase == 1:         #เคสแรก คือ จำนวนที่เปิดรับของแต่ละโรงเรียนจะเพียงพอต่อจัดสรรพอดี วิธีคำนวณก็จะวนลูปและก็เช็คผ่านคำสั่ง model.predict 
        index = 0           #ไปเรื่อยๆ ถ้าโรงเรียนไหนเต็มแล้วก็จะตัดโรงเรียนนั้นออกและเทรนข้อมูลใหม่และเช็คไปเรื่อยๆจนครบ ซึ่งจำนวนคนจะครบพอดีไม่มีเหลือ
        while(True):
            if index == len(inputNameMember):break
            name = inputNameMember[index]
            schoolChoose= model.predict(name, k=2)
            for nameSchool in school:
                if schoolChoose == nameSchool:
                    if len(result[nameSchool]) == num:
                        numDel = 0
                        for j in range(len(training_data)):
                            if training_data[j][1] == nameSchool:
                                training_data[j] = 1
                                numDel += 1
                        for j in range(numDel):
                            training_data.remove(1)
                        model = GzipModel(training_data)
                        break
                    else:
                        result[nameSchool].append(name)
                        index += 1
                        break
                else:
                    continue
    else:                             #เคสที่สอง คือ แต่ละโรงเรียนก็จะเปิดรับคนตามจำนวน num ซึ่งจะมีจำนวนคนที่จะเกินมา 1-2 คน วิธีคำนวณ                                    
        studentLeft = []              #วิธีคำนวณ ก็จะวนลูปเช็คไปเรื่อยๆจนครบ ก็จะเหลือเศษออกมา ซึ่งถ้าหากมีโรงเรียนที่ยังไม่เต็มตามจำนวน Num
        for name in inputNameMember:  #ก็จำเป็นที่จะต้องส่งจำนวนเข้าไปจนเต็ม และเพิ่มค่า num และวนเช็คจนครบทุกคน
            schoolChoose= model.predict(name, k=2)
            for nameSchool in school:
                if schoolChoose == nameSchool:
                    if len(result[nameSchool]) == num:
                        studentLeft.append(name)
                        break
                    else:
                        result[nameSchool].append(name)
                        break
                else:
                    continue
        for name in studentLeft:
            schoolChoose = model.predict(name, k=2)
            while(True):              
                if len(result[schoolChoose]) != num:
                    result[schoolChoose].append(name)
                schoolLeft = []
                count = 0
                for nameSchool in school:
                    if len(result[nameSchool]) < num:
                        schoolLeft.append(nameSchool) 
                        count += 1
                if count == 0 :
                    num +=1
                else:
                    result[schoolLeft[random.randint(0, count-1)]].append(name)
                    break
            
    return result



app.mount("/public", StaticFiles(directory="public"), name='public')
@app.get("/")
async def get():
    with open('public/html/index.html', 'r',encoding='utf-8') as file:
        index = file.read()
    return HTMLResponse(index)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        num = await websocket.receive_text() #รับจำนวนผู้คัดสรรจาก client ผ่าน websocket
        num = int(num)
        allName = []
        count = 0
        while(True):                         #รับชื่อผู้คัดสรรตามจำนวนจาก client ผ่าน websocket
            if count == num:break
            name = await websocket.receive_text()
            if isThaiText(name):             #ตรวจสอบชื่อภาษาไทย
                allName.append(name)
                count+=1
                await websocket.send_text(f"Successful enter name!!!")
            else :
                await websocket.send_text(f"Please input Thai name.")
        conTojson = json.dumps(classify4King(allName))#เรียกใช้ method classify4King และแปลงเป็น json ส่งกลับไปที่ client
        loaded_json = json.loads(conTojson)
        await websocket.send_json(loaded_json)
        