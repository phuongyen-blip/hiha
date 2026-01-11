import customtkinter as ctk
from PIL import Image, ImageSequence
import os
import pygame
from config import COLORS, IMG_DIR, MUSIC_DIR
from ui.streak_badge import StreakBadge

class LeftPanel(ctk.CTkFrame):
    def __init__(self, master, shop_callback, data=None):
        super().__init__(master, fg_color="transparent")
        
        # Khởi tạo các biến trạng thái animation
        self.gif_frames = []
        self.animation_id = None
        self.current_frame_idx = 0
        
        # Khởi tạo âm thanh
        pygame.mixer.init()
        self.is_playing = False
        
        self.shop_callback = shop_callback
        self.data = data
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Thẻ Capoo ---
        self.capoo_card = ctk.CTkFrame(self, fg_color=COLORS['card_bg'], corner_radius=25, 
                                       border_width=1, border_color=COLORS['card_border'])
        self.capoo_card.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        self.bubble = ctk.CTkLabel(self.capoo_card, text="Sẵn sàng chưa?", 
                                   font=("Segoe UI", 15, "italic"), 
                                   fg_color=COLORS['input_bg'], corner_radius=15, 
                                   pady=10, padx=20)
        self.bubble.pack(pady=(25, 5))
        
        self.capoo_label = ctk.CTkLabel(self.capoo_card, text="")
        self.capoo_label.pack(expand=True, fill="both", padx=20, pady=10)

        # --- Thẻ Nhạc Nền ---
        self.music_card = ctk.CTkFrame(self, fg_color=COLORS['card_bg'], corner_radius=25, 
                                        border_width=1, border_color=COLORS['card_border'])
        self.music_card.grid(row=1, column=0, sticky="ew", pady=(20, 10))

        music_label = ctk.CTkLabel(self.music_card, text="Nhạc Nền Tập Trung", 
                                   font=("Segoe UI", 13, "bold"), text_color=COLORS['text_sub'])
        music_label.pack(pady=(12, 5))

        self.play_btn = ctk.CTkButton(self.music_card, text="▶ PLAY", width=90, height=32, corner_radius=16,
                                      fg_color=COLORS['primary'], hover_color=COLORS['primary_hover'],
                                      command=self.toggle_music)
        self.play_btn.pack(side="left", padx=(30, 10), pady=(0, 20))

        self.vol_slider = ctk.CTkSlider(self.music_card, from_=0, to=1, width=160,
                                        button_color=COLORS['primary'], progress_color=COLORS['primary'],
                                        command=self.change_volume)
        self.vol_slider.pack(side="left", padx=(10, 30), pady=(0, 20))
        self.vol_slider.set(0.5)

        # --- Nút Shop ---
        self.shop_btn = ctk.CTkButton(self, text="🛍️ CỬA HÀNG", width=180, height=40, 
                                      corner_radius=20, fg_color=COLORS['primary'],
                                      hover_color=COLORS['primary_hover'],
                                      font=("Segoe UI", 12, "bold"),
                                      command=self.shop_callback)
        self.shop_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # --- Streak Badge ---
        if self.data:
            button_frame = ctk.CTkFrame(self, fg_color="transparent")
            button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
            button_frame.grid_columnconfigure(1, weight=1)
            
            self.streak_badge = StreakBadge(button_frame, self.data)
            self.streak_badge.pack(side="left", padx=(0, 10))

    def toggle_music(self):
        if not os.path.exists(MUSIC_DIR):
            os.makedirs(MUSIC_DIR)
            return

        songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
        if not songs: return

        if not self.is_playing:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(MUSIC_DIR, songs[0]))
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_btn.configure(text="⏸ PAUSE", fg_color=COLORS['warning'])
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_btn.configure(text="▶ PLAY", fg_color=COLORS['primary'])

    def change_volume(self, value):
        pygame.mixer.music.set_volume(value)

    def update_mood(self, mood):
        msgs = {'IDLE': "Sẵn sàng học chưa?", 'FOCUS': "Suỵt! Đang tập trung...", 
                'SLEEP': "Zzz... Nghỉ ngơi nào.", 'HAPPY': "Tuyệt vời quá!", 
                'EATING': "Măm măm..."}
        self.bubble.configure(text=msgs.get(mood, "..."))
        path = os.path.join(IMG_DIR, f"{mood}.gif")
        if os.path.exists(path):
            img = Image.open(path)
            self.gif_frames = [ctk.CTkImage(light_image=f.convert("RGBA").resize((260, 260)), 
                              size=(260, 260)) for f in ImageSequence.Iterator(img)]
            self.current_frame_idx = 0
            if self.animation_id: self.after_cancel(self.animation_id)
            self.animate()

    def animate(self):
        if self.gif_frames:
            self.capoo_label.configure(image=self.gif_frames[self.current_frame_idx])
            self.current_frame_idx = (self.current_frame_idx + 1) % len(self.gif_frames)
            self.animation_id = self.after(100, self.animate)