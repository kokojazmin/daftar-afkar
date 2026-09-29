#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QTimer, QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineScript, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow

APP_ID = "daftar-afkar"
APP_NAME = "دفتر افکار"

# The page keeps its data in window.__DA (injected below). It is written to a
# plain JSON file, so records survive closing the app regardless of how
# Chromium flushes its own storage.
POLL_JS = (
    "(function(){if(!window.__DA_DIRTY)return null;"
    "window.__DA_DIRTY=0;return JSON.stringify(window.__DA||{});})()"
)
FLUSH_JS = "JSON.stringify(window.__DA||null)"


def app_data_dir() -> Path:
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    path = Path(base) / APP_ID
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_file() -> Path:
    return app_data_dir() / "data.json"


def load_data() -> dict:
    try:
        data = json.loads(data_file().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_data(raw) -> None:
    if not raw:
        return
    try:
        data = json.loads(raw)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    path = data_file()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(760, 900)
        self.setMinimumSize(520, 650)
        self._closing = False
        self._done = False

        profile = QWebEngineProfile.defaultProfile()
        storage = app_data_dir() / "webengine"
        storage.mkdir(parents=True, exist_ok=True)
        profile.setPersistentStoragePath(str(storage))
        profile.setCachePath(str(storage / "cache"))
        profile.downloadRequested.connect(self._download_requested)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)

        script = QWebEngineScript()
        script.setName("daftar-store")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(False)
        script.setSourceCode("window.__DA=" + json.dumps(load_data()) + ";")
        self.view.page().scripts().insert(script)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._poll)
        self.timer.start()

        html = Path(__file__).with_name("index.html")
        self.view.load(QUrl.fromLocalFile(str(html.resolve())))

    def _poll(self):
        self.view.page().runJavaScript(POLL_JS, save_data)

    def closeEvent(self, event: QCloseEvent):
        if self._done:
            event.accept()
            return
        event.ignore()
        if self._closing:
            return
        self._closing = True
        self.timer.stop()
        self.view.page().runJavaScript(FLUSH_JS, self._on_flush)
        QTimer.singleShot(2000, self._finish)  # safety net

    def _on_flush(self, raw):
        save_data(raw)
        self._finish()

    def _finish(self):
        if self._done:
            return
        self._done = True
        self.close()

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
