import customtkinter as ctk
from config import COLORS, STREAK_MILESTONES

class StreakBadge(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master, fg_color="transparent")
        self.data = data
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(header, text="🔥 Streak", font=("Segoe UI", 11, "bold"), 
                     text_color=COLORS['text']).pack(side="left")
        
        streak_value = self.data['streak']['current_streak']
        ctk.CTkLabel(header, text=f"{streak_value} ngày", font=("Segoe UI", 11, "bold"), 
                     text_color=COLORS['primary']).pack(side="right")
        
        # Milestone bar
        milestones = STREAK_MILESTONES
        max_milestone = milestones[-1]['days']  # 100
        current_streak = streak_value
        
        # Progress container
        bar_frame = ctk.CTkFrame(self, fg_color=COLORS['input_bg'], corner_radius=8, height=50)
        bar_frame.pack(fill="x")
        bar_frame.grid_propagate(False)
        
        # Background bar
        bg_bar = ctk.CTkFrame(bar_frame, fg_color=COLORS['card_border'], corner_radius=4, height=6)
        bg_bar.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.15)
        
        # Progress bar
        progress_width = min(current_streak / max_milestone, 1.0)
        progress_bar = ctk.CTkFrame(bar_frame, fg_color=COLORS['primary'], corner_radius=4, height=6)
        progress_bar.place(relx=0.05, rely=0.2, relwidth=progress_width * 0.9, relheight=0.15)
        
        # Milestones markers
        for milestone in milestones:
            days = milestone['days']
            emoji = milestone['emoji']
            pos = (days / max_milestone) * 0.9 + 0.05  # Tính vị trí (0-1)
            
            is_reached = days in self.data['streak']['milestones_reached']
            marker_color = COLORS['success'] if is_reached else COLORS['text_sub']
            
            # Marker point
            marker = ctk.CTkLabel(bar_frame, text="●", font=("Arial", 8), text_color=marker_color)
            marker.place(relx=pos, rely=0.5, anchor="center")
            
            # Milestone label
            label_text = f"{days}"
            label_color = COLORS['success'] if is_reached else COLORS['text_sub']
            label_font = ("Segoe UI", 9, "bold") if is_reached else ("Segoe UI", 9)
            
            label = ctk.CTkLabel(bar_frame, text=label_text, font=label_font, text_color=label_color)
            label.place(relx=pos, rely=0.75, anchor="center")

    def update_streak(self, data):
        """Cập nhật streak bar"""
        self.data = data
        # Xóa các widget cũ
        for widget in self.winfo_children():
            widget.destroy()
        # Vẽ lại
        self.setup_ui()

