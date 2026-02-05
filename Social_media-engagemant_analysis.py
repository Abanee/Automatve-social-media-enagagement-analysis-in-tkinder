import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import math
import time
import random
from tkinter import filedialog, ttk, Toplevel
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.model_selection import train_test_split
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import datetime
import threading
import customtkinter as ctk
from tkinter import messagebox

# =============================================================================
# 🎨 THEME MANAGER (From New UI)
# =============================================================================
class ThemeManager:
    """
    Refined Palette for Social Media Analysis (Instagram/TikTok style gradients).
    """
    THEMES = {
        "dark": {
            "name": "Midnight Influencer",
            "bg_primary": "#0F0F1A",
            "bg_secondary": "#181828",
            "bg_header": "#181828",
            "card_bg": "#232336",
            "accent": "#E1306C",
            "accent_hover": "#FD1D1D",
            "gradient_start": "#0F0F1A",
            "gradient_end": "#2A1B3D",
            "text_main": "#FFFFFF",
            "text_muted": "#A8A8C0",
            "success": "#00DC82",
            "danger": "#FF2E63",
            "warning": "#FFC107",
            "border": "#2D2D44",
            "shadow": "#000000",
            "ml_head1":"#6E026F",#ml insight heading
            "metrics_border1" :"#362F4F",#metic table border
            "ins_bg1":"#F0F2F5",#ml insight container bg
            "tab_col11":"#F0F2F5",#metric table
            "tab_col21":"#F0F2F5",#metric table
            "metrics_txt1" :"#362F4F",#metrics table text
            "ml_bg1":"#F0F2F5",#ml text bg
            "ml_txt1":"#362F4F",#ml text
            "Indigo_colour1" :"#5B23FF", #eda box colour
            "mean_col1":"#008BFF",#eda mean
            "eda_txt1":"#362f4f",#eda text
            "eda_bg1":"#F0F2F5",#eda bg
            "viral_bg1":"#F0F2F5",#viral table bg
            "viral_txt1":"#362f4f"#viral table bg
            
        },
        "light": {
            "name": "Daylight Trending",
            "bg_primary": "#F0F2F5",
            "bg_secondary": "#FFFFFF",
            "bg_header": "#FFFFFF",
            "card_bg": "#FFFFFF",
            "accent": "#833AB4",
            "accent_hover": "#C13584",
            "gradient_start": "#F0F2F5",
            "gradient_end": "#E8EAF6",
            "text_main": "#1A1A1A",
            "text_muted": "#65676B",
            "success": "#10B981",
            "danger": "#EF4444",
            "warning": "#F59E0B",
            "border": "#E4E6EB",
            "shadow": "#D1D5DB",
            "ml_head1":"#6E026F",
            "metrics_border1" :"#362F4F",
            "ins_bg1":"#F0F2F5",
            "tab_col11":"#F0F2F5",
            "tab_col21":"#F0F2F5",
            "metrics_txt1" :"#362F4F",
            "ml_bg1":"#F0F2F5",
            "ml_txt1":"#362F4F",
            "Indigo_colour1" :"#5B23FF", 
            "mean_col1":"#008BFF",
            "eda_txt1":"#362f4f",
            "eda_bg1":"#F0F2F5",
            "viral_bg1":"#F0F2F5",
            "viral_txt1":"#362f4f"
        }
    }
    
    current_mode = "light"

    @classmethod
    def get(cls, key):
        return cls.THEMES[cls.current_mode][key]

    @classmethod
    def toggle(cls):
        cls.current_mode = "light" if cls.current_mode == "dark" else "dark"
# =============================================================================
# 🖌️ GRADIENT FRAME (From New UI)
# =============================================================================
class GradientFrame(tk.Canvas):
    """A Canvas that draws a vertical gradient background."""
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.c1 = color1
        self.c2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _hex_to_rgb(self, hex_val):
        hex_val = hex_val.lstrip("#")
        return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

    def _draw_gradient(self, event=None):
        self.delete("grad")
        w = self.winfo_width()
        h = self.winfo_height()
        
        steps = 100 
        r1, g1, b1 = self._hex_to_rgb(self.c1)
        r2, g2, b2 = self._hex_to_rgb(self.c2)
        
        dr = (r2 - r1) / steps
        dg = (g2 - g1) / steps
        db = (b2 - b1) / steps
        
        for i in range(steps):
            r = int(r1 + (dr * i))
            g = int(g1 + (dg * i))
            b = int(b1 + (db * i))
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            y0 = int(i * (h / steps))
            y1 = int((i + 1) * (h / steps)) + 1
            self.create_rectangle(0, y0, w, y1, fill=color, outline="", tags="grad")
        
        self.tag_lower("grad")

# =============================================================================
# 🎮 GAME-STYLE LOADING SCREEN (From New UI)
# =============================================================================
# class GameLoader:
#     def __init__(self, root, on_complete_callback):
#         self.root = root
#         self.on_complete = on_complete_callback
#         self.width = 1200
#         self.height = 800
        
#         self.bg_color = ThemeManager.get("bg_primary")
#         self.accent_color = ThemeManager.get("accent")
#         self.text_color = ThemeManager.get("text_main")
        
#         self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=self.bg_color, highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)
        
#         self.progress = 0
#         self.loading_text_items = [
#             "Connecting to Social APIs...",
#             "Fetching Engagement Metrics...",
#             "Training ML Sentiment Models...",
#             "Optimizing Visualization Matrix...",
#             "Finalizing Dashboard...",
#             "Launching Analytics Engine..."
#         ]
#         self.pulse_size = 0
#         self.pulse_growing = True
        
#         self.draw_logo(self.width/2, self.height/2 - 50)
#         self.draw_progress_bar_bg(self.width/2, self.height/2 + 80)
        
#         self.update_animation()

#     def draw_logo(self, x, y):
#         self.pulse_id = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill=ThemeManager.get("border"), outline="")
#         self.canvas.create_text(x, y, text="🚀", font=("Segoe UI Emoji", 50), fill=self.accent_color)
#         self.canvas.create_text(x, y+60, text="Social Engagement Analysis", font=("Segoe UI", 26, "bold"), fill=self.text_color)

#     def draw_progress_bar_bg(self, x, y):
#         w = 400
#         h = 12
#         self.canvas.create_rectangle(x - w/2, y, x + w/2, y + h, fill=ThemeManager.get("border"), outline="", tags="prog_bg")
#         self.text_id = self.canvas.create_text(x, y + 30, text="Starting...", font=("Segoe UI", 11), fill=ThemeManager.get("text_muted"))
#         self.bar_id = self.canvas.create_rectangle(x - w/2, y, x - w/2, y + h, fill=self.accent_color, outline="")

#     def update_animation(self):
#         self.progress += 2.0 
#         bar_width = 400
#         current_w = bar_width * (self.progress / 100)
#         center_x = self.width / 2
#         bar_y = self.height / 2 + 80
        
#         self.canvas.coords(self.bar_id, center_x - 200, bar_y, (center_x - 200) + current_w, bar_y + 12)
        
#         if self.pulse_growing:
#             self.pulse_size += 0.5
#             if self.pulse_size > 15: self.pulse_growing = False
#         else:
#             self.pulse_size -= 0.5
#             if self.pulse_size < 0: self.pulse_growing = True
            
#         base_r = 60
#         r = base_r + self.pulse_size
#         logo_y = self.height/2 - 50
#         self.canvas.coords(self.pulse_id, center_x - r, logo_y - r, center_x + r, logo_y + r)
        
#         idx = int((self.progress / 100) * len(self.loading_text_items))
#         if idx < len(self.loading_text_items):
#             self.canvas.itemconfig(self.text_id, text=self.loading_text_items[idx])

#         if self.progress < 100:
#             self.root.after(20, self.update_animation)
#         else:
#             self.canvas.destroy()
#             self.on_complete()

# =============================================================================
# 🎮 GAME-STYLE LOADING SCREEN (Fixed)
# =============================================================================
class GameLoader:
    def __init__(self, root, on_complete_callback):
        self.root = root
        self.on_complete = on_complete_callback
        self.width = 1200
        self.height = 800
        
        self.bg_color = ThemeManager.get("bg_primary")
        self.accent_color = ThemeManager.get("accent")
        self.text_color = ThemeManager.get("text_main")
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.progress = 0
        self.loading_text_items = [
            "Connecting to Social APIs...",
            "Fetching Engagement Metrics...",
            "Training ML Sentiment Models...",
            "Optimizing Visualization Matrix...",
            "Finalizing Dashboard...",
            "Launching Analytics Engine..."
        ]
        self.pulse_size = 0
        self.pulse_growing = True
        
        self.draw_logo(self.width/2, self.height/2 - 50)
        self.draw_progress_bar_bg(self.width/2, self.height/2 + 80)
        
        self.update_animation()

    def draw_logo(self, x, y):
        self.pulse_id = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill=ThemeManager.get("border"), outline="")
        self.canvas.create_text(x, y, text="🚀", font=("Segoe UI Emoji", 50), fill=self.accent_color)
        self.canvas.create_text(x, y+60, text="Social Engagement Analysis", font=("Segoe UI", 26, "bold"), fill=self.text_color)

    def draw_progress_bar_bg(self, x, y):
        w = 400
        h = 12
        self.canvas.create_rectangle(x - w/2, y, x + w/2, y + h, fill=ThemeManager.get("border"), outline="", tags="prog_bg")
        self.text_id = self.canvas.create_text(x, y + 30, text="Starting...", font=("Segoe UI", 11), fill=ThemeManager.get("text_muted"))
        self.bar_id = self.canvas.create_rectangle(x - w/2, y, x - w/2, y + h, fill=self.accent_color, outline="")

    def update_animation(self):
        # --- FIX START: Check if window still exists before updating ---
        try:
            if not self.canvas.winfo_exists():
                return
        except:
            return
        # --- FIX END ---

        self.progress += 2.0 
        bar_width = 400
        current_w = bar_width * (self.progress / 100)
        center_x = self.width / 2
        bar_y = self.height / 2 + 80
        
        self.canvas.coords(self.bar_id, center_x - 200, bar_y, (center_x - 200) + current_w, bar_y + 12)
        
        if self.pulse_growing:
            self.pulse_size += 0.5
            if self.pulse_size > 15: self.pulse_growing = False
        else:
            self.pulse_size -= 0.5
            if self.pulse_size < 0: self.pulse_growing = True
            
        base_r = 60
        r = base_r + self.pulse_size
        logo_y = self.height/2 - 50
        self.canvas.coords(self.pulse_id, center_x - r, logo_y - r, center_x + r, logo_y + r)
        
        idx = int((self.progress / 100) * len(self.loading_text_items))
        if idx < len(self.loading_text_items):
            self.canvas.itemconfig(self.text_id, text=self.loading_text_items[idx])

        if self.progress < 100:
            self.root.after(20, self.update_animation)
        else:
            self.canvas.destroy()
            self.on_complete()

# =============================================================================
# 🧩 UI COMPONENTS (From New UI)
# =============================================================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, width=140, height=45, corner_radius=20, 
                 command=None, bg_color=None, fg_color=None, hover_color=None):
        super().__init__(parent, borderwidth=0, relief="flat", highlightthickness=0)
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.radius = corner_radius
        self.parent_bg = bg_color if bg_color else ThemeManager.get("bg_header")
        
        self.normal_color = fg_color if fg_color else ThemeManager.get("accent")
        self.hover_color = hover_color if hover_color else ThemeManager.get("accent_hover")
        self.text_color = "#FFFFFF"

        self.configure(width=width, height=height, bg=self.parent_bg)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.draw()

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def draw(self):
        self.delete("all")
        self.rect_id = self.round_rectangle(2, 2, self.width-2, self.height-2, 
                                           radius=self.radius, fill=self.normal_color)
        font_size = 11
        self.create_text(self.width/2, self.height/2, text=self.text, 
                         fill=self.text_color, font=("Segoe UI", font_size, "bold"))

    def on_enter(self, e):
        self.itemconfig(self.rect_id, fill=self.hover_color)
        self.configure(cursor="hand2")

    def on_leave(self, e):
        self.itemconfig(self.rect_id, fill=self.normal_color)
        self.configure(cursor="")

    def on_click(self, e):
        if self.command: self.command()

class HamburgerButton(tk.Canvas):
    def __init__(self, parent, command, bg_color):
        super().__init__(parent, width=40, height=40, bg=bg_color, highlightthickness=0)
        self.command = command
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", lambda e: self.configure(cursor="hand2"))
        self.draw()

    def draw(self):
        self.delete("all")
        fill_color = ThemeManager.get("text_main")
        self.create_line(8, 12, 32, 12, width=3, fill=fill_color, capstyle="round")
        self.create_line(8, 20, 32, 20, width=3, fill=fill_color, capstyle="round")
        self.create_line(8, 28, 32, 28, width=3, fill=fill_color, capstyle="round")

class ModernCard(tk.Canvas):
    def __init__(self, parent, width=220, height=150, title="", value="", icon="", trend="", bg_override=None):
        super().__init__(parent, width=width, height=height, borderwidth=0, highlightthickness=0)
        self.title_txt = title
        self.value_txt = value
        self.icon_txt = icon
        self.trend_txt = trend
        self.bg_color = bg_override if bg_override else ThemeManager.get("gradient_start") 
        self.draw()

    def draw(self):
        self.delete("all")
        self.configure(bg=self.bg_color)
        
        w, h = int(self.cget("width")), int(self.cget("height"))
        card_bg = ThemeManager.get("card_bg")
        text_main = ThemeManager.get("text_main")
        text_muted = ThemeManager.get("text_muted")
        accent = ThemeManager.get("accent")
        border = ThemeManager.get("border")
        
        self.create_polygon([13,3, w-7,3, w+3,3, w+3,13, w+3,h-7, w+3,h+3, w-7,h+3, 13,h+3, 3,h+3, 3,h-7, 3,13, 3,3],
                             smooth=True, fill=ThemeManager.get("shadow"), stipple="gray25")

        self.create_polygon([10,0, w-10,0, w,0, w,10, w,h-10, w,h, w-10,h, 10,h, 0,h, 0,h-10, 0,10, 0,0],
                            smooth=True, fill=card_bg, outline=border)
        
        self.create_oval(20, 20, 65, 65, fill=accent, outline="")
        self.create_text(42, 42, text=self.icon_txt, font=("Segoe UI Emoji", 18), fill="#FFFFFF")
        
        self.create_text(20, 90, text=self.title_txt, anchor="w", font=("Segoe UI", 10, "bold"), fill=text_muted)
        self.create_text(20, 120, text=self.value_txt, anchor="w", font=("Segoe UI", 22, "bold"), fill=text_main)
        
        if self.trend_txt:
            col = ThemeManager.get("success") if "+" in self.trend_txt else ThemeManager.get("danger")
            self.create_text(w-20, 35, text=self.trend_txt, anchor="e", font=("Segoe UI", 11, "bold"), fill=col)

class SidebarButton(tk.Frame):
    def __init__(self, parent, text, icon, command, is_active=False):
        colors = ThemeManager.get
        super().__init__(parent, bg=colors("bg_secondary"), cursor="hand2")
        self.command = command
        self.pack(fill="x", pady=6, padx=15)
        
        bg_color = colors("bg_primary") if is_active else colors("bg_secondary")
        fg_color = colors("accent") if is_active else colors("text_muted")
        
        if is_active:
             self.config(bg=colors("card_bg"), highlightbackground=colors("accent"), highlightthickness=0)
        
        self.icon_lbl = tk.Label(self, text=icon, bg=self.cget("bg"), fg=fg_color, font=("Segoe UI Emoji", 14))
        self.icon_lbl.pack(side="left", padx=(15, 12), pady=12)
        
        self.text_lbl = tk.Label(self, text=text, bg=self.cget("bg"), fg=fg_color, font=("Segoe UI", 12, "bold"), anchor="w")
        self.text_lbl.pack(side="left", fill="x", expand=True)
        
        for w in (self, self.icon_lbl, self.text_lbl):
            w.bind("<Button-1>", lambda e: command())
            w.bind("<Enter>", self.on_enter)
            w.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.icon_lbl.config(fg=ThemeManager.get("accent"))
        self.text_lbl.config(fg=ThemeManager.get("accent"))

    def on_leave(self, e):
        self.icon_lbl.config(fg=ThemeManager.get("text_muted"))
        self.text_lbl.config(fg=ThemeManager.get("text_muted"))

# =============================================================================
# 📱 GLOBAL VARIABLES (From Old Project)
# =============================================================================
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                    PASTE YOUR GLOBAL VARIABLES HERE                      ║
# ║                    (original_df, cleaned_df, etc.)                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

original_df = None
cleaned_df = None
regression_model = None
classification_model = None
regression_trained = False
regression_insights_shown = False
eda_completed = False
prediction_df = None

