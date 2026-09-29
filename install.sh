```bash
#!/bin/bash

set -euo pipefail

REPO_URL="https://github.com/kokojazmin/daftar-afkar.git"
APP_NAME="daftar-afkar"
BUILD_DIR="${TMPDIR:-/tmp}/daftar-afkar-build"

cleanup() {
    rm -rf "$BUILD_DIR"
}

trap cleanup EXIT

printf '\n'
printf '  دفتر افکار - نصب کننده\n'
printf '  =====================\n\n'

# Check operating system
if [[ ! -f /etc/arch-release ]]; then
    echo "خطا: این نصب‌کننده فقط برای Arch Linux و توزیع‌های مبتنی بر آن طراحی شده است."
    exit 1
fi

# Check required commands
for command in git makepkg sudo; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "خطا: دستور موردنیاز پیدا نشد: $command"
        exit 1
    fi
done

# Check that makepkg is not being run as root
if [[ "$EUID" -eq 0 ]]; then
    echo "خطا: این اسکریپت را با root اجرا نکنید."
    echo "مثال:"
    echo "  bash install.sh"
    exit 1
fi

# Remove previous temporary build
rm -rf "$BUILD_DIR"

echo "→ دریافت آخرین نسخه از GitHub..."
git clone --depth=1 "$REPO_URL" "$BUILD_DIR"

cd "$BUILD_DIR"

echo "→ بررسی وابستگی‌های ساخت..."
makepkg --syncdeps --needed --noconfirm

echo "→ ساخت و نصب پکیج..."
makepkg --install --noconfirm

printf '\n'
printf '✓ دفتر افکار با موفقیت نصب شد.\n\n'
printf 'برای اجرای برنامه:\n'
printf '  %s\n\n' "$APP_NAME"
printf 'همچنین می‌توانید آن را از منوی برنامه‌های دسکتاپ اجرا کنید.\n'
```
