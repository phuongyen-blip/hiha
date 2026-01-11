import customtkinter as ctk
import time
from config import COLORS

class FlashcardPanel(ctk.CTkFrame):
    def __init__(self, master, data, save_func):
        super().__init__(master, fg_color=COLORS['card_bg'], corner_radius=25, 
                         border_width=1, border_color=COLORS['card_border'])
        self.data = data
        self.save_func = save_func
        
        # State
        self.current_deck = None
        self.current_card_idx = 0
        self.is_flipped = False
        self.learned_cards = set()
        
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ========== Header ==========
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(header, text="📇 Flashcard", 
                     font=("Segoe UI", 18, "bold"), text_color=COLORS['text']).pack(side="left")

        # ========== View Selection ==========
        self.view_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.view_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        self.view_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(self.view_frame, text="Tất Cả Deck", width=120, height=32, corner_radius=14,
                     fg_color=COLORS['primary'], text_color="white",
                     command=self.show_deck_list).grid(row=0, column=0, padx=(0, 10))

        self.view_label = ctk.CTkLabel(self.view_frame, text="", font=("Segoe UI", 12), 
                                       text_color=COLORS['text_sub'])
        self.view_label.grid(row=0, column=1, sticky="ew")

        # ========== Main Content ==========
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Khởi tạo views
        self.show_deck_list()

    def show_deck_list(self):
        """Hiển thị danh sách deck"""
        self.current_deck = None
        self.view_label.configure(text="Danh sách Deck")
        self.clear_content()

        # Nút tạo deck mới
        new_deck_btn = ctk.CTkButton(self.content_frame, text="➕ Tạo Deck Mới", 
                                     height=40, corner_radius=12,
                                     fg_color=COLORS['success'], hover_color="#16A34A",
                                     command=self.show_create_deck).pack(fill="x", pady=(0, 15))

        # Danh sách deck
        if not self.data.get('flashcard_decks', []):
            ctk.CTkLabel(self.content_frame, text="Chưa có deck nào. Tạo deck mới để bắt đầu!", 
                         font=("Segoe UI", 13), text_color=COLORS['text_sub']).pack(pady=30)
            return

        for deck in self.data['flashcard_decks']:
            self.render_deck_card(deck)

    def render_deck_card(self, deck):
        """Render một deck card"""
        card = ctk.CTkFrame(self.content_frame, fg_color=COLORS['input_bg'], 
                           corner_radius=12, border_width=1, border_color=COLORS['card_border'])
        card.pack(fill="x", pady=8, padx=5)

        # Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)

        ctk.CTkLabel(info_frame, text=deck['name'], font=("Segoe UI", 13, "bold"), 
                    text_color=COLORS['text']).pack(anchor="w")

        card_count = len(deck.get('cards', []))
        ctk.CTkLabel(info_frame, text=f"📝 {card_count} thẻ", font=("Segoe UI", 11), 
                    text_color=COLORS['text_sub']).pack(anchor="w")

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=12, pady=12)

        ctk.CTkButton(btn_frame, text="Học", width=70, height=32, corner_radius=10,
                     fg_color=COLORS['primary'], hover_color=COLORS['primary_hover'],
                     command=lambda d=deck: self.start_learning(d)).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Chỉnh", width=70, height=32, corner_radius=10,
                     fg_color=COLORS['warning'], hover_color="#D97706",
                     command=lambda d=deck: self.edit_deck(d)).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Xóa", width=50, height=32, corner_radius=10,
                     fg_color=COLORS['danger'], hover_color="#DC2626",
                     command=lambda d=deck: self.delete_deck(d)).pack(side="left", padx=5)

    def show_create_deck(self):
        """Hiển thị form tạo deck"""
        self.current_deck = 'CREATE'
        self.view_label.configure(text="Tạo Deck Mới")
        self.clear_content()

        ctk.CTkLabel(self.content_frame, text="Tên Deck", font=("Segoe UI", 12, "bold"), 
                    text_color=COLORS['text']).pack(anchor="w", pady=(0, 5))

        name_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Ví dụ: Unit 1 - Tiếng Anh", 
                                  border_width=1, border_color=COLORS['card_border'],
                                  fg_color=COLORS['input_bg'])
        name_entry.pack(fill="x", pady=(0, 20))

        # Thêm thẻ
        ctk.CTkLabel(self.content_frame, text="Thêm Thẻ (Câu hỏi|Đáp án)", 
                    font=("Segoe UI", 12, "bold"), text_color=COLORS['text']).pack(anchor="w", pady=(0, 5))

        cards_text = ctk.CTkTextbox(self.content_frame, height=200, border_width=1, 
                                    border_color=COLORS['card_border'], fg_color=COLORS['input_bg'],
                                    text_color=COLORS['text'])
        cards_text.pack(fill="both", expand=True, pady=(0, 15))
        cards_text.insert("1.0", "Ví dụ:\nApple|Quả táo\nBanana|Quả chuối")

        def save_deck():
            name = name_entry.get().strip()
            if not name:
                return

            cards_content = cards_text.get("1.0", "end-1c").strip().split('\n')
            cards = []
            for line in cards_content:
                if '|' in line:
                    q, a = line.split('|', 1)
                    cards.append({'id': str(time.time()), 'question': q.strip(), 'answer': a.strip()})

            new_deck = {
                'id': str(time.time()),
                'name': name,
                'cards': cards,
                'created_at': str(__import__('datetime').datetime.now())
            }
            self.data['flashcard_decks'].append(new_deck)
            self.save_func()
            self.show_deck_list()

        ctk.CTkButton(self.content_frame, text="✅ Lưu Deck", height=40, corner_radius=12,
                     fg_color=COLORS['success'], hover_color="#16A34A",
                     command=save_deck).pack(fill="x")

        ctk.CTkButton(self.content_frame, text="❌ Hủy", height=35, corner_radius=12,
                     fg_color=COLORS['input_bg'], text_color=COLORS['text'],
                     command=self.show_deck_list).pack(fill="x", pady=(10, 0))

    def start_learning(self, deck):
        """Bắt đầu học deck"""
        if not deck.get('cards'):
            return

        self.current_deck = deck
        self.current_card_idx = 0
        self.is_flipped = False
        self.learned_cards = set()
        self.view_label.configure(text=f"Học: {deck['name']}")
        self.show_flashcard()

    def show_flashcard(self):
        """Hiển thị flashcard"""
        if not self.current_deck or not isinstance(self.current_deck, dict):
            self.show_deck_list()
            return

        cards = self.current_deck.get('cards', [])
        if not cards or self.current_card_idx >= len(cards):
            self.show_learning_complete()
            return

        self.clear_content()
        card = cards[self.current_card_idx]

        # Progress bar
        progress = self.current_card_idx / len(cards)
        progress_bar = ctk.CTkProgressBar(self.content_frame, height=8, corner_radius=4,
                                         progress_color=COLORS['primary'], 
                                         fg_color=COLORS['input_bg'])
        progress_bar.pack(fill="x", pady=(0, 20))
        progress_bar.set(progress)

        # Card counter
        ctk.CTkLabel(self.content_frame, text=f"Thẻ {self.current_card_idx + 1}/{len(cards)}", 
                    font=("Segoe UI", 11), text_color=COLORS['text_sub']).pack(pady=(0, 15))

        # Flashcard
        flashcard = ctk.CTkFrame(self.content_frame, fg_color=COLORS['primary'], 
                                corner_radius=16, border_width=2, 
                                border_color=COLORS['primary_hover'])
        flashcard.pack(fill="both", expand=True, pady=(0, 25))

        text_content = card['answer'] if self.is_flipped else card['question']
        label_text = "Đáp án" if self.is_flipped else "Câu hỏi"

        ctk.CTkLabel(flashcard, text=label_text, font=("Segoe UI", 12, "italic"), 
                    text_color="rgba(255,255,255,0.6)").pack(pady=(15, 10))

        ctk.CTkLabel(flashcard, text=text_content, font=("Segoe UI", 20, "bold"), 
                    text_color="white", wraplength=400).pack(expand=True, padx=20, pady=20)

        ctk.CTkLabel(flashcard, text="👆 Bấm để lật thẻ", font=("Segoe UI", 11, "italic"), 
                    text_color="rgba(255,255,255,0.6)").pack(pady=(10, 15))

        flashcard.bind("<Button-1>", lambda e: self.flip_card())

        # Buttons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="⬅ Quay Lại", width=100, height=36, corner_radius=12,
                     fg_color=COLORS['input_bg'], text_color=COLORS['text'],
                     command=self.prev_card).grid(row=0, column=0, padx=5)

        ctk.CTkButton(btn_frame, text="✅ Đã Hiểu", width=100, height=36, corner_radius=12,
                     fg_color=COLORS['success'], hover_color="#16A34A",
                     command=self.mark_learned).grid(row=0, column=1, padx=5)

        ctk.CTkButton(btn_frame, text="➡ Tiếp →", width=100, height=36, corner_radius=12,
                     fg_color=COLORS['primary'], hover_color=COLORS['primary_hover'],
                     command=self.next_card).grid(row=0, column=2, padx=5)

    def flip_card(self):
        """Lật thẻ"""
        self.is_flipped = not self.is_flipped
        self.show_flashcard()

    def next_card(self):
        """Thẻ tiếp theo"""
        self.current_card_idx += 1
        self.is_flipped = False
        self.show_flashcard()

    def prev_card(self):
        """Thẻ trước"""
        if self.current_card_idx > 0:
            self.current_card_idx -= 1
            self.is_flipped = False
            self.show_flashcard()

    def mark_learned(self):
        """Đánh dấu là đã hiểu"""
        self.learned_cards.add(self.current_card_idx)
        self.next_card()

    def show_learning_complete(self):
        """Hiển thị khi hoàn thành học"""
        self.clear_content()
        completion_pct = (len(self.learned_cards) / len(self.current_deck['cards']) * 100) if self.current_deck['cards'] else 0

        ctk.CTkLabel(self.content_frame, text="🎉 Hoàn Thành!", font=("Segoe UI", 24, "bold"), 
                    text_color=COLORS['primary']).pack(pady=20)

        ctk.CTkLabel(self.content_frame, text=f"Bạn đã hiểu {int(completion_pct)}% thẻ", 
                    font=("Segoe UI", 14), text_color=COLORS['text']).pack(pady=10)

        ctk.CTkLabel(self.content_frame, text=f"{len(self.learned_cards)}/{len(self.current_deck['cards'])} thẻ", 
                    font=("Segoe UI", 13), text_color=COLORS['text_sub']).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Học Lại", width=120, height=40, corner_radius=12,
                     fg_color=COLORS['primary'], hover_color=COLORS['primary_hover'],
                     command=lambda d=self.current_deck: self.start_learning(d)).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Quay Lại", width=120, height=40, corner_radius=12,
                     fg_color=COLORS['input_bg'], text_color=COLORS['text'],
                     command=self.show_deck_list).pack(side="left", padx=5)

    def edit_deck(self, deck):
        """Chỉnh sửa deck"""
        # TODO: Implement editing
        pass

    def delete_deck(self, deck):
        """Xóa deck"""
        self.data['flashcard_decks'] = [d for d in self.data['flashcard_decks'] if d['id'] != deck['id']]
        self.save_func()
        self.show_deck_list()

    def clear_content(self):
        """Xóa nội dung"""
        for w in self.content_frame.winfo_children():
            w.destroy()