import json
import os
from datetime import datetime

# =============================================================================
# 🔐 USER MANAGEMENT & LOGIN SYSTEM
# =============================================================================
class UserManager:
    FILE_NAME = "user_data.json"

    @staticmethod
    def load_users():
        if not os.path.exists(UserManager.FILE_NAME):
            return {}
        try:
            with open(UserManager.FILE_NAME, "r") as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def save_user(username, phone):
        users = UserManager.load_users()
        key = f"{username}_{phone}"
        
        if key in users:
            # User exists, return existing data (Restore History)
            users[key]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Ensure stats exist
            if "stats" not in users[key]:
                users[key]["stats"] = {"uploads": 0, "models_trained": 0, "insights_generated": 0}
        else:
            # Register new user
            users[key] = {
                "username": username,
                "phone": phone,
                "joined": datetime.now().strftime("%Y-%m-%d"),
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "stats": {"uploads": 0, "models_trained": 0, "insights_generated": 0}
            }
        
        with open(UserManager.FILE_NAME, "w") as f:
            json.dump(users, f, indent=4)
        
        return users[key]

    @staticmethod
    def update_stat(username, phone, stat_key):
        """Call this function when user uploads data or trains model to save history"""
        users = UserManager.load_users()
        key = f"{username}_{phone}"
        if key in users:
            if "stats" not in users[key]: users[key]["stats"] = {}
            users[key]["stats"][stat_key] = users[key]["stats"].get(stat_key, 0) + 1
            with open(UserManager.FILE_NAME, "w") as f:
                json.dump(users, f, indent=4)

# =============================================================================
# 🔐 UPDATED LOGIN SCREEN (Fixes Crash)
# =============================================================================
class LoginScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        
        # Configure Theme
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # 1. Main Background
        self.frame = ctk.CTkFrame(root, fg_color="#f0f2f5", corner_radius=0)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 2. Center Card
        self.card = ctk.CTkFrame(
            self.frame, 
            width=400, 
            height=500, 
            corner_radius=20, 
            fg_color="white",
            border_width=1,
            border_color="#e0e0e0"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False) 
        
        # 3. UI Elements
        ctk.CTkLabel(self.card, text="👤", font=("Segoe UI Emoji", 48)).pack(pady=(50, 10))
        ctk.CTkLabel(self.card, text="Welcome", font=("Segoe UI", 26, "bold"), text_color="#1a1a1a").pack(pady=(0, 5))
        ctk.CTkLabel(self.card, text="Sign in to your dashboard", font=("Segoe UI", 12), text_color="#757575").pack(pady=(0, 30))
        
        self.user_entry = ctk.CTkEntry(self.card, width=320, height=50, corner_radius=12, placeholder_text="Username", font=("Segoe UI", 14), border_color="#e0e0e0", fg_color="#f9f9f9", text_color="#333333")
        self.user_entry.pack(pady=(0, 15))
        
        self.phone_entry = ctk.CTkEntry(self.card, width=320, height=50, corner_radius=12, placeholder_text="Phone Number", font=("Segoe UI", 14), border_color="#e0e0e0", fg_color="#f9f9f9", text_color="#333333")
        self.phone_entry.pack(pady=(0, 25))
        
        self.login_btn = ctk.CTkButton(self.card, text="Login / Register", width=320, height=50, corner_radius=12, font=("Segoe UI", 15, "bold"), fg_color="#8e44ad", hover_color="#732d91", command=self.do_login)
        self.login_btn.pack(pady=(0, 20))
        
        self.err_lbl = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 12), text_color="#e74c3c")
        self.err_lbl.pack()

    def do_login(self):
        u = self.user_entry.get().strip()
        p = self.phone_entry.get().strip()
        
        if not u or not p:
            self.err_lbl.configure(text="⚠️ Please fill in all fields")
            self.user_entry.configure(border_color="#e74c3c")
            self.phone_entry.configure(border_color="#e74c3c")
            return
            
        self.user_entry.configure(border_color="#e0e0e0")
        self.phone_entry.configure(border_color="#e0e0e0")

        # Save User Data
        user_data = UserManager.save_user(u, p)
        
        # --- FIX: REMOVED self.frame.destroy() ---
        # We let the Main App clean up the screen to prevent errors.
        self.on_success(user_data)

# =============================================================================
# 🔧 HELPER FUNCTIONS (From Old Project)
# =============================================================================
def count_hashtags(hashtag_str):
    if pd.isna(hashtag_str) or not str(hashtag_str).strip():
        return 0
    tags = str(hashtag_str).replace('#', ' ').split()
    return len([t for t in tags if t.strip()])

def get_best_hour(df, platform=None, content_type=None):
    if df is None or 'Hour' not in df.columns or 'Reach' not in df.columns:
        return "12:00"
    temp = df.copy()
    if platform and platform != "All Platforms":
        temp = temp[temp['Platform'] == platform]
    if content_type and content_type != "All Content":
        temp = temp[temp['Content_Type'] == content_type]
    if temp.empty and platform and platform != "All Platforms":
        temp = df[df['Platform'] == platform]
    if temp.empty:
        temp = df
    if not temp.empty:
        hourly_perf = temp.groupby('Hour')['Reach'].mean()
        if not hourly_perf.empty:
            best_hr = hourly_perf.idxmax()
            return f"{int(best_hr)}:00"
    return "12:00"

def get_dynamic_insights(class_name, target_col="Platform"):
    if cleaned_df is None:
        return ["#SocialMedia"], "2-5", "12:00", "Tue–Thu"
    if target_col == "Platform":
        filtered = cleaned_df[cleaned_df['Platform'] == class_name]
    elif target_col == "Content_Type":
        filtered = cleaned_df[cleaned_df['Content_Type'] == class_name]
    else:
        filtered = cleaned_df
    if filtered.empty:
        filtered = cleaned_df
    
    hashtags_list = ["#SocialMedia"]
    if 'Hashtags' in filtered.columns and 'Reach' in filtered.columns:
        temp_df = filtered[['Hashtags', 'Reach']].dropna(subset=['Hashtags']).copy()
        if not temp_df.empty:
            temp_df['Hashtags_clean'] = temp_df['Hashtags'].astype(str).str.replace(r'[#]', '', regex=True)
            temp_df['Hashtags_list'] = temp_df['Hashtags_clean'].str.split()
            exploded = temp_df.explode('Hashtags_list')
            exploded = exploded[exploded['Hashtags_list'].str.strip() != '']
            if not exploded.empty:
                hashtag_stats = exploded.groupby('Hashtags_list')['Reach'].mean().sort_values(ascending=False)
                top_hashtags = hashtag_stats.head(5).index.tolist()
                hashtags_list = [f"#{tag}" for tag in top_hashtags]
    
    hashtag_range = "2-5"
    if 'Hashtags' in filtered.columns:
        temp_counts = filtered['Hashtags'].dropna().astype(str)
        counts = temp_counts.str.replace(r'[#]', ' ', regex=True).str.split().str.len()
        if not counts.empty:
            q25 = int(counts.quantile(0.25))
            q75 = int(counts.quantile(0.75))
            q25 = max(1, q25)
            q75 = max(q25, q75)
            hashtag_range = f"{q25}-{q75}"
    
    best_time = "12:00"
    if 'Hour' in filtered.columns and 'Reach' in filtered.columns:
        hourly_perf = filtered.groupby('Hour')['Reach'].mean()
        if not hourly_perf.empty:
            best_hour = hourly_perf.idxmax()
            best_time = f"{int(best_hour)}:00"
    
    perfect_days = "Tue–Thu"
    if 'Day' in filtered.columns and 'Reach' in filtered.columns:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_avg = filtered.groupby('Day')['Reach'].mean()
        avg_reach = filtered['Reach'].mean()
        daily_avg = daily_avg.reindex([d for d in day_order if d in daily_avg.index])
        if not daily_avg.empty:
            top_days = daily_avg.nlargest(3)
            boosts = []
            for day in top_days.index:
                boost = ((daily_avg[day] - avg_reach) / avg_reach * 100) if avg_reach > 0 else 0
                short_day = day[:3]
                boosts.append(f"{short_day} (+{boost:.0f}%)")
            perfect_days = ", ".join(boosts)
    
    return hashtags_list, hashtag_range, best_time, perfect_days

# =============================================================================
# 🔧 RESPONSIVE UTILITY FUNCTIONS
# =============================================================================
def get_device_type(root):
    """Determine device type based on window width"""
    width = root.winfo_width()
    if width < 768:
        return "mobile"
    elif width < 1024:
        return "tablet"
    else:
        return "desktop"

def get_responsive_font(base_size, root):
    """Return font size based on device type"""
    device = get_device_type(root)
    if device == "mobile":
        return max(10, int(base_size * 0.75))
    elif device == "tablet":
        return max(12, int(base_size * 0.9))
    return base_size

