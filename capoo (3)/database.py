import json
import os
import urllib.request
import threading
import hashlib
from config import DATA_FILE, IMG_DIR, MOOD_URLS

# ========== User Authentication ==========
def hash_password(password):
    """Hash password với SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Kiểm tra password"""
    return hash_password(password) == hashed

def load_users_db():
    """Tải database người dùng"""
    users_file = "capoo_users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users_db(users):
    """Lưu database người dùng"""
    users_file = "capoo_users.json"
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(username, password):
    """Đăng ký người dùng mới"""
    users = load_users_db()
    if username in users:
        return False, "Tên tài khoản đã tồn tại"
    
    users[username] = {
        'password': hash_password(password),
        'created_at': str(__import__('datetime').datetime.now())
    }
    save_users_db(users)
    return True, "Đăng ký thành công"

def login_user(username, password):
    """Kiểm tra đăng nhập"""
    users = load_users_db()
    if username not in users:
        return False, "Tài khoản không tồn tại"
    
    if verify_password(password, users[username]['password']):
        return True, "Đăng nhập thành công"
    else:
        return False, "Sai mật khẩu"

# ========== User Data Management ==========
def load_user_data(username):
    """Tải dữ liệu của người dùng cụ thể"""
    user_file = f"capoo_data_{username}.json"
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            return get_default_user_data()
    return get_default_user_data()

def get_default_user_data():
    """Dữ liệu mặc định cho người dùng mới"""
    return {
        'tasks': [],
        'coins': 0,
        'items': [],
        'flashcard_decks': [],
        'current_mood': 'IDLE',
        'streak': {
            'current_streak': 0,
            'total_days': 0,
            'last_login_date': None,
            'milestones_reached': [],
            'pause_count': 0
        }
    }

def save_user_data(username, data):
    """Lưu dữ liệu người dùng"""
    user_file = f"capoo_data_{username}.json"
    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== Legacy Support (Backward Compatibility) ==========
def load_data():
    """Load dữ liệu (legacy support)"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {'tasks': data, 'coins': 0, 'items': [], 'flashcard_decks': [], 'current_mood': 'IDLE'}
                return data
        except: 
            return get_default_user_data()
    return get_default_user_data()

def save_data(data):
    """Lưu dữ liệu (legacy support)"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ensure_assets(callback):
    """Tải asset GIF từ Tenor"""
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    
    def download_logic():
        for mood, url in MOOD_URLS.items():
            path = os.path.join(IMG_DIR, f"{mood}.gif")
            if not os.path.exists(path):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
                        f.write(resp.read())
                except: pass
        callback()

    threading.Thread(target=download_logic, daemon=True).start()

# ========== Streak System ==========
def check_and_update_streak(data):
    """
    Kiểm tra streak hàng ngày. Nếu người dùng không vào trong 24 giờ, streak sẽ bị gián đoạn.
    Nếu vào lại trong 24 giờ, streak sẽ tiếp tục và total_days tăng lên.
    """
    from datetime import datetime, timedelta
    from config import STREAK_BREAK_HOURS
    
    if 'streak' not in data:
        data['streak'] = {
            'current_streak': 0,
            'total_days': 0,
            'last_login_date': None,
            'milestones_reached': [],
            'pause_count': 0
        }
    
    today = datetime.now().date()
    today_str = str(today)
    last_login = data['streak']['last_login_date']
    
    if last_login is None:
        # Lần đầu tiên vào
        data['streak']['last_login_date'] = today_str
        data['streak']['current_streak'] = 1
        data['streak']['total_days'] = 1
    elif last_login == today_str:
        # Đã vào hôm nay rồi, không cần làm gì
        pass
    else:
        # Kiểm tra nếu vào hôm nay (ngày hôm sau)
        last_login_date = datetime.strptime(last_login, '%Y-%m-%d').date()
        days_gap = (today - last_login_date).days
        
        if days_gap == 1:
            # Vào đúng hôm sau, streak tiếp tục
            data['streak']['current_streak'] += 1
            data['streak']['total_days'] += 1
        else:
            # Quá 24 giờ, streak bị gián đoạn
            data['streak']['current_streak'] = 1
            data['streak']['total_days'] += 1
        
        data['streak']['last_login_date'] = today_str
    
    return data

def reward_milestone(data):
    """
    Kiểm tra nếu streak đạt milestone nào đó và cấp phát coins.
    Trả về số coins được cấp phát.
    """
    from config import STREAK_MILESTONES
    
    if 'streak' not in data:
        return 0
    
    current_streak = data['streak']['current_streak']
    milestones_reached = data['streak']['milestones_reached']
    coins_earned = 0
    
    for milestone in STREAK_MILESTONES:
        milestone_days = milestone['days']
        if current_streak == milestone_days and milestone_days not in milestones_reached:
            coins_earned = milestone['coins']
            data['coins'] += coins_earned
            milestones_reached.append(milestone_days)
            break
    
    return coins_earned