# سایت شخصی / آکادمیک — Nima Parifard

Django + SQLite. همه‌ی محتوا (پروژه، مقاله، کتاب، دوره، اخبار، سابقه) از پنل `/admin/` اضافه می‌شود؛ برای محتوای جدید لازم نیست کد بزنی.

## اجرا (اولین بار)

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_initial_data      # رزومه‌ات را در سایت می‌ریزد (امن است، چند بار هم اجرا شود تکراری نمی‌سازد)
python manage.py createsuperuser        # یوزر ادمین خودت
python manage.py runserver
```

سایت: http://127.0.0.1:8000 — پنل: http://127.0.0.1:8000/admin/

## چیزی اضافه کنم؟ (همه در /admin)

| می‌خواهم... | کجا |
|---|---|
| پروژه جدید + عکس/ویدیو/دمو | **Projects** ← پایین صفحه «media items»: عکس، ویدیو mp4، یا لینک یوتیوب/Vimeo |
| مقاله‌ای که دارم می‌نویسم | **Publications** ← status = *In preparation* و `progress` (درصد پیشرفت) |
| خبر | **News** (تیک *pinned* = بالای لیست) |
| کتاب (در حال خواندن / تمام‌شده / لیست) | **Books** |
| دوره + گواهی | **Courses** |
| سابقه کاری/تدریس، تحصیلات، مهارت‌ها، جوایز | **Experience / Education / Skill groups / Awards** |
| عکس، بیو، لینک‌ها، فایل CV | **Site profile** |

ترتیب نمایش با ستون `order` (عدد کمتر = بالاتر) قابل تغییر است و بیشتر لیست‌ها مستقیماً در خود جدول ویرایش می‌شوند.

## بهینه‌سازی و کش (چه چیزی خودکار انجام می‌شود)

- **عکس‌ها**: هر عکس آپلودشده خودکار به نسخه‌های WebP (480/960/1600px) تبدیل می‌شود و با `srcset` + `loading=lazy` نمایش داده می‌شود؛ هر بازدیدکننده کوچک‌ترین نسخه‌ی کافی را می‌گیرد.
- **ویدیو**: `preload="none"` — فایل ویدیو تا وقتی کسی Play نزند دانلود نمی‌شود. لینک یوتیوب هم تا کلیک نشود iframe لود نمی‌کند.
- **کش مرورگر**: فایل‌های `static` (در حالت production) با نام hash‌دار و کش یک‌ساله؛ فایل‌های `/media/` هم کش یک‌ساله و `immutable` (آپلود جدید همیشه اسم جدید می‌گیرد).
- **کش صفحات**: HTML هر صفحه یک روز سمت سرور کش می‌شود، مرورگرها هر ۵ دقیقه با ETag چک می‌کنند (پاسخ 304 بسیار سبک).
  با هر Save در ادمین، کش صفحات خودکار پاک می‌شود، پس تغییرات فوراً دیده می‌شوند. (وقتی در ادمین لاگین هستی همیشه نسخه‌ی تازه می‌بینی.)
- فشرده‌سازی gzip، sitemap.xml و robots.txt هم فعال است.

## Deploy (production)

```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY='<random-long-string>'
export DJANGO_ALLOWED_HOSTS='yourdomain.com'
export SITE_URL='https://yourdomain.com'
python manage.py collectstatic --noinput
gunicorn config.wsgi        # پشت nginx/Caddy با HTTPS
```

نکات:
- برای سرعت بهتر و **seek کردن ویدیو** (Range requests)، مسیر `/media/` را مستقیم از nginx/Caddy یا CDN سرو کن (`alias /path/to/media/;`).
- پوشه‌ی `media/` و فایل `db.sqlite3` را بکاپ بگیر؛ داده‌ی واقعی تو همین‌هاست.
- ویدیوهای سنگین را بهتر است در یوتیوب (unlisted) بگذاری و لینکش را در media item وارد کنی.
- اگر بعداً ترافیک زیاد شد، فقط `DATABASES` را به PostgreSQL عوض کن.

## ساختار

```
config/      تنظیمات و urls
core/        پروفایل، سابقه، تحصیلات، مهارت، جوایز، اخبار + کش/تصویر
portfolio/   پروژه‌ها + گالری (عکس/ویدیو/embed)
research/    مقالات (منتشرشده / در داوری / preprint / در حال نوشتن)
learning/    کتاب‌ها و دوره‌ها
templates/   static/   قالب‌ها و CSS/JS (بدون هیچ framework سنگین)
```

## نسخه‌ی استاتیک (هاست رایگان، بدون نیاز به Python روی سرور)

```powershell
build_static.bat          # یا: python manage.py build_static --site-url https://xxx.pages.dev
```
خروجی در پوشه‌ی `dist/` ساخته می‌شود (HTML + CSS/JS هش‌دار + media + sitemap + 404 + `_headers`).
هر بار در ادمین چیزی عوض کردی، دوباره build کن و `dist` را دوباره آپلود کن.

- **Cloudflare Pages:** Workers & Pages ← Create ← Pages ← *Upload assets* ← پوشه‌ی `dist` را بکش و رها کن.
- **GitHub Pages:** محتوای `dist` را در ریپوی `<username>.github.io` بگذار (برای ریپوی معمولی با زیرمسیر، لینک‌ها خراب می‌شوند).
- محدودیت Cloudflare Pages: هر فایل حداکثر ۲۵MB. ویدیوهای سنگین را در یوتیوب بگذار.
