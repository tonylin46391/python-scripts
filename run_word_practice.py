import os
import sys
import subprocess
import webbrowser


def candidate_app_paths() -> list[str]:
    paths = []
    # 1) PyInstaller onefile 暫存資料夾 (_MEIPASS)
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS  # type: ignore[attr-defined]
        paths.append(os.path.join(base, "word_practice_app.py"))
    # 2) 同目錄
    here = os.path.dirname(os.path.abspath(__file__))
    paths.append(os.path.join(here, "word_practice_app.py"))
    # 3) 上層與常見放置位置
    parent = os.path.dirname(here)
    paths.append(os.path.join(parent, "word_practice_app.py"))
    return paths


def main() -> None:
    # 嘗試多個候選路徑
    app_path = None
    for p in candidate_app_paths():
        if os.path.exists(p):
            app_path = p
            break
    if app_path is None:
        raise FileNotFoundError("找不到應用程式檔案: word_practice_app.py")

    # 先嘗試開啟預設瀏覽器（Streamlit 會自動開，但部分情境可能被防火牆阻擋）
    try:
        webbrowser.open_new_tab("http://localhost:8501")
    except Exception:
        pass

    # 以目前 Python 啟動 streamlit 模組執行 App
    cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.headless=false"]
    # 使用非封鎖方式啟動，讓視窗保持
    subprocess.Popen(cmd, cwd=os.path.dirname(app_path))


if __name__ == "__main__":
    main()


