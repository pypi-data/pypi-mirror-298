# UzAI

**UzAI** - bu oddiy sun'iy intellekt (AI) tizimi bo'lib, foydalanuvchining kiritgan savollariga oldindan belgilangan javoblarni beradi. Ushbu kutubxona oddiy savol-javoblarni avtomatlashtirish uchun moslashuvchan va foydalanuvchi do'stona interfeysni taklif qiladi. Bu dasturchilar va yangi o'rganayotganlar uchun sun'iy intellekt algoritmlarini yaratishda asosiy vosita sifatida foydalanishga mo'ljallangan.

## O'rnatish

**UzAI** kutubxonasini PyPI orqali o'rnatish juda oson. Buning uchun siz terminalga yoki buyruq satriga quyidagi buyruqni kiriting:

```bash
pip install uzai
```

## foydalanish
```python
from uzai import UzAi

# AI obyektini yaratish
ai = UzAi()

# Foydalanuvchidan savol olish
savol = input('Savol kiriting: ')

# Savolni AI ga uzatish
ai.question(savol)

# Oldindan belgilangan javoblarni kiritish
ai.response([
    {'ques': 'salom', 'resp': 'Salom, qanday yordam bera olaman?'},
])

#tasodifiy javoblarni aytish
ai.random_response([
    {'ques': 'qalaysan', 'ran_resp': 'yaxshiman, o\'zingiz qalaysiz?|yaxshi, siz yaxshimisiz?'}
])

# Javobni chiqarish
ai.run()

```