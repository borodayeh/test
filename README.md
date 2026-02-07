# Ergo Health Reminder (Windows Desktop)

اپلیکیشن ساده‌ی ارگونومی با Python/Tkinter برای یادآوری استراحت و تحرک.

## اجرا

```bash
python main.py
```

## ساخت فایل EXE با PyInstaller

- تک‌فایل و بدون کنسول:

```bash
pyinstaller --onefile --noconsole main.py
```

- تک‌فایل، بدون کنسول، با آیکون اختیاری:

```bash
pyinstaller --onefile --noconsole --icon app.ico main.py
```

خروجی در پوشه `dist/` ساخته می‌شود.
