import customtkinter as ctk
import time
from config import COLORS, SUBJECTS, COINS_PER_FOCUS, MAX_PAUSE_BEFORE_WARNING

class RightPanel(ctk.CTkFrame):
    def __init__(self, master, data, save_func, mood_func, coin_callback):
        super().__init__(master, fg_color=COLORS['card_bg'], corner_radius=25, 
                         border_width=1, border_color=COLORS['card_border'])
        self.data = data
        self.tasks = data['tasks']
        self.save_func = save_func
        self.mood_func = mood_func
        self.coin_callback = coin_callback
        
        # Khởi tạo các biến trạng thái timer
        self.timer_seconds = 25 * 60
        self.total_seconds = 25 * 60
        self.timer_running = False
        self.timer_mode = 'WORK'
        
        # Streak tracking
        if 'streak' not in self.data:
            self.data['streak'] = {
                'current_streak': 0,
                'total_days': 0,
                'last_login_date': None,
                'milestones_reached': [],
                'pause_count': 0
            }
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ========== Timer Section ==========
        timer_card = ctk.CTkFrame(self, fg_color=COLORS['input_bg'], corner_radius=20)
        timer_card.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))

        # Mode buttons
        self.mode_frame = ctk.CTkFrame(timer_card, fg_color="transparent")
        self.mode_frame.pack(pady=(15, 10), padx=20)
        
        modes = [('Học bài', 'WORK'), ('Nghỉ ngắn', 'SHORT_BREAK'), ('Nghỉ dài', 'LONG_BREAK')]
        for txt, m in modes:
            btn = ctk.CTkButton(self.mode_frame, text=txt, width=80, height=28, corner_radius=14, 
                          fg_color=COLORS['card_bg'], text_color=COLORS['text'],
                          hover_color=COLORS['card_border'],
                          command=lambda mode=m: self.set_timer_mode(mode))
            btn.pack(side="left", padx=4)

        # Timer display
        self.timer_display = ctk.CTkLabel(timer_card, text="25:00", 
                                          font=("Inter", 60, "bold"), text_color=COLORS['primary'])
        self.timer_display.pack(pady=(5, 10))
        
        # Time slider
        self.time_slider = ctk.CTkSlider(timer_card, from_=1, to=120, 
                                         button_color=COLORS['primary'],
                                         progress_color=COLORS['primary'],
                                         command=self.on_slider_move)
        self.time_slider.pack(fill="x", padx=20, pady=(8, 5))
        self.time_slider.set(25)

        # Progress bar
        self.progress = ctk.CTkProgressBar(timer_card, height=6, corner_radius=3,
                                           progress_color=COLORS['primary'], fg_color=COLORS['card_bg'])
        self.progress.pack(fill="x", padx=20, pady=(8, 12))
        self.progress.set(1.0)

        # Start button
        self.start_btn = ctk.CTkButton(timer_card, text="BẮT ĐẦU", font=("Segoe UI", 14, "bold"), 
                                      fg_color=COLORS['primary'], width=200, height=42, corner_radius=21, 
                                      command=self.toggle_timer)
        self.start_btn.pack(pady=(0, 15))

        # ========== Task List Section ==========
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=1, column=0, sticky="ew", padx=20, pady=(15, 12))
        ctk.CTkLabel(header, text="Nhiệm Vụ Hôm Nay", 
                     font=("Segoe UI", 18, "bold"), text_color=COLORS['text']).pack(side="left")

        # Input Area
        input_container = ctk.CTkFrame(self, fg_color=COLORS['input_bg'], corner_radius=16)
        input_container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))
        
        self.sub_menu = ctk.CTkOptionMenu(input_container, values=SUBJECTS, width=90, 
                                          fg_color=COLORS['card_bg'], 
                                          button_color=COLORS['card_bg'],
                                          button_hover_color=COLORS['card_border'],
                                          text_color=COLORS['text'], corner_radius=10)
        self.sub_menu.pack(side="left", padx=8, pady=8)

        self.entry = ctk.CTkEntry(input_container, placeholder_text="Bạn định học gì tiếp theo?", 
                                  border_width=0, fg_color="transparent", 
                                  font=("Segoe UI", 13), text_color=COLORS['text'])
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        self.entry.bind("<Return>", lambda e: self.add_task())

        self.add_btn = ctk.CTkButton(input_container, text="+", width=40, height=40, 
                                     corner_radius=12, fg_color=COLORS['primary'],
                                     hover_color=COLORS['primary_hover'],
                                     command=self.add_task)
        self.add_btn.pack(side="right", padx=8, pady=8)

        # Task List
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)
        self.render_tasks()

    def render_tasks(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for t in self.tasks:
            # Task Card
            is_done = t['completed']
            row = ctk.CTkFrame(self.scroll, 
                               fg_color=COLORS['bg'] if not is_done else "#F8FAFC", 
                               corner_radius=12, border_width=1, 
                               border_color=COLORS['card_border'] if not is_done else COLORS['success'])
            row.pack(fill="x", pady=5, padx=5)
            
            check = ctk.CTkCheckBox(row, text="", width=20, 
                                    checkbox_height=18, checkbox_width=18,
                                    border_color=COLORS['primary'],
                                    hover_color=COLORS['primary_hover'],
                                    command=lambda task=t: self.toggle_task(task))
            check.pack(side="left", padx=(12, 8), pady=10)
            if is_done: check.select()

            # Subject Label
            sub_lbl = ctk.CTkLabel(row, text=t['subject'], 
                                   fg_color=COLORS['primary'] if not is_done else COLORS['text_sub'], 
                                   text_color="white", corner_radius=6, 
                                   font=("Segoe UI", 9, "bold"), width=55)
            sub_lbl.pack(side="left", padx=5, pady=10)

            # Task Title
            task_font = ("Segoe UI", 13, "overstrike" if is_done else "normal")
            task_color = COLORS['text'] if not is_done else COLORS['text_sub']
            ctk.CTkLabel(row, text=t['title'], font=task_font, text_color=task_color).pack(side="left", padx=3)

            # Delete Button
            ctk.CTkButton(row, text="✕", width=28, height=28, fg_color="transparent", 
                          text_color=COLORS['danger'], hover_color="#FEE2E2", corner_radius=6,
                          command=lambda task=t: self.delete_task(task)).pack(side="right", padx=10, pady=10)

    def add_task(self):
        title = self.entry.get().strip()
        if title:
            self.tasks.insert(0, {'id': str(time.time()), 'title': title, 'subject': self.sub_menu.get(), 'completed': False})
            self.entry.delete(0, 'end')
            self.render_tasks(); self.save_func(); self.mood_func('HAPPY')

    def toggle_task(self, task):
        task['completed'] = not task['completed']
        self.render_tasks(); self.save_func()
        if task['completed']: self.mood_func('HAPPY')

    def delete_task(self, task):
        self.tasks.remove(task)
        self.render_tasks(); self.save_func()

    # ========== Timer Methods ==========
    def on_slider_move(self, value):
        if not self.timer_running:
            self.timer_seconds = int(value) * 60
            self.total_seconds = self.timer_seconds
            self.update_timer_display()
            self.progress.set(1.0)

    def set_timer_mode(self, mode):
        self.timer_running = False
        self.timer_mode = mode
        self.start_btn.configure(text="BẮT ĐẦU", fg_color=COLORS['primary'])
        minutes = 25 if mode == 'WORK' else (5 if mode == 'SHORT_BREAK' else 15)
        self.timer_seconds = minutes * 60
        self.total_seconds = self.timer_seconds
        self.time_slider.set(minutes)
        self.progress.set(1.0)
        self.update_timer_display()
        mood_map = {'WORK': 'IDLE', 'SHORT_BREAK': 'EATING', 'LONG_BREAK': 'SLEEP'}
        self.mood_func(mood_map[mode])

    def update_timer_display(self):
        mins, secs = divmod(self.timer_seconds, 60)
        self.timer_display.configure(text=f"{mins:02}:{secs:02}")

    def toggle_timer(self):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.time_slider.configure(state="disabled")
            self.start_btn.configure(text="TẠM DỪNG", fg_color=COLORS['warning'])
            if self.timer_mode == 'WORK': self.mood_func('FOCUS')
            self.run_timer_loop()
        else:
            # Tạm dừng timer - tăng pause count
            self.time_slider.configure(state="normal")
            self.start_btn.configure(text="TIẾP TỤC", fg_color=COLORS['primary'])
            if self.timer_mode == 'WORK': 
                self.mood_func('IDLE')
                # Tăng pause count
                self.data['streak']['pause_count'] += 1
                self.save_func()
                
                # Kiểm tra cảnh báo
                if self.data['streak']['pause_count'] >= MAX_PAUSE_BEFORE_WARNING:
                    self.show_pause_warning()

    def run_timer_loop(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.update_timer_display()
            self.progress.set(self.timer_seconds / self.total_seconds)
            self.after(1000, self.run_timer_loop)
        elif self.timer_seconds == 0:
            self.timer_running = False
            self.time_slider.configure(state="normal")
            self.start_btn.configure(text="HOÀN THÀNH", fg_color=COLORS['success'])
            self.mood_func('HAPPY')
            
            # Thưởng xu nếu là chế độ học
            if self.timer_mode == 'WORK':
                self.data['coins'] += COINS_PER_FOCUS
                # Reset pause count khi hoàn thành timer
                self.data['streak']['pause_count'] = 0
                self.save_func()
                self.coin_callback(self.data['coins'])

    def show_pause_warning(self):
        """Hiển thị cảnh báo nếu người dùng pause quá nhiều lần"""
        pause_count = self.data['streak']['pause_count']
        
        # Tạo cửa sổ cảnh báo
        warning_window = ctk.CTkToplevel(self.master)
        warning_window.title("⚠️ Cảnh báo")
        warning_window.geometry("400x200")
        warning_window.configure(fg_color=COLORS['card_bg'])
        
        # Icon cảnh báo
        ctk.CTkLabel(warning_window, text="⚠️", font=("Arial", 40)).pack(pady=(20, 10))
        
        # Thông điệp
        msg = f"Bạn đã tạm dừng {pause_count} lần!\nHãy cố gắng hoàn thành phiên học mà không tạm dừng."
        ctk.CTkLabel(warning_window, text=msg, font=("Segoe UI", 13), 
                     text_color=COLORS['warning']).pack(pady=10, padx=20)
        
        # Button OK
        ctk.CTkButton(warning_window, text="OK, Sẽ cố gắng!", 
                     fg_color=COLORS['primary'],
                     command=warning_window.destroy).pack(pady=20)