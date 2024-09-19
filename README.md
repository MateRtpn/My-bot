# Bot-Moxz

## ทำอะไรได้บ้าง

- **/hello** - ทักทายผู้ใช้
- **/ping** - ตรวจสอบความเร็วในการตอบสนองของบอท
- **/info** - แสดงข้อมูลเกี่ยวกับเซิร์ฟเวอร์หรือผู้ใช้
- **/commands** - แสดงรายการคำสั่งทั้งหมดที่ใช้ได้
- **/ban** - แบนผู้ใช้ (ต้องมี `ADMIN_ROLE`)
- **/clear** - ลบข้อความที่ระบุ (ต้องมี `ADMIN_ROLE`)
- **/shutdown** - ปิดบอท (ใช้ได้เฉพาะผู้ที่มี `OWNER_ROLE`)

## วิธีติดตั้งและใช้งาน
 python -m venv venv



## สร้างไฟล์ .env และใส่ค่า environment variables
   ```bash

   DISCORD_TOKEN= discord bot token

   CHANNEL_ID= channel id

   ADMIN_ROLE= admin role id

   OWNER_ROLE= owner role id
