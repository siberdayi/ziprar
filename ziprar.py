import tkinter as tk
from tkinter import filedialog, messagebox
import pyzipper
import rarfile
import threading
import webbrowser

archive_path = ""
wordlist_path = ""

def select_archive():
    global archive_path
    file_path = filedialog.askopenfilename(title="Şifreli ZIP/RAR dosyasını seç", filetypes=[("Arşiv Dosyaları", "*.zip *.rar"), ("Tüm Dosyalar", "*.*")])
    if file_path:
        archive_path = file_path
        archive_label.config(text=f"Seçilen: {file_path}")

def select_wordlist():
    global wordlist_path
    file_path = filedialog.askopenfilename(title="Wordlist (TXT) dosyasını seç", filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")])
    if file_path:
        wordlist_path = file_path
        wordlist_label.config(text=f"Seçilen: {file_path}")

def crack_password():
    if not archive_path or not wordlist_path:
        messagebox.showerror("Hata", "Lütfen bir arşiv ve wordlist seçin!")
        return
    
    thread = threading.Thread(target=bruteforce_attack)
    thread.start()

def bruteforce_attack():
    try:
        archive = None
        if archive_path.endswith(".zip"):
            archive = pyzipper.AESZipFile(archive_path)
        elif archive_path.endswith(".rar"):
            archive = rarfile.RarFile(archive_path)
        else:
            messagebox.showerror("Hata", "Geçersiz dosya türü!")
            return

        with open(wordlist_path, "r", encoding="latin-1") as f:
            passwords = f.readlines()
        
        total = len(passwords)
        for i, password in enumerate(passwords):
            password = password.strip()
            try:
                if archive_path.endswith(".zip"):
                    archive.extractall(pwd=password.encode("utf-8"))
                elif archive_path.endswith(".rar"):
                    archive.extractall(pwd=password)
                messagebox.showinfo("Başarılı!", f"Şifre bulundu: {password}")
                return
            except:
                pass
            
            progress_label.config(text=f"Denendi: {i+1}/{total} (%{int((i+1)/total*100)})")
            root.update()
        
        messagebox.showwarning("Başarısız", "Şifre bulunamadı! Farklı bir wordlist deneyin.")
    except Exception as e:
        messagebox.showerror("Hata", str(e))

def open_telegram():
    webbrowser.open("https://t.me/sistemci")

root = tk.Tk()
root.title("ZipRar Dayı")
root.geometry("500x350")
root.configure(bg="black")

archive_label = tk.Label(root, text="ZIP/RAR Dosyası Seçin", fg="white", bg="black")
archive_label.pack()
archive_button = tk.Button(root, text="Dosya Seç ZIP/RAR", command=select_archive)
archive_button.pack()

wordlist_label = tk.Label(root, text="Wordlist Seçin", fg="white", bg="black")
wordlist_label.pack()
wordlist_button = tk.Button(root, text="Dosya Seç Wordlist", command=select_wordlist)
wordlist_button.pack()

start_button = tk.Button(root, text="Start", command=crack_password)
start_button.pack()

progress_label = tk.Label(root, text="Durum: Bekleniyor", fg="white", bg="black")
progress_label.pack()

telegram_button = tk.Button(root, text="telegram kanalımıza abone oldun mu? hadi ozaman", command=open_telegram)
telegram_button.pack()

credit_label = tk.Label(root, text="Sıber Dayı tarafından kodlandı,youtube:siberdayı", fg="white", bg="black")
credit_label.pack()

root.mainloop()
