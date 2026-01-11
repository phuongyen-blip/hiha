import customtkinter as ctk
from config import COLORS, SHOP_ITEMS

class ShopWindow(ctk.CTkToplevel):
    def __init__(self, parent, data, save_func):
        super().__init__(parent)
        self.title("🛍️ Cửa Hàng")
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(fg_color=COLORS['bg'])
        
        self.data = data
        self.save_func = save_func
        
        # Center window on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (600 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ========== Header với Coin Counter ==========
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        ctk.CTkLabel(header, text="Cửa Hàng", 
                     font=("Segoe UI", 18, "bold"), text_color=COLORS['text']).pack(side="left")

        # Coin display
        self.coin_label = ctk.CTkLabel(header, text="💰 0", 
                                       font=("Segoe UI", 14, "bold"), 
                                       text_color=COLORS['primary'])
        self.coin_label.pack(side="right")
        self.update_coin_display()

        # ========== Shop Items ==========
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll.grid_columnconfigure(0, weight=1)

        self.render_shop()

    def render_shop(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for item in SHOP_ITEMS:
            # Item Card
            card = ctk.CTkFrame(self.scroll, fg_color=COLORS['input_bg'], 
                               corner_radius=16, border_width=1, 
                               border_color=COLORS['card_border'])
            card.pack(fill="x", pady=8, padx=5)

            # Left side: emoji and name
            left_frame = ctk.CTkFrame(card, fg_color="transparent")
            left_frame.pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(left_frame, text=item['emoji'], 
                        font=("Segoe UI", 28)).pack()

            ctk.CTkLabel(left_frame, text=item['name'], 
                        font=("Segoe UI", 11, "bold"), 
                        text_color=COLORS['text']).pack()

            # Right side: cost and button
            right_frame = ctk.CTkFrame(card, fg_color="transparent")
            right_frame.pack(side="right", padx=15, pady=12)

            ctk.CTkLabel(right_frame, text=f"💰 {item['cost']}", 
                        font=("Segoe UI", 12, "bold"), 
                        text_color=COLORS['primary']).pack(side="left", padx=(0, 10))

            # Buy button
            btn_state = "normal" if self.data['coins'] >= item['cost'] else "disabled"
            btn_fg = COLORS['primary'] if self.data['coins'] >= item['cost'] else COLORS['text_sub']
            
            ctk.CTkButton(right_frame, text="MUA", width=60, height=32, corner_radius=12,
                         fg_color=btn_fg, hover_color=COLORS['primary_hover'] if btn_state == "normal" else btn_fg,
                         state=btn_state,
                         command=lambda i=item: self.buy_item(i)).pack(side="left")

    def buy_item(self, item):
        if self.data['coins'] >= item['cost']:
            self.data['coins'] -= item['cost']
            
            # Thêm vật phẩm vào danh sách (nếu chưa có)
            if item['id'] not in self.data['items']:
                self.data['items'].append(item['id'])
            
            self.save_func()
            self.update_coin_display()
            self.render_shop()

    def update_coin_display(self):
        self.coin_label.configure(text=f"💰 {self.data['coins']}")

    def update_coins_from_timer(self, coins):
        """Được gọi từ main.py khi timer hoàn thành"""
        self.update_coin_display()
