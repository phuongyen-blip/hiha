import os

APP_NAME = "Study with Capoo v2.0"
DATA_FILE = "capoo_tasks.json"
IMG_DIR = "capoo_images"

COLORS = {
    'bg': '#F8FAFC',          # Xám trắng cực nhẹ cho nền chính
    'card_bg': '#FFFFFF',
    'card_border': '#E2E8F0',  # Viền mảnh hơn, tinh tế hơn
    'primary': '#6366F1',     # Màu Indigo hiện đại (thay cho xanh Cyan)
    'primary_hover': '#4F46E5',
    'text': '#1E293B',        # Xám đậm (không dùng đen tuyệt đối)
    'text_sub': '#64748B',
    'danger': '#FF6B6B',
    'success': '#22C55E',
    'warning': '#F59E0B',
    'input_bg': '#F1F5F9'
}

MOOD_URLS = {
    'IDLE': 'https://media.tenor.com/TS7aSPWwXJ4AAAAi/capoo-waiting.gif',
    'FOCUS': 'https://media.tenor.com/vDw6g_xPS5oAAAAi/rexx.gif',
    'SLEEP': 'https://media.tenor.com/aOI-lNajTVYAAAAi/blue-bugcat.gif',
    'HAPPY': 'https://media.tenor.com/8oRk0EBWv1AAAAAi/bugcat-capoo.gif',
    'EATING': 'https://media.tenor.com/y3ME7qOn0D0AAAAi/arena-fotosintesis.gif'
}

SUBJECTS = ['Toán', 'Văn', 'Lí', 'Hóa', 'Sử', 'Địa', 'Anh', 'Code', 'Khác']
MUSIC_DIR = "capoo_music" # Thư mục chứa các file .mp3 của bạn

# ========== Reward System ==========
COINS_PER_FOCUS = 10  # 10 xu cho mỗi phiên học 25 phút

# ========== Shop Items ==========
SHOP_ITEMS = [
    {'id': 'item_1', 'name': 'Mũ Party', 'cost': 50, 'emoji': '🎩'},
    {'id': 'item_2', 'name': 'Kính mặt trời', 'cost': 75, 'emoji': '😎'},
    {'id': 'item_3', 'name': 'Quả bóng', 'cost': 30, 'emoji': '⚽'},
    {'id': 'item_4', 'name': 'Hoa hồng', 'cost': 100, 'emoji': '🌹'},
]

# ========== Streak System ==========
STREAK_MILESTONES = [
    {'days': 5, 'coins': 50, 'emoji': '🔥'},
    {'days': 10, 'coins': 100, 'emoji': '🔥🔥'},
    {'days': 25, 'coins': 250, 'emoji': '⭐'},
    {'days': 50, 'coins': 500, 'emoji': '👑'},
    {'days': 100, 'coins': 1000, 'emoji': '💎'},
]
STREAK_BREAK_HOURS = 24  # Streak bị gián đoạn nếu không vào trong 24 giờ
MAX_PAUSE_BEFORE_WARNING = 5  # Cảnh báo nếu pause > 5 lần