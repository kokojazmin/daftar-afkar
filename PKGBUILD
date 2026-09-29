# Maintainer: kokojazmin <mobinboloke33@gmail.com>
pkgname=daftar-afkar-git
pkgver=0.1.0.r2.g89b8b36
pkgrel=1
pkgdesc='دفتر افکار CBT - Persian thought record journal'
arch=('any')
url='https://github.com/kokojazmin/daftar-afkar'
license=('MIT')
depends=('python' 'pyside6' 'qt6-webengine')
makedepends=('git')
provides=('daftar-afkar')
conflicts=('daftar-afkar')
source=('git+https://github.com/kokojazmin/daftar-afkar.git')
sha256sums=('SKIP')

pkgver() {
  cd "$srcdir/daftar-afkar"
  printf '0.1.0.r%s.g%s\n' \
    "$(git rev-list --count HEAD)" \
    "$(git rev-parse --short HEAD)"
}

package() {
  cd "$srcdir/daftar-afkar"

  install -Dm755 main.py "$pkgdir/usr/share/daftar-afkar/main.py"
  install -Dm644 index.html "$pkgdir/usr/share/daftar-afkar/index.html"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/daftar-afkar/LICENSE"
  install -Dm644 daftar-afkar.desktop "$pkgdir/usr/share/applications/daftar-afkar.desktop"
  install -Dm644 daftar-afkar.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/daftar-afkar.svg"

  install -Dm755 /dev/stdin "$pkgdir/usr/bin/daftar-afkar" <<'EOF_SCRIPT'
#!/bin/sh
exec /usr/bin/python /usr/share/daftar-afkar/main.py "$@"
EOF_SCRIPT
}
