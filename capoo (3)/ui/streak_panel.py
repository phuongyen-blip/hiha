import customtkinter as ctk
from config import COLORS, STREAK_MILESTONES

class StreakPanel(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master, fg_color=COLORS['card_bg'], corner_radius=20, 
                         border_width=1, border_color=COLORS['card_border'])
        self.data = data
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        # ========== Streak Counter ==========
        streak_container = ctk.CTkFrame(self, fg_color=COLORS['input_bg'], corner_radius=15)
        streak_container.pack(fill="x", padx=15, pady=15)
        
        # Flame icon + current streak
        top_frame = ctk.CTkFrame(streak_container, fg_color="transparent")
        top_frame.pack(fill="x", padx=12, pady=10)
        
        streak_value = self.data['streak']['current_streak']
        ctk.CTkLabel(top_frame, text="🔥", font=("Arial", 28)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(top_frame, text=f"{streak_value} ngày", 
                     font=("Segoe UI", 16, "bold"), text_color=COLORS['primary']).pack(side="left")
        
        # Subtitle
        ctk.CTkLabel(streak_container, text="Chuỗi hiện tại", 
                     font=("Segoe UI", 11), text_color=COLORS['text_sub']).pack(anchor="w", padx=12, pady=(0, 10))
        
        # ========== Milestones Progress Bar ==========
        milestone_label = ctk.CTkLabel(self, text="🏆 Các mốc thành tích", 
                                       font=("Segoe UI", 13, "bold"), text_color=COLORS['text'])
        milestone_label.pack(anchor="w", padx=15, pady=(10, 8))
        
        milestones_reached = self.data['streak']['milestones_reached']
        
        # Milestone items
        for milestone in STREAK_MILESTONES:
            days = milestone['days']
            coins = milestone['coins']
            emoji = milestone['emoji']
            is_reached = days in milestones_reached
            
            mile_frame = ctk.CTkFrame(self, fg_color=COLORS['input_bg'] if is_reached else COLORS['card_bg'], 
                                      corner_radius=12, border_width=1,
                                      border_color=COLORS['success'] if is_reached else COLORS['card_border'])
            mile_frame.pack(fill="x", padx=15, pady=5)
            
            # Left side: day & emoji
            left = ctk.CTkFrame(mile_frame, fg_color="transparent")
            left.pack(side="left", padx=12, pady=10)
            
            if is_reached:
                ctk.CTkLabel(left, text="✅ " + emoji, font=("Arial", 16)).pack(side="left", padx=(0, 8))
            else:
                ctk.CTkLabel(left, text=emoji, font=("Arial", 16), text_color=COLORS['text_sub']).pack(side="left", padx=(0, 8))
            
            day_text = f"{days} ngày"
            day_color = COLORS['success'] if is_reached else COLORS['text']
            ctk.CTkLabel(left, text=day_text, font=("Segoe UI", 12, "bold"), text_color=day_color).pack(side="left")
            
            # Right side: coins reward
            coin_text = f"+{coins} xu"
            coin_color = COLORS['success'] if is_reached else COLORS['text_sub']
            coin_style = ("Segoe UI", 11, "bold") if is_reached else ("Segoe UI", 11)
            ctk.CTkLabel(mile_frame, text=coin_text, font=coin_style, text_color=coin_color).pack(side="right", padx=12, pady=10)
        
        # ========== Pause Count Warning ==========
        pause_count = self.data['streak'].get('pause_count', 0)
        if pause_count > 0:
            pause_frame = ctk.CTkFrame(self, fg_color="#FFF3CD", corner_radius=12, border_width=1,
                                       border_color=COLORS['warning'])
            pause_frame.pack(fill="x", padx=15, pady=15)
            
            pause_text = f"⏸️ Đã tạm dừng {pause_count} lần"
            pause_msg = "Hãy cố gắng không tạm dừng để giữ streak!" if pause_count < 5 else "⚠️ Quá nhiều tạm dừng!"
            
            ctk.CTkLabel(pause_frame, text=pause_text, font=("Segoe UI", 11, "bold"), 
                         text_color=COLORS['warning']).pack(anchor="w", padx=12, pady=(10, 5))
            ctk.CTkLabel(pause_frame, text=pause_msg, font=("Segoe UI", 10), 
                         text_color=COLORS['text_sub']).pack(anchor="w", padx=12, pady=(0, 10))

    def update_streak(self, data):
        """Cập nhật streak panel khi dữ liệu thay đổi"""
        self.data = data
        # Xóa các widget cũ
        for widget in self.winfo_children():
            widget.destroy()
        # Vẽ lại UI
        self.setup_ui()
