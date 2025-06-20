import os
import re
import threading
import time
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from utils import (
    fetch_documents,
    download_and_open,
    list_local_files,
    delete_local_file,
    load_local_grand_prix,
    get_gp_dir
)
import requests
import mimetypes
import webbrowser

GRAND_PRIX_URLS = load_local_grand_prix()

def open_folder():
    gp = gp_var.get()
    folder = os.path.abspath(f"f1_documents/{gp.replace(' ', '_')}")
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.startfile(folder)

def search_files():
    for widget in result_inner.winfo_children():
        widget.destroy()
    gp = gp_var.get()
    keyword = kw_entry.get()
    url = GRAND_PRIX_URLS.get(gp)
    if not url:
        return
    docs = fetch_documents(url, keyword)
    if not docs:
        ttk.Label(result_inner, text="No matching files found.").pack()
        return
    for name, link in docs:
        match = re.search(r'Published on(\d{2}\.\d{2}\.\d{2} \d{2}:\d{2})CET', name)
        if match:
            cet_str = match.group(1)
            try:
                cet_dt = datetime.strptime(cet_str, '%y.%m.%d %H:%M')
                beijing_dt = cet_dt + timedelta(hours=7)
                time_str = beijing_dt.strftime('%Y-%m-%d %H:%M') + ' BJT'
            except:
                time_str = cet_str + ' CET'
            clean_name = name.split('Published on')[0].strip()
            display_name = f"{time_str} - {clean_name}"
        else:
            display_name = name.strip()

        btn = ttk.Button(result_inner, text=display_name,
                         command=lambda n=name, l=link, g=gp: threading.Thread(
                             target=download_with_progress, args=(n, l, g)).start())
        btn.pack(fill='x', padx=5, pady=2)

def show_local_files_window():
    gp = gp_var.get()
    files = list_local_files(gp)
    win = tk.Toplevel(root)
    win.title(f"{gp} 本地文件管理")
    win.geometry("500x400")
    listbox = tk.Listbox(win, width=70)
    listbox.pack(fill='both', expand=True)
    for f in files:
        listbox.insert(tk.END, f)

    def open_selected():
        selected = listbox.curselection()
        if selected:
            filename = listbox.get(selected[0])
            path = os.path.abspath(f"f1_documents/{gp.replace(' ', '_')}/{filename}")
            os.startfile(path)

    def delete_selected():
        selected = listbox.curselection()
        if selected:
            filename = listbox.get(selected[0])
            confirm = messagebox.askyesno("确认删除", f"确定要删除文件：{filename} 吗？")
            if confirm:
                success = delete_local_file(gp, filename)
                if success:
                    listbox.delete(selected[0])
                    messagebox.showinfo("删除成功", f"{filename} 已删除。")
                else:
                    messagebox.showerror("错误", "删除失败。")

    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=5)
    ttk.Button(btn_frame, text="打开文件", command=open_selected).pack(side='left', padx=10)
    ttk.Button(btn_frame, text="删除文件", command=delete_selected).pack(side='left', padx=10)

def download_with_progress(name, url, grand_prix):
    gp_dir = get_gp_dir(grand_prix)
    response = requests.get(url, stream=True)

    content_disp = response.headers.get("Content-Disposition", "")
    if "filename=" in content_disp:
        name = content_disp.split("filename=")[-1].strip("\"'")
    else:
        if not name.lower().endswith(('.pdf', '.doc', '.xls')):
            guessed_ext = mimetypes.guess_extension(response.headers.get("Content-Type", "").split(";")[0])
            name += guessed_ext if guessed_ext else ".pdf"

    local_path = os.path.join(gp_dir, name)

    if os.path.exists(local_path):
        progress["maximum"] = 1
        progress["value"] = 1
        progress.pack()
        progress_label_var.set(f"文件已存在：{name}")
        progress.update()
        time.sleep(0.8)
        progress.pack_forget()
        progress_label_var.set("")
        try:
            os.startfile(local_path)
        except:
            webbrowser.open(local_path)
        return

    total = int(response.headers.get("Content-Length", 0))
    progress["maximum"] = total
    progress["value"] = 0
    progress.pack()

    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            if chunk:
                f.write(chunk)
                progress["value"] += len(chunk)
                progress.update()

    progress.pack_forget()
    progress_label_var.set(f"已保存文件：{name}")
    progress.update()
    time.sleep(0.8)
    progress_label_var.set("")

    try:
        os.startfile(local_path)
    except:
        webbrowser.open(local_path)

# =================== GUI 主体 ===================
root = tk.Tk()
root.title("F1 文件查询器")
root.geometry("900x600")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10), background="#f0f2f5")
style.configure("TFrame", background="#f0f2f5")
style.configure("TEntry", padding=5)

main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=15, pady=15)

left_panel = ttk.Frame(main_frame, width=240)
left_panel.pack(side='left', fill='y', padx=(0, 20))

ttk.Label(left_panel, text="Grand Prix:").pack(anchor='w')
gp_var = tk.StringVar()
gp_menu = ttk.Combobox(left_panel, textvariable=gp_var, values=list(GRAND_PRIX_URLS.keys()), state="readonly")
gp_menu.pack(fill='x')
if GRAND_PRIX_URLS:
    gp_menu.current(0)

ttk.Label(left_panel, text="关键词:").pack(anchor='w', pady=(10, 0))
kw_entry = ttk.Entry(left_panel)
kw_entry.pack(fill='x')

def set_keyword_and_search(keyword):
    kw_entry.delete(0, tk.END)
    kw_entry.insert(0, keyword)
    search_files()

quick_keywords = [
    ("违规通知", "Infringement"),
    ("官方裁决", "Decision"),
    ("传唤通知", "Summons")
]

quick_frame = ttk.Frame(left_panel)
quick_frame.pack(pady=10)
for label, word in quick_keywords:
    ttk.Button(quick_frame, text=label, command=lambda w=word: set_keyword_and_search(w), width=20).pack(pady=2)

ttk.Button(left_panel, text="搜索", command=search_files).pack(pady=5)
ttk.Button(left_panel, text="打开下载文件夹", command=open_folder).pack(pady=5)
ttk.Button(left_panel, text="查看本地文件", command=show_local_files_window).pack(pady=5)

right_panel = ttk.Frame(main_frame)
right_panel.pack(side='left', fill='both', expand=True)

canvas = tk.Canvas(right_panel, bg="white")
scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

result_inner = ttk.Frame(canvas)
canvas.create_window((0, 0), window=result_inner, anchor='nw')

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

result_inner.bind("<Configure>", on_frame_configure)

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=5)
progress.pack_forget()
progress_label_var = tk.StringVar()
progress_label = ttk.Label(root, textvariable=progress_label_var)
progress_label.pack()
progress_label_var.set("")

root.mainloop()
