# lanlipu_portable_monitor_brightness_setting

สคริปต์ Bash สำหรับตั้งค่าความสว่าง ความคมชัด และสีของพอร์ทเทเบิลมอนิเตอร์ RTK (RealTek) 6432 โดยใช้เครื่องมือ `ddcutil` และ `xrandr` เพื่อควบคุมทั้งฮาร์ดแวร์และซอฟต์แวร์

## ข้อกำหนดเบื้องต้น

- ระบบปฏิบัติการ Linux ที่รองรับ `ddcutil` และ `xrandr`
- ติดตั้ง `ddcutil` (สคริปต์จะพยายามติดตั้งให้หากไม่มี บน Ubuntu/Debian)
- สิทธิ์ sudo สำหรับรันคำสั่ง `ddcutil`
- พอร์ทเทเบิลมอนิเตอร์ RTK 6432 เชื่อมต่อและตรวจจับได้

## การติดตั้ง

1. โคลน repository นี้ไปยังเครื่องของคุณ:
   ```
   git clone https://github.com/pbseiya/lanlipu_portable_monitor_brightness_setting.git
   cd lanlipu_portable_monitor_brightness_setting
   ```

2. ทำให้ไฟล์สคริปต์เป็นไฟล์ที่รันได้:
   ```
   chmod +x portable_monitor_setting.sh
   ```

## การใช้งาน

รันสคริปต์โดยใช้คำสั่ง:
```
./portable_monitor_setting.sh
```

สคริปต์จะ:
- ตรวจจับพอร์ทเทเบิลมอนิเตอร์ RTK 6432 อัตโนมัติ
- แสดงเมนูให้เลือกประเภทเมนู (Simple หรือ Advanced)
- ใช้การตั้งค่าที่เหมาะสมตามโหมดที่เลือก

### เมนูหลัก

- **Simple Menu**: มี 3 โหมดพื้นฐานสำหรับผู้ใช้ทั่วไป
- **Advanced Menu**: มี 8 โหมดสำหรับงานเฉพาะ เช่น การเขียนโค้ด ความบันเทิง การเล่นเกม

### โหมดต่างๆ

#### Simple Menu
1. **Standard Mode**: ค่าเริ่มต้นจากโรงงาน (Preset 0x05, Contrast 50, RGB 50/50/50, Brightness 100, Software Brightness 1.0)
2. **Boost Mode**: ความสว่างสูงและความคมชัด (Preset 0x08, Contrast 75, RGB 80/80/80, Brightness 100, Software Brightness 1.0)
3. **Max Mode**: สูงสุดฮาร์ดแวร์ + ซอฟต์แวร์ (Preset 0x08, Contrast 100, RGB 80/80/80, Brightness 100, Software Brightness 1.2)

#### Advanced Menu
1. **Standard Mode**: ค่าเริ่มต้นจากโรงงาน
2. **Code: Light Mode**: เหมาะสำหรับการเขียนโค้ดในสภาพแสงสว่าง (Preset 0x05, Contrast 75, RGB 50/50/50, Brightness 100, Software Brightness 1.0)
3. **Code: Dark Mode**: เหมาะสำหรับการเขียนโค้ดในสภาพแสงมืด เพื่อลดความเมื่อยล้าของสายตา (Preset 0x05, Contrast 60, RGB 50/50/50, Brightness 40, Software Brightness 1.0)
4. **Movie Mode**: เหมาะสำหรับดูหนัง อบอุ่นและภาพยนตร์ (Preset 0x04, Contrast 80, RGB 50/50/50, Brightness 90, Software Brightness 1.0)
5. **Reading Mode**: เหมาะสำหรับอ่านเว็บหรือ e-book (Preset 0x04, Contrast 45, RGB 50/50/50, Brightness 35, Software Brightness 0.9)
6. **Game: FPS/Competitive**: เหมาะสำหรับเกม FPS ที่ต้องการการมองเห็นสูงสุด (Preset 0x08, Contrast 85, RGB 80/80/80, Brightness 100, Software Brightness 1.0)
7. **Game: RPG/Immersive**: เหมาะสำหรับเกม RPG ที่ต้องการสีสันสดใส (Preset 0x02, Contrast 80, RGB 50/50/50, Brightness 95, Software Brightness 1.0)
8. **Max Mode**: โหมดสูงสุด (Preset 0x08, Contrast 100, RGB 80/80/80, Brightness 100, Software Brightness 1.2)

## สคริปต์เสริม (Utility Scripts)

### `extract_edid.py`
สคริปต์ Python นี้ใช้สำหรับตรวจสอบและดึงข้อมูลดิบ (Raw EDID) จาก output ของ `ddcutil`.
- **จำเป็นต้องใช้เมื่อไหร่**: จอพกพาบางรุ่น (เช่น RTK ตัวนี้) อาจจะไม่ยอมส่งค่า EDID ผ่านเครื่องมือปกติ
- **มันทำอะไร**: สคริปต์นี้จะไปแกะรหัส Hex จากคำสั่ง `ddcutil detect --verbose` ออกมา เพื่อให้เรานำไปถอดรหัส (Decode) ดูสเปกเชิงลึกได้ (เช่น ค่าความสว่าง Nits, HDR)

## การแก้ปัญหา

- **ไม่พบมอนิเตอร์**: ตรวจสอบว่ามอนิเตอร์เชื่อมต่ออย่างถูกต้องและ `ddcutil detect` สามารถตรวจจับได้ หากไม่พบ สคริปต์จะถามให้ force try บน Display 1
- **สิทธิ์ไม่เพียงพอ**: ตรวจสอบว่าคุณมีสิทธิ์ sudo และ `ddcutil` ติดตั้งอย่างถูกต้อง
- **ไม่ทำงาน**: ตรวจสอบว่า output ของ xrandr เป็น DP-1 (สามารถแก้ไขในสคริปต์ได้ถ้าจำเป็น)

## ใบอนุญาต

โปรเจกต์นี้ใช้ใบอนุญาต MIT