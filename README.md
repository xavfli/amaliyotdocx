# 📄 AmaliyotDocx – Talabalar amaliyot hujjatlarini avtomatlashtirish

AmaliyotDocx — bu Django asosida ishlab chiqilgan veb-loyiha bo‘lib, u orqali oliy ta’lim muassasalarining bitiruvchi yoki 3-kurs talabalari uchun amaliyotga tegishli barcha hujjatlarni avtomatik ravishda shakllantirish va ZIP ko‘rinishida yuklab olish imkoniyati yaratilgan.

---

## 🚀 Loyihaning asosiy imkoniyatlari

✅ Excel (`.xlsx`) yoki Word (`.docx`) fayli orqali talabalar ro‘yxatini yuklash  
✅ Har bir talaba uchun quyidagi hujjatlarni yaratish:
- `shartnoma.docx` (korxona va universitet o‘rtasidagi)
- `kundalik.docx` (talaba kundaligi)
- `yollanma.docx` (yo‘llanma)

✅ Yuklangan ma’lumotlarga asoslangan holda ZIP fayl ko‘rinishida barcha talabalarning hujjatlarini yuklab olish  
✅ Har bir talaba uchun alohida papka: `Hujjatlar/1/`, `Hujjatlar/2/` va hokazo  
✅ Boshlanish va tugash sanalarini foydalanuvchi o‘zi tanlaydi  
✅ 3-kurs uchun — ishlab chiqarish amaliyoti  
✅ 4-kurs uchun — bitiruv oldi amaliyoti  
✅ Talabalar ma’lumotlarini REST API orqali ko‘rish, yaratish, o‘zgartirish, o‘chirish  
✅ Login / Register orqali tizimga kirish va foydalanuvchi boshqaruvi

---

## 🛠 Texnologiyalar

| Texnologiya       | Izoh |
|-------------------|------|
| Python 3.12+      | Backend asosiy dasturlash tili |
| Django 5.x        | Web-framework |
| Django REST       | API yaratish uchun |
| docxtpl           | Word shablon fayllarni to‘ldirish uchun |
| openpyxl          | Excel fayllarni o‘qish uchun |
| HTML/CSS (Jinja)  | Templatelar |

---

## 🔐 Login / Register

> Tizimga faqat ro‘yxatdan o‘tgan foydalanuvchilar kirishi mumkin.

- `/login/` – foydalanuvchi kirish
- `/register/` – yangi foydalanuvchini ro‘yxatga olish
- `/logout/` – chiqish

---

## 📁 Hujjatlar tuzilmasi (zip)


````
Hujjatlar/
├── 1/
│   ├── shartnoma.docx
│   ├── kundalik.docx
│   └── yollanma.docx
├── 2/
│   ├── ...

````

> Har bir papka talabaning tartib raqamiga ko‘ra yaratiladi (id emas).

---

## ⚙️ Ishga tushurish (local)

1. Loyihani klon qiling:

````
```bash
git clone https://github.com/xavfli/amaliyotdocx.git
cd amaliyotdocx
````

2. Virtual muhit yarating:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Talab qilinadigan kutubxonalarni o‘rnating:

```bash
pip install -r requirements.txt
```

4. Migratsiyalarni bajarish:

```bash
python manage.py migrate
```

5. Superuser yaratish:

```bash
python manage.py createsuperuser
```

6. Serverni ishga tushuring:

```bash
python manage.py runserver
```

---

## 🌐 API endpointlari

```http
GET     /api/students/           - Barcha talabalar ro‘yxati
POST    /api/students/           - Yangi talaba qo‘shish
GET     /api/students/<id>/      - Talaba haqida ma’lumot
PUT     /api/students/<id>/      - Ma’lumotni yangilash
DELETE  /api/students/<id>/      - Talabani o‘chirish
```

---

## 📄 Shablonlar joylashuvi

* `app_excel/templates/app_excel/shartnoma_template.docx`
* `app_excel/templates/app_excel/kundalik_template.docx`
* `app_excel/templates/app_excel/yollanma_template.docx`

> Har bir Word fayl `{{ }}` orqali kontekstni oladi.

---

## 👨‍💻 Muallif

**Boburbek (xavfli)**
GitHub: [xavfli](https://github.com/xavfli)

---

## ✅ Foydalanishdagi maqsad

Ushbu loyiha OTMdagi dekant, fakultet yoki kafedra xodimlari tomonidan bitiruvchi talabalar amaliyoti hujjatlarini avtomatik tarzda shakllantirishni yengillashtirish maqsadida ishlab chiqilgan.

---

## 💡 Takliflar

Agar loyiha sizga foydali bo‘lsa:

* ⭐ GitHubda yulduz qo‘yish
* 🤝 Fork qilish
* 🛠 Yangi featurelar qo‘shish

xush kelibsiz!





---

Agar sizga `requirements.txt` yoki `API dokumentatsiyasi` ham kerak bo‘lsa, bemalol ayting — tayyorlab beraman.

