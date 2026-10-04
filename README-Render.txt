# الخطوات للرفع على Render.com (ببلاش ويشتغل 24 ساعة)

## 1. ارفع على GitHub
1. اعمل ريبو جديد على github.com (اسمه fekra-ai-bot)
2. ارفع 3 ملفات دول:
   - bot_render.py (غير اسمه لـ bot.py بعد الرفع)
   - requirements.txt
   - render.yaml

## 2. اربط Render
1. ادخل render.com وسجل دخول بـ GitHub
2. دوس New + > Blueprint
3. اختار الريبو بتاعك
4. هيطلب منك الـ Environment Variables - حط دول:

   BOT_TOKEN = 8870740034:AAEnii8gXQqBvOdo_yaOodJt22yrhsBnGsQ
   SUPABASE_URL = https://khnzvskyutkrmaiyvaqgc.supabase.co
   SUPABASE_KEY = [المفتاح اللي جبته من Supabase]

5. دوس Apply

## 3. مبروك!
بعد دقيقتين البوت هيبقى Online ويرد على /start من غير ما تحتاج لابتوب ولا DNS

## ملاحظة مهمة
لو عايز تغير اسم الملف، في render.yaml غير startCommand لـ:
  python bot.py
