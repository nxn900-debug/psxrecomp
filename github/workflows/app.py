import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("PS1 Cue Files", "*.cue")])
    if filepath:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filepath)

def convert_to_exe():
    cue_file = entry_path.get()
    if not cue_file:
        messagebox.showerror("خطأ", "الرجاء اختيار ملف اللعبة أولاً")
        return
    
    label_status.config(text="جاري التفكيك والتحويل... الرجاء الانتظار")
    root.update()

    try:
        # 1. تشغيل أداة psxrecomp في الخلفية لتوليد الكود
        subprocess.run(["psxrecomp.exe", "generate", cue_file], check=True)
        
        # 2. تشغيل المترجم (مثال GCC) في الخلفية لتحويل الكود إلى لعبة exe
        subprocess.run(["gcc", "output_code.c", "-o", "MyGame.exe"], check=True)
        
        label_status.config(text="تم التحويل بنجاح! اللعبة جاهزة.")
        messagebox.showinfo("نجاح", "تم إنشاء ملف exe للعبتك!")
    except Exception as e:
        label_status.config(text="حدث خطأ أثناء التحويل.")
        messagebox.showerror("خطأ", str(e))

# --- تصميم الواجهة الرسومية ---
root = tk.Tk()
root.title("PS1 to EXE Converter")
root.geometry("400x200")

tk.Label(root, text="اختر ملف اللعبة (.cue):").pack(pady=10)

entry_path = tk.Entry(root, width=40)
entry_path.pack(pady=5)

tk.Button(root, text="تصفح", command=select_file).pack(pady=5)
tk.Button(root, text="تحويل إلى EXE", command=convert_to_exe, bg="green", fg="white").pack(pady=15)

label_status = tk.Label(root, text="")
label_status.pack()

root.mainloop()
