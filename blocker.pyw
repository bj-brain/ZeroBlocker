import customtkinter as ctk
import tkinter.messagebox as messagebox
import ctypes
import sys
import os
import webbrowser

# --- 60-30-10 UI/UX Color Rule Definitions (Light Mode, Dark Mode) ---
# 60% - Main App Background
COLOR_60 = ("#F4F4F5", "#121212") 
# 30% - Sidebar, Cards, and Elevated Elements
COLOR_30 = ("#FFFFFF", "#1E1E1E") 
# 10% - Primary Accent Color
COLOR_10 = "#029CFF" 

# Text Colors
TEXT_MAIN = ("#18181B", "#F4F4F5")
TEXT_SUB = ("#52525B", "#A1A1AA")
DANGER = "#EF4444"

# Typography
FONT_HEADING = ("Segoe UI Variable Display", 24, "bold")
FONT_SUBHEADING = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 13)
FONT_BTN = ("Segoe UI", 14, "bold")

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"

# --- Popular Presets Data ---
PRESETS = {
    "Social Media": ["facebook.com", "instagram.com", "twitter.com", "tiktok.com"],
    "Video & Streaming": ["youtube.com", "netflix.com", "hulu.com", "twitch.tv"],
    "Gaming": ["roblox.com", "discord.com", "steampowered.com", "epicgames.com"],
    "Productivity Killers": ["reddit.com", "pinterest.com", "9gag.com", "tumblr.com"]
}

class FocusBlockerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZeroBlock")
        self.geometry("850x580")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("System")
        self.configure(fg_color=COLOR_60)

        # Main Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar (30%) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_30)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1) 

        self.logo = ctk.CTkLabel(self.sidebar, text="ZeroBlock", font=("Segoe UI Variable Display", 26, "bold"), text_color=COLOR_10)
        self.logo.grid(row=0, column=0, padx=20, pady=(25, 35), sticky="w")

        # Sidebar Navigation
        self.btn_home = self.create_nav_btn("Home", 1, self.show_home)
        self.btn_blocked = self.create_nav_btn("Currently Blocked", 2, self.show_blocked)
        self.btn_presets = self.create_nav_btn("Popular Sites", 3, self.show_presets)
        self.btn_trouble = self.create_nav_btn("Troubleshooting", 4, self.show_troubleshooting)
        self.btn_about = self.create_nav_btn("About", 7, self.show_about) 

        # --- Content Frames ---
        self.frames = {}
        for name in ["Home", "Blocked", "Presets", "Trouble", "About"]:
            self.frames[name] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # --- Initialize Views ---
        self.entry_fields = []
        self.setup_home_frame()
        self.setup_blocked_frame()
        self.setup_presets_frame()
        self.setup_trouble_frame()
        self.setup_about_frame()

        self.show_home() # Default View

    def create_nav_btn(self, text, row, command):
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", text_color=TEXT_SUB,
                            hover_color=COLOR_60, anchor="w", font=FONT_BTN, command=command, corner_radius=6)
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        return btn

    def select_nav_btn(self, selected_btn):
        for btn in [self.btn_home, self.btn_blocked, self.btn_presets, self.btn_trouble, self.btn_about]:
            btn.configure(fg_color="transparent", text_color=TEXT_SUB)
        selected_btn.configure(fg_color=COLOR_10, text_color="#FFFFFF")

    def hide_all_frames(self):
        for frame in self.frames.values():
            frame.grid_forget()

    # --- Routing ---
    def show_home(self):
        self.hide_all_frames()
        self.select_nav_btn(self.btn_home)
        self.frames["Home"].grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

    def show_blocked(self):
        self.hide_all_frames()
        self.select_nav_btn(self.btn_blocked)
        self.refresh_blocked_list()
        self.frames["Blocked"].grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

    def show_presets(self):
        self.hide_all_frames()
        self.select_nav_btn(self.btn_presets)
        self.frames["Presets"].grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

    def show_troubleshooting(self):
        self.hide_all_frames()
        self.select_nav_btn(self.btn_trouble)
        self.frames["Trouble"].grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

    def show_about(self):
        self.hide_all_frames()
        self.select_nav_btn(self.btn_about)
        self.frames["About"].grid(row=0, column=1, sticky="nsew", padx=35, pady=35)

    # --- 1. Home View (+ Dynamic Inputs) ---
    def setup_home_frame(self):
        frame = self.frames["Home"]
        ctk.CTkLabel(frame, text="Block Distracting Websites", font=FONT_HEADING, text_color=TEXT_MAIN).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(frame, text="Add URLs to your local blocklist to redirect distracting domains instantly.", font=FONT_BODY, text_color=TEXT_SUB, wraplength=500, justify="left").pack(anchor="w", pady=(0, 25))

        self.home_scroll = ctk.CTkScrollableFrame(frame, width=500, height=220, fg_color="transparent")
        self.home_scroll.pack(anchor="w", fill="x", pady=(0, 15))
        
        self.add_input_row()

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(anchor="w", fill="x")

        ctk.CTkButton(btn_frame, text="+ Add Website", command=self.add_input_row, 
                      fg_color=COLOR_30, text_color=TEXT_MAIN, hover_color=COLOR_60, border_width=1, border_color=COLOR_10, font=FONT_BTN, width=140, height=40).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_frame, text="Block All Added", command=self.process_home_blocks, 
                      fg_color=COLOR_10, hover_color="#0284D8", font=FONT_BTN, width=140, height=40).pack(side="left")

    def add_input_row(self):
        row = ctk.CTkFrame(self.home_scroll, fg_color="transparent")
        row.pack(fill="x", pady=5)
        entry = ctk.CTkEntry(row, width=400, height=40, font=("Segoe UI", 14), placeholder_text="e.g., facebook.com", corner_radius=8, border_color=COLOR_30)
        entry.pack(side="left")
        self.entry_fields.append(entry)

    def process_home_blocks(self):
        sites = [e.get() for e in self.entry_fields if e.get().strip()]
        if sites:
            self.block_sites(sites)
            for e in self.entry_fields: e.delete(0, 'end')

    # --- 2. Currently Blocked View (Cards) ---
    def setup_blocked_frame(self):
        frame = self.frames["Blocked"]
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(header, text="Currently Blocked", font=FONT_HEADING, text_color=TEXT_MAIN).pack(side="left")
        self.lbl_blocked_count = ctk.CTkLabel(frame, text="0 websites in list", font=FONT_BODY, text_color=TEXT_SUB)
        self.lbl_blocked_count.pack(anchor="w", pady=(0, 15))

        self.scroll_blocked = ctk.CTkScrollableFrame(frame, width=500, height=300, fg_color="transparent")
        self.scroll_blocked.pack(anchor="w", fill="both", expand=True, pady=(0, 15))

        ctk.CTkButton(frame, text="Clear All Blocks", command=self.clear_all_blocks, 
                      fg_color=DANGER, hover_color="#DC2626", font=FONT_BTN, width=150, height=40).pack(anchor="w")

    def refresh_blocked_list(self):
        for widget in self.scroll_blocked.winfo_children(): widget.destroy()
        sites = self.get_blocked_sites()
        self.lbl_blocked_count.configure(text=f"{len(sites)} websites in list")

        for site in sorted(sites):
            # 30% Space Card UI
            card = ctk.CTkFrame(self.scroll_blocked, fg_color=COLOR_30, corner_radius=8)
            card.pack(fill="x", pady=6, ipady=8)
            
            ctk.CTkLabel(card, text=site, font=FONT_SUBHEADING, text_color=TEXT_MAIN).pack(side="left", padx=20)
            ctk.CTkButton(card, text="Unblock", width=90, height=30, fg_color="transparent", text_color=DANGER, border_width=1, border_color=DANGER,
                          command=lambda s=site: self.unblock_single_site(s)).pack(side="right", padx=20)

    # --- 3. Popular Sites View (Grouped) ---
    def setup_presets_frame(self):
        frame = self.frames["Presets"]
        ctk.CTkLabel(frame, text="Popular Sites", font=FONT_HEADING, text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(frame, text="Quickly block specific domains from popular categories.", font=FONT_BODY, text_color=TEXT_SUB).pack(anchor="w", pady=(0, 15))

        scroll = ctk.CTkScrollableFrame(frame, width=500, height=400, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for category, sites in PRESETS.items():
            # Category Header
            cat_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            cat_frame.pack(fill="x", pady=(15, 5))
            ctk.CTkLabel(cat_frame, text=category, font=FONT_SUBHEADING, text_color=COLOR_10).pack(side="left")
            ctk.CTkButton(cat_frame, text="Block Entire Category", width=140, height=28, fg_color=COLOR_10, font=("Segoe UI", 12, "bold"),
                          command=lambda s=sites: self.block_sites(s)).pack(side="right")
            
            # Individual Site Cards
            for site in sites:
                card = ctk.CTkFrame(scroll, fg_color=COLOR_30, corner_radius=6)
                card.pack(fill="x", pady=3, ipady=4)
                ctk.CTkLabel(card, text=site, font=FONT_BODY, text_color=TEXT_MAIN).pack(side="left", padx=20)
                ctk.CTkButton(card, text="Block", width=70, height=26, fg_color="transparent", border_width=1, border_color=TEXT_SUB, text_color=TEXT_MAIN,
                              command=lambda s=site: self.block_sites([s])).pack(side="right", padx=20)

    # --- 4. Troubleshooting View ---
    def setup_trouble_frame(self):
        frame = self.frames["Trouble"]
        ctk.CTkLabel(frame, text="Troubleshooting & Verification", font=FONT_HEADING, text_color=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkLabel(frame, text="How do I verify it works?", font=FONT_SUBHEADING, text_color=COLOR_10).pack(anchor="w", pady=(0, 5))
        ans1 = "Open your browser in incognito mode (to bypass browser caching) and attempt to navigate to any blocked website. You should see a 'This site can't be reached' error."
        ctk.CTkLabel(frame, text=ans1, font=FONT_BODY, text_color=TEXT_SUB, wraplength=480, justify="left").pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(frame, text="Is this safe to run?", font=FONT_SUBHEADING, text_color=COLOR_10).pack(anchor="w", pady=(0, 5))
        ans2 = "Absolutely. Modifying the local hosts file is a standard network engineering practice. The generated script runs on your machine only and contains zero background processes."
        ctk.CTkLabel(frame, text=ans2, font=FONT_BODY, text_color=TEXT_SUB, wraplength=480, justify="left").pack(anchor="w")

    # --- 5. About Us View ---
    def setup_about_frame(self):
        frame = self.frames["About"]
        ctk.CTkLabel(frame, text="About", font=FONT_HEADING, text_color=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # Name
        ctk.CTkLabel(frame, text="Baanujan Vijayarajan", font=("Segoe UI Variable Display", 20, "bold"), text_color=COLOR_10).pack(anchor="w")
        
        # Bio Profile
        bio = ("Software engineering and cybersecurity student currently pursuing studies at BCAS Campus and "
               "Goldsmiths, University of London. Passionate about full-stack development, AI security research, "
               "and building efficient, local utility tools.")
        ctk.CTkLabel(frame, text=bio, font=FONT_BODY, text_color=TEXT_SUB, wraplength=480, justify="left").pack(anchor="w", pady=(10, 25))
        
        # Clean Button Links
        links_frame = ctk.CTkFrame(frame, fg_color="transparent")
        links_frame.pack(anchor="w", fill="x")

        btn_li = ctk.CTkButton(links_frame, text="🔗 LinkedIn", fg_color=COLOR_30, text_color=TEXT_MAIN, hover_color=COLOR_60, font=FONT_BTN, width=140, height=40)
        btn_li.pack(side="left", padx=(0, 15))
        btn_li.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/baanujan-vijayarajan/"))

        btn_gh = ctk.CTkButton(links_frame, text="💻 GitHub", fg_color=COLOR_30, text_color=TEXT_MAIN, hover_color=COLOR_60, font=FONT_BTN, width=140, height=40)
        btn_gh.pack(side="left")
        btn_gh.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bj-brain/"))

    # --- Core OS Networking Logic ---
    def clean_url(self, url):
        return url.replace("https://", "").replace("http://", "").replace("www.", "").strip()

    def get_blocked_sites(self):
        blocked = set()
        try:
            with open(HOSTS_PATH, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(REDIRECT_IP) and "localhost" not in line.lower():
                        parts = line.split()
                        if len(parts) >= 2:
                            blocked.add(parts[1].replace("www.", ""))
        except Exception: pass
        return list(blocked)

    def block_sites(self, site_list):
        cleaned = [self.clean_url(s) for s in site_list if s.strip()]
        if not cleaned: return
        try:
            with open(HOSTS_PATH, 'r+') as file:
                content = file.read()
                added = 0
                for site in cleaned:
                    if site not in content:
                        file.write(f"\n{REDIRECT_IP} www.{site}")
                        file.write(f"\n{REDIRECT_IP} {site}\n")
                        added += 1
            if added > 0:
                os.system("ipconfig /flushdns")
                messagebox.showinfo("Success", f"Blocked {added} domain(s) successfully.")
            else:
                messagebox.showinfo("Notice", "Domains are already blocked.")
        except PermissionError: messagebox.showerror("Permission Denied", "Administrator rights required.")

    def unblock_single_site(self, site):
        try:
            with open(HOSTS_PATH, 'r') as file: lines = file.readlines()
            with open(HOSTS_PATH, 'w') as file:
                for line in lines:
                    if f"{REDIRECT_IP} {site}" not in line and f"{REDIRECT_IP} www.{site}" not in line:
                        file.write(line)
            os.system("ipconfig /flushdns")
            self.refresh_blocked_list() # Instantly refresh UI
        except PermissionError: messagebox.showerror("Permission Denied", "Administrator rights required.")

    def clear_all_blocks(self):
        try:
            with open(HOSTS_PATH, 'r') as file: lines = file.readlines()
            with open(HOSTS_PATH, 'w') as file:
                for line in lines:
                    if not line.strip().startswith(REDIRECT_IP) or "localhost" in line.lower():
                        file.write(line)
            os.system("ipconfig /flushdns")
            messagebox.showinfo("Success", "All domains unblocked.")
            self.refresh_blocked_list()
        except PermissionError: messagebox.showerror("Permission Denied", "Administrator rights required.")

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if __name__ == "__main__":
    if is_admin():
        app = FocusBlockerApp()
        app.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)