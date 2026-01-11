import customtkinter as ctk
from config import COLORS
from database import register_user, login_user

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Capoo - Đăng Nhập")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(fg_color=COLORS['bg'])
        
        # Kết quả đăng nhập
        self.login_result = None
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main Frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_frame.grid_columnconfigure(0, weight=1)

        # ========== Logo / Title ==========
        title = ctk.CTkLabel(main_frame, text="📚 Study with Capoo", 
                            font=("Segoe UI", 24, "bold"), text_color=COLORS['primary'])
        title.grid(row=0, column=0, pady=(0, 30))

        # ========== Username Input ==========
        ctk.CTkLabel(main_frame, text="Tên Tài Khoản", 
                    font=("Segoe UI", 12, "bold"), text_color=COLORS['text']).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(main_frame, placeholder_text="Nhập tên tài khoản", 
                                          border_width=1, border_color=COLORS['card_border'],
                                          fg_color=COLORS['input_bg'], text_color=COLORS['text'],
                                          placeholder_text_color=COLORS['text_sub'])
        self.username_entry.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        # ========== Password Input ==========
        ctk.CTkLabel(main_frame, text="Mật Khẩu", 
                    font=("Segoe UI", 12, "bold"), text_color=COLORS['text']).grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(main_frame, placeholder_text="Nhập mật khẩu", 
                                          show="•", border_width=1, border_color=COLORS['card_border'],
                                          fg_color=COLORS['input_bg'], text_color=COLORS['text'],
                                          placeholder_text_color=COLORS['text_sub'])
        self.password_entry.grid(row=4, column=0, sticky="ew", pady=(0, 25))

        # ========== Message Label ==========
        self.message_label = ctk.CTkLabel(main_frame, text="", 
                                         font=("Segoe UI", 11), text_color=COLORS['danger'])
        self.message_label.grid(row=5, column=0, sticky="w", pady=(0, 15))

        # ========== Buttons ==========
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=6, column=0, sticky="ew", pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.login_btn = ctk.CTkButton(button_frame, text="ĐĂNG NHẬP", 
                                      font=("Segoe UI", 13, "bold"),
                                      fg_color=COLORS['primary'], hover_color=COLORS['primary_hover'],
                                      command=self.handle_login)
        self.login_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.register_btn = ctk.CTkButton(button_frame, text="ĐĂNG KÝ", 
                                         font=("Segoe UI", 13, "bold"),
                                         fg_color=COLORS['success'], hover_color="#16A34A",
                                         command=self.handle_register)
        self.register_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # ========== Guest Button ==========
        self.guest_btn = ctk.CTkButton(main_frame, text="🎮 Chơi dưới tên Guest", 
                                      font=("Segoe UI", 11),
                                      fg_color="transparent", text_color=COLORS['text_sub'],
                                      hover_color=COLORS['input_bg'],
                                      command=self.handle_guest)
        self.guest_btn.grid(row=7, column=0, sticky="ew")

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.show_message("Vui lòng nhập đầy đủ thông tin", "danger")
            return

        success, message = login_user(username, password)
        if success:
            self.login_result = {'type': 'login', 'username': username}
            self.destroy()
        else:
            self.show_message(message, "danger")

    def handle_register(self):
        """Xử lý đăng ký"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.show_message("Vui lòng nhập đầy đủ thông tin", "danger")
            return

        if len(username) < 3:
            self.show_message("Tên tài khoản phải từ 3 ký tự trở lên", "danger")
            return

        if len(password) < 6:
            self.show_message("Mật khẩu phải từ 6 ký tự trở lên", "danger")
            return

        success, message = register_user(username, password)
        if success:
            self.show_message("Đăng ký thành công! Vui lòng đăng nhập", "success")
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            self.show_message(message, "danger")

    def handle_guest(self):
        """Chơi dưới tên Guest"""
        self.login_result = {'type': 'guest', 'username': 'Guest'}
        self.destroy()

    def show_message(self, text, color_type):
        """Hiển thị thông báo"""
        color = COLORS['danger'] if color_type == 'danger' else COLORS['success']
        self.message_label.configure(text=text, text_color=color)

    def get_login_result(self):
        """Trả về kết quả đăng nhập"""
        return self.login_result
