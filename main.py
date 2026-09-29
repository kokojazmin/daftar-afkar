#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView

APP_ID = "daftar-afkar"
APP_NAME = "دفتر افکار"


def app_data_dir() -> Path:
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    path = Path(base) / APP_ID
    path.mkdir(parents=True, exist_ok=True)
    return path


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(760, 900)
        self.setMinimumSize(520, 650)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        profile = QWebEngineProfile.defaultProfile()
        storage = app_data_dir() / "webengine"
        storage.mkdir(parents=True, exist_ok=True)
        profile.setPersistentStoragePath(str(storage))
        profile.setCachePath(str(storage / "cache"))
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        profile.downloadRequested.connect(self._download_requested)

        html = Path(__file__).with_name("index.html")
        self.view.load(QUrl.fromLocalFile(str(html.resolve())))

    def _download_requested(self, download):
        downloads = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        )
        downloads.mkdir(parents=True, exist_ok=True)
        name = download.downloadFileName() or "thought-records.txt"
        download.setDownloadDirectory(str(downloads))
        download.setDownloadFileName(name)
        download.accept()


def main():
    # Prevent Qt/Chromium from trying to use an application-wide shared cache.
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-background-networking")
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName("DaftarAfkar")
    app.setDesktopFileName(APP_ID)

    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
