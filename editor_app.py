import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
# ADDED ImageFilter for the blur effect
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

# =================CONFIGURATION=================
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# File Paths
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
POSTER_TEMPLATE_PATH = os.path.join(ASSETS_DIR, "Winners Poster.png")

# FONTS
FONT_PATH = os.path.join(ASSETS_DIR, "ChromiumOne.otf")
FONT_PATH_EDITION = os.path.join(ASSETS_DIR, "Montserrat.ttf")

# --- POSTER CONFIGURATION ---
POSTER_EDITION_POS = (0.783, 0.2835)
EDITION_GRADIENT_TOP = "#f6b715"
EDITION_GRADIENT_BOTTOM = "#ff7b00"

POSTER_LAYOUT = {
    1: {"pos": (0.50, 0.480), "width_limit": 0.265, "max_font": 80},
    2: {"pos": (0.185, 0.5785), "width_limit": 0.225, "max_font": 70},
    3: {"pos": (0.815, 0.579), "width_limit": 0.225, "max_font": 70},
}

# --- Professional Theme Colors (GUI) ---
BG_COLOR = "#000000"
FG_COLOR = "#FFFFFF"
ACCENT_LIGHT = "#02ccfe"
ACCENT_DARK = "#000435"
BUTTON_TEXT = "#000000"

# --- NEW METALLIC & GLOW COLORS ---
GOLD_TOP = "#ffd700"
GOLD_BOTTOM = "#e0a800"
GOLD_GLOW = "#ffec8b"  # Bright yellow-gold glow

SILVER_TOP = "#e8e8e8"
SILVER_BOTTOM = "#8c8c8c"
SILVER_GLOW = "#ffffff"  # White glow

BRONZE_TOP = "#e3a857"
BRONZE_BOTTOM = "#8c5324"
BRONZE_GLOW = "#ffc880"  # Peachy-orange glow

RANK_DATA = {
    1: {"file_key": "1st", "medal": os.path.join(ASSETS_DIR, "medal_1.png"),
        "grad_top": GOLD_TOP, "grad_bottom": GOLD_BOTTOM, "glow_color": GOLD_GLOW,
        "color": "#ffc000", "suffix": "1st place edit.png"},
    2: {"file_key": "2nd", "medal": os.path.join(ASSETS_DIR, "medal_2.png"),
        "grad_top": SILVER_TOP, "grad_bottom": SILVER_BOTTOM, "glow_color": SILVER_GLOW,
        "color": "#9e9e9e", "suffix": "2nd place edit.png"},
    3: {"file_key": "3rd", "medal": os.path.join(ASSETS_DIR, "medal_3.png"),
        "grad_top": BRONZE_TOP, "grad_bottom": BRONZE_BOTTOM, "glow_color": BRONZE_GLOW,
        "color": "#cd7f32", "suffix": "3rd place edit.png"},
}

# Sizing Configuration
MAX_FONT_SIZE_PHOTO = 500
MEDAL_SCALE_RATIO = 0.35
LOGO_SCALE_RATIO = 0.50
TEXT_BOTTOM_PADDING_RATIO = 0.15
TEXT_SIDE_PADDING_RATIO = 0.03
SIDE_PADDING_RATIO = -0.03


# ===============================================

def load_image(path):
    print(f"Processing file: {path}...")
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        return img.convert("RGBA")
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return None


# --- Drawing Functions ---

def draw_centered_solid_text(base_image, text, center_x_ratio, center_y_ratio, max_width_ratio, hex_color, max_font=500,
                             font_path=None):
    """Standard solid-color text (for Poster team names)."""
    draw = ImageDraw.Draw(base_image)
    W, H = base_image.size
    if font_path is None: font_path = FONT_PATH
    center_x, center_y = W * center_x_ratio, H * center_y_ratio
    max_pixels = W * max_width_ratio
    font_size = max_font
    font = None
    while font_size > 5:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            return
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_pixels: break
        font_size -= 2
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x_pos, y_pos = center_x - (text_width / 2), center_y - (text_height / 2)
    shadow_offset = max(1, int(font_size * 0.04))
    draw.text((x_pos + shadow_offset, y_pos + shadow_offset), text, font=font, fill="#000000")
    draw.text((x_pos, y_pos), text, font=font, fill=hex_color)


