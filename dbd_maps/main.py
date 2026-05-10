import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Словарь с данными о картах
MAPS = {
    "Autohaven": {
        "release_date": "2016-06-14",
        "icon": "images/autohaven/autohaven_icon.jpg",
        "variants": {
            "Azarovs resting place": {"clock_image": "images/autohaven/azarovs_resting_place.jpg"},
            "Gas Heaven": {"clock_image": "images/autohaven/gas_heaven.jpg"},
            "Blood lodge": {"clock_image": "images/autohaven/blood_lodge.jpg"},
            "Wreckers yard": {"clock_image": "images/autohaven/wreckers_yard.jpg"},
        }
    },
    "Coldwind farm": {
        "release_date": "2016-06-14",
        "icon": "images/coldwind/coldwind_icon.jpg",
        "variants": {
            "Fractured cowshed": {"clock_image": "images/coldwind/fractured_cowshed.jpg"},
            "Rancid abbatoir": {"clock_image": "images/coldwind/rancid_abbatoir.jpg"},
            "Rotten fields": {"clock_image": "images/coldwind/rotten_fields.jpg"},
            "Thompson house": {"clock_image": "images/coldwind/thompson_house.jpg"},
            "Torment creek": {"clock_image": "images/coldwind/torment_creek.jpg"}
        }
    },
    "MacMillan": {
        "release_date": "2016-06-14",
        "icon": "images/macmillan/macmillan_icon.jpg",
        "variants": {
            "Suffocation pit": {"clock_image": "images/macmillan/suffocation_pit.jpg"},
            "Shelter woods": {"clock_image": "images/macmillan/shelter_woods.jpg"},
            "Coal tower": {"clock_image": "images/macmillan/coal_tower.jpg"},
            "Groaning storehouse": {"clock_image": "images/macmillan/groaning_storehouse.jpg"},
            "Ironworks": {"clock_image": "images/macmillan/ironworks.jpg"}
        }
    },
    "Grave of Glennvale": {
        "release_date": "2020-03-10",
        "icon": "images/grave_of_glennvale/grave_of_glennvale_icon.jpg",
        "variants": {
            "Dead Dawg Saloon": {"clock_image": "images/grave_of_glennvale/grave_of_glennvale.jpg"},
        }
    },
    "Badham preschool": {
        "release_date": "2017-10-31",
        "icon": "images/badham/badham_icon.jpg",
        "variants": {
            "Badham preschool": {"clock_image": "images/badham/badham.jpg"},
        }
    },
    "Crotus Prenn Asylum": {
        "release_date": "2016-08-18",
        "icon": "images/crotus/crotus_icon.jpg",
        "variants": {
            "Fath. Campbell's Chapel": {"clock_image": "images/crotus/fath.camp.jpg"},
            "Disturbed ward": {"clock_image": "images/crotus/disturbed_ward.jpg"}
        }
    },
    "Red Forest": {
        "release_date": "2017-07-27",
        "icon": "images/red_forest/red_forest_icon.jpg",
        "variants": {
            "Mothers dwelling": {"clock_image": "images/red_forest/mothers_dwelling.jpg"},
            "Temple of purgation": {"clock_image": "images/red_forest/temple_of_purgation.jpg"}
        }
    },
    "Backwater Swamp": {
        "release_date": "2016-12-08",
        "icon": "images/backwater_swamp/backwater_swamp_icon.jpg",
        "variants": {
            "Grim Pantry": {"clock_image": "images/backwater_swamp/grim_pantry.jpg"},
            "Pale Rose": {"clock_image": "images/backwater_swamp/pale_rose.jpg"}
        }
    },
    "Yamaoka Estate": {
        "release_date": "2018-09-18",
        "icon": "images/yamaoka_estate/yamaoka_estate_icon.jpg",
        "variants": {
            "Family residence": {"clock_image": "images/yamaoka_estate/family_residence.jpg"},
            "Sanctum of wrath": {"clock_image": "images/yamaoka_estate/sanctum_of_wrath.jpg"}
        }
    },
}


