# دفتر افکار — نسخه Qt برای Arch Linux

این نسخه، رابط HTML/JavaScript اصلی را داخل Qt 6 / PySide6 و QtWebEngine اجرا می‌کند؛ بنابراین منطق و ظاهر فرم اصلی حفظ می‌شود، ولی برنامه مانند یک اپ دسکتاپ از منوی برنامه‌ها اجرا می‌شود.

## اجرای محلی

```bash
sudo pacman -S python pyside6 qt6-webengine
python main.py
```

## ساخت بسته

```bash
makepkg -si
```

## AUR

این پروژه برای AUR به‌صورت `daftar-afkar-git` طراحی شده است. URL مخزن GitHub داخل `PKGBUILD` را با مخزن واقعی جایگزین کنید.

پس از انتشار در AUR:

```bash
yay -S daftar-afkar-git
```

برای دریافت تغییرات بعدی:

```bash
yay -Syu
```

در نسخه git، تغییرات جدید مخزن در نسخه تولیدشده توسط `pkgver()` منعکس می‌شوند و yay می‌تواند بسته را به‌روزرسانی کند.