def draw_gradient_text_centered(base_image, text, center_x_ratio, center_y_ratio, max_width_ratio, top_color,
                                bottom_color, max_font=30, font_path=None):
    """Gradient text (for Poster Edition #)."""
    W, H = base_image.size
    if font_path is None: font_path = FONT_PATH
    draw_dummy = ImageDraw.Draw(base_image)
    max_pixels = W * max_width_ratio
    font_size = max_font
    font = None
    while font_size > 5:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            return
        bbox = draw_dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_pixels: break
        font_size -= 2
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x_pos = int((W * center_x_ratio) - (text_width / 2))
    y_pos = int((H * center_y_ratio) - (text_height / 2))

    shadow_offset = max(1, int(font_size * 0.06))
    draw_dummy.text((x_pos + shadow_offset, y_pos + shadow_offset), text, font=font, fill="#000000")

    pad = 10
    mask_w, mask_h = text_width + (pad * 2), text_height + (pad * 2)
    mask_img = Image.new('L', (mask_w, mask_h), 0)
    draw_mask = ImageDraw.Draw(mask_img)
    draw_mask.text((pad, pad), text, font=font, fill=255)

    color_block = Image.new('RGB', (1, 5))
    draw_color = ImageDraw.Draw(color_block)
    draw_color.rectangle((0, 0, 0, 3), fill=top_color)
    draw_color.point((0, 4), fill=bottom_color)
    gradient_fill = color_block.resize((mask_w, mask_h), resample=Image.Resampling.BILINEAR)
    gradient_fill.putalpha(mask_img)
    base_image.paste(gradient_fill, (x_pos - pad, y_pos - pad), gradient_fill)


# --- NEW: SHINY & GLOWING TEXT FUNCTION ---
def draw_shiny_text_bottom(base_image, text, top_color, bottom_color, glow_color):
    """Draws bottom-aligned text with Glow + Shadow + Metallic Gradient."""
    W, H = base_image.size
    draw_dummy = ImageDraw.Draw(base_image)
    max_text_width = W * (1 - (TEXT_SIDE_PADDING_RATIO * 2))
    font_size = MAX_FONT_SIZE_PHOTO
    font = None

    # 1. Calculate Size & Position
    while font_size > 50:
        try:
            font = ImageFont.truetype(FONT_PATH, font_size)
        except OSError:
            return
        bbox = draw_dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_text_width: break
        font_size -= 10
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x_pos = int((W - text_width) // 2)
    y_pos = int(H - (H * TEXT_BOTTOM_PADDING_RATIO) - text_height)

    # --- LAYER 1: THE GLOW (Back) ---
    # Dynamic blur radius based on font size
    blur_radius = int(font_size * 0.12)
    # Padding needed to accommodate the blur spreading out
    glow_pad = blur_radius + 20
    glow_w, glow_h = text_width + glow_pad * 2, text_height + glow_pad * 2

    # Create separate canvas for glow
    glow_canvas = Image.new('RGBA', (glow_w, glow_h), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow_canvas)
    # Draw solid text in glow color
    draw_glow.text((glow_pad, glow_pad), text, font=font, fill=glow_color)
    # Apply strong blur
    glow_blurred = glow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))
    # Paste glow layer first (offset by padding)
    base_image.paste(glow_blurred, (x_pos - glow_pad, y_pos - glow_pad), glow_blurred)

    # --- LAYER 2: SHARP SHADOW (Middle) ---
    shadow_offset = int(font_size * 0.04)
    draw_dummy.text((x_pos + shadow_offset, y_pos + shadow_offset), text, font=font, fill="#000000")

    # --- LAYER 3: METALLIC GRADIENT (Front) ---
    grad_pad = 10
    mask_w, mask_h = text_width + grad_pad * 2, text_height + grad_pad * 2
    mask_img = Image.new('L', (mask_w, mask_h), 0)
    draw_mask = ImageDraw.Draw(mask_img)
    draw_mask.text((grad_pad, grad_pad), text, font=font, fill=255)

    grad_source = Image.new('RGB', (1, 2))
    draw_grad = ImageDraw.Draw(grad_source)
    draw_grad.point((0, 0), fill=top_color)
    draw_grad.point((0, 1), fill=bottom_color)
    gradient_fill = grad_source.resize((mask_w, mask_h), resample=Image.Resampling.BILINEAR)
    gradient_fill.putalpha(mask_img)

    # Paste gradient layer last
    base_image.paste(gradient_fill, (x_pos - grad_pad, y_pos - grad_pad), gradient_fill)


