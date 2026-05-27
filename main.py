import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import keyboard
import time
import threading
import pyperclip
import json
import os


class h1(simpledialog.Dialog):
    def __init__(self, p, t, n, h, ph):
        self.n1 = n
        self.h1 = h
        self.p1 = list(ph) + [""] * (4 - len(ph))
        super().__init__(p, t)

    def body(self, m):
        ttk.Label(m, text="Название:").grid(row=0, column=0, sticky="w", pady=2)
        self.e1 = ttk.Entry(m, width=40)
        self.e1.insert(0, self.n1)
        self.e1.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(m, text="Горячая клавиша:").grid(row=1, column=0, sticky="w", pady=2)
        self.e2 = ttk.Entry(m, width=20)
        self.e2.insert(0, self.h1)
        self.e2.grid(row=1, column=1, pady=2, padx=5, sticky="w")
        ttk.Label(m, text="(кликни и нажми клавишу)", font=("Arial", 8)).grid(row=2, column=1, sticky="w", padx=5)

        self.e2.bind("<Button-1>", self.r1)

        ttk.Label(m, text="Фразы:", font=("Arial", 9, "bold")).grid(row=3, column=0, columnspan=2, sticky="w",
                                                                    pady=(10, 2))

        self.f1 = []
        for i in range(4):
            ttk.Label(m, text=f"{i + 1}:").grid(row=4 + i, column=0, sticky="w", pady=2)
            e = ttk.Entry(m, width=40)
            e.insert(0, self.p1[i])
            e.grid(row=4 + i, column=1, pady=2, padx=5)
            self.f1.append(e)
        return self.e1

    def r1(self, e):
        def w1():
            ev = keyboard.read_event(suppress=False)
            if ev.event_type == keyboard.KEY_DOWN:
                self.e2.delete(0, tk.END)
                self.e2.insert(0, ev.name)

        threading.Thread(target=w1, daemon=True).start()
        return "break"

    def apply(self):
        self.result = {
            "name": self.e1.get().strip() or "Без названия",
            "hotkey": self.e2.get().strip(),
            "phrases": [e.get().strip() for e in self.f1 if e.get().strip()]
        }