# =============================================================================
# 📱 MAIN APP CONTROLLER
# =============================================================================
class SocialAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social pulse")
        try:
            # Load the logo image
            icon_image = Image.open("logo_social.png")
            
            # Convert it to a Tkinter-compatible photo
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            # Set the window icon (False means it applies to this specific window)
            self.root.iconphoto(False, icon_photo)
        except Exception as e:
            print(f"Could not load window icon: {e}")
        self.root.geometry("1200x700")
        
        
        # Trigger Loader
       
        self.loader = GameLoader(self.root, self.show_login_screen)

    def show_login_screen(self):
        """Shows login screen after loader finishes"""
        LoginScreen(self.root, self.handle_login_success)

    def handle_login_success(self, user_data):
        """Called when login is successful"""
        self.current_user_data = user_data
        self.init_main_app()

    def init_main_app(self):
        self.current_page = "Home"
        self.sidebar_visible = True 
        self.view_mode = "desktop" 
        self.hamburger_btn = None
        self.eda_completed = False
        
        self.build_ui()
        self.root.bind('<Configure>', self.on_resize)

    def build_ui(self):
        # 1. Destroy existing widgets (This safely removes the Login Screen)
        for widget in self.root.winfo_children():
            widget.destroy()

        # 2. Reset critical UI references
        self.dashboard_scrollbar = None
        self.page_title_canvas = None

        colors = ThemeManager.get
        
        # --- CRITICAL FIX FOR YOUR ERROR ---
        # Safely attempts to set the background color
        try:
            # Try standard Tkinter background
            self.root.configure(bg=colors("bg_primary"))
        except:
            try:
                # If that fails (because it's a CTk window), try CustomTkinter param
                self.root.configure(fg_color=colors("bg_primary"))
            except:
                pass # If both fail, ignore it (prevents crash)
        # ------------------------------------

        # Main Containers
        self.main_container = tk.Frame(self.root, bg=colors("bg_primary"))
        
        # Header
        self.header = tk.Frame(self.main_container, bg=colors("bg_header"), height=80)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)
        
        tk.Frame(self.header, bg=colors("border"), height=1).pack(side="bottom", fill="x")

        # Content - Using GRADIENT FRAME
        self.content_area = GradientFrame(self.main_container, colors("gradient_start"), colors("gradient_end"))
        self.content_area.pack(fill="both", expand=True, side="top")
        
        # Sidebar
        self.sidebar_frame = tk.Frame(self.root, bg=colors("bg_secondary"), width=300)
        
        self.render_header_elements()
        self.rebuild_sidebar_content()
        self.render_layout()

    def on_resize(self, event):
        if event.widget != self.root: return
        width = event.width
        new_mode = "desktop"
        if width < 850: new_mode = "mobile"
        elif width < 1150: new_mode = "tablet"
            
        if new_mode != self.view_mode:
            self.view_mode = new_mode
            self.render_layout()
            self.root.update_idletasks()
            if hasattr(self, 'page_title_canvas'):
                 self.draw_gradient_title(self.page_title_canvas, 10, 30, "Social Media Engagement Analysis")
            
        elif self.view_mode != "desktop":
            # BUG FIX: Removed self.render_dashboard_content()
            # This prevents the app from resetting to Home whenever you navigate in mobile view
            if hasattr(self, 'page_title_canvas'):
                 self.draw_gradient_title(self.page_title_canvas, 10, 30, "Social Media Engagement Analysis")

    def mount_fullscreen_on_contentarea(self, frame):
        win_id = self.contentarea.create_window(0, 0, window=frame, anchor="nw")

        def _resize_to_canvas(event=None):
            cw = self.contentarea.winfo_width()
            ch = self.contentarea.winfo_height()
            self.contentarea.itemconfigure(win_id, width=cw, height=ch)
            self.contentarea.configure(scrollregion=self.contentarea.bbox("all"))

        self.contentarea.bind("<Configure>", _resize_to_canvas)
        self.root.after(0, _resize_to_canvas)
        return win_id


    def render_layout(self):
        self.sidebar_frame.place_forget()
        self.sidebar_frame.pack_forget()
        self.main_container.place_forget()
        self.main_container.pack_forget()
        
        if hasattr(self, 'hamburger_btn') and self.hamburger_btn:
            self.hamburger_btn.destroy()

        if self.view_mode == "desktop":
            self.sidebar_frame.pack(side="left", fill="y")
            self.main_container.pack(side="right", fill="both", expand=True)
            self.sidebar_visible = True
            self.rebuild_sidebar_content()
            
        else:
            self.main_container.place(x=0, y=0, relwidth=1, relheight=1)
            
            colors = ThemeManager.get
            self.hamburger_btn = HamburgerButton(self.header, self.toggle_sidebar, colors("bg_header"))
            self.hamburger_btn.place(x=20, y=20)
            
            self.sidebar_visible = False
            self.rebuild_sidebar_content()

        self.render_dashboard_content()
        self.update_header_padding()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.place_forget()
            self.sidebar_visible = False
        else:
            self.sidebar_frame.configure(width=300)
            self.sidebar_frame.place(x=0, y=0, relheight=1)
            self.sidebar_frame.lift()
            self.sidebar_visible = True

    def rebuild_sidebar_content(self):
        # 1. Clear existing sidebar items
        for w in self.sidebar_frame.winfo_children(): w.destroy()
        colors = ThemeManager.get
        
        # 2. Sidebar Header
        header_frame = tk.Frame(self.sidebar_frame, bg=colors("bg_secondary"), height=90)
        header_frame.pack(fill="x", pady=(25, 30), padx=20)

        # --- LOGO REPLACEMENT START ---
        try:
            # Load the image
            logo_img = Image.open("logo_social.png")
            
            # Resize it to fit nicely (40x40 pixels)
            logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
            
            # Create a persistent reference to prevent garbage collection
            self.sidebar_logo_icon = ImageTk.PhotoImage(logo_img)
            
            # Display the Logo
            tk.Label(header_frame, image=self.sidebar_logo_icon, bg=colors("bg_secondary")).pack(side="left", padx=(0, 10))
            
        except Exception as e:
            # Fallback: If image is missing, show the emoji so the app doesn't crash
            print(f"Could not load logo.png: {e}")
            tk.Label(header_frame, text="⚡", font=("Segoe UI Emoji", 24), 
                     bg=colors("bg_secondary"), fg=colors("accent")).pack(side="left")
        # --- LOGO REPLACEMENT END ---

        # tk.Label(header_frame, text="SocialPulse", font=("Segoe UI", 22, "bold"), 
        #          bg=colors("bg_secondary"), fg=colors("text_main")).pack(side="left")
        tk.Label(header_frame, text="SocialPulse", font=("Segoe UI", 22, "bold"), 
                 bg=colors("bg_secondary"), fg=colors("text_main")).pack(side="left", padx=10)

        # Close button for mobile view
        if self.view_mode != "desktop":
            close_btn = tk.Label(header_frame, text="✕", font=("Arial", 20), 
                                 bg=colors("bg_secondary"), fg=colors("text_muted"), cursor="hand2")
            close_btn.pack(side="right")
            close_btn.bind("<Button-1>", lambda e: self.toggle_sidebar())

        # 3. Navigation Logic Wrapper
        def nav_handler(page_name, command_func):
            # A. Set the current page so we know what to highlight
            self.current_page = page_name
            
            # B. Execute the actual page function (e.g., show_home)
            command_func()
            
            # C. MOBILE FIX: Close the sidebar if we are not on desktop
            if self.view_mode != "desktop":
                self.toggle_sidebar()
            
            # D. COLOR FIX: Re-render sidebar to apply the "active" color to the clicked button
            self.rebuild_sidebar_content()

        # Navigation Items
        navs = [
            ("Home", "🏠", self.show_home), 
            ("Dataset", "📁", self.show_dataset), 
            ("Preprocessing", "🔨", self.show_preprocessing), 
            ("Processing", "⚙️", self.show_processing), 
            ("ML Models", "🧠", self.show_train_ml), 
            ("Visualization", "📊", self.show_visualization)
        ]
        
        # 4. Create Buttons
        for name, icon, cmd in navs:
            # Check if this button matches the current page
            is_active = (name == getattr(self, 'current_page', "Home"))
            
            # Create the button with the wrapper handler
            SidebarButton(self.sidebar_frame, name, icon, 
                         command=lambda n=name, c=cmd: nav_handler(n, c), 
                         is_active=is_active)

        # 5. Footer Area
        footer = tk.Frame(self.sidebar_frame, bg=colors("bg_secondary"))
        footer.pack(side="bottom", fill="x", pady=20, padx=20)
        
        t_btn = RoundedButton(footer, text="Switch Theme 🎨", width=250, height=40, corner_radius=15, 
                              bg_color=colors("bg_secondary"), 
                              fg_color=colors("bg_primary"),
                              hover_color=colors("border"), 
                              command=self.toggle_theme)
        t_btn.text_color = colors("text_main")
        t_btn.draw()
        t_btn.pack(side="top", pady=(0, 15))

        tk.Label(footer, text="Logged in as Admin", font=("Segoe UI", 10), 
                 bg=colors("bg_secondary"), fg=colors("text_muted")).pack(side="top")
        

    def render_dashboard_content(self):

        # 1. Clear Screen & Reset Scroll
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        self.content_area.yview_moveto(0)
        self.content_area.xview_moveto(0)
        
        colors = ThemeManager.get

        # 2. Main Scrollable Container
        main_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))
        window_id = self.content_area.create_window(0, 0, window=main_frame, anchor="nw")

        # ==========================================================
        # 🔧 CRITICAL FIX FOR DARK MODE / THEME SWITCHING
        # ==========================================================
        self.root.update_idletasks()
        
        # Get width of the canvas
        current_w = self.content_area.winfo_width()
        
        # If canvas isn't drawn yet (width=1), fall back to the Window width
        if current_w <= 1:
            current_w = self.root.winfo_width()
            
        # Apply width (Safe check to ensure we don't pass negative numbers)
        target_w = max(1, current_w - 20)
        self.content_area.itemconfig(window_id, width=target_w)

        # ==========================================================
        # DATA PROCESSING
        # ==========================================================
        global cleaned_df
        has_data = cleaned_df is not None
        
        fmt_reach, fmt_eng = "0", "0.00%"
        spotlight_title = "No Data Available"
        spotlight_content = "Upload a dataset to start"
        spotlight_val, spotlight_sub = "0%", "Waiting for data..."
        
        if has_data:
            try:
                total_reach = cleaned_df['Reach'].sum()
                avg_eng = cleaned_df['Engagement_Rate'].mean()
                if total_reach > 1_000_000: fmt_reach = f"{total_reach/1_000_000:.1f}M"
                elif total_reach > 1_000: fmt_reach = f"{total_reach/1_000:.1f}K"
                else: fmt_reach = str(total_reach)
                fmt_eng = f"{avg_eng:.2f}%"
                
                best_idx = cleaned_df['Engagement_Rate'].idxmax()
                best_post = cleaned_df.loc[best_idx]
                spotlight_title = f"Top {best_post.get('Platform', 'Post')} Post"
                spotlight_content = str(best_post.get('Content_Type', 'Unknown'))
                spotlight_val = f"{best_post.get('Engagement_Rate', 0):.2f}%"
                spotlight_sub = f"Reached {int(best_post.get('Reach', 0)):,} users"
            except: pass

        # ==========================================================
        # UI COMPONENTS
        # ==========================================================

        # --- A. HEADER SECTION ---
        header_frame = tk.Frame(main_frame, bg=colors("bg_header"), pady=30, padx=30)
        header_frame.pack(fill="x")

        canvas_av = tk.Canvas(header_frame, width=100, height=100, bg=colors("bg_header"), highlightthickness=0)
        canvas_av.create_oval(5, 5, 95, 95, fill=colors("accent"), outline="")
        initial = self.current_user_data['username'][0].upper() if hasattr(self, 'current_user_data') and self.current_user_data else "U"
        canvas_av.create_text(50, 50, text=initial, font=("Segoe UI", 40, "bold"), fill="white")
        
        txt_frame = tk.Frame(header_frame, bg=colors("bg_header"))
        u_name = self.current_user_data.get('username', 'User') if hasattr(self, 'current_user_data') and self.current_user_data else "User"
        
        # --- FIX: ROBUST DATETIME HANDLING ---
        import datetime as dt_module
        current_date = dt_module.datetime.now().strftime("%A, %d %B %Y")
        
        lbl_welcome = tk.Label(txt_frame, text=f"Welcome back, {u_name}!", font=("Segoe UI", 24, "bold"), bg=colors("bg_header"), fg=colors("text_main"))
        lbl_date = tk.Label(txt_frame, text=f"{current_date} | Dashboard Overview", font=("Segoe UI", 12), bg=colors("bg_header"), fg=colors("text_muted"))
        
        lbl_welcome.pack(anchor="w")
        lbl_date.pack(anchor="w")

        # --- B. KPI CARDS ---
        kpi_container = tk.Frame(main_frame, bg=colors("gradient_start"), pady=20, padx=20)
        kpi_container.pack(fill="x")

        def create_kpi(parent, title, value, icon, col):
            card = tk.Frame(parent, bg=colors("card_bg"), padx=20, pady=20)
            tk.Frame(card, bg=col, height=4).pack(fill="x", pady=(0, 15))
            tk.Label(card, text=icon, font=("Segoe UI Emoji", 20), bg=colors("card_bg")).pack(anchor="w")
            tk.Label(card, text=value, font=("Segoe UI", 28, "bold"), bg=colors("card_bg"), fg=colors("text_main")).pack(anchor="w", pady=5)
            tk.Label(card, text=title, font=("Segoe UI", 11), bg=colors("card_bg"), fg=colors("text_muted")).pack(anchor="w")
            return card

        kpi_cards = [
            create_kpi(kpi_container, "Total Reach", fmt_reach, "👥", "#6366F1"),
            create_kpi(kpi_container, "Avg Engagement", fmt_eng, "⚡", "#F59E0B"),
            create_kpi(kpi_container, "Analysis Status", "Active" if has_data else "Idle", "🟢" if has_data else "⚪", "#10B981")
        ]

        # --- C. SPLIT SECTION (Spotlight & Feed) ---
        split_container = tk.Frame(main_frame, bg=colors("gradient_start"), padx=20, pady=10)
        split_container.pack(fill="both", expand=True)

        # Spotlight
        spotlight_frame = tk.Frame(split_container, bg=colors("card_bg"), padx=25, pady=25)
        tk.Label(spotlight_frame, text="🏆 HIGHEST PERFORMING POST", font=("Segoe UI", 10, "bold"), bg=colors("card_bg"), fg=colors("text_muted")).pack(anchor="w", pady=(0, 10))
        tk.Label(spotlight_frame, text=spotlight_title, font=("Segoe UI", 18, "bold"), bg=colors("card_bg"), fg=colors("text_main")).pack(anchor="w")
        tk.Label(spotlight_frame, text=spotlight_content, font=("Segoe UI", 14), bg=colors("card_bg"), fg=colors("accent")).pack(anchor="w", pady=(0, 15))
        tk.Frame(spotlight_frame, bg=colors("border"), height=1).pack(fill="x", pady=15)
        tk.Label(spotlight_frame, text=spotlight_val, font=("Segoe UI", 28, "bold"), bg=colors("card_bg"), fg="#10B981").pack(anchor="w")
        tk.Label(spotlight_frame, text=spotlight_sub, font=("Segoe UI", 11), bg=colors("card_bg"), fg=colors("text_muted")).pack(anchor="w")

        # Feed
        feed_frame = tk.Frame(split_container, bg=colors("card_bg"), padx=25, pady=25)
        tk.Label(feed_frame, text="Recent Data Activity", font=("Segoe UI", 12, "bold"), bg=colors("card_bg"), fg=colors("text_main")).pack(anchor="w", pady=(0, 15))

        def add_feed_item(parent, title, desc, color):
            item = tk.Frame(parent, bg=colors("card_bg"))
            item.pack(fill="x", pady=8)
            tk.Label(item, text="●", fg=color, bg=colors("card_bg"), font=("Arial", 14)).pack(side="left", padx=(0, 10))
            info = tk.Frame(item, bg=colors("card_bg"))
            info.pack(side="left", fill="x")
            tk.Label(info, text=title, font=("Segoe UI", 10, "bold"), bg=colors("card_bg"), fg=colors("text_main")).pack(anchor="w")
            tk.Label(info, text=desc, font=("Segoe UI", 9), bg=colors("card_bg"), fg=colors("text_muted")).pack(anchor="w")

        if has_data:
            try:
                recent = cleaned_df.tail(4).iloc[::-1]
                for _, row in recent.iterrows():
                    plat = row.get('Platform', 'Unknown')
                    p_col = "#E1306C" if plat == "Instagram" else "#1DA1F2" if plat == "Twitter" else "#0A66C2"
                    add_feed_item(feed_frame, f"New {plat} Post", f"Reach: {row.get('Reach',0)} | {row.get('Content_Type','')}", p_col)
            except: add_feed_item(feed_frame, "Data Error", "Could not parse recent rows", "#EF4444")
        else:
            add_feed_item(feed_frame, "System Ready", "Dashboard initialized", "#10B981")
            add_feed_item(feed_frame, "Waiting for Data", "Please upload a CSV file", "#F59E0B")
            add_feed_item(feed_frame, "Tip", "Use 'Load Dataset' button", "#6366F1")

        # --- SCROLL & RESPONSIVE LOGIC ---
        # FIX: Explicitly clean up old scrollbar to prevent "bad window path" on theme switch
        if hasattr(self, 'dashboard_scrollbar') and self.dashboard_scrollbar:
            try: self.dashboard_scrollbar.destroy()
            except: pass

        self.dashboard_scrollbar = tk.Scrollbar(self.content_area, orient="vertical", command=self.content_area.yview)
        self.content_area.configure(yscrollcommand=self.dashboard_scrollbar.set)
        self.dashboard_scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

        def _on_mousewheel(event):
            if self.content_area.winfo_exists():
                self.content_area.yview_scroll(int(-1*(event.delta/120)), "units")
        self.root.bind_all("<MouseWheel>", _on_mousewheel)

        self.last_layout_mode = None 

        def on_canvas_resize(event):
            w = event.width
            if w < 100: return
            
            target_w = w - 20 
            self.content_area.itemconfig(window_id, width=target_w)
            
            if w < 700: current_mode = "mobile"
            elif w < 1000: current_mode = "tablet"
            else: current_mode = "desktop"
            
            if current_mode != self.last_layout_mode:
                self.last_layout_mode = current_mode
                
                # Header
                if current_mode == "mobile":
                    canvas_av.pack_forget(); txt_frame.pack_forget()
                    canvas_av.pack(side="top", pady=(0,10))
                    txt_frame.pack(side="top")
                    lbl_welcome.config(justify="center"); lbl_date.config(justify="center")
                else:
                    canvas_av.pack_forget(); txt_frame.pack_forget()
                    canvas_av.pack(side="left", padx=(0, 20))
                    txt_frame.pack(side="left")
                    lbl_welcome.config(justify="left"); lbl_date.config(justify="left")

                # KPI Grid
                for c in kpi_cards: c.grid_forget()
                if current_mode == "desktop":
                    kpi_container.grid_columnconfigure((0,1,2), weight=1)
                    for i, c in enumerate(kpi_cards): c.grid(row=0, column=i, sticky="ew", padx=10)
                else:
                    kpi_container.grid_columnconfigure((0,1,2), weight=0)
                    kpi_container.grid_columnconfigure(0, weight=1)
                    for i, c in enumerate(kpi_cards): c.grid(row=i, column=0, sticky="ew", pady=10)

                # Split Section
                spotlight_frame.pack_forget()
                feed_frame.pack_forget()
                if current_mode == "desktop":
                    spotlight_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
                    feed_frame.pack(side="right", fill="both", expand=True)
                else:
                    spotlight_frame.pack(fill="x", pady=(0, 20))
                    feed_frame.pack(fill="x")

        self.content_area.bind("<Configure>", on_canvas_resize)

        def update_scroll(event):
            self.content_area.configure(scrollregion=self.content_area.bbox("all"))
        main_frame.bind("<Configure>", update_scroll)
        
        self.root.after(100, lambda: on_canvas_resize(type('obj', (object,), {'width': self.content_area.winfo_width() - 1})))


    def draw_gradient_title(self, canvas, x, y, text):
        """Draws multi-colored text that scales based on window width"""
        canvas.delete("all") 
        
        colors = ["#405DE6", "#5851DB", "#833AB4", "#C13584", "#E1306C", "#FD1D1D"] 
        
        # --- CHANGED: Get the width of the CANVAS (The Header), not the whole Root Window ---
        area_width = canvas.winfo_width()
        
        # Fallback if canvas hasn't rendered yet (e.g. on startup)
        if area_width <= 1: 
            area_width = self.root.winfo_width()
            # If desktop, subtract sidebar width to estimate correctly
            if self.view_mode == "desktop":
                area_width -= 300

        # 1. Determine safe left margin 
        min_safe_x = 10
        if self.view_mode != "desktop":
            min_safe_x = 70 
            
        # 2. Calculate max text width 
        max_text_width = area_width - min_safe_x - 30
        
        font_size = 26 
        if self.view_mode == "mobile": font_size = 20
        
        min_size = 10
        
        title_font = tkfont.Font(family="Segoe UI", size=font_size, weight="bold")
        
        # 3. Responsive Scaling Loop 
        while title_font.measure(text) > max_text_width and font_size > min_size:
            font_size -= 1
            title_font.configure(size=font_size)
            
        center_y = int(canvas.winfo_height() / 2)
        if center_y < 15: center_y = 30
        
        # --- CENTER CALCULATION ---
        # Calculate total width of the text
        total_text_width = title_font.measure(text)
        
        # Calculate Center relative to the CANVAS, not the screen
        centered_x = (area_width - total_text_width) // 2
        
        # Apply the safe margin
        current_x = max(centered_x, min_safe_x)
        
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            canvas.create_text(current_x, center_y, text=char, font=title_font, fill=color, anchor="w")
            current_x += title_font.measure(char)



    def render_header_elements(self):
        colors = ThemeManager.get
        
        title_canvas = tk.Canvas(self.header, bg=colors("bg_header"), highlightthickness=0, height=60)
        title_canvas.pack(side="left", fill="x", expand=True, padx=(0, 20), pady=10)
        
        self.page_title_canvas = title_canvas 
        self.draw_gradient_title(title_canvas, 10, 30, "Social Media Engagement Analysis")

    def update_header_padding(self):
        if hasattr(self, 'page_title_canvas'):
             self.draw_gradient_title(self.page_title_canvas, 10, 30, "Social Media Engagement Analysis")

    def toggle_theme(self):
        ThemeManager.toggle()
        self.build_ui()

    # =============================================================================
    # PAGE FUNCTIONS - These call your old project functions
    # =============================================================================
    
    def show_home(self):
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        """Navigate to home page"""
        self.render_dashboard_content()
    
    def show_dataset(self):
        """Navigate to dataset page - CENTERED"""
        global original_df
        
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        # --- LOGIC PRESERVED, ALIGNMENT CHANGED ---
        # 1. Create a frame for content
        main_frame = tk.Frame(self.content_area, bg=ThemeManager.get("gradient_start"))
        
        # 2. CENTERED WINDOW CREATION
        # We start at x=0, but the resize function below immediately centers it.
        # anchor="n" means the top-center of the frame is placed at the coordinate.
        window_id = self.content_area.create_window(self.content_area.winfo_width() // 2, 0, window=main_frame, anchor="n")
        
        # 3. Dynamic Centering Function
        def resize_dataset(event):
            self.content_area._draw_gradient(event)
            # Move the window to the exact center of the new width
            self.content_area.coords(window_id, event.width // 2, 0)
            # Optional: Limit width if you want margins, or keep full width
            self.content_area.itemconfig(window_id, width=event.width)
            
        self.content_area.bind("<Configure>", resize_dataset)
        
        # --- REST OF YOUR ORIGINAL UI LOGIC BELOW ---
        device = get_device_type(self.root)
        
        if device == "mobile":
            title_font = get_responsive_font(18, self.root); entry_width = 25
            button_width = 100; button_height = 45; padding_y = 15; padding_x = 10
        elif device == "tablet":
            title_font = get_responsive_font(20, self.root); entry_width = 40
            button_width = 120; button_height = 42; padding_y = 18; padding_x = 15
        else:  # desktop
            title_font = get_responsive_font(22, self.root); entry_width = 60
            button_width = 130; button_height = 40; padding_y = 20; padding_x = 20
        
        tk.Label(main_frame, text="📂 Dataset Upload",
                font=("Segoe UI", title_font, "bold"), 
                bg=ThemeManager.get("gradient_start"), 
                fg=ThemeManager.get("text_main")).pack(pady=padding_y)
        
        # Centered Container
        container = tk.Frame(main_frame, bg=ThemeManager.get("gradient_start"))
        container.pack(pady=padding_y, padx=padding_x, fill="x")
        
        path_var = tk.StringVar()
        
        if device == "mobile":
            entry_frame = tk.Frame(container, bg=ThemeManager.get("gradient_start"))
            entry_frame.pack(fill="x", pady=(0, 10))
            tk.Entry(entry_frame, textvariable=path_var, width=entry_width, font=("Segoe UI", 11), relief="solid", borderwidth=1).pack(fill="x", padx=5)
            
            button_frame = tk.Frame(container, bg=ThemeManager.get("gradient_start"))
            button_frame.pack(fill="x")
            RoundedButton(button_frame, text="Browse File", width=button_width, height=button_height,
                          bg_color=ThemeManager.get("gradient_start"),
                          command=lambda: self.browse_dataset(path_var)).pack(pady=5)
        else:
            # Use an inner frame to center the input row components
            row = tk.Frame(container, bg=ThemeManager.get("gradient_start"))
            row.pack(anchor="center") 
            
            tk.Entry(row, textvariable=path_var, width=entry_width, font=("Segoe UI", 12), relief="solid", borderwidth=1).pack(side="left", padx=padding_x)
            RoundedButton(row, text="Browse", width=button_width, height=button_height,
                          bg_color=ThemeManager.get("gradient_start"),
                          command=lambda: self.browse_dataset(path_var)).pack(side="left")
        
        info_text = "Select a CSV file to upload and analyze"
        if device == "mobile": info_text = "Select CSV file"
        
        tk.Label(main_frame, text=info_text, font=("Segoe UI", 11), 
                bg=ThemeManager.get("gradient_start"), fg=ThemeManager.get("text_muted"), 
                wraplength=300 if device == "mobile" else 500).pack(pady=(padding_y, 0))
        
        # Force a resize update to ensure centering happens immediately
        self.root.update_idletasks()
        resize_dataset(type('Event', (object,), {'width': self.content_area.winfo_width()}))
    
    def browse_dataset(self, path_var):
        """Handle dataset browsing and upload"""
        global original_df
        
        path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path: 
            return
        
        try:
            path_var.set(path)
            original_df = pd.read_csv(path)
            
            # --- Responsive Alert ---
            alert = Toplevel(self.root)
            alert.configure(bg=ThemeManager.get("card_bg"))
            
            # Get exact dimensions of the main app window
            self.root.update_idletasks()
            app_w = self.root.winfo_width()
            app_h = self.root.winfo_height()
            app_x = self.root.winfo_rootx()
            app_y = self.root.winfo_rooty()
            
            device_type = get_device_type(self.root)
            
            # Dynamic sizing based on app window
            if device_type == "mobile":
                alert_w = int(app_w * 0.85)
                alert_h = 280 
                pos_x = app_x + (app_w // 2) - (alert_w // 2)
                pos_y = app_y + (app_h // 2) - (alert_h // 2)
                title_f = 13
                btn_w = 100
                btn_h = 40
                wrap_len = alert_w - 20
                pad_y_container = 10
            else:
                alert_w = 420
                alert_h = 250
                pos_x = app_x + (app_w // 2) - (alert_w // 2)
                pos_y = app_y + (app_h // 2) - (alert_h // 2)
                title_f = 16
                btn_w = 130
                btn_h = 40
                wrap_len = 380
                pad_y_container = 15

            # Apply geometry
            alert.geometry(f"{alert_w}x{alert_h}+{pos_x}+{pos_y}")

            # Content
            tk.Label(alert, text="✅ CSV Uploaded Successfully", 
                     bg=ThemeManager.get("card_bg"), 
                     fg=ThemeManager.get("text_main"),
                     font=("Segoe UI", title_f, "bold"),
                     wraplength=wrap_len).pack(pady=(25, 10))
            
            info_frame = tk.Frame(alert, bg=ThemeManager.get("card_bg"))
            info_frame.pack(pady=5)
            
            tk.Label(info_frame, 
                     text=f"Rows: {len(original_df)} | Columns: {len(original_df.columns)}", 
                     bg=ThemeManager.get("card_bg"), 
                     fg=ThemeManager.get("text_main"),
                     font=("Segoe UI", title_f - 2)).pack()
            
            # Buttons Container
            button_container = tk.Frame(alert, bg=ThemeManager.get("card_bg"))
            button_container.pack(pady=pad_y_container)
            
            # Preview Button
            RoundedButton(button_container, text="Preview Data", 
                          width=btn_w, height=btn_h,
                          bg_color=ThemeManager.get("card_bg"),
                          command=lambda: [alert.destroy(), self.show_table(original_df, "Dataset Preview")]).pack(side="left", padx=5)

        except Exception as e:
            # Error Alert Logic (Responsive)
            error_alert = Toplevel(self.root)
            error_alert.configure(bg=ThemeManager.get("card_bg"))
            
            # Get dimensions again for error box
            self.root.update_idletasks()
            app_w = self.root.winfo_width()
            app_h = self.root.winfo_height()
            app_x = self.root.winfo_rootx()
            app_y = self.root.winfo_rooty()
            
            device_type = get_device_type(self.root)
            
            if device_type == "mobile":
                err_w = int(app_w * 0.85)
                err_h = 220
                pos_x = app_x + (app_w // 2) - (err_w // 2)
                pos_y = app_y + (app_h // 2) - (err_h // 2)
                error_font = 12
                wrap_len = err_w - 20
            else:
                err_w = 400
                err_h = 250
                pos_x = app_x + (app_w // 2) - (err_w // 2)
                pos_y = app_y + (app_h // 2) - (err_h // 2)
                error_font = 14
                wrap_len = 380
            
            error_alert.geometry(f"{err_w}x{err_h}+{pos_x}+{pos_y}")
            
            tk.Label(error_alert, text=f"❌ Error Loading File\n\n{str(e)}", 
                     bg=ThemeManager.get("card_bg"), 
                     fg=ThemeManager.get("danger"),
                     font=("Segoe UI", error_font),
                     wraplength=wrap_len).pack(pady=20)
            
            RoundedButton(error_alert, text="OK", 
                          width=100, height=40,
                          bg_color=ThemeManager.get("card_bg"),
                          command=error_alert.destroy).pack(pady=10)

    def show_preprocessing(self):
        """Navigate to preprocessing page - CENTERED"""
        global original_df, cleaned_df
        
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        colors = ThemeManager.get
        
        # --- LOGIC PRESERVED, ALIGNMENT CHANGED ---
        main_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))
        # Center the window using anchor="n" and width // 2
        window_id = self.content_area.create_window(self.content_area.winfo_width() // 2, 0, window=main_frame, anchor="n")

        def resize_pre(event):
            self.content_area._draw_gradient(event)
            self.content_area.coords(window_id, event.width // 2, 0)
            self.content_area.itemconfig(window_id, width=event.width)

        self.content_area.bind("<Configure>", resize_pre)

        # --- ORIGINAL UI CONTENT ---
        title_size = get_responsive_font(24, self.root)
        
        tk.Label(main_frame, text="🧹 Data Preprocessing",
                font=("Segoe UI", title_size, "bold"), 
                bg=colors("gradient_start"), fg=colors("text_main")).pack(pady=(40, 10))

        tk.Label(main_frame, text="Handling missing values and optimizing data types.",
                font=("Segoe UI", get_responsive_font(12, self.root)), 
                bg=colors("gradient_start"), fg=colors("text_muted")).pack(pady=(0, 30))

        def run_cleaning():
            global cleaned_df, original_df
            if original_df is None:
                err_alert = Toplevel(self.root)
                err_alert.geometry("350x150")
                err_alert.configure(bg=colors("card_bg"))
                tk.Label(err_alert, text="❌ No Dataset Found!\nPlease upload a CSV first.", 
                         bg=colors("card_bg"), fg=colors("danger"), font=("Segoe UI", 11), pady=20).pack()
                return

            try:
                # --- ENHANCED CLEANING LOGIC ---
                df = original_df.copy()
                
                # 1. Remove exact duplicate rows
                df.drop_duplicates(inplace=True)
                
                for c in df.columns:
                    # 2. Clean categorical strings (strip whitespace)
                    if df[c].dtype == "object":
                        df[c] = df[c].astype(str).str.strip()
                    
                    # 3. Handle Missing Values
                    if df[c].isnull().any():
                        if df[c].dtype in ["int64", "float64"]:
                            # Fill numeric with Median
                            df[c] = df[c].fillna(df[c].median())
                        else:
                            # Robust Mode Imputation (check if mode exists to avoid IndexError)
                            col_mode = df[c].mode()
                            if not col_mode.empty:
                                df[c] = df[c].fillna(col_mode[0])
                            else:
                                # Fallback if column is entirely empty
                                df[c] = df[c].fillna("Unknown")
                
                cleaned_df = df
                # -------------------------------

            except Exception as e:
                print(f"Error: {e}")
                return

            alert = Toplevel(self.root)
            alert.configure(bg=colors("card_bg"))
            alert.geometry("420x240")
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 210
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 120
            alert.geometry(f"+{x}+{y}")
            
            tk.Label(alert, text="✨ Data Cleaning Completed", bg=colors("card_bg"), fg=colors("success"),
                    font=("Segoe UI", 16, "bold")).pack(pady=(30, 20))
            
            RoundedButton(alert, text="View Cleaned Data", width=200, height=45,
                          bg_color=colors("card_bg"),
                          command=lambda: [alert.destroy(), self.show_table(cleaned_df, "Cleaned Data Preview")]).pack()

        RoundedButton(main_frame, text="Start Auto-Cleaning", width=220, height=50,
                      bg_color=colors("gradient_start"), fg_color=colors("accent"),
                      command=run_cleaning).pack(pady=20)
        
        hint_frame = tk.Frame(main_frame, bg=colors("card_bg"), highlightbackground=colors("border"), highlightthickness=1)
        hint_frame.pack(pady=40, padx=20)

        self.root.update_idletasks()
        resize_pre(type('Event', (object,), {'width': self.content_area.winfo_width()}))


    def show_processing(self):
        """Navigate to Processing/EDA page (Logic Preserved)"""
        global cleaned_df
        
        # 1. Clear Screen & Setup Environment
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        # Map Theme Colors to your constants
        colors = ThemeManager.get
        PRIMARY_BG = colors("gradient_start")
        CARD_BG = colors("card_bg")
        TEXT = colors("text_main")
        ACCENT = colors("accent")
        MUTED = colors("text_muted")
        indigo_color = colors("Indigo_colour1")
        mean_col=colors("mean_col1")
        eda_txt=colors("eda_txt1")
        eda_bg = colors("eda_bg1")
        viral_bg=colors("viral_bg1")
        viral_txt=colors("viral_txt1")
        
        
        # Create a "content_frame" inside the canvas to mimic your original structure
        content_frame = tk.Frame(self.content_area, bg=PRIMARY_BG)

        window_id = self.content_area.create_window(
            0, 0, window=content_frame, anchor="nw"
        )

        def _resize(event=None):
            self.content_area.itemconfigure(
                window_id,
                width=self.content_area.winfo_width(),
                height=self.content_area.winfo_height()
            )

        self.content_area.bind("<Configure>", _resize)
        self.root.after(0, _resize)

        # 2. Header
        font_size = get_responsive_font(22, self.root)
        tk.Label(content_frame, text="⚙️ Data Processing (EDA)",
                 font=("Segoe UI", font_size, "bold"), bg=PRIMARY_BG, fg=TEXT).pack(pady=20)
        
        # Internal function to render charts (Your 'show_box_plots' logic)
        # --- PASTE THIS INSIDE show_processing() ---
        def show_box_plots():
            # 1. Clear previous content
            for w in content_frame.winfo_children():
                w.destroy()
            
            font_size = get_responsive_font(22, self.root)
            tk.Label(content_frame, text="📊 Engagement Rate Box Plots",
                    font=("Segoe UI", font_size, "bold"), bg=PRIMARY_BG, fg=TEXT).pack(pady=20)
            
            # 2. Scroll Setup - FIXED FOR FULL SCREEN
            scroll_container = tk.Frame(content_frame, bg=CARD_BG)
            scroll_container.pack(fill="both", expand=True, padx=10, pady=5)
            
            scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
            # Ensure canvas expands to fill the whole screen
            canvas = tk.Canvas(scroll_container, bg=CARD_BG, highlightthickness=0)
            scrollable_frame = tk.Frame(canvas, bg=CARD_BG)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=canvas.yview)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # --- FULL WIDTH FIX ---
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            canvas.bind("<Configure>", on_canvas_configure)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            # Force immediate update
            self.root.update_idletasks()
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                canvas.itemconfig(canvas_window, width=canvas_width)

            # 3. Figure Config (Responsive Scaling)
            self.root.update_idletasks() # Force geometry update
            win_w = self.root.winfo_width()
            sidebar_w = 300 if get_device_type(self.root) == "desktop" else 0
            # Calculate width in inches for Matplotlib (95% of available space)
            avail_w_inches = (win_w - sidebar_w - 50) / 100 
            if avail_w_inches < 4: avail_w_inches = 4

            fig_size = (avail_w_inches, 5)
            title_fs, label_fs, tick_fs = 14, 11, 10
            rot = 45
            

            # --- Graph 1: Platform ---
            fig1, ax1 = plt.subplots(figsize=fig_size)
            sns.boxplot(data=cleaned_df, x="Platform", y="Engagement_Rate", ax=ax1, color=indigo_color)
            
            # Mean markers
            means = cleaned_df.groupby("Platform")["Engagement_Rate"].mean()
            ax1.scatter(means.index, means.values, color=mean_col, marker='D', s=80, zorder=5)
            
            ax1.set_title("Engagement Rate by Platform", fontweight='bold', fontsize=title_fs, color=eda_txt)
            ax1.set_xlabel("Platform", fontweight='bold', fontsize=label_fs, color=eda_txt, labelpad=15)
            ax1.set_ylabel("Engagement Rate (%)", fontweight='bold', fontsize=label_fs, color=eda_txt, labelpad=15)
            # ✨ FIXED: Rotate x-axis labels using tick_params (no warning)
            ax1.tick_params(colors="#E2E8F0", labelsize=tick_fs, axis='x', labelrotation=45)
            ax1.set_facecolor(eda_bg)
            fig1.patch.set_facecolor(eda_bg)
            fig1.tight_layout()
            
            canvas1 = FigureCanvasTkAgg(fig1, scrollable_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="x", expand=True, padx=20, pady=10)

           # --- Graph 2: Content Type ---
            fig2, ax2 = plt.subplots(figsize=fig_size)
            sns.boxplot(data=cleaned_df, x="Content_Type", y="Engagement_Rate", ax=ax2, color=indigo_color)
            
            # Mean markers
            means = cleaned_df.groupby("Content_Type")["Engagement_Rate"].mean()
            ax2.scatter(means.index, means.values, color=mean_col, marker='D', s=80, zorder=5)
            
            ax2.set_title("Engagement Rate by Content Type", fontweight='bold', fontsize=title_fs, color=eda_txt)
            ax2.set_xlabel("Content Type", fontweight='bold', fontsize=label_fs, color=eda_txt, labelpad=15)
            ax2.set_ylabel("Engagement Rate (%)", fontweight='bold', fontsize=label_fs, color=eda_txt, labelpad=15)
            # ✨ FIXED: Rotate x-axis labels using tick_params (no warning)
            ax2.tick_params(colors="#E2E8F0", labelsize=tick_fs, axis='x', labelrotation=45)
            ax2.set_facecolor(eda_bg)
            fig2.patch.set_facecolor(eda_bg)
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, scrollable_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="x", expand=True, padx=20, pady=10)

            # --- Viral Posts Table (Full Width Fix) ---
            tk.Label(scrollable_frame, text="🔥 TOP 5 VIRAL POSTS", 
                     font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=ACCENT).pack(pady=20)
            
            viral_posts = cleaned_df.sort_values(by="Reach", ascending=False).head(5)
            table_frame = tk.Frame(scrollable_frame, bg=CARD_BG)
            table_frame.pack(fill="x", padx=20, pady=10)

            # Force table columns to stretch
            for i in range(7): table_frame.grid_columnconfigure(i, weight=1)

            headers = ["Platform", "Content", "Reach", "Eng.Rate", "Likes", "Shares", "Saves"]
            for i, h in enumerate(headers):
                tk.Label(table_frame, text=h, bg=viral_bg, fg=viral_txt, font=("Segoe UI", 10, "bold"),
                         relief="flat", pady=10).grid(row=0, column=i, sticky="nsew")

            for r, (_, row) in enumerate(viral_posts.iterrows(), 1):
                vals = [row["Platform"], row["Content_Type"], f"{int(row['Reach']):,}", 
                        f"{row['Engagement_Rate']:.3f}", int(row['Likes']), int(row['Shares']), int(row['Saves'])]
                for c, v in enumerate(vals):
                    tk.Label(table_frame, text=v, bg=viral_bg, fg=viral_txt, font=("Segoe UI", 10),
                             pady=5, relief="flat").grid(row=r, column=c, sticky="nsew")

            # Mousewheel support
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 3. Main Logic
        def run_eda():
            if cleaned_df is None: return
            
            alert = Toplevel(self.root)
            alert.configure(bg=PRIMARY_BG)
            
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            if current_width <= 600:
                alert_w = int(current_width * 0.92)
                alert_h = int(current_height * 0.55)
                font_scale, grid_cols = 0.85, 2
            else:
                alert_w, alert_h = 600, 560
                font_scale, grid_cols = 1.0, 2

            # Center Alert
            x = self.root.winfo_rootx() + (current_width // 2) - (alert_w // 2)
            y = self.root.winfo_rooty() + (current_height // 2) - (alert_h // 2)
            alert.geometry(f"{alert_w}x{alert_h}+{x}+{y}")

            def r_font(size, weight="normal"): return ("Segoe UI", int(size * font_scale), weight)

            frame = tk.Frame(alert, bg=PRIMARY_BG)
            frame.pack(fill="both", expand=True, padx=15, pady=15)

            # Section 1: Engagement
            tk.Label(frame, text="📈 Engagement Rate Analysis", bg=PRIMARY_BG, fg=TEXT,
                     font=r_font(13, "bold"), anchor="center").pack(fill="x", pady=(0, 5))
            
            best_platform_er = cleaned_df.groupby("Platform")["Engagement_Rate"].mean().idxmax()
            best_content_er = cleaned_df.groupby("Content_Type")["Engagement_Rate"].mean().idxmax()
            
            tk.Label(frame, text=f"Platform: {best_platform_er}\nContent: {best_content_er}",
                     bg=PRIMARY_BG, fg=ACCENT, font=r_font(11, "bold")).pack(pady=5)
            
            er_df = cleaned_df[(cleaned_df["Platform"] == best_platform_er) &
                               (cleaned_df["Content_Type"] == best_content_er)]
            
            er_stats_frame = tk.Frame(frame, bg=PRIMARY_BG)
            er_stats_frame.pack(fill="x", pady=5)
            
            er_stats = {
                "Minimum": er_df["Engagement_Rate"].min(),
                "Q1 (25%)": er_df["Engagement_Rate"].quantile(0.25),
                "Median": er_df["Engagement_Rate"].median(),
                "Q3 (75%)": er_df["Engagement_Rate"].quantile(0.75),
                "Maximum": er_df["Engagement_Rate"].max(),
                "Std Dev": er_df["Engagement_Rate"].std()
            }
            
            for i, (k, v) in enumerate(er_stats.items()):
                r, c = i // grid_cols, i % grid_cols
                tk.Label(er_stats_frame, text=f"{k}: {v:.2f}", bg=PRIMARY_BG, fg=MUTED,
                         font=r_font(10)).grid(row=r, column=c, sticky="w", padx=20, pady=2)
            
            er_stats_frame.grid_columnconfigure(0, weight=1)
            er_stats_frame.grid_columnconfigure(1, weight=1)
            ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

            # Section 2: Reach
            tk.Label(frame, text="📊 Reach Analysis", bg=PRIMARY_BG, fg=TEXT,
                     font=r_font(13, "bold"), anchor="center").pack(fill="x", pady=(0, 5))
            
            best_platform_reach = cleaned_df.groupby("Platform")["Reach"].mean().idxmax()
            best_content_reach = cleaned_df.groupby("Content_Type")["Reach"].mean().idxmax()
            
            tk.Label(frame, text=f"Platform: {best_platform_reach}\nContent: {best_content_reach}",
                     bg=PRIMARY_BG, fg=ACCENT, font=r_font(11, "bold")).pack(pady=5)
            
            reach_df = cleaned_df[(cleaned_df["Platform"] == best_platform_reach) &
                                  (cleaned_df["Content_Type"] == best_content_reach)]
            
            reach_stats_frame = tk.Frame(frame, bg=PRIMARY_BG)
            reach_stats_frame.pack(fill="x", pady=5)
            
            reach_stats = {
                "Minimum": reach_df["Reach"].min(),
                "Q1 (25%)": reach_df["Reach"].quantile(0.25),
                "Median": reach_df["Reach"].median(),
                "Q3 (75%)": reach_df["Reach"].quantile(0.75),
                "Maximum": reach_df["Reach"].max(),
                "Std Dev": reach_df["Reach"].std()
            }
            
            for i, (k, v) in enumerate(reach_stats.items()):
                r, c = i // grid_cols, i % grid_cols
                tk.Label(reach_stats_frame, text=f"{k}: {v:,.0f}", bg=PRIMARY_BG, fg=MUTED,
                         font=r_font(10)).grid(row=r, column=c, sticky="w", padx=20, pady=2)
            
            reach_stats_frame.grid_columnconfigure(0, weight=1)
            reach_stats_frame.grid_columnconfigure(1, weight=1)

            # On Close logic
            def on_eda_close():
                self.eda_completed = True
                alert.destroy()
                if cleaned_df is not None:
                    show_box_plots()

            alert.protocol("WM_DELETE_WINDOW", on_eda_close)

        # 4. Trigger Button
        RoundedButton(content_frame, text="🔧 Run EDA", width=140, height=40,
                      bg_color=PRIMARY_BG,
                      command=run_eda).pack(pady=30)

        # 5. Persistent State Check
        if hasattr(self, 'eda_completed') and self.eda_completed and cleaned_df is not None:
            show_box_plots()
    
    def center_alert(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')

    # def show_loading(self, message="Processing...", sub_message="Please wait"):
    #     loading = tk.Toplevel(self.root)
    #     loading.configure(bg=ThemeManager.get("card_bg")) 
        
    #     # Dimensions of the loading box
    #     width, height = 380, 280

    #     # ==========================================================
    #     # 🔧 FIX: CENTER ON CONTENT AREA
    #     # ==========================================================
    #     try:
    #         # 1. Get the absolute screen coordinates of the Content Area
    #         c_x = self.content_area.winfo_rootx()
    #         c_y = self.content_area.winfo_rooty()
    #         c_w = self.content_area.winfo_width()
    #         c_h = self.content_area.winfo_height()

    #         # 2. Calculate center relative to the Content Area
    #         x = c_x + (c_w // 2) - (width // 2)
    #         y = c_y + (c_h // 2) - (height // 2)
            
    #         # Fallback if content area isn't drawn yet (width=1)
    #         if c_w <= 1: raise Exception("Canvas not ready")

    #     except:
    #         # Fallback: Center on the main application window
    #         x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (width // 2)
    #         y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (height // 2)

    #     loading.geometry(f"{width}x{height}+{x}+{y}")
    #     # ==========================================================

    #     loading.overrideredirect(True)
    #     loading.attributes("-topmost", True) # Keeps it above everything
    #     loading.grab_set()

    #     # 2. Canvas Setup (Modern Spinner)
    #     spinner_size = 80
    #     canvas = tk.Canvas(
    #         loading, 
    #         width=spinner_size, 
    #         height=spinner_size, 
    #         bg=ThemeManager.get("card_bg"), 
    #         highlightthickness=0
    #     )
    #     canvas.pack(pady=(40, 20))

    #     # 3. Typography
    #     tk.Label(loading, text=message, font=("Segoe UI", 16, "bold"), 
    #              bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("text_main")).pack(pady=(0, 5))
        
    #     tk.Label(loading, text=sub_message, font=("Segoe UI", 11), 
    #              bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("text_muted")).pack()

    #     # 4. Smooth Animation Loop
    #     state = {"rotation": 0, "pulse": 0} 

    #     def animate():
    #         if not loading.winfo_exists():
    #             return
    #         canvas.delete("all")
            
    #         # Breathing effect math
    #         ease_sine = math.sin(state["pulse"]) 
    #         extent = 160 + (ease_sine * 130)
            
    #         # Draw the spinning arc
    #         canvas.create_arc(
    #             10, 10, spinner_size-10, spinner_size-10,
    #             start=state["rotation"],
    #             extent=extent,
    #             style="arc",
    #             width=5, 
    #             outline=ThemeManager.get("text_main")
    #         )

    #         state["rotation"] = (state["rotation"] + 8) % 360
    #         state["pulse"] += 0.08
    #         loading.after(20, animate)

    #     animate()
    #     loading.update()
    #     return loading
    def show_loading(self, message="Processing...", sub_message="Please wait"):
        loading = tk.Toplevel(self.root)
        loading.configure(bg=ThemeManager.get("card_bg")) 
        
        # Dimensions of the loading box
        width, height = 380, 280

        # Center logic
        try:
            c_x = self.content_area.winfo_rootx()
            c_y = self.content_area.winfo_rooty()
            c_w = self.content_area.winfo_width()
            c_h = self.content_area.winfo_height()
            x = c_x + (c_w // 2) - (width // 2)
            y = c_y + (c_h // 2) - (height // 2)
            if c_w <= 1: raise Exception("Canvas not ready")
        except:
            x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (width // 2)
            y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (height // 2)

        loading.geometry(f"{width}x{height}+{x}+{y}")
        loading.overrideredirect(True)
        loading.attributes("-topmost", True)
        loading.grab_set()

        # Canvas Setup
        spinner_size = 80
        canvas = tk.Canvas(
            loading, 
            width=spinner_size, 
            height=spinner_size, 
            bg=ThemeManager.get("card_bg"), 
            highlightthickness=0
        )
        canvas.pack(pady=(40, 20))

        tk.Label(loading, text=message, font=("Segoe UI", 16, "bold"), 
                 bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("text_main")).pack(pady=(0, 5))
        
        tk.Label(loading, text=sub_message, font=("Segoe UI", 11), 
                 bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("text_muted")).pack()

        # Smooth Animation Loop
        state = {"rotation": 0, "pulse": 0} 

        def animate():
            # --- FIX START: Stop animation if window or app is destroyed ---
            try:
                if not loading.winfo_exists():
                    return
            except:
                return
            # --- FIX END ---
            
            canvas.delete("all")
            
            ease_sine = math.sin(state["pulse"]) 
            extent = 160 + (ease_sine * 130)
            
            canvas.create_arc(
                10, 10, spinner_size-10, spinner_size-10,
                start=state["rotation"],
                extent=extent,
                style="arc",
                width=5, 
                outline=ThemeManager.get("text_main")
            )

            state["rotation"] = (state["rotation"] + 8) % 360
            state["pulse"] += 0.08
            
            # Use 'loading.after' instead of 'root.after' so it dies with the window
            loading.after(20, animate)

        animate()
        loading.update()
        return loading


    
    def show_regression_insights(self):
        global prediction_df
        self.show_table(prediction_df, "Regression: Actual vs Predicted")

    def show_classification_insights(self, model, accuracy, report, cm, target):
        alert = Toplevel(self.root)
        alert.title("Classification Results")
        alert.configure(bg=ThemeManager.get("card_bg"))
        alert.geometry("500x400")
        self.center_alert(alert)

        tk.Label(alert, text="🎯 Model Performance", font=("Segoe UI", 18, "bold"), 
                 bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("accent")).pack(pady=20)
        tk.Label(alert, text=f"Target: {target}", font=("Segoe UI", 12), 
                 bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("text_main")).pack()
        tk.Label(alert, text=f"Accuracy: {accuracy:.2%}", font=("Segoe UI", 16, "bold"), 
                 bg=ThemeManager.get("card_bg"), fg=ThemeManager.get("success")).pack(pady=10)
        
        RoundedButton(alert, text="Close", width=120, height=40, 
                      command=alert.destroy).pack(pady=20)

    def show_train_ml(self):
        """Navigate to ML training page"""
        global cleaned_df
        
        # 1. Clear Screen
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        colors = ThemeManager.get
        
        # 2. Setup Container Frame
        # Create a "content_frame" inside the canvas to mimic your original structure
        content_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))

        window_id = self.content_area.create_window(
            0, 0, window=content_frame, anchor="nw"
        )

        def _resize(event=None):
            self.content_area.itemconfigure(
                window_id,
                width=self.content_area.winfo_width(),
                height=self.content_area.winfo_height()
            )

        self.content_area.bind("<Configure>", _resize)
        self.root.after(0, _resize)


        # 3. Responsive Dimensions
        device = get_device_type(self.root)
        self.root.update_idletasks()
        
        if device == "mobile":
            title_font = 18; btn_width = 180; btn_height = 50; btn_font = 11
            layout_mode = "vertical"; padding_x = 10; padding_y = 15
        elif device == "tablet":
            title_font = 22; btn_width = 200; btn_height = 55; btn_font = 12
            layout_mode = "horizontal"; padding_x = 20; padding_y = 40
        else:
            title_font = 24; btn_width = 240; btn_height = 65; btn_font = 13
            layout_mode = "horizontal"; padding_x = 30; padding_y = 60

        # 4. Header
        tk.Label(content_frame, text="🤖 Train Machine Learning Model", 
                 font=("Segoe UI", title_font, "bold"),
                 bg=colors("gradient_start"), fg=colors("text_main")).pack(pady=(padding_y + 40, 20))

        if cleaned_df is None:
            tk.Label(content_frame, text="⚠️ Please upload dataset and run preprocessing first", 
                     font=("Segoe UI", 14), bg=colors("gradient_start"), fg=colors("danger")).pack(pady=20)
            return

        # 5. Training Logic
        def train_regression():
            loading = self.show_loading("Training Regression...", "Training LightGBM Regressor")
            def perform():
                try:
                    global regression_model, prediction_df, regression_trained
                    numeric_cols = cleaned_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                    target_col = "Engagement_Rate" if "Engagement_Rate" in numeric_cols else numeric_cols[0]
                    X = cleaned_df.drop(columns=[target_col]).copy()
                    y = cleaned_df[target_col]
                    
                    for col in X.select_dtypes(include=['object']).columns:
                        X[col] = pd.Categorical(X[col]).codes
                    
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LGBMRegressor(n_estimators=100, learning_rate=0.05, verbose=-1)
                    model.fit(X_train, y_train)
                    
                    regression_model = model
                    prediction_df = cleaned_df.copy()
                    prediction_df['Predicted'] = model.predict(X)
                    regression_trained = True
                    
                    self.root.after(0, lambda: [loading.destroy(), self.show_regression_insights()])
                except Exception as e:
                    self.root.after(0, lambda: [loading.destroy(), print(f"Error: {e}")])
            threading.Thread(target=perform, daemon=True).start()


        def train_classification():
            loading = self.show_loading("Training Classification...", "Training CatBoost Classifier")
            
            def perform():
                try:
                    global classification_model
                    # 1. Prepare Data
                    categorical_cols = cleaned_df.select_dtypes(include=['object']).columns.tolist()
                    
                    # Safety check if no categorical columns exist
                    if not categorical_cols:
                        self.root.after(0, lambda: [loading.destroy(), tk.messagebox.showerror("Error", "No categorical columns found for classification.")])
                        return

                    target_col = "Platform" if "Platform" in categorical_cols else categorical_cols[0]
                    
                    X = cleaned_df.drop(columns=[target_col])
                    y = cleaned_df[target_col]
                    
                    # 2. Identify Categorical Features for CatBoost
                    cat_features = [i for i, col in enumerate(X.columns) if X[col].dtype == 'object']
                    
                    # 3. Split Data
                    # Stratify is important for classification to keep class balance
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
                    
                    # 4. Train Model
                    model = CatBoostClassifier(iterations=100, cat_features=cat_features, verbose=False)
                    model.fit(X_train, y_train)
                    classification_model = model
                    
                    # 5. Predictions & Metrics
                    y_pred = model.predict(X_test)
                    acc = accuracy_score(y_test, y_pred)
                    
                    # --- CRITICAL FIX: Calculate Report & Matrix HERE ---
                    # We must generate these BEFORE passing them to the UI
                    report = classification_report(y_test, y_pred, output_dict=True)
                    cm = confusion_matrix(y_test, y_pred)
                    
                    # 6. Show Results (Pass the actual 'report' and 'cm', NOT empty {})
                    self.root.after(0, lambda: [loading.destroy(), self.show_classification_insights(model, acc, report, cm, target_col)])
                
                except Exception as e:
                    # Print error to console for debugging
                    print(f"Training Error: {e}")
                    self.root.after(0, lambda: [loading.destroy(), self.center_alert(Toplevel(self.root))]) 
            
            threading.Thread(target=perform, daemon=True).start()
        # 6. Buttons
        btn_frame = tk.Frame(content_frame, bg=colors("gradient_start"))
        btn_frame.pack(pady=40)

        reg_btn = RoundedButton(btn_frame, text="📈 REGRESSION", width=btn_width, height=btn_height, 
                                command=train_regression, bg_color=colors("gradient_start"))
        reg_btn.pack(side="left" if layout_mode == "horizontal" else "top", padx=padding_x, pady=padding_y)

        clf_btn = RoundedButton(btn_frame, text="🎯 CLASSIFICATION", width=btn_width, height=btn_height, 
                                command=train_classification, bg_color=colors("gradient_start"))
        clf_btn.pack(side="left" if layout_mode == "horizontal" else "top", padx=padding_x, pady=padding_y)

    # =============================================================================
    # 🔮 ENHANCED REGRESSION INSIGHTS INTEGRATION
    # =============================================================================


    def show_regression_insights(self):
        global regression_model, cleaned_df, regression_trained, prediction_df, regression_insights_shown

        # 🔒 Only allow if model was trained
        if not regression_trained or regression_model is None or cleaned_df is None:
            self.show_train_ml()
            return

        # --- HELPER FUNCTION: Get Insights Dynamically ---
        def get_dynamic_insights(filter_platform):
            from collections import Counter
            
            # Filter data
            if filter_platform == "Overall":
                df_subset = cleaned_df
            else:
                df_subset = cleaned_df[cleaned_df['Platform'] == filter_platform]
            
            if df_subset.empty:
                return [], "N/A", "N/A", "N/A"

            # 1. Top Hashtags
            all_tags = []
            for tag_str in df_subset['Hashtags'].astype(str):
                # Extract words starting with #
                tags = [t.strip() for t in tag_str.split() if t.strip().startswith("#")]
                all_tags.extend(tags)
            
            # Get top 5 most common
            top_tags = [tag for tag, count in Counter(all_tags).most_common(5)]
            
            # 2. Hashtag Range
            if 'Hashtag_count' in df_subset.columns:
                min_h = df_subset['Hashtag_count'].min()
                max_h = df_subset['Hashtag_count'].max()
                avg_h = int(df_subset['Hashtag_count'].mean())
                h_range = f"{min_h}-{max_h} (Avg: {avg_h})"
            else:
                h_range = "N/A"

            # 3. Best Time & Days (based on Engagement Rate)
            try:
                b_time = df_subset.groupby('Time')['Engagement_Rate'].mean().idxmax()
            except:
                b_time = "N/A"
            
            try:
                p_days = df_subset.groupby('Days')['Engagement_Rate'].mean().idxmax()
            except:
                p_days = "N/A"

            return top_tags, h_range, b_time, p_days
        # -------------------------------------------------
        
        # 1. Clear Screen & Setup Background
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        # Map your local variable names to the class theme system
        colors = ThemeManager.get
        PRIMARY_BG = colors("gradient_start")
        CARD_BG = colors("card_bg")
        TEXT = colors("text_main")
        MUTED = colors("text_muted")
        ACCENT = colors("accent")
        ml_head = colors("ml_head1")
        metrics_border = colors("metrics_border1")
        tab_col1=colors("tab_col11")
        tab_col2 = colors("tab_col21")
        metrics_txt =colors("metrics_txt1")
        ml_bg=colors("ml_bg1")
        ml_txt=colors("ml_txt1")
        ins_bg = colors("ins_bg1")
        
        # Create a "content_frame" inside the canvas to mimic your original structure
        content_frame = tk.Frame(self.content_area, bg=PRIMARY_BG)

        window_id = self.content_area.create_window(
            0, 0, window=content_frame, anchor="nw"
        )

        def _resize(event=None):
            self.content_area.itemconfigure(
                window_id,
                width=self.content_area.winfo_width(),
                height=self.content_area.winfo_height()
            )

        self.content_area.bind("<Configure>", _resize)
        self.root.after(0, _resize)


        # =============================
        # 1. UPDATED RESPONSIVE DIMENSIONS
        # =============================
        device = get_device_type(self.root)
        self.root.update_idletasks()
        
        # Default values (Desktop)
        title_font = 22
        section_font = 16
        text_font = 12
        padding_x = 20      # Outer padding
        inner_pad = 20      # Padding inside cards
        canvas_width = self.root.winfo_width() - 320 # Sidebar offset
        dropdown_layout = "horizontal" 

        if device == "mobile":
            title_font = 16          
            section_font = 14
            text_font = 10
            padding_x = 5           
            inner_pad = 5           
            canvas_width = self.root.winfo_width() - 20     
            dropdown_layout = "vertical" 
        elif device == "tablet":
            title_font = 20
            section_font = 15
            text_font = 11
            padding_x = 15
            inner_pad = 15
            canvas_width = self.root.winfo_width() - 100
        
        # Title
        tk.Label(content_frame, text="🔮 REGRESSION MODEL INSIGHTS", 
                 font=("Segoe UI", title_font, "bold"), bg=PRIMARY_BG, fg=TEXT, wraplength=canvas_width-20).pack(pady=20)
        
        regression_insights_shown = True
        
        # Scrollable container
        scroll_container = tk.Frame(content_frame, bg="#ffffff")
        scroll_container.pack(fill="both", expand=True, padx=padding_x, pady=5)
        
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
        canvas = tk.Canvas(scroll_container, bg=CARD_BG, highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=CARD_BG)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # RESPONSIVE CANVAS WIDTH
        def update_canvas_width(event=None):
            try:
                current_width = scroll_container.winfo_width()
                width = max(280, current_width - 25) 
                canvas.itemconfig(canvas_window, width=width)
            except:
                pass
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=canvas.yview)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        scroll_container.bind("<Configure>", update_canvas_width)
        
        # [DATA PREPARATION LOGIC]
        numeric_cols = cleaned_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        target_col = "Engagement_Rate" if "Engagement_Rate" in numeric_cols else numeric_cols[0]
        feature_cols = [col for col in cleaned_df.columns if col != target_col]
        
        X = cleaned_df[feature_cols].copy()
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = pd.Categorical(X[col]).codes
        
        X_train, X_test, y_train, y_test = train_test_split(X, cleaned_df[target_col], test_size=0.2, random_state=42)
        y_pred_test = regression_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred_test)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred_test)

        # === 1. MODEL HEADER ===
        tk.Label(scrollable_frame, text="✅ REGRESSION MODEL TRAINED!", 
                 font=("Segoe UI", 16 if device=="mobile" else 18, "bold"), bg=CARD_BG, fg=ml_head, wraplength=canvas_width-40).pack(pady=(20, 5))
        tk.Label(scrollable_frame, text="⚡ Powered by LightGBM Algorithm", 
                 font=("Segoe UI", 11), bg=CARD_BG, fg=MUTED).pack(pady=(0, 20))
        
        # === 2. PERFORMANCE SUMMARY ===
        tk.Label(scrollable_frame, text="📊 MODEL PERFORMANCE SUMMARY", 
                 font=("Segoe UI", section_font, "bold"), bg=CARD_BG, fg=ml_head, wraplength=canvas_width-40).pack(pady=(20, 10))
        
        metrics_frame = tk.Frame(scrollable_frame, bg=metrics_border, relief="solid", bd=1)
        metrics_frame.pack(fill="x", padx=padding_x, pady=10)
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        
        metrics_data = [
            ["📈 MSE", f"{mse:.6f}"], ["📏 RMSE", f"{rmse:.6f}"], ["⭐ R² Score", f"{r2:.4f}"],
            ["🎯 Target", str(target_col)], ["📊 Test Size", f"{len(X_test)} samples"]
        ]
        
        for row_idx, (metric, value) in enumerate(metrics_data):
            bg_color = tab_col1 if row_idx % 2 == 0 else tab_col2
            tk.Label(metrics_frame, text=metric, bg=bg_color, fg=metrics_txt, font=("Segoe UI", text_font, "bold"), relief="solid", bd=1).grid(row=row_idx, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(metrics_frame, text=value, bg=bg_color, fg=metrics_txt, font=("Segoe UI", text_font), relief="solid", bd=1).grid(row=row_idx, column=1, sticky="nsew", padx=1, pady=1)
        
        # prediction_df creation
        y_all_pred = regression_model.predict(X)
        prediction_df = cleaned_df.copy()
        prediction_df['Predicted'] = y_all_pred
        
        # === 3. TOP PERFORMING INSIGHTS ===
        tk.Label(scrollable_frame, text="🥇 TOP PERFORMING INSIGHTS", 
                 font=("Segoe UI", section_font, "bold"), bg=CARD_BG, fg=ml_head, wraplength=canvas_width-40).pack(pady=(30, 10))
        
        top_insights_frame = tk.Frame(scrollable_frame, bg=ins_bg, relief="solid", bd=2)
        top_insights_frame.pack(fill="x", padx=padding_x, pady=10)
        
        all_platform_best = prediction_df.groupby('Platform')['Predicted'].mean().idxmax()
        all_platform_score = prediction_df.groupby('Platform')['Predicted'].mean().max()
        all_content_best = prediction_df.groupby('Content_Type')['Predicted'].mean().idxmax()
        all_content_score = prediction_df.groupby('Content_Type')['Predicted'].mean().max()

        if device == "mobile":
            text_wrap = canvas_width - (inner_pad * 2) - 15 
            h_font_size = 12; p_font_size = 10
        else:
            text_wrap = canvas_width - (padding_x * 4) 
            h_font_size = 14; p_font_size = 12

        tk.Label(top_insights_frame, text=f"🥇 BEST PLATFORM: {all_platform_best}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size, "bold"), wraplength=text_wrap, justify="left").pack(pady=(15,5), anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"   Predicted Score: {all_platform_score:.3f}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", p_font_size), wraplength=text_wrap, justify="left").pack(anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"🎥 BEST CONTENT: {all_content_best}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size, "bold"), wraplength=text_wrap, justify="left").pack(pady=(15,5), anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"   Predicted Score: {all_content_score:.3f}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", p_font_size), wraplength=text_wrap, justify="left").pack(anchor="w", padx=inner_pad)

        # Dynamic Insights Logic (Initial Load)
        hashtags, h_range, b_time, p_days = get_dynamic_insights("Overall")
        
        tk.Label(top_insights_frame, text=f"TOP HASHTAGS: {' '.join(hashtags)}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size-1, "bold"), wraplength=text_wrap, justify="left").pack(pady=(15,5), anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"📊 HASHTAG RANGE: {h_range} per post", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size, "bold"), wraplength=text_wrap, justify="left").pack(pady=(0,15), anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"⏰ BEST TIME: {b_time}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size, "bold"), wraplength=text_wrap, justify="left").pack(pady=(15,5), anchor="w", padx=inner_pad)
        tk.Label(top_insights_frame, text=f"📅 PERFECT DAYS: {p_days}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_font_size, "bold"), wraplength=text_wrap, justify="left").pack(pady=(15,20), anchor="w", padx=inner_pad)

        summary_frame = tk.Frame(top_insights_frame, bg=ins_bg, relief="solid", bd=1)
        summary_frame.pack(fill="x", padx=inner_pad, pady=(0,15))
        tk.Label(summary_frame, text="✅ POST ON PERFECT DAYS with BEST CONTENT + TOP HASHTAGS = MAX ENGAGEMENT", fg=ml_txt, bg=ml_bg, font=("Segoe UI", p_font_size, "bold"), wraplength=text_wrap-10, justify="center").pack(pady=10)

        # === 4. INTERACTIVE SELECTOR ===
        tk.Label(scrollable_frame, text="🎛️ INTERACTIVE STRATEGY SELECTOR", font=("Segoe UI", section_font, "bold"), bg=CARD_BG, fg="#8B5CF6", wraplength=canvas_width-40).pack(pady=(30, 10))
        
        dropdown_frame = tk.Frame(scrollable_frame, bg=ml_bg, relief="solid", bd=2)
        dropdown_frame.pack(fill="x", padx=padding_x, pady=10)
        
        platform_var = tk.StringVar(value="All Platforms")
        platforms = sorted(prediction_df['Platform'].unique().tolist()) + ["All Platforms"]
        platform_dropdown = ttk.Combobox(dropdown_frame, textvariable=platform_var, values=platforms, state="readonly", font=("Segoe UI", 11))
        
        content_var = tk.StringVar(value="All Content")
        contents = sorted(prediction_df['Content_Type'].unique().tolist()) + ["All Content"]
        content_dropdown = ttk.Combobox(dropdown_frame, textvariable=content_var, values=contents, state="readonly", font=("Segoe UI", 11))
        
        if dropdown_layout == "vertical":
            platform_dropdown.pack(side="top", fill="x", padx=10, pady=(10, 5))
            content_dropdown.pack(side="top", fill="x", padx=10, pady=(5, 10))
        else:
            platform_dropdown.pack(side="left", expand=True, padx=20, pady=10)
            content_dropdown.pack(side="right", expand=True, padx=20, pady=10)
        
        results_container = tk.Frame(scrollable_frame, bg=ml_bg)
        results_container.pack(fill="x", padx=padding_x, pady=10)

        def update_insights():
            for widget in results_container.winfo_children(): widget.destroy()
            res_frame = tk.Frame(results_container, bg=ml_bg, relief="solid", bd=2)
            res_frame.pack(fill="x", pady=10)
            
            sel_p = platform_var.get()
            sel_c = content_var.get()
            
            # Re-run logic for filtered results
            hashtags, h_range, b_time, p_days = get_dynamic_insights(sel_p if sel_p != "All Platforms" else "Overall")
            
            if device == "mobile":
                res_wrap = canvas_width - (inner_pad * 2) - 15
                h_res_font = 12; p_res_font = 10
            else:
                res_wrap = canvas_width - (padding_x * 4)
                h_res_font = 13; p_res_font = 11

            tk.Label(res_frame, text=f"🥇 TARGETING: {sel_p} | {sel_c}", fg=ml_head, bg=ml_bg, font=("Segoe UI", h_res_font, "bold"), wraplength=res_wrap).pack(pady=10)
            
            # ADDED: Dynamic Hashtag Labels
            tk.Label(res_frame, text=f"TOP HASHTAGS: {' '.join(hashtags)}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_res_font-1, "bold"), wraplength=res_wrap, justify="left").pack(pady=(15,5), anchor="w", padx=inner_pad)
            tk.Label(res_frame, text=f"📊 HASHTAG RANGE: {h_range} per post", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_res_font, "bold"), wraplength=res_wrap, justify="left").pack(pady=(0,15), anchor="w", padx=inner_pad)
            
            # Existing Time & Day Labels
            tk.Label(res_frame, text=f"⏰ BEST TIME: {b_time}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_res_font, "bold"), wraplength=res_wrap, justify="left").pack(anchor="w", padx=inner_pad)
            tk.Label(res_frame, text=f"📅 PERFECT DAYS: {p_days}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", h_res_font, "bold"), wraplength=res_wrap, justify="left").pack(anchor="w", padx=inner_pad, pady=(0, 15))

        RoundedButton(scrollable_frame, text="🔄 UPDATE INSIGHTS", width=230, height=45, command=update_insights).pack(pady=10)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Back Button
        RoundedButton(scrollable_frame, text="🔙 Back to ML", width=180, height=45, command=self.show_train_ml).pack(pady=20)


    # =============================================================================
    # 🎯 CLASSIFICATION INSIGHTS & STRATEGY PAGES
    # =============================================================================

    def show_classification_insights(self, model, accuracy, report, cm, target_col):
        global classification_model, cleaned_df
        
        # 1. Clear Screen & Setup Background
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        colors = ThemeManager.get
        PRIMARY_BG = colors("gradient_start")
        CARD_BG = colors("card_bg")
        TEXT = colors("text_main")
        MUTED = colors("text_muted")
        ACCENT = colors("accent")
        ml_head = colors("ml_head1")
        metrics_border = colors("metrics_border1")
        tab_col1=colors("tab_col11")
        tab_col2 = colors("tab_col21")
        metrics_txt =colors("metrics_txt1")
        ml_bg=colors("ml_bg1")
        ml_txt=colors("ml_txt1")
        ins_bg = colors("ins_bg1")
        

        # Create a "content_frame" inside the canvas to mimic your original structure
        content_frame = tk.Frame(self.content_area, bg=PRIMARY_BG)

        window_id = self.content_area.create_window(
            0, 0, window=content_frame, anchor="nw"
        )

        def _resize(event=None):
            self.content_area.itemconfigure(
                window_id,
                width=self.content_area.winfo_width(),
                height=self.content_area.winfo_height()
            )

        self.content_area.bind("<Configure>", _resize)
        self.root.after(0, _resize)


        # --- Helper Function: Get Dynamic Insights ---
        def get_dynamic_insights(class_label):
            try:
                class_df = cleaned_df[cleaned_df[target_col] == class_label]
                if class_df.empty: return ["N/A"], "N/A", "N/A", "N/A"

                # 1. Top Hashtags
                all_hashtags = []
                if 'Hashtags' in class_df.columns:
                    for tags in class_df['Hashtags'].dropna():
                        if isinstance(tags, str):
                            all_hashtags.extend(tags.replace(',', ' ').split())
                
                if all_hashtags:
                    from collections import Counter
                    common_hashtags = [tag for tag, count in Counter(all_hashtags).most_common(5)]
                else:
                    common_hashtags = ["No Hashtags Found"]

                # 2. Hashtag Range
                if 'Hashtag_count' in class_df.columns:
                    min_h = class_df['Hashtag_count'].min()
                    max_h = class_df['Hashtag_count'].max()
                    avg_h = class_df['Hashtag_count'].mean()
                    hashtag_range = f"{min_h}-{max_h} (Avg: {avg_h:.1f})"
                else:
                    hashtag_range = "N/A"

                # 3. Best Time
                if 'Time' in class_df.columns and not class_df['Time'].empty:
                    best_time = class_df['Time'].mode()[0]
                else:
                    best_time = "N/A"

                # 4. Best Days
                if 'Days' in class_df.columns and not class_df['Days'].empty:
                    best_days = class_df['Days'].mode()[0]
                else:
                    best_days = "N/A"
                    
                return common_hashtags, hashtag_range, best_time, best_days
            except Exception as e:
                print(f"Error in insights: {e}")
                return ["Error"], "Error", "Error", "Error"

        # --- RESPONSIVE DIMENSIONS ---
        device = get_device_type(self.root)
        self.root.update_idletasks()
        
        if device == "mobile":
            title_font = 18; section_font = 14; text_font = 10; padding_x = 8
            title_text = "🎯 CLASSIFICATION MODEL\nINSIGHTS"; title_font_size = 15; title_wraplength = 280
        elif device == "tablet":
            title_font = 20; section_font = 15; text_font = 11; padding_x = 15
            title_text = "🎯 CLASSIFICATION MODEL INSIGHTS"; title_font_size = 18; title_wraplength = 500
        else:
            title_font = 22; section_font = 16; text_font = 12; padding_x = 20
            title_text = "🎯 CLASSIFICATION MODEL INSIGHTS"; title_font_size = 22; title_wraplength = 0
        
        # Title
        tk.Label(content_frame, text=title_text, font=("Segoe UI", title_font_size, "bold"), 
                 bg=PRIMARY_BG, fg=TEXT, wraplength=title_wraplength, justify="center").pack(pady=20)
        
        # Scrollable container
        scroll_container = tk.Frame(content_frame, bg=CARD_BG)
        scroll_container.pack(fill="both", expand=True, padx=padding_x, pady=5)
        
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
        canvas = tk.Canvas(scroll_container, bg=CARD_BG, highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=CARD_BG)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        def update_canvas_width(event=None):
            try:
                curr_width = scroll_container.winfo_width()
                width = max(280, curr_width - (25 if device == "mobile" else 50))
                canvas.itemconfig(canvas_window, width=width)
            except: pass
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scroll_container.bind("<Configure>", update_canvas_width)

        # --- MODEL STATUS ---
        trained_text = "✅ CLASSIFICATION MODEL TRAINED!"
        tk.Label(scrollable_frame, text=trained_text, font=("Segoe UI", 16 if device != "mobile" else 14, "bold"), 
                 bg=CARD_BG, fg=ml_head).pack(pady=(20, 5))
        tk.Label(scrollable_frame, text="⚡ Powered by CatBoost Algorithm", font=("Segoe UI", 10), 
                 bg=CARD_BG, fg=MUTED).pack(pady=(0, 20))

        # --- METRICS SUMMARY ---
        summary_title = "📊 MODEL PERFORMANCE SUMMARY"
        tk.Label(scrollable_frame, text=summary_title, font=("Segoe UI", 16, "bold"), 
                 bg=CARD_BG, fg=ml_head).pack(pady=(20, 10))
        
        metrics_frame = tk.Frame(scrollable_frame, bg="#1F2A44", relief="solid", bd=1)
        metrics_frame.pack(fill="x", padx=padding_x, pady=10)
        metrics_frame.grid_columnconfigure(0, weight=1); metrics_frame.grid_columnconfigure(1, weight=1)
        
        metrics_data = [
            ["🎯 Target", str(target_col)],
            ["📊 Accuracy", f"{accuracy*100:.1f}%"],
            ["📈 Precision", f"{report['weighted avg']['precision']:.3f}"],
            ["⭐ F1-Score", f"{report['weighted avg']['f1-score']:.3f}"]
        ]
        
        for i, (m, v) in enumerate(metrics_data):
            bg = tab_col1 if i % 2 == 0 else tab_col1
            tk.Label(metrics_frame, text=m, bg=bg, fg=metrics_txt, font=("Segoe UI", 10, "bold"), bd=1, relief="solid").grid(row=i, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(metrics_frame, text=v, bg=bg, fg=metrics_txt, font=("Segoe UI", 10), bd=1, relief="solid").grid(row=i, column=1, sticky="nsew", padx=1, pady=1)

        # --- CONFUSION MATRIX ---
        tk.Label(scrollable_frame, text="🔢 CONFUSION MATRIX", font=("Segoe UI", 16, "bold"), 
                 bg=CARD_BG, fg=ml_head).pack(pady=(30, 10))
        
        cm_frame = tk.Frame(scrollable_frame, bg="#1a1a24", relief="solid")
        cm_frame.pack(padx=20, pady=10)
        cm_text = "\n".join([" ".join(f"{val:4d}" for val in row) for row in cm])
        tk.Label(cm_frame, text=cm_text, bg=ml_bg, fg="#1a1a24", font=("Courier", 10, "bold")).pack(pady=20, padx=30)

        # --- INTERACTIVE INSIGHTS ---
        tk.Label(scrollable_frame, text="🎛️ PER-CLASS INSIGHTS", font=("Segoe UI", 16, "bold"), 
                 bg=CARD_BG, fg="#8B5CF6").pack(pady=(30, 10))
        
        all_classes = [c for c in report.keys() if c not in ['accuracy', 'macro avg', 'weighted avg']]
        dropdown_frame = tk.Frame(scrollable_frame, bg=ml_bg, relief="solid", bd=2)
        dropdown_frame.pack(fill="x", padx=padding_x, pady=10)

        class_var = tk.StringVar(value=all_classes[0] if all_classes else "")
        tk.Label(dropdown_frame, text="Select Class:", bg=ml_bg, fg=ml_txt, font=("Segoe UI", 11)).pack(side="left", padx=10, pady=10)
        class_dropdown = ttk.Combobox(dropdown_frame, textvariable=class_var, values=all_classes, state="readonly", width=25)
        class_dropdown.pack(side="left", padx=10, pady=10)

        results_container = tk.Frame(scrollable_frame, bg=ml_bg)
        results_container.pack(fill="x", padx=padding_x, pady=10)

        def show_class_insights_internal():
            for w in results_container.winfo_children(): w.destroy()
            selected = class_var.get()
            if not selected: return
            
            res_frame = tk.Frame(results_container, bg=ml_bg, relief="solid", bd=2)
            res_frame.pack(fill="x", pady=10)
            
            # Fetch Data
            hashtags, h_range, b_time, b_days = get_dynamic_insights(selected)
            metrics = report[selected]

            tk.Label(res_frame, text=f"📊 INSIGHTS FOR: {selected}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", 12, "bold")).pack(pady=10, anchor="w", padx=20)
            
            stats_text = f"Precision: {metrics['precision']:.2f} | Recall: {metrics['recall']:.2f} | F1: {metrics['f1-score']:.2f}"
            tk.Label(res_frame, text=stats_text, fg=ml_txt, bg=ml_bg, font=("Segoe UI", 10)).pack(anchor="w", padx=40)
            
            tk.Label(res_frame, text=f"HASHTAGS: {' '.join(hashtags)}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", 10, "bold"), wraplength=400).pack(pady=5, anchor="w", padx=20)
            tk.Label(res_frame, text=f"⏰ BEST TIME: {b_time}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
            tk.Label(res_frame, text=f"📅 BEST DAYS: {b_days}", fg=ml_txt, bg=ml_bg, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(0, 10))

        RoundedButton(scrollable_frame, text="🔍 SHOW INSIGHTS", width=230, height=45, command=show_class_insights_internal).pack(pady=10)

        # Back Button
        RoundedButton(scrollable_frame, text="🔙 Back to ML", width=180, height=45, command=self.show_train_ml).pack(pady=30)

        # Mousewheel
        def _on_mousewheel(event):
            try: canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except: pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def show_time_analysis(self):
        """Displays Time Analysis Page"""
        global cleaned_df
        
        # Clear Screen
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        colors = ThemeManager.get
        content_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))
        self.content_area.create_window(0, 0, window=content_frame, anchor="nw", width=self.root.winfo_width())

        tk.Label(content_frame, text="⏰ TIME ANALYSIS", font=("Segoe UI", 20, "bold"), bg=colors("gradient_start"), fg=colors("text_main")).pack(pady=20)
        
        if cleaned_df is None or 'Hour' not in cleaned_df.columns or 'Reach' not in cleaned_df.columns:
            tk.Label(content_frame, text="⚠️ Data not available for time analysis.", font=("Segoe UI", 14), bg=colors("gradient_start"), fg=colors("danger")).pack(pady=20)
            RoundedButton(content_frame, text="← Back", width=100, height=40, command=self.show_regression_insights).pack(pady=20)
            return

        info_frame = tk.Frame(content_frame, bg="#1F2A44", relief="solid", bd=2)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === BEST TIME BY PLATFORM ===
        platform_times = []
        platforms = cleaned_df['Platform'].unique()
        for plat in sorted(platforms):
            plat_data = cleaned_df[cleaned_df['Platform'] == plat]
            if not plat_data.empty:
                hourly_avg = plat_data.groupby('Hour')['Reach'].mean().sort_values(ascending=False)
                if not hourly_avg.empty:
                    top_hours = sorted(hourly_avg.head(3).index)
                    time_str = " / ".join([f"{int(h)}:00" for h in top_hours])
                    platform_times.append(f"{plat.upper()}: {time_str}")
        
        # === BEST DAYS ===
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if 'Day' in cleaned_df.columns:
            daily_avg = cleaned_df.groupby('Day')['Reach'].mean()
            avg_reach = cleaned_df['Reach'].mean()
            daily_avg = daily_avg.reindex([d for d in day_order if d in daily_avg.index])
            
            best_days_text = "📅 BEST DAYS: "
            if not daily_avg.empty:
                top_days = daily_avg.nlargest(2)
                boosts = []
                for day in top_days.index:
                    boost = ((daily_avg[day] - avg_reach) / avg_reach * 100) if avg_reach > 0 else 0
                    short_day = day[:3]
                    boosts.append(f"{short_day} (+{boost:.0f}%)")
                best_days_text += ", ".join(boosts)
            else:
                best_days_text += "Data unavailable"
        else:
            best_days_text = "Data unavailable"

        # Combine text
        times_lines = ["🔥 BEST POSTING TIMES BY PLATFORM"] + platform_times + ["", best_days_text]
        times_text = "\n".join(times_lines)
        
        tk.Label(info_frame, text=times_text, bg="#1F2A44", fg="#FBBF24", font=("Segoe UI", 11), justify="left").pack(pady=30, padx=30)
        RoundedButton(info_frame, text="← Back", width=100, height=40, command=self.show_regression_insights).pack(pady=20)

    def show_content_strategy(self):
        """Displays Content Strategy Page"""
        global cleaned_df
        
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        colors = ThemeManager.get
        content_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))
        self.content_area.create_window(0, 0, window=content_frame, anchor="nw", width=self.root.winfo_width())

        tk.Label(content_frame, text="📱 CONTENT STRATEGY", font=("Segoe UI", 20, "bold"), bg=colors("gradient_start"), fg=colors("text_main")).pack(pady=20)
        
        if cleaned_df is None or 'Content_Type' not in cleaned_df.columns or 'Reach' not in cleaned_df.columns:
            tk.Label(content_frame, text="⚠️ Data not available for content strategy.", font=("Segoe UI", 14), bg=colors("gradient_start"), fg=colors("danger")).pack(pady=20)
            RoundedButton(content_frame, text="← Back", width=100, height=40, command=self.show_regression_insights).pack(pady=20)
            return

        table_frame = tk.Frame(content_frame, bg="#1F2A44", relief="solid", bd=2)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Headers
        tk.Label(table_frame, text="Content", bg="#2A3A5E", fg="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="nsew")
        tk.Label(table_frame, text="Hashtags", bg="#2A3A5E", fg="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=1, sticky="nsew")
        tk.Label(table_frame, text="Boost", bg="#2A3A5E", fg="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=2, sticky="nsew")

        # Logic
        avg_reach_global = cleaned_df['Reach'].mean()
        content_performance = cleaned_df.groupby('Content_Type')['Reach'].mean().sort_values(ascending=False)
        
        for i, (content_type, avg_reach) in enumerate(content_performance.items(), 1):
            boost_pct = ((avg_reach - avg_reach_global) / avg_reach_global * 100) if avg_reach_global > 0 else 0
            boost_str = f"+{boost_pct:.0f}%"

            content_data = cleaned_df[cleaned_df['Content_Type'] == content_type]
            hashtags_list = ["#SocialMedia"]
            if 'Hashtags' in content_data.columns:
                temp_df = content_data[['Hashtags', 'Reach']].dropna(subset=['Hashtags']).copy()
                if not temp_df.empty:
                    # Simple split logic to find top tags
                    all_tags = []
                    for t in temp_df['Hashtags']:
                        if isinstance(t, str): all_tags.extend(t.replace('#','').split())
                    
                    if all_tags:
                        from collections import Counter
                        top = Counter(all_tags).most_common(3)
                        hashtags_list = [f"#{t[0]}" for t in top]
            
            hashtags_str = " ".join(hashtags_list)

            tk.Label(table_frame, text=content_type, bg="#1E2749", fg=colors("text_main"), font=("Segoe UI", 11)).grid(row=i, column=0, sticky="nsew", padx=2, pady=2)
            tk.Label(table_frame, text=hashtags_str, bg="#1E2749", fg="#FBBF24", font=("Segoe UI", 11)).grid(row=i, column=1, sticky="nsew", padx=2, pady=2)
            tk.Label(table_frame, text=boost_str, bg="#1E2749", fg="#10B981", font=("Segoe UI", 11, "bold")).grid(row=i, column=2, sticky="nsew", padx=2, pady=2)
        
        btn_row = len(content_performance) + 1
        RoundedButton(table_frame, text="← Back", width=100, height=40, command=self.show_regression_insights).grid(row=btn_row, column=0, columnspan=3, pady=20)


    def show_visualization(self):
        """Navigate to visualization page with Full Screen Width Fix"""
        global cleaned_df
        
        # 1. Clear Screen
        self.content_area.delete("all")
        self.content_area._draw_gradient()
        
        # Map Theme Colors
        colors = ThemeManager.get
        PRIMARY_BG = colors("gradient_start") 
        CARD_BG = colors("card_bg")            
        TEXT = colors("text_main")            
        
        # Create the main content container
        content_frame = tk.Frame(self.content_area, bg=PRIMARY_BG)

        window_id = self.content_area.create_window(
            0, 0, window=content_frame, anchor="nw"
        )

        def _resize(event=None):
            self.content_area.itemconfigure(
                window_id,
                width=self.content_area.winfo_width(),
                height=self.content_area.winfo_height()
            )

        self.content_area.bind("<Configure>", _resize)
        self.root.after(0, _resize)

        
        def resize_main_canvas(event):
            canvas_width = event.width
            self.content_area.itemconfig(window_id, width=canvas_width)
        self.content_area.bind("<Configure>", resize_main_canvas)

        # Check for data
        if cleaned_df is None:
            tk.Label(content_frame, text="⚠️ Please upload dataset first", 
                     font=("Segoe UI", 14), bg=PRIMARY_BG, fg=colors("danger")).pack(pady=20)
            return

        # ============================================================
        # 2. SCROLLABLE CONTAINER SETUP
        # ============================================================
        
        scroll_container = tk.Frame(content_frame, bg=PRIMARY_BG)
        scroll_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        v_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
        self.viz_canvas = tk.Canvas(scroll_container, bg=PRIMARY_BG, highlightthickness=0)  # Changed here
        v_scrollbar.pack(side="right", fill="y")
        self.viz_canvas.pack(side="left", fill="both", expand=True) 
        
        self.viz_canvas.configure(yscrollcommand=v_scrollbar.set) 
        v_scrollbar.configure(command=self.viz_canvas.yview)
        
        # The frame actually holding the graphs
        dashboard_inner_frame = tk.Frame(self.viz_canvas, bg=PRIMARY_BG)
        
        # BINDING THE INNER FRAME TO CANVAS WIDTH
        canvas_window = self.viz_canvas.create_window((0, 0), window=dashboard_inner_frame, anchor="nw")

        def on_inner_canvas_configure(event):
            self.viz_canvas.itemconfig(canvas_window, width=event.width)
            
        self.viz_canvas.bind("<Configure>", on_inner_canvas_configure)
        
        # Update scroll region whenever data changes
        dashboard_inner_frame.bind("<Configure>", lambda e: self.viz_canvas.configure(scrollregion=self.viz_canvas.bbox("all")))

        # ============================================================
        # SMOOTH SCROLL LOGIC
        # ============================================================
        def _on_mousewheel(event):
            """Handles mousewheel events for Windows, Mac, and Linux"""
            if self.viz_canvas.winfo_exists():
                # Windows & MacOS (event.delta)
                if hasattr(event, 'delta') and event.delta != 0:
                    # Reverse sign if scrolling feels wrong (some systems differ)
                    if event.delta > 0:
                        self.viz_canvas.yview_scroll(-1, "units") # Scroll Up
                    else:
                        self.viz_canvas.yview_scroll(1, "units")  # Scroll Down
                
                # Linux (event.num)
                elif hasattr(event, 'num'):
                    if event.num == 4:
                        self.viz_canvas.yview_scroll(-1, "units") # Scroll Up
                    elif event.num == 5:
                        self.viz_canvas.yview_scroll(1, "units")  # Scroll Down
        
        def _bind_mousewheel(event):
            """Bind mousewheel to application when entering this area"""
            self.viz_canvas.bind_all("<MouseWheel>", _on_mousewheel) # Windows/Mac
            self.viz_canvas.bind_all("<Button-4>", _on_mousewheel)   # Linux Up
            self.viz_canvas.bind_all("<Button-5>", _on_mousewheel)   # Linux Down
        
        def _unbind_mousewheel(event):
            """Unbind to prevent scrolling other areas when leaving"""
            self.viz_canvas.unbind_all("<MouseWheel>")
            self.viz_canvas.unbind_all("<Button-4>")
            self.viz_canvas.unbind_all("<Button-5>")
        
        # Activate scrolling only when hovering over the dashboard content
        # This prevents the scroll from getting stuck on this page
        dashboard_inner_frame.bind("<Enter>", _bind_mousewheel)
        dashboard_inner_frame.bind("<Leave>", _unbind_mousewheel)
        self.viz_canvas.bind("<Enter>", _bind_mousewheel)
        self.viz_canvas.bind("<Leave>", _unbind_mousewheel)

        # ============================================================
        # 3. DASHBOARD CONTENT
        # ============================================================
        
        # Detect dimensions and save to self for access in update_dashboard
        self.root.update_idletasks()
        screen_width = self.root.winfo_width()
        
        if screen_width <= 600:
            device = "mobile"; self.cols = 1; self.chart_figsize = (5, 4); font_title = 16
        elif screen_width <= 1100:
            device = "tablet"; self.cols = 1; self.chart_figsize = (8, 4.5); font_title = 20
        else:
            device = "desktop"; self.cols = 2; self.chart_figsize = (6, 4.5); font_title = 24

        # Header
        tk.Label(dashboard_inner_frame, text="📊 ANALYTICS DASHBOARD", 
                 font=("Segoe UI", font_title, "bold"),
                 bg=PRIMARY_BG, fg=TEXT).pack(pady=15)
       
        # Selector Frame
        selector_frame = tk.Frame(dashboard_inner_frame, bg="#1F2A44", relief="solid", bd=1)
        selector_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Save platform_var to self so update_dashboard can access it
        self.platform_var = tk.StringVar(value="All Platforms")
        platforms = ["All Platforms"] + sorted(cleaned_df['Platform'].unique().tolist())
        
        tk.Label(selector_frame, text="Filter Platform:", bg="#1F2A44", fg="#FBBF24", font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=10)

        # KPI Container - Save to self
        self.kpi_container = tk.Frame(dashboard_inner_frame, bg=PRIMARY_BG)
        self.kpi_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Chart Container - Save to self
        self.charts_container = tk.Frame(dashboard_inner_frame, bg=PRIMARY_BG)
        self.charts_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Configure Grid
        if self.cols == 2:
            self.charts_container.grid_columnconfigure(0, weight=1)
            self.charts_container.grid_columnconfigure(1, weight=1)
        else:
            self.charts_container.grid_columnconfigure(0, weight=1)

        # Dropdown binding
        try:
            platform_dropdown = ttk.Combobox(selector_frame, textvariable=self.platform_var, values=platforms, state="readonly")
            platform_dropdown.pack(side="left", padx=10, pady=10)
            platform_dropdown.bind("<<ComboboxSelected>>", self.update_dashboard)
        except: pass 

        # Initial Load
        self.update_dashboard()

    def create_kpi(self, parent, c_idx, title, val, icon, color):
        """Helper method to create KPI cards"""
        colors = ThemeManager.get
        CARD_BG = colors("card_bg")
        TEXT = colors("text_main")
        
        card = tk.Frame(parent, bg=CARD_BG, relief="solid", bd=1)
        card.grid(row=0, column=c_idx, sticky="nsew", padx=5)
        parent.grid_columnconfigure(c_idx, weight=1)
        
        tk.Label(card, text=icon, bg=CARD_BG, font=("Segoe UI Emoji", 14)).pack(pady=(10, 2))
        tk.Label(card, text=title, bg=CARD_BG, fg=colors("text_muted"), font=("Segoe UI", 10, "bold")).pack()
        tk.Label(card, text=val, bg=CARD_BG, fg=TEXT, font=("Segoe UI", 16, "bold")).pack(pady=(2, 10))
        tk.Frame(card, bg=color, height=3).pack(fill="x", side="bottom")

    def update_dashboard(self, event=None):
        """Updates the dashboard based on filters"""
        global cleaned_df
        
        # 1. CLEANUP using self.
        for w in self.kpi_container.winfo_children(): w.destroy()
        for w in self.charts_container.winfo_children(): w.destroy()
        plt.close('all')

        colors = ThemeManager.get
        CARD_BG = colors("card_bg")
        TEXT = colors("text_main")

        # 2. DATA FILTERING using self.platform_var
        sel_plat = self.platform_var.get()
        df = cleaned_df.copy()
        
        if sel_plat != "All Platforms":
            df = df[df['Platform'] == sel_plat]

        if len(df) == 0: return

        # 3. KPI CALCULATIONS
        total_posts = len(df)
        avg_eng = df['Engagement_Rate'].mean()
        tot_reach = df['Reach'].sum()

        # --- Peak Time Logic ---
        peak_time = "N/A"
        # Ensure Hour column exists
        if 'Hour' not in df.columns and 'Time' in df.columns:
            try: df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
            except: pass
            
        if 'Hour' in df.columns:
            hourly_perf = df.groupby('Hour')['Reach'].mean()
            if not hourly_perf.empty:
                best_hour = hourly_perf.idxmax()
                am_pm = "AM" if best_hour < 12 else "PM"
                display_hour = best_hour if best_hour <= 12 else best_hour - 12
                if display_hour == 0: display_hour = 12
                peak_time = f"{int(display_hour)}:00 {am_pm}"

        # 4. CREATE KPI CARDS using self.kpi_container
        self.create_kpi(self.kpi_container, 0, "Total Posts", f"{total_posts:,}", "📝", "#10B981")
        self.create_kpi(self.kpi_container, 1, "Avg. Eng. Rate", f"{avg_eng:.2f}%", "📈", "#FBBF24")
        self.create_kpi(self.kpi_container, 2, "Total Reach", f"{tot_reach/1000000:.1f}M", "👥", "#6366F1")
        self.create_kpi(self.kpi_container, 3, "Peak Time", peak_time, "⏰", "#8B5CF6")

        # 5. CHARTS GENERATION
        bg_col, txt_col = CARD_BG, TEXT
        
        # Grid positioning variables
        chart_row = 0
        chart_col = 0

        # Helper to create consistent frames
        def get_chart_frame():
            nonlocal chart_row, chart_col
            # Use self.charts_container here
            frame = tk.Frame(self.charts_container, bg=bg_col, bd=1, relief="solid")
            frame.grid(row=chart_row, column=chart_col, sticky="nsew", padx=5, pady=5)
            
            # Logic to move to next column/row using self.cols
            chart_col += 1
            if chart_col >= self.cols: 
                chart_col = 0
                chart_row += 1
            return frame

        # --- CHART 1: CONTENT DISTRIBUTION (Pie) ---
        f1 = get_chart_frame()
        fig1, ax1 = plt.subplots(figsize=self.chart_figsize, dpi=100)
        
        content_counts = df['Content_Type'].value_counts()
        colors1 = ["#003f5c", "#665191", "#38BDF8", "#A855F7"]
        
        wedges, texts, autotexts = ax1.pie(
            content_counts, labels=content_counts.index, 
            autopct='%1.1f%%', startangle=90, 
            colors=colors1[:len(content_counts)],
            textprops={'color': txt_col}
        )
        for text in autotexts: text.set_color('white') # Make % white
        
        ax1.set_title("Content Distribution", color=txt_col, fontweight="bold", fontsize=12, pad=10)
        fig1.patch.set_facecolor(bg_col)
        
        canvas1 = FigureCanvasTkAgg(fig1, f1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

        # --- CHART 2: ENGAGEMENT BY DAY (Bar) ---
        f2 = get_chart_frame()
        fig2, ax2 = plt.subplots(figsize=self.chart_figsize, dpi=100)
        
        # FIX: Check for 'Days' instead of 'Day'
        if 'Days' in df.columns:
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            # Only include days that exist in the filtered data
            existing_days = [d for d in day_order if d in df['Days'].unique()]
            
            # FIX: Group by 'Days' instead of 'Day'
            day_data = df.groupby('Days')['Engagement_Rate'].mean().reindex(existing_days)
            
            ax2.bar([str(d)[:3] for d in day_data.index], day_data.values, color="#38BDF8")
        
        ax2.set_title("Avg Engagement by Day", color=txt_col, fontweight="bold", fontsize=12, pad=10)
        ax2.set_xlabel("Day of Week", color=txt_col, fontsize=10, fontweight="bold")
        ax2.set_ylabel("Engagement Rate (%)", color=txt_col, fontsize=10, fontweight="bold")
        ax2.tick_params(colors=txt_col)
        ax2.spines['bottom'].set_color(txt_col)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(txt_col)
        ax2.set_facecolor(bg_col)
        fig2.patch.set_facecolor(bg_col)
        
        canvas2 = FigureCanvasTkAgg(fig2, f2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

        # --- CHART 3: MONTHLY TREND (Line) ---
        f3 = get_chart_frame()
        fig3, ax3 = plt.subplots(figsize=self.chart_figsize, dpi=100)
        
        if 'Month' in df.columns:
            month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            m_data = df.groupby('Month')['Engagement_Rate'].mean().reindex(month_order).dropna()
            
            ax3.plot(m_data.index, m_data.values, color="#38BDF8", marker='o', linewidth=2, markersize=6)
            # FIX: Set ticks first, then labels
            ax3.set_xticks(range(len(m_data.index)))
            ax3.set_xticklabels(m_data.index, rotation=45, ha='right')  # Added ha='right' for better alignment
        
        ax3.set_title("Monthly Trend", color=txt_col, fontweight="bold", fontsize=12, pad=10)
        ax3.set_xlabel("Month", color=txt_col, fontsize=10, fontweight="bold")
        ax3.set_ylabel("Engagement Rate (%)", color=txt_col, fontsize=10, fontweight="bold")
        ax3.tick_params(colors=txt_col)
        ax3.spines['bottom'].set_color(txt_col)
        ax3.spines['left'].set_color(txt_col)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.set_facecolor(bg_col)
        fig3.patch.set_facecolor(bg_col)
        
        # FIX: Add tight_layout to prevent label cutoff
        fig3.tight_layout()
        
        canvas3 = FigureCanvasTkAgg(fig3, f3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

        # --- CHART 4: TOP HASHTAGS (Horizontal Bar) ---
        f4 = get_chart_frame()
        fig4, ax4 = plt.subplots(figsize=self.chart_figsize, dpi=100)
        
        has_data = False
        if 'Hashtags' in df.columns and 'Reach' in df.columns:
            try:
                # Split hashtags, explode them to new rows, and calculate mean Reach
                tags_exploded = df.assign(Hashtag=df['Hashtags'].str.split()).explode('Hashtag')
                if not tags_exploded.empty:
                    top_tags = tags_exploded.groupby('Hashtag')['Reach'].mean().nlargest(5).sort_values()
                    
                    if not top_tags.empty:
                        bars = ax4.barh(top_tags.index, top_tags.values, color="#A855F7", alpha=0.8)
                        
                        # ✨ NEW: Add value labels at the right side of each bar
                        for i, (hashtag, value) in enumerate(top_tags.items()):
                            # Format the value as full number with comma separators
                            label = f'{int(value):,}'
                            
                            # Position text at the end of the bar with some padding
                            ax4.text(value, i, f'  {label}', 
                                    va='center', ha='left',
                                    color=txt_col, fontweight='bold', 
                                    fontsize=9)
                        
                        # Format x-axis as K (thousands)
                        ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}K'))
                        has_data = True
            except: pass
        
        if not has_data:
            ax4.text(0.5, 0.5, "No Hashtag Data", ha='center', va='center', color=txt_col)
        
        ax4.set_title("Top Hashtags (by Reach)", color=txt_col, fontweight="bold", fontsize=12, pad=10)
        ax4.set_xlabel("Average Reach", color=txt_col, fontsize=10, fontweight="bold")
        ax4.set_ylabel("Hashtag", color=txt_col, fontsize=10, fontweight="bold")
        ax4.tick_params(colors=txt_col)
        ax4.spines['bottom'].set_color(txt_col)
        ax4.spines['left'].set_color(txt_col)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.set_facecolor(bg_col)
        fig4.patch.set_facecolor(bg_col)
        
        canvas4 = FigureCanvasTkAgg(fig4, f4)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

        # FIX: Force update of scroll region to show all charts
        self.root.update_idletasks()
        self.viz_canvas.configure(scrollregion=self.viz_canvas.bbox("all"))

    def show_table(self, dataframe, title="Data Preview"):
        """Display dataframe in a table view - Full Screen Fix"""
        # 1. Clear previous content
        self.content_area.delete("all")
        self.content_area._draw_gradient()

        colors = ThemeManager.get

        # 2. Create the Main Frame
        main_frame = tk.Frame(self.content_area, bg=colors("gradient_start"))

        # 3. Create a window item on the canvas
        # We save the ID (window_id) so we can resize it later
        window_id = self.content_area.create_window(0, 0, window=main_frame, anchor="nw")

        # 4. DYNAMIC RESIZING FUNCTION
        # This function forces the main_frame to exactly match the canvas size
        def resize_frame(event):
            canvas_width = event.width
            canvas_height = event.height
            self.content_area.itemconfig(window_id, width=canvas_width, height=canvas_height)

        # Bind the resize event to the Content Area (Canvas)
        self.content_area.bind("<Configure>", resize_frame)

        # 5. Header Section
        header_frame = tk.Frame(main_frame, bg=colors("gradient_start"))
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        tk.Label(header_frame, text=f"📋 {title}", 
                 font=("Segoe UI", 20, "bold"),
                 bg=colors("gradient_start"), 
                 fg=colors("text_main")).pack(side="left")

        # 6. Table Container (The 'Card' look)
        table_container = tk.Frame(main_frame, bg=colors("card_bg"))
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 7. Scrollbars (Added Horizontal Scrollbar for wide data)
        y_scroll = ttk.Scrollbar(table_container, orient="vertical")
        x_scroll = ttk.Scrollbar(table_container, orient="horizontal")

        # 8. Treeview Configuration
        cols = list(dataframe.columns)
        tree = ttk.Treeview(table_container, columns=cols, show='headings',
                            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)

        # 9. Layout - Pack tree to fill available space
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        # 10. Column Styling
        for col in cols:
            tree.heading(col, text=col, anchor="w")
            # Set a minimum width but allow expansion
            tree.column(col, width=120, minwidth=100, anchor="w")

        # 11. Data Insertion (Limit to 100 rows for preview performance)
        for idx, row in dataframe.head(100).iterrows():
            tree.insert('', 'end', values=list(row))
            
        # Force an update of the GUI tasks to get accurate dimensions immediately
        self.content_area.update_idletasks()
        
        # Get the current width and height of the content area
        current_w = self.content_area.winfo_width()
        current_h = self.content_area.winfo_height()
        
        # If valid dimensions exist, apply them to the window item right now
        if current_w > 1 and current_h > 1:
            self.content_area.itemconfig(window_id, width=current_w, height=current_h)

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    app = SocialAnalyticsApp(root)
    root.mainloop()