# --- GUI & Main Logic ---
def get_inputs(root):
    dialog = tk.Toplevel(root)
    dialog.title("Enter Edition & Teams")
    win_w, win_h = 500, 300
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    dialog.geometry(f"{win_w}x{win_h}+{int((screen_w - win_w) / 2)}+{int((screen_h - win_h) / 2)}")
    dialog.configure(bg=BG_COLOR)
    tk.Label(dialog, text="E N T E R   D A T A", bg=BG_COLOR, fg=ACCENT_LIGHT, font=("Segoe UI", 12, "bold")).pack(
        pady=(20, 5))
    text_box = tk.Text(dialog, height=4, width=40, bg=ACCENT_DARK, fg=FG_COLOR, insertbackground=ACCENT_LIGHT,
                       font=("Consolas", 14), bd=0, padx=15, pady=10)
    text_box.pack(pady=10)
    text_box.focus_set()

    def check_lines(event):
        if event.keysym in ("BackSpace", "Delete"): return
        if event.keysym == "Return" and (text_box.get("1.0", "end-1c").count("\n") + 1) >= 4: return "break"

    text_box.bind("<KeyPress>", check_lines)
    result = None

    def on_submit():
        content = text_box.get("1.0", tk.END).strip()
        if content:
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            cleaned = [l.split('.', 1)[-1].strip() if '.' in l and l.split('.', 1)[0].isdigit() else l for l in lines]
            if len(cleaned) >= 4:
                nonlocal result; result = {"edition": cleaned[0], "teams": cleaned[1:4]}; dialog.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter exactly 4 lines.")
        else:
            messagebox.showwarning("Input Error", "Box is empty.")

    tk.Button(dialog, text="PROCESS ALL", command=on_submit, bg=ACCENT_LIGHT, fg=BUTTON_TEXT, activebackground=FG_COLOR,
              activeforeground=BUTTON_TEXT, font=("Helvetica", 11, "bold"), bd=0, padx=30, pady=12,
              cursor="hand2").pack(pady=15)
    root.wait_window(dialog)
    return result


def process_poster(edition, teams, output_folder):
    print("Processing Poster...")
    try:
        poster = Image.open(POSTER_TEMPLATE_PATH).convert("RGBA")
    except FileNotFoundError:
        print("Poster template not found."); return
    draw_gradient_text_centered(poster, edition, POSTER_EDITION_POS[0], POSTER_EDITION_POS[1], 0.20,
                                EDITION_GRADIENT_TOP, EDITION_GRADIENT_BOTTOM, max_font=32, font_path=FONT_PATH_EDITION)
    for i in range(3):
        rank = i + 1;
        config = RANK_DATA[rank];
        layout = POSTER_LAYOUT[rank]
        draw_centered_solid_text(poster, teams[i].upper(), layout["pos"][0], layout["pos"][1], layout["width_limit"],
                                 config["color"], max_font=layout["max_font"])
    poster.save(os.path.join(output_folder, "Winners Poster Edit.png"))
    print("Saved Poster.")


def main():
    root = tk.Tk();
    root.withdraw()
    files = filedialog.askopenfilenames(title="Select 3 photos",
                                        filetypes=[("Images", "*.jpg *.jpeg *.png"), ("All Files", "*.*")])
    if not files: return
    selected = {}
    for p in files:
        if "1st" in os.path.basename(p).lower():
            selected[1] = p
        elif "2nd" in os.path.basename(p).lower():
            selected[2] = p
        elif "3rd" in os.path.basename(p).lower():
            selected[3] = p
    if len(selected) != 3: messagebox.showerror("Error", "Need 1st, 2nd, and 3rd place files."); return
    data = get_inputs(root)
    if not data: return
    edition, teams = data["edition"], data["teams"]
    out_dir = os.path.dirname(selected[1])
    print("\nStarting Processing...")
    for rank in range(1, 4):
        cfg = RANK_DATA[rank]
        print(f"--- Processing Rank {rank} ---")
        base = load_image(selected[rank])
        if base is None: continue
        W, H = base.size
        try:
            logo, medal = Image.open(LOGO_PATH).convert("RGBA"), Image.open(cfg["medal"]).convert("RGBA")
        except FileNotFoundError:
            return

        def resize(img, w):
            return img.resize((w, int(img.height * (w / img.width))), Image.Resampling.LANCZOS)

        r_medal, r_logo = resize(medal, int(W * MEDAL_SCALE_RATIO)), resize(logo, int(W * LOGO_SCALE_RATIO))
        my, ly = (r_medal.size[1] - r_logo.size[1]) // 2, 0 if r_logo.size[1] < r_medal.size[1] else (r_logo.size[1] -
                                                                                                      r_medal.size[
                                                                                                          1]) // 2
        sp = int(W * SIDE_PADDING_RATIO)
        base.paste(r_medal, (sp, my), r_medal);
        base.paste(r_medal, (W - r_medal.size[0] - sp, my), r_medal)
        base.paste(r_logo, ((W - r_logo.size[0]) // 2, ly), r_logo)

        # DRAW GLOWING METALLIC TEXT
        draw_shiny_text_bottom(base, teams[rank - 1].upper(), cfg["grad_top"], cfg["grad_bottom"], cfg["glow_color"])

        base.save(os.path.join(out_dir, cfg["suffix"]))
    process_poster(edition, teams, out_dir)
    messagebox.showinfo("Success", "All files processed!")


if __name__ == "__main__":
    main()