class app:
    def __init__(self, r):
        self.r = r
        self.r.title("ФСБ | v2.0")
        self.r.geometry("500x600")
        self.r.resizable(False, False)

        self.f1 = "binds.json"
        self.i1 = False
        self.h2 = []

        self.c1 = self.l1()
        self.c2()

        self.r.protocol("WM_DELETE_WINDOW", self.s1)

    def l1(self):
        if os.path.exists(self.f1):
            try:
                with open(self.f1, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    self.d1 = d.get('cd', "0.3")
                    self.d2 = d.get('rd', "1.2")
                    return d.get('cards', self.d3())
            except:
                return self.d3()
        return self.d3()

    def d3(self):
        self.d1 = "0.3"
        self.d2 = "1.2"
        return [
            {"name": "Задержание", "desc": "Наручники", "hotkey": "f4",
             "phrases": ["Я достал наручники с пояса", "Я задержал человека напротив",
                         "Я заломал руки человеку напротив", "Я повел человека напротив за собой"]},
            {"name": "Посадка", "desc": "В машину", "hotkey": "f5",
             "phrases": ["Я открыл дверь автомобиля", "Я посадил задержанного", "Я захлопнул дверь",
                         "!do Подозреваемый в машине"]},
            {"name": "Обыск", "desc": "Поиск", "hotkey": "f6",
             "phrases": ["Я надел перчатки", "Я провел руками по карманам", "Я изъял запрещенные предметы",
                         "!do Обыск завершен"]},
            {"name": "Арест", "desc": "КПЗ", "hotkey": "f7",
             "phrases": ["Я открыл камеру", "Я завел задержанного", "Я закрыл дверь камеры", "!do Гражданин арестован"]}
        ]

    def s1(self):
        try:
            d = {
                'cards': self.c1,
                'cd': self.e3.get() if hasattr(self, 'e3') else "0.3",
                'rd': self.e4.get() if hasattr(self, 'e4') else "1.2"
            }
            with open(self.f1, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
        except:
            pass
        self.r.destroy()

    def c2(self):
        t1 = ttk.Frame(self.r, padding=8)
        t1.pack(fill="x")

        ttk.Label(t1, text="Задержка:").pack(side="left")
        self.e3 = ttk.Entry(t1, width=6)
        self.e3.insert(0, self.d1)
        self.e3.pack(side="left", padx=3)

        ttk.Label(t1, text="Меж строк:").pack(side="left", padx=(8, 3))
        self.e4 = ttk.Entry(t1, width=6)
        self.e4.insert(0, self.d2)
        self.e4.pack(side="left")

        b1 = ttk.Frame(t1)
        b1.pack(side="right")

        self.b2 = ttk.Button(b1, text="+ Бинд", command=self.a1, width=8)
        self.b2.pack(side="left", padx=2)

        self.b3 = ttk.Button(b1, text="💾", command=self.s1, width=3)
        self.b3.pack(side="left", padx=2)

        cf = ttk.Frame(self.r, padding=5)
        cf.pack(fill="both", expand=True)

        self.cv = tk.Canvas(cf, highlightthickness=0)
        self.sf = ttk.Frame(self.cv)
        self.sf.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))

        self.cv.create_window((0, 0), window=self.sf, anchor="nw", width=480)
        self.cv.pack(side="left", fill="both", expand=True)

        def on_mw(e):
            if self.sf.winfo_reqheight() > self.cv.winfo_height():
                self.cv.yview_scroll(int(-1 * (e.delta / 120)), "units")

        self.cv.bind_all("<MouseWheel>", on_mw)

        bf = ttk.Frame(self.r, padding=10, relief="raised")
        bf.pack(fill="x", side="bottom")

        self.l1 = ttk.Label(bf, text="Статус: Выкл", font=("Arial", 10, "bold"), foreground="red")
        self.l1.pack(side="left", pady=5)

        bb = ttk.Frame(bf)
        bb.pack(side="right")

        self.b4 = ttk.Button(bb, text="Экспорт", command=self.e5, width=8)
        self.b4.pack(side="left", padx=2)

        self.b5 = ttk.Button(bb, text="Импорт", command=self.i2, width=8)
        self.b5.pack(side="left", padx=2)

        self.b6 = ttk.Button(bb, text="ВКЛ", command=self.t1, width=10)
        self.b6.pack(side="left", padx=2)

        self.r1()

    def e5(self):
        from tkinter import filedialog
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f:
            try:
                d = {'cards': self.c1, 'cd': self.e3.get(), 'rd': self.e4.get()}
                with open(f, 'w', encoding='utf-8') as fp:
                    json.dump(d, fp, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", f"Сохранено")
            except Exception as er:
                messagebox.showerror("Ошибка", str(er))

    def i2(self):
        from tkinter import filedialog
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    d = json.load(fp)
                self.c1 = d.get('cards', self.c1)
                self.e3.delete(0, tk.END)
                self.e3.insert(0, d.get('cd', "0.3"))
                self.e4.delete(0, tk.END)
                self.e4.insert(0, d.get('rd', "1.2"))
                self.r1()
                if self.i1:
                    self.r2()
                messagebox.showinfo("Успех", "Импорт выполнен")
            except Exception as er:
                messagebox.showerror("Ошибка", str(er))

    def r1(self):
        for w in self.sf.winfo_children():
            w.destroy()

        if not self.c1:
            l = ttk.Label(self.sf, text="Нет биндов", font=("Arial", 12))
            l.pack(pady=50)
            return

        for i, c in enumerate(self.c1):
            b = ttk.LabelFrame(self.sf, text=f" [{c['hotkey'] or 'НЕТ'}] ", padding=8)
            b.pack(fill="x", padx=5, pady=5)

            tf = ttk.Frame(b)
            tf.pack(side="left", fill="both", expand=True)

            tl = ttk.Label(tf, text=c["name"], font=("Arial", 10, "bold"))
            tl.pack(anchor="w")

            dl = ttk.Label(tf, text=c["desc"] if c["desc"] else f"{len(c['phrases'])} фраз",
                           font=("Arial", 8), foreground="gray")
            dl.pack(anchor="w", pady=(2, 0))

            bf = ttk.Frame(b)
            bf.pack(side="right", fill="y")

            eb = ttk.Button(bf, text="Ред", width=8, command=lambda x=i: self.e6(x))
            eb.pack(side="top", pady=2)

            db = ttk.Button(bf, text="Удал", width=8, command=lambda x=i: self.d4(x))
            db.pack(side="bottom", pady=2)

    def a1(self):
        d = h1(self.r, "Новый бинд", "Новое действие", "", ["", "", "", ""])
        if d.result:
            r = d.result
            n = {"name": r["name"], "desc": "Новый", "hotkey": r["hotkey"], "phrases": r["phrases"]}
            self.c1.append(n)
            self.r1()
            if self.i1:
                self.r2()

    def e6(self, i):
        c = self.c1[i]
        d = h1(self.r, f"Правка", c["name"], c["hotkey"], c["phrases"])
        if d.result:
            r = d.result
            self.c1[i]["name"] = r["name"]
            self.c1[i]["hotkey"] = r["hotkey"]
            self.c1[i]["phrases"] = r["phrases"]
            self.c1[i]["desc"] = "Изменен"
            self.r1()
            if self.i1:
                self.r2()

    def d4(self, i):
        if messagebox.askyesno("Удаление", f"Удалить '{self.c1[i]['name']}'?"):
            self.c1.pop(i)
            self.r1()
            if self.i1:
                self.r2()

    def t1(self):
        if not self.i1:
            self.i1 = True
            self.l1.config(text="Статус: АКТИВЕН", foreground="green")
            self.b6.config(text="СТОП")
            self.r2()
        else:
            self.i1 = False
            self.l1.config(text="Статус: Выкл", foreground="red")
            self.b6.config(text="ВКЛ")
            self.c3()

    def c3(self):
        for h in self.h2:
            try:
                keyboard.remove_hotkey(h)
            except:
                pass
        self.h2.clear()

    def r2(self):
        self.c3()
        for c in self.c1:
            hk = c["hotkey"].strip()
            if hk:
                try:
                    hook = keyboard.add_hotkey(hk, lambda x=c: self.p1(x))
                    self.h2.append(hook)
                except:
                    pass

    def p1(self, c):
        threading.Thread(target=self.e7, args=(c,)).start()

    def e7(self, c):
        try:
            cd = float(self.e3.get())
            rd = float(self.e4.get())
        except:
            cd = 0.3
            rd = 1.2

        ph = [p for p in c["phrases"] if p.strip()]
        oc = pyperclip.paste()

        for p in ph:
            if not self.i1:
                break
            pyperclip.copy(p)
            keyboard.send("/")
            time.sleep(cd)
            keyboard.send("ctrl+v")
            time.sleep(0.1)
            keyboard.send("enter")
            time.sleep(rd)

        pyperclip.copy(oc)


if __name__ == "__main__":
    r = tk.Tk()
    a = app(r)
    r.mainloop()
