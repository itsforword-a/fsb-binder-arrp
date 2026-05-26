import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import keyboard
import time
import threading
import pyperclip


class EditPhrasesDialog(simpledialog.Dialog):
    def __init__(self, parent, title, name, hotkey, phrases):
        self.p_name = name
        self.p_hotkey = hotkey
        self.p_phrases = list(phrases) + [""] * (4 - len(phrases))
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Название действия:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = ttk.Entry(master, width=40)
        self.name_entry.insert(0, self.p_name)
        self.name_entry.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(master, text="Горячая клавиша:").grid(row=1, column=0, sticky="w", pady=2)
        self.hk_entry = ttk.Entry(master, width=15)
        self.hk_entry.insert(0, self.p_hotkey)
        self.hk_entry.grid(row=1, column=1, pady=2, padx=5, sticky="w")

        ttk.Label(master, text="RP отыгровка (строки):", font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=2,
                                                                                         sticky="w", pady=(10, 2))

        self.phrase_entries = []
        for i in range(4):
            ttk.Label(master, text=f"Стр {i + 1}:").grid(row=3 + i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(master, width=40)
            entry.insert(0, self.p_phrases[i])
            entry.grid(row=3 + i, column=1, pady=2, padx=5)
            self.phrase_entries.append(entry)
        return self.name_entry

    def apply(self):
        self.result = {
            "name": self.name_entry.get().strip() or "Без названия",
            "hotkey": self.hk_entry.get().strip(),
            "phrases": [e.get().strip() for e in self.phrase_entries if e.get().strip()]
        }


class RPBinderPRO:
    def __init__(self, root):
        self.root = root
        self.root.title("ФСБ | beta v0.1")
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        self.is_running = False
        self.active_hotkeys = []

        self.cards = [
            {"name": "Задержание", "desc": "Наручники и залом рук", "hotkey": "F4",
             "phrases": ["Я достал наручники с пояса", "Я задержал человека напротив",
                         "Я заломал руки человеку напротив", "Я повел человека напротив за собой"]},
            {"name": "Посадка в авто", "desc": "Посадить в машину", "hotkey": "F5",
             "phrases": ["Я открыл дверь автомобиля", "Я посадил задержанного", "Я захлопнул дверь",
                         "Подозреваемый в машине"]},
            {"name": "Обыск", "desc": "Поиск предметов", "hotkey": "F6",
             "phrases": ["Я надел перчатки", "Я провел руками по карманам", "Я изъял запрещенные предметы",
                         "Обыск завершен"]},
            {"name": "Арест", "desc": "Передача в КПЗ", "hotkey": "F7",
             "phrases": ["Я открыл камеру", "Я завел задержанного", "Я закрыл дверь камеры", "Гражданин арестован"]}
        ]

        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=8)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Задержка чата:").pack(side="left")
        self.delay_entry = ttk.Entry(top_frame, width=5)
        self.delay_entry.insert(0, "0.3")
        self.delay_entry.pack(side="left", padx=3)

        ttk.Label(top_frame, text="Меж строк:").pack(side="left", padx=(8, 3))
        self.row_delay_entry = ttk.Entry(top_frame, width=5)
        self.row_delay_entry.insert(0, "1.2")
        self.row_delay_entry.pack(side="left")

        self.add_btn = ttk.Button(top_frame, text="+ Добавить бинд", command=self.add_new_card)
        self.add_btn.pack(side="right")

        self.canvas_frame = ttk.Frame(self.root, padding=5)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=440)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        bottom_frame = ttk.Frame(self.root, padding=10, relief="raised")
        bottom_frame.pack(fill="x", side="bottom")

        self.status_label = ttk.Label(bottom_frame, text="Статус: Выключен", font=("Arial", 10, "bold"),
                                      foreground="red")
        self.status_label.pack(side="left", pady=5)

        self.start_btn = ttk.Button(bottom_frame, text="ВКЛЮЧИТЬ БИНДЕР", command=self.toggle_binder, width=20)
        self.start_btn.pack(side="right")

        self.render_cards()

    def render_cards(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for idx, card in enumerate(self.cards):
            card_box = ttk.LabelFrame(self.scrollable_frame, text=f" [{card['hotkey'] or 'НЕТ'}] ", padding=8)
            card_box.pack(fill="x", padx=5, pady=5)

            text_frame = ttk.Frame(card_box)
            text_frame.pack(side="left", fill="both", expand=True)

            title_lbl = ttk.Label(text_frame, text=card["name"], font=("Arial", 10, "bold"))
            title_lbl.pack(anchor="w")

            desc_text = card["desc"] if card["desc"] else f"Строк: {len(card['phrases'])}"
            desc_lbl = ttk.Label(text_frame, text=desc_text, font=("Arial", 8), foreground="gray")
            desc_lbl.pack(anchor="w", pady=(2, 0))

            btn_frame = ttk.Frame(card_box)
            btn_frame.pack(side="right", fill="y")

            edit_btn = ttk.Button(btn_frame, text="⚙ Редактировать", width=16, command=lambda i=idx: self.edit_card(i))
            edit_btn.pack(side="top", pady=2)

            del_btn = ttk.Button(btn_frame, text="❌ Удалить", width=16, command=lambda i=idx: self.delete_card(i))
            del_btn.pack(side="bottom", pady=2)

    def add_new_card(self):
        dialog = EditPhrasesDialog(self.root, "Создание нового бинда", "Новое действие", "", ["", "", "", ""])
        if dialog.result:
            res = dialog.result
            new_card = {
                "name": res["name"],
                "desc": "Пользовательский бинд",
                "hotkey": res["hotkey"],
                "phrases": res["phrases"]
            }
            self.cards.append(new_card)
            self.render_cards()
            if self.is_running:
                self.restart_hotkeys()

    def edit_card(self, idx):
        card = self.cards[idx]
        dialog = EditPhrasesDialog(self.root, f"Настройка: {card['name']}", card["name"], card["hotkey"],
                                   card["phrases"])
        if dialog.result:
            res = dialog.result
            self.cards[idx]["name"] = res["name"]
            self.cards[idx]["hotkey"] = res["hotkey"]
            self.cards[idx]["phrases"] = res["phrases"]
            self.cards[idx]["desc"] = "Изменен пользователем"
            self.render_cards()
            if self.is_running:
                self.restart_hotkeys()

    def delete_card(self, idx):
        if messagebox.askyesno("Удаление", f"Вы уверены, что хотите удалить '{self.cards[idx]['name']}'?"):
            self.cards.pop(idx)
            self.render_cards()
            if self.is_running:
                self.restart_hotkeys()

    def toggle_binder(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Статус: АКТИВЕН", foreground="green")
            self.start_btn.config(text="ОСТАНОВИТЬ")
            self.restart_hotkeys()
        else:
            self.is_running = False
            self.status_label.config(text="Статус: Выключен", foreground="red")
            self.start_btn.config(text="ВКЛЮЧИТЬ БИНДЕР")
            self.clear_hotkeys()

    def clear_hotkeys(self):
        for hk in self.active_hotkeys:
            try:
                keyboard.remove_hotkey(hk)
            except:
                pass
        self.active_hotkeys.clear()

    def restart_hotkeys(self):
        self.clear_hotkeys()
        for card in self.cards:
            hk = card["hotkey"].strip()
            if hk:
                try:
                    hook = keyboard.add_hotkey(hk, lambda c=card: self.play_macro(c))
                    self.active_hotkeys.append(hook)
                except:
                    pass

    def play_macro(self, card):
        threading.Thread(target=self._execute_typing, args=(card,)).start()

    def _execute_typing(self, card):
        try:
            chat_delay = float(self.delay_entry.get())
            row_delay = float(self.row_delay_entry.get())
        except ValueError:
            chat_delay = 0.3
            row_delay = 1.2

        phrases = [p for p in card["phrases"] if p.strip()]
        old_clipboard = pyperclip.paste()

        for phrase in phrases:
            if not self.is_running:
                break

            pyperclip.copy(phrase)
            keyboard.send("/")
            time.sleep(chat_delay)

            keyboard.send("ctrl+v")
            time.sleep(0.1)
            keyboard.send("enter")

            time.sleep(row_delay)

        pyperclip.copy(old_clipboard)


if __name__ == "__main__":
    root = tk.Tk()
    app = RPBinderPRO(root)
    root.mainloop()