class ImageListButton(tk.Frame):
    def __init__(self, parent, image_path, text, command, width=380, height=45):
        super().__init__(parent, width=width, height=height, cursor="hand2")
        self.command = command
        self.pack_propagate(False)

        self.background_photo = None
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                self.background_photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Ошибка загрузки фона {image_path}: {e}")

        if self.background_photo:
            self.bg_label = tk.Label(self, image=self.background_photo)
        else:
            self.bg_label = tk.Label(self, bg="#3a3a3a")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.text_bg = tk.Frame(self, bg="#000000", bd=0)
        self.text_bg.place(x=10, y=height // 2 - 12, width=width - 50, height=24)

        self.text_label = tk.Label(self.text_bg, text=text, font=("Arial", 11, "bold"),
                                   fg="white", bg="#000000")
        self.text_label.pack(fill=tk.BOTH, expand=True, padx=5)

        self.arrow_bg = tk.Frame(self, bg="#000000", bd=0)
        self.arrow_bg.place(x=width - 35, y=height // 2 - 12, width=25, height=24)

        self.arrow_label = tk.Label(self.arrow_bg, text="▶", font=("Arial", 9),
                                    fg="white", bg="#000000")
        self.arrow_label.pack(fill=tk.BOTH, expand=True)

        self.bind("<Button-1>", self.on_click)
        self.bg_label.bind("<Button-1>", self.on_click)
        self.text_label.bind("<Button-1>", self.on_click)
        self.arrow_label.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.text_label.config(fg="yellow")
        self.arrow_label.config(fg="yellow")

    def on_leave(self, event):
        self.text_label.config(fg="white")
        self.arrow_label.config(fg="white")

    def on_click(self, event):
        if self.command:
            self.command()


class FloatingWindow:
    _open_windows = []

    def __init__(self, parent, image_path):
        for window in FloatingWindow._open_windows:
            try:
                if window.window.winfo_exists():
                    window.window.lift()
                    window.window.attributes('-topmost', True)
                    window.window.attributes('-topmost', False)
                    return
            except:
                FloatingWindow._open_windows.remove(window)

        self.window = tk.Toplevel(parent)
        self.window.title("Карта с часами")
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)

        FloatingWindow._open_windows.append(self)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.moving = False
        self.resizing = False
        self.start_x = 0
        self.start_y = 0
        self.start_width = 0
        self.start_height = 0
        self.start_win_x = 0
        self.start_win_y = 0
        self.resize_timer = None

        if os.path.exists(image_path):
            try:
                self.original_image = Image.open(image_path)
                self.img_width, self.img_height = self.original_image.size

                window_width = self.img_width
                window_height = self.img_height

                max_width = 1200
                max_height = 900

                if window_width > max_width or window_height > max_height:
                    ratio = min(max_width / window_width, max_height / window_height)
                    window_width = int(window_width * ratio)
                    window_height = int(window_height * ratio)

                self.window.geometry(f"{window_width}x{window_height}")
                self.window.minsize(200, 150)

                self.show_image(window_width, window_height)

                self.img_label.bind("<Button-1>", self.start_move)
                self.img_label.bind("<B1-Motion>", self.do_move)
                self.img_label.bind("<ButtonRelease-1>", self.stop_move)

                self.resize_handle = tk.Frame(self.window, cursor="size_nw_se", bg="gray", width=12, height=12)
                self.resize_handle.place(relx=1.0, rely=1.0, anchor="se")
                self.resize_handle.bind("<Button-1>", self.start_resize)
                self.resize_handle.bind("<B1-Motion>", self.do_resize)
                self.resize_handle.bind("<ButtonRelease-1>", self.stop_resize)

                self.setup_context_menu()

            except Exception as e:
                self.show_error(f"Ошибка: {e}")
        else:
            self.show_error(f"Файл не найден:\n{image_path}")

    def show_image(self, width, height):
        img_copy = self.original_image.copy()
        img_copy = img_copy.resize((width, height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img_copy)
        self.img_label = tk.Label(self.window, image=self.photo)
        self.img_label.pack(expand=True, fill=tk.BOTH)
        self.img_label.image = self.photo

    def on_close(self):
        if self in FloatingWindow._open_windows:
            FloatingWindow._open_windows.remove(self)
        self.window.destroy()

    def start_move(self, event):
        self.moving = True
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_win_x = self.window.winfo_x()
        self.start_win_y = self.window.winfo_y()
        return "break"

    def do_move(self, event):
        if self.moving:
            dx = event.x_root - self.start_x
            dy = event.y_root - self.start_y
            new_x = self.start_win_x + dx
            new_y = self.start_win_y + dy
            self.window.geometry(f"+{new_x}+{new_y}")
            return "break"

    def stop_move(self, event):
        self.moving = False

    def start_resize(self, event):
        self.resizing = True
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_width = self.window.winfo_width()
        self.start_height = self.window.winfo_height()
        return "break"

    def do_resize(self, event):
        if self.resizing:
            new_width = max(200, self.start_width + (event.x_root - self.start_x))
            new_height = max(150, self.start_height + (event.y_root - self.start_y))
            self.window.geometry(f"{new_width}x{new_height}")
            if self.resize_timer:
                self.window.after_cancel(self.resize_timer)
            self.resize_timer = self.window.after(50, lambda: self.update_image(new_width, new_height))
            return "break"

    def update_image(self, width, height):
        if width > 10 and height > 10:
            img_copy = self.original_image.copy()
            img_copy = img_copy.resize((width, height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img_copy)
            self.img_label.configure(image=self.photo)
            self.img_label.image = self.photo

    def stop_resize(self, event):
        self.resizing = False
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        self.update_image(width, height)

    def reset_size(self):
        new_width = self.img_width
        new_height = self.img_height
        max_width = 1200
        max_height = 900
        if new_width > max_width or new_height > max_height:
            ratio = min(max_width / new_width, max_height / new_height)
            new_width = int(new_width * ratio)
            new_height = int(new_height * ratio)
        self.window.geometry(f"{new_width}x{new_height}")
        self.update_image(new_width, new_height)

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Всегда поверх", command=self.toggle_topmost)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Сбросить размер", command=self.reset_size)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Закрыть", command=self.on_close)
        self.window.bind("<Button-3>", self.show_context_menu)
        if hasattr(self, 'img_label') and self.img_label:
            self.img_label.bind("<Button-3>", self.show_context_menu)
        if hasattr(self, 'resize_handle'):
            self.resize_handle.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def toggle_topmost(self):
        current = self.window.attributes('-topmost')
        self.window.attributes('-topmost', not current)

    def show_error(self, message):
        error_label = tk.Label(self.window, text=message, font=("Arial", 12), fg="red")
        error_label.pack(expand=True)


class DBDClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DBD Карты и часы")
        self.root.geometry("450x600")
        self.root.configure(bg="#2a2a2a")
        self.root.minsize(400, 500)

        self.main_frame = tk.Frame(self.root, bg="#2a2a2a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Dead by Daylight - Карты и часы",
                                    font=("Arial", 14, "bold"), bg="#2a2a2a", fg="white")
        self.title_label.pack(pady=15)

        self.canvas = tk.Canvas(self.main_frame, bg="#2a2a2a", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#2a2a2a")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Привязываем колесико мыши ко всему окну
        self.bind_mousewheel()

        self.current_sort = "date"
        self.create_buttons()

    def bind_mousewheel(self):
        """Привязывает колесико мыши ко всем виджетам"""

        def on_mousewheel(event):
            # Прокручиваем Canvas
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            return "break"

        # Для Windows
        self.root.bind_all("<MouseWheel>", on_mousewheel)

        # Также привязываем к самому Canvas на случай если фокус на нем
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas.bind("<Button-4>", on_mousewheel_linux)
        self.canvas.bind("<Button-5>", on_mousewheel_linux)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def sort_maps_by_name(self, maps_list):
        return sorted(maps_list, key=lambda x: x[0])

    def sort_maps_by_date(self, maps_list):
        return sorted(maps_list, key=lambda x: x[1].get("release_date", "0000-00-00"), reverse=True)

    def sort_variants_by_name(self, variants_list):
        return sorted(variants_list, key=lambda x: x[0])

    def create_buttons(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        sort_panel = tk.Frame(self.scrollable_frame, bg="#2a2a2a")
        sort_panel.pack(fill=tk.X, padx=10, pady=5)

        sort_label = tk.Label(sort_panel, text="📋 Сортировка:",
                              font=("Arial", 10), bg="#2a2a2a", fg="white")
        sort_label.pack(side=tk.LEFT, padx=5)

        def sort_by_name():
            self.current_sort = "name"
            self.create_buttons()

        def sort_by_date():
            self.current_sort = "date"
            self.create_buttons()

        btn_name_bg = "#4a6a4a" if self.current_sort == "name" else "#3a3a3a"
        btn_date_bg = "#4a6a4a" if self.current_sort == "date" else "#3a3a3a"

        btn_name = tk.Button(sort_panel, text="По названию (А-Я)", command=sort_by_name,
                             font=("Arial", 9), padx=8, pady=3, bg=btn_name_bg, fg="white",
                             activebackground="#555555", cursor="hand2")
        btn_name.pack(side=tk.LEFT, padx=5)

        btn_date = tk.Button(sort_panel, text="По дате (новые сначала)", command=sort_by_date,
                             font=("Arial", 9), padx=8, pady=3, bg=btn_date_bg, fg="white",
                             activebackground="#555555", cursor="hand2")
        btn_date.pack(side=tk.LEFT, padx=5)

        maps_list = list(MAPS.items())

        if self.current_sort == "name":
            maps_list = self.sort_maps_by_name(maps_list)
        else:
            maps_list = self.sort_maps_by_date(maps_list)

        for map_name, data in maps_list:
            def make_command(m=map_name):
                return lambda: self.show_variants(m)

            btn = ImageListButton(self.scrollable_frame, data["icon"], map_name, make_command(), width=380, height=75)
            btn.pack(pady=5, padx=10, anchor="center")

    def clear_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_variants(self, map_name):
        self.clear_frame()

        top_panel = tk.Frame(self.scrollable_frame, bg="#2a2a2a")
        top_panel.pack(fill=tk.X, padx=15, pady=10)

        back_btn = tk.Button(top_panel, text="← Назад", command=self.back_to_menu,
                             font=("Arial", 11), padx=15, pady=5, cursor="hand2", width=10,
                             bg="#3a3a3a", fg="white", activebackground="#4a4a4a")
        back_btn.pack(side=tk.LEFT)

        title = tk.Label(top_panel, text=f"{map_name}",
                         font=("Arial", 16, "bold"), bg="#2a2a2a", fg="white")
        title.pack(side=tk.LEFT, padx=15)

        buttons_container = tk.Frame(self.scrollable_frame, bg="#2a2a2a")
        buttons_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        variants_list = list(MAPS[map_name]["variants"].items())
        variants_list = self.sort_variants_by_name(variants_list)

        for var_name, var_data in variants_list:
            def make_command(m=map_name, v=var_name):
                return lambda: self.show_clock_image(m, v)

            btn = tk.Button(buttons_container, text=var_name,
                            command=make_command(),
                            font=("Arial", 11), padx=15, pady=8, bg="#3a3a3a",
                            activebackground="#4a4a4a", cursor="hand2", relief=tk.RAISED,
                            bd=1, fg="white")
            btn.pack(fill=tk.X, pady=5)

            def on_enter(e, b=btn):
                b.configure(bg="#4a6a4a")

            def on_leave(e, b=btn):
                b.configure(bg="#3a3a3a")

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def back_to_menu(self):
        self.clear_frame()
        self.create_buttons()

    def show_clock_image(self, map_name, variant_name):
        self.clear_frame()

        top_panel = tk.Frame(self.scrollable_frame, bg="#2a2a2a")
        top_panel.pack(fill=tk.X, padx=15, pady=10)

        back_btn = tk.Button(top_panel, text="← Назад",
                             command=lambda: self.show_variants(map_name),
                             font=("Arial", 11), padx=15, pady=5, cursor="hand2", width=10,
                             bg="#3a3a3a", fg="white", activebackground="#4a4a4a")
        back_btn.pack(side=tk.LEFT)

        display_name = variant_name[:35] + "..." if len(variant_name) > 35 else variant_name
        title = tk.Label(top_panel, text=f"🕐 {display_name}",
                         font=("Arial", 13, "bold"), bg="#2a2a2a", fg="white")
        title.pack(side=tk.LEFT, padx=15)

        clock_path = MAPS[map_name]["variants"][variant_name]["clock_image"]

        image_frame = tk.Frame(self.scrollable_frame, bg="#2a2a2a")
        image_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        if os.path.exists(clock_path):
            float_btn = tk.Button(self.scrollable_frame, text="🪟 Открыть в отдельном окне",
                                  command=lambda: FloatingWindow(self.root, clock_path),
                                  font=("Arial", 10), padx=12, pady=5, cursor="hand2",
                                  bg="#3a3a3a", fg="white", activebackground="#4a4a4a")
            float_btn.pack(pady=10)

        try:
            if os.path.exists(clock_path):
                img = Image.open(clock_path)
                preview_width = 380
                preview_height = 300
                img_copy = img.copy()
                img_copy.thumbnail((preview_width, preview_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_copy)
                img_label = tk.Label(image_frame, image=photo, bg="#2a2a2a")
                img_label.image = photo
                img_label.pack(expand=True)
            else:
                error_label = tk.Label(image_frame, text=f"Файл не найден:\n{clock_path}",
                                       font=("Arial", 11), bg="#2a2a2a", fg="#ff6666")
                error_label.pack(expand=True)
        except Exception as e:
            error_label = tk.Label(image_frame, text=f"Ошибка загрузки:\n{e}",
                                   font=("Arial", 11), bg="#2a2a2a", fg="#ff6666")
            error_label.pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DBDClockApp(root)
    root.mainloop()