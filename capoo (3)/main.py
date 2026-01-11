import customtkinter as ctk
from config import APP_NAME, COLORS
from database import load_user_data, save_user_data, load_data, save_data, ensure_assets, check_and_update_streak, reward_milestone
from ui.login_window import LoginWindow
from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from ui.shop_panel import ShopWindow

class CapooApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        # Load user data
        if username == 'Guest':
            self.data = load_data()  # Load legacy data for guests
        else:
            self.data = load_user_data(username)
        
        # Check and update streak
        self.data = check_and_update_streak(self.data)
        
        # Check if reached any milestone and reward coins
        milestone_coins = reward_milestone(self.data)
        if milestone_coins > 0:
            print(f"🎉 Đạt mốc streak! Nhận được {milestone_coins} xu!")
        
        self.title(f"{APP_NAME} - {username}")
        self.geometry("1400x750")
        self.configure(fg_color=COLORS['bg'])

        self.shop_window = None
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left panel: Capoo character
        self.left_panel = LeftPanel(self, self.open_shop, self.data)
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Right panel: Tasks & Timer
        self.right_panel = RightPanel(self, self.data, self.save_all, self.update_mood, self.update_shop_coins)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)

        ensure_assets(lambda: self.left_panel.update_mood('IDLE'))
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_shop(self):
        """Mở cửa sổ cửa hàng"""
        if self.shop_window is None or not self.shop_window.winfo_exists():
            self.shop_window = ShopWindow(self, self.data, self.save_all)
        else:
            self.shop_window.lift()
            self.shop_window.focus()

    def update_mood(self, mood):
        self.left_panel.update_mood(mood)

    def update_shop_coins(self, coins):
        """Callback từ right_panel khi timer hoàn thành"""
        if self.shop_window and self.shop_window.winfo_exists():
            self.shop_window.update_coins_from_timer(coins)
        # Update streak panel nếu có milestone mới
        milestone_coins = reward_milestone(self.data)
        if milestone_coins > 0:
            # Update streak badge
            if hasattr(self.left_panel, 'streak_badge'):
                self.left_panel.streak_badge.update_streak(self.data)

    def save_all(self):
        if self.username == 'Guest':
            save_data(self.data)
        else:
            save_user_data(self.username, self.data)

    def on_close(self):
        self.save_all()
        self.destroy()

def main():
    """Hiển thị login window trước"""
    login = LoginWindow()
    login.mainloop()
    
    result = login.get_login_result()
    if result is None:
        return
    
    # Khởi động ứng dụng chính
    app = CapooApp(result['username'])
    app.mainloop()

if __name__ == "__main__":
    main()