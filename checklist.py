import csv
import pygame
import textwrap
import sys
import os
import win32gui
import win32con
import win32api
import win32ui
import win32com.shell.shell as shell
import win32com.shell.shellcon as shellcon
from ctypes import windll, create_unicode_buffer, sizeof, byref, c_int
import tkinter as tk
from tkinter import filedialog
import subprocess

# ──────────────────────────────────────────────────────────────────────────────
# 1) PYGAME INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────

# Initialize tkinter for file dialog
root = tk.Tk()
root.withdraw()  # Hide the main window

pygame.init()

# Starting window size
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700

# Create a borderless window
screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.NOFRAME
)
pygame.display.set_caption("Custom Frameless CSV Checklist")

# Get window handle
hwnd = win32gui.GetForegroundWindow()

# Set window styles
style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
style = style & ~win32con.WS_CAPTION & ~win32con.WS_THICKFRAME
style = style | win32con.WS_MAXIMIZEBOX | win32con.WS_MINIMIZEBOX | win32con.WS_SYSMENU
win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

# Add rounded corners
ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
ex_style = ex_style | win32con.WS_EX_LAYERED
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

# Set window composition attributes for rounded corners
try:
    import ctypes
    from ctypes import wintypes
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWCP_ROUND = 2
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        wintypes.HWND(hwnd),
        DWMWA_WINDOW_CORNER_PREFERENCE,
        ctypes.byref(wintypes.INT(DWMWCP_ROUND)),
        ctypes.sizeof(wintypes.INT)
    )
except:
    pass  # Rounded corners not supported on this Windows version

# Center window
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
x = (screen_width - WINDOW_WIDTH) // 2
y = (screen_height - WINDOW_HEIGHT) // 2
win32gui.SetWindowPos(hwnd, 0, x, y, WINDOW_WIDTH, WINDOW_HEIGHT, 0)

# ──────────────────────────────────────────────────────────────────────────────
# 2) UI CONSTANTS & COLORS
# ──────────────────────────────────────────────────────────────────────────────

# Height (pixels) of our custom title bar
TITLEBAR_HEIGHT = 40

# Column header row height (60 px)
ROW_HEADER_HEIGHT = 60
# Checkbox square size (20 px) and scrollbar width (16 px)
BOX_SIZE = 16 # Increased size for better visibility
SCROLLBAR_WIDTH = 17 # Increased width for a wider thumb
# Padding inside cells
PADDING = 8
# Padding inside scrollbar track around the thumb
THUMB_PADDING = 3
# Column width (px)
COLUMN_WIDTH = 170

# Shadow constants
SHADOW_HEIGHT = 2
SHADOW_BLUR_HEIGHT = 2
SHADOW_OFFSET = 3

# Window control button dimensions
BUTTON_WIDTH = 55
BUTTON_HEIGHT = TITLEBAR_HEIGHT # Make button height same as title bar height

# Application Icon file
APP_ICON_FILE = "checklist.png"

# Fonts
FONT = pygame.font.SysFont("Consolas", 18)
HEADER_FONT = pygame.font.SysFont("Consolas", 28, bold=True)

# Dark-mode palette
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
HEADER_BG = (45, 45, 45)
HEADER_TEXT = (200, 200, 200)
ROW_ALT_COLOR_1 = (35, 35, 35)
ROW_ALT_COLOR_2 = (40, 40, 40)
CHECKBOX_BG = (55, 55, 55)
CHECKBOX_HOVER_BG = (65, 65, 65)  # Lighter color for checkbox hover
CHECKBOX_CHECKED = (50, 200, 50)
CHECKBOX_CHECKED_HOVER = (60, 220, 60)  # Brighter green for checked hover
# Scrollbar colors (greyish)
SCROLLBAR_BG = (45, 45, 45)  # Slightly darker base
SCROLLBAR_BG_GRADIENT = (55, 55, 55)  # Slightly lighter for gradient effect
SCROLLBAR_FG = (120, 120, 120) # Normal thumb color
SCROLLBAR_HOVER_FG = (150, 150, 150) # Lighter thumb color on hover
TITLE_CLIENT_BG = (25, 25, 25)
TITLE_CLIENT_TEXT = (230, 230, 230)
HEADER_SHADOW_COLOR = (20, 20, 20)  # Dark shadow for header text

# Animation constants
ANIMATION_SPEED = 0.2  # Speed of checkbox animation
CHECKBOX_ANIMATION_OFFSET = 2  # How many pixels the checkbox moves up/down during animation
CHECKBOX_HOVER_ANIMATION_SPEED = 0.1 # Speed of hover animation

# Vertical offset for fine-tuning title text position
TITLE_Y_OFFSET = 5 # Adjust this value to shift the title text up (negative) or down (positive)

# Button colors
BUTTON_NORMAL_BG = (100, 100, 100)
BUTTON_HOVER_BG = (150, 150, 150)
BUTTON_PRESSED_BG = (80, 80, 80)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Popup colors
POPUP_BG = (45, 45, 45)
POPUP_BORDER = (70, 70, 70)
POPUP_TEXT = (220, 220, 220)
LOAD_BUTTON_BG = (60, 60, 60)
LOAD_BUTTON_HOVER = (80, 80, 80)
LOAD_BUTTON_TEXT = (255, 255, 255)

# Helper function for drawing anti-aliased rounded rectangles (approximation)
def draw_rounded_anti_aliased_rect(surface, color, rect, radius):
    # Create a temporary surface with alpha channel
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0)) # Fill with transparency

    # Draw the rounded rectangle onto the temporary surface
    pygame.draw.rect(temp_surface, color, temp_surface.get_rect(), border_radius=radius)

    # Blit the temporary surface onto the target surface
    surface.blit(temp_surface, rect.topleft)

# Helper function to draw text with shadow
def draw_text_with_shadow(surface, text, x, y, font, color, shadow_color, shadow_offset=1):
    # Draw shadow
    shadow_surf = font.render(text, True, shadow_color)
    surface.blit(shadow_surf, (x + shadow_offset, y + shadow_offset))
    # Draw main text
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))

# ──────────────────────────────────────────────────────────────────────────────
# 3) WINDOW MANAGEMENT
# ──────────────────────────────────────────────────────────────────────────────

class WindowManager:
    def __init__(self):
        self.dragging = False
        self.drag_offset = (0, 0)
        self.resizing = False
        self.resize_edge = None
        self.is_maximized = False
        self.original_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.original_pos = (0, 0)
        self.hwnd = hwnd
        
        # Get screen dimensions
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # Resize border width
        self.RESIZE_BORDER = 5
        
        # Store initial window size for resizing
        self.resize_start_size = None
        self.resize_start_pos = None
        self.resize_mouse_start = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if we're in the resize area
                if self.is_resize_area(mouse_pos):
                    self.resizing = True
                    self.resize_edge = self.get_resize_edge(mouse_pos)
                    # Store initial window state and mouse position
                    rect = win32gui.GetWindowRect(self.hwnd)
                    self.resize_start_size = (rect[2] - rect[0], rect[3] - rect[1])
                    self.resize_start_pos = (rect[0], rect[1])
                    self.resize_mouse_start = mouse_pos
                    return True
                
                # Only start dragging if we're in the title bar area but not on buttons
                if mouse_pos[1] < TITLEBAR_HEIGHT:
                    # Get button rectangles
                    min_rect, max_rect, close_rect = get_button_rects(pygame.display.get_surface().get_size()[0])
                    
                    # Only start dragging if we're not on any buttons
                    if not (min_rect.collidepoint(mouse_pos) or 
                           max_rect.collidepoint(mouse_pos) or 
                           close_rect.collidepoint(mouse_pos)):
                        self.dragging = True
                        self.drag_offset = (mouse_pos[0], mouse_pos[1])
                        return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                self.resizing = False
                self.resize_edge = None
                self.resize_start_size = None
                self.resize_start_pos = None
                self.resize_mouse_start = None
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_drag(event.pos)
            elif self.resizing:
                self.handle_resize(event.pos)
            else:
                # Update cursor based on position
                self.update_cursor(event.pos)
        
        return False
    
    def update_cursor(self, pos):
        if self.is_resize_area(pos):
            edge = self.get_resize_edge(pos)
            if edge in ['left', 'right']:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            elif edge in ['top', 'bottom']:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            elif edge in ['topleft', 'bottomright']:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
            elif edge in ['topright', 'bottomleft']:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def is_resize_area(self, pos):
        x, y = pos
        w, h = pygame.display.get_surface().get_size()
        
        return (x < self.RESIZE_BORDER or x > w - self.RESIZE_BORDER or
                y < self.RESIZE_BORDER or y > h - self.RESIZE_BORDER)
    
    def get_resize_edge(self, pos):
        x, y = pos
        w, h = pygame.display.get_surface().get_size()
        
        if x < self.RESIZE_BORDER:
            if y < self.RESIZE_BORDER:
                return 'topleft'
            elif y > h - self.RESIZE_BORDER:
                return 'bottomleft'
            return 'left'
        elif x > w - self.RESIZE_BORDER:
            if y < self.RESIZE_BORDER:
                return 'topright'
            elif y > h - self.RESIZE_BORDER:
                return 'bottomright'
            return 'right'
        elif y < self.RESIZE_BORDER:
            return 'top'
        elif y > h - self.RESIZE_BORDER:
            return 'bottom'
        return None
    
    def handle_drag(self, pos):
        if not self.is_maximized:
            # Get current window position
            rect = win32gui.GetWindowRect(self.hwnd)
            x = rect[0] + (pos[0] - self.drag_offset[0])
            y = rect[1] + (pos[1] - self.drag_offset[1])
            win32gui.SetWindowPos(self.hwnd, 0, x, y, 0, 0, win32con.SWP_NOSIZE)
    
    def handle_resize(self, pos):
        if not self.is_maximized and self.resize_start_size and self.resize_start_pos and self.resize_mouse_start:
            start_x, start_y = self.resize_start_pos
            start_w, start_h = self.resize_start_size
            mouse_start_x, mouse_start_y = self.resize_mouse_start
            
            # Calculate mouse movement
            dx = pos[0] - mouse_start_x
            dy = pos[1] - mouse_start_y
            
            # Initialize new position and size
            x, y = start_x, start_y
            w, h = start_w, start_h
            
            # Update based on which edge is being dragged
            if self.resize_edge in ['left', 'topleft', 'bottomleft']:
                new_width = start_w - dx
                if new_width >= 400:  # Minimum width
                    x = start_x + dx
                    w = new_width
            
            if self.resize_edge in ['right', 'topright', 'bottomright']:
                new_width = start_w + dx
                if new_width >= 400:  # Minimum width
                    w = new_width
            
            if self.resize_edge in ['top', 'topleft', 'topright']:
                new_height = start_h - dy
                if new_height >= 300:  # Minimum height
                    y = start_y + dy
                    h = new_height
            
            if self.resize_edge in ['bottom', 'bottomleft', 'bottomright']:
                new_height = start_h + dy
                if new_height >= 300:  # Minimum height
                    h = new_height
            
            # Update window position and size
            win32gui.SetWindowPos(self.hwnd, 0, x, y, w, h, 0)
            
            # Update Pygame surface size
            pygame.display.set_mode((w, h), pygame.NOFRAME)
    
    def maximize_window(self):
        if not self.is_maximized:
            # Store current window state
            rect = win32gui.GetWindowRect(self.hwnd)
            self.original_size = (rect[2] - rect[0], rect[3] - rect[1])
            self.original_pos = (rect[0], rect[1])
            
            # Get work area (screen minus taskbar)
            try:
                work_area = win32gui.SystemParametersInfo(win32con.SPI_GETWORKAREA)
                x, y, w, h = work_area
            except:
                # Fallback to full screen if work area not available
                x, y = 0, 0
                w = self.screen_width
                h = self.screen_height
            
            # Maximize window
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOP,
                x, y, w, h,
                win32con.SWP_SHOWWINDOW
            )
            
            # Update Pygame surface size
            pygame.display.set_mode((w, h), pygame.NOFRAME)
        else:
            # Restore window
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOP,
                self.original_pos[0],
                self.original_pos[1],
                self.original_size[0],
                self.original_size[1],
                win32con.SWP_SHOWWINDOW
            )
            
            # Update Pygame surface size
            pygame.display.set_mode(self.original_size, pygame.NOFRAME)
        
        self.is_maximized = not self.is_maximized
    
    def minimize_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
    
    def close_window(self):
        win32gui.DestroyWindow(self.hwnd)

# ──────────────────────────────────────────────────────────────────────────────
# 4) CSV LOADING & STATE
# ──────────────────────────────────────────────────────────────────────────────

# Initialize empty data structures
headers = []
rows = []
checked = []

# ──────────────────────────────────────────────────────────────────────────────
# 5) UI RENDERING
# ──────────────────────────────────────────────────────────────────────────────

def draw_wrapped_text(surface, text, x, y, width, font, color):
    # Split text into words
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    # Calculate average character width for better wrapping
    avg_char_w = font.size("M")[0]
    max_chars = max(1, int(width / avg_char_w))
    
    # First, try to wrap the entire text
    full_text = " ".join(words)
    if font.size(full_text)[0] <= width:
        lines = [full_text]
    else:
        # If full text doesn't fit, wrap word by word
        for word in words:
            word_width = font.size(word + " ")[0]
            if current_width + word_width <= width:
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
        
        if current_line:
            lines.append(" ".join(current_line))
    
    # Draw each line
    line_height = font.get_linesize()
    for i, line in enumerate(lines):
        txt_surf = font.render(line, True, color)
        surface.blit(txt_surf, (x, y + i * line_height))
    
    return len(lines) * line_height

def get_button_rects(window_width):
    # Button vertical position flush with title bar top
    top_y = 0
    
    # Calculate horizontal positions from the right edge, flush with window edge
    close_x = window_width - BUTTON_WIDTH
    close_rect = pygame.Rect(close_x, top_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Position maximize/restore button with padding from the close button
    max_x = close_x - PADDING - BUTTON_WIDTH
    max_rect = pygame.Rect(max_x, top_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Position minimize button with padding from the maximize/restore button
    min_x = max_x - PADDING - BUTTON_WIDTH
    min_rect = pygame.Rect(min_x, top_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    return min_rect, max_rect, close_rect

# Load system icons
def load_system_icon(icon_name, size):
    local_icon_path = f"{icon_name}_white.png"
    if not os.path.exists(local_icon_path):
        raise FileNotFoundError(f"Icon file not found: {local_icon_path}")
        
    try:
        icon_surface = pygame.image.load(local_icon_path).convert_alpha()
        scaled_icon_surface = pygame.transform.scale(icon_surface, (size, size))
        print(f"Loaded icon {icon_name}: original size {icon_surface.get_size()}, scaled size {scaled_icon_surface.get_size()}")
        return scaled_icon_surface
    except pygame.error as e:
        raise Exception(f"Error loading icon file {local_icon_path}: {e}")

# Load system icons for window controls
MINIMIZE_ICON = load_system_icon("minimize", 12)  # Minimize icon (12x12 px)
MAXIMIZE_ICON = load_system_icon("maximize", 8)  # Maximize icon (8x8 px)
RESTORE_ICON = load_system_icon("restore", 12)   # Restore icon (12x12 px)
CLOSE_ICON = load_system_icon("close", 13)     # Close icon (13x13 px)

def draw_load_popup(surface, width, height):
    # Popup dimensions
    popup_width = 300
    popup_height = 150
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    
    # Draw shadow
    shadow_color_dark = (20, 20, 20)
    shadow_color_light = (30, 30, 30)
    shadow_height = 2
    shadow_blur_height = 2
    shadow_offset = 3
    
    # Draw shadow with blur effect
    pygame.draw.rect(surface, shadow_color_dark, 
                    (popup_x + shadow_offset, popup_y + shadow_offset, 
                     popup_width, popup_height + shadow_height), 
                    border_radius=10)
    pygame.draw.rect(surface, shadow_color_light, 
                    (popup_x + shadow_offset, popup_y + shadow_offset + shadow_height, 
                     popup_width, shadow_blur_height), 
                    border_radius=10)
    pygame.draw.rect(surface, shadow_color_light, 
                    (popup_x + shadow_offset, popup_y + shadow_offset + shadow_height + shadow_blur_height//2, 
                     popup_width, shadow_blur_height - shadow_blur_height//2), 
                    border_radius=10)
    
    # Draw popup background with border
    draw_rounded_anti_aliased_rect(surface, POPUP_BG, 
                                 pygame.Rect(popup_x, popup_y, popup_width, popup_height), 
                                 radius=10)
    pygame.draw.rect(surface, POPUP_BORDER, 
                    (popup_x, popup_y, popup_width, popup_height), 
                    2, border_radius=10)
    
    # Draw text
    text = "No CSV File Loaded"
    text_surf = HEADER_FONT.render(text, True, POPUP_TEXT)
    text_rect = text_surf.get_rect(centerx=popup_x + popup_width//2, y=popup_y + 20)
    surface.blit(text_surf, text_rect)
    
    # Draw button
    button_width = 150
    button_height = 40
    button_x = popup_x + (popup_width - button_width) // 2
    button_y = popup_y + popup_height - button_height - 20
    
    # Check if mouse is hovering over button
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    is_hovering = button_rect.collidepoint(mouse_pos)
    
    # Draw button with hover effect
    button_color = LOAD_BUTTON_HOVER if is_hovering else LOAD_BUTTON_BG
    draw_rounded_anti_aliased_rect(surface, button_color, button_rect, radius=5)
    
    # Draw button text
    button_text = "Load CSV File"
    button_text_surf = FONT.render(button_text, True, LOAD_BUTTON_TEXT)
    button_text_rect = button_text_surf.get_rect(center=button_rect.center)
    surface.blit(button_text_surf, button_text_rect)
    
    return button_rect

def draw_all(screen, window_manager, app_icon_surface, checkbox_animation_state):
    w, h = screen.get_size()
    screen.fill(BG_COLOR)

    # Draw title bar with rounded corners
    pygame.draw.rect(screen, TITLE_CLIENT_BG, (0, 0, w, TITLEBAR_HEIGHT))
    title_surf = HEADER_FONT.render("CSV Checklist Table", True, TITLE_CLIENT_TEXT)

    # Draw application icon if loaded
    icon_width = 0 # Default width if no icon
    if app_icon_surface:
        # Position icon to the left, vertically centered within the title bar
        icon_x = PADDING
        icon_y = (TITLEBAR_HEIGHT - app_icon_surface.get_height()) // 2
        screen.blit(app_icon_surface, (icon_x, icon_y))
        icon_width = app_icon_surface.get_width()

    # Calculate vertical position for top-left to align center with button icons' center
    title_y = TITLEBAR_HEIGHT // 2 - title_surf.get_height() // 2 + TITLE_Y_OFFSET
    title_x = PADDING + icon_width + PADDING

    # Draw title with shadow
    draw_text_with_shadow(screen, "CSV Checklist Table", title_x, title_y, HEADER_FONT, TITLE_CLIENT_TEXT, HEADER_SHADOW_COLOR)

    # Draw window control buttons
    min_rect, max_rect, close_rect = get_button_rects(w)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Draw minimize button
    if min_rect.collidepoint(mouse_pos):
        # Use a darker gray for the pressed state, BUTTON_HOVER_BG for hover when not pressed
        bg = (80, 80, 80) if mouse_pressed else BUTTON_HOVER_BG
    else:
        bg = TITLE_CLIENT_BG
    pygame.draw.rect(screen, bg, min_rect)
    icon_rect = MINIMIZE_ICON.get_rect(center=min_rect.center)
    screen.blit(MINIMIZE_ICON, icon_rect)

    # Draw maximize/restore button
    if max_rect.collidepoint(mouse_pos):
        # Use a darker gray for the pressed state, BUTTON_HOVER_BG for hover when not pressed
        bg = (80, 80, 80) if mouse_pressed else BUTTON_HOVER_BG
    else:
        bg = TITLE_CLIENT_BG
    pygame.draw.rect(screen, bg, max_rect)
    icon = MAXIMIZE_ICON if not window_manager.is_maximized else RESTORE_ICON
    icon_rect = icon.get_rect(center=max_rect.center)
    screen.blit(icon, icon_rect)

    # Draw close button
    if close_rect.collidepoint(mouse_pos):
        bg = (255, 0, 0) if mouse_pressed else (200, 0, 0)
    else:
        bg = TITLE_CLIENT_BG
    pygame.draw.rect(screen, bg, close_rect)
    icon_rect = CLOSE_ICON.get_rect(center=close_rect.center)
    screen.blit(CLOSE_ICON, icon_rect)

    # If no data is loaded, show the load popup
    if not headers:
        load_button_rect = draw_load_popup(screen, w, h)
        pygame.display.flip()
        return 0, pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), min_rect, max_rect, close_rect, 0, 0, load_button_rect  # Return the actual load button rect

    # Calculate available width for content
    available_width = w - SCROLLBAR_WIDTH - 50  # 50 for checkbox column
    min_column_width = 170
    total_columns = len(headers)
    
    # Calculate optimal column widths based on content
    column_widths = []
    for i, col_name in enumerate(headers):
        # Get the maximum width needed for this column
        max_width = 0
        # Check header width
        header_width = FONT.size(col_name)[0] + 2 * PADDING
        max_width = max(max_width, header_width)
        
        # Check all data widths in this column
        for row in rows:
            text_width = FONT.size(row[col_name])[0] + 2 * PADDING
            max_width = max(max_width, text_width)
        
        # Ensure minimum width
        max_width = max(max_width, min_column_width)
        column_widths.append(max_width)
    
    # Calculate how many columns can fit in one row
    columns_per_row = 1
    while True:
        total_width = sum(column_widths[:columns_per_row])
        if total_width > available_width and columns_per_row > 1:
            columns_per_row -= 1
            break
        if columns_per_row >= total_columns:
            break
        columns_per_row += 1
    
    # Adjust column widths to fit available space
    if columns_per_row < total_columns:
        # Calculate total width of columns in each row
        for row in range((total_columns + columns_per_row - 1) // columns_per_row):
            start_col = row * columns_per_row
            end_col = min(start_col + columns_per_row, total_columns)
            row_width = sum(column_widths[start_col:end_col])
            
            if row_width > available_width:
                # Scale down columns in this row
                scale = available_width / row_width
                for i in range(start_col, end_col):
                    column_widths[i] = int(column_widths[i] * scale)
    
    total_rows = (total_columns + columns_per_row - 1) // columns_per_row

    # Draw column headers with shadow
    header_y = TITLEBAR_HEIGHT
    header_height_total = ROW_HEADER_HEIGHT * total_rows
    pygame.draw.rect(screen, HEADER_BG, (0, header_y, w - SCROLLBAR_WIDTH, header_height_total))

    # Draw a subtle shadow line below the header with a blur effect approximation
    shadow_color_dark = (20, 20, 20)
    shadow_color_light = (30, 30, 30)
    shadow_height = 2
    shadow_blur_height = 2

    pygame.draw.rect(screen, shadow_color_dark, (0, header_y + header_height_total, w - SCROLLBAR_WIDTH, shadow_height))
    pygame.draw.rect(screen, shadow_color_light, (0, header_y + header_height_total + shadow_height, w - SCROLLBAR_WIDTH, shadow_blur_height // 2))
    pygame.draw.rect(screen, shadow_color_light, (0, header_y + header_height_total + shadow_height + shadow_blur_height // 2, w - SCROLLBAR_WIDTH, shadow_blur_height - shadow_blur_height // 2))

    # Draw headers with shadow
    for i, col_name in enumerate(headers):
        row = i // columns_per_row
        col = i % columns_per_row
        x = 50 + col * column_widths[i]
        y = header_y + row * ROW_HEADER_HEIGHT + PADDING
        
        draw_text_with_shadow(screen, col_name, x + PADDING, y, FONT, HEADER_TEXT, HEADER_SHADOW_COLOR)

    # Draw visible data rows
    available_h = h - TITLEBAR_HEIGHT - header_height_total - shadow_height - shadow_blur_height
    max_visible_rows_float = available_h / (ROW_HEADER_HEIGHT * total_rows) if (ROW_HEADER_HEIGHT * total_rows) > 0 else 0
    max_visible_rows = int(max_visible_rows_float)

    # Define the clipping area for the checklist rows
    content_area_y = header_y + header_height_total + shadow_height + shadow_blur_height
    content_area_rect = pygame.Rect(0, content_area_y, w - SCROLLBAR_WIDTH, h - content_area_y)
    screen.set_clip(content_area_rect)

    start = int(scroll_y)
    end = min(len(rows), int(scroll_y) + max_visible_rows + 1)

    for idx in range(start, end):
        vertical_offset = (scroll_y - int(scroll_y)) * (ROW_HEADER_HEIGHT * total_rows)
        base_row_y_in_content_area = (ROW_HEADER_HEIGHT * total_rows) * (idx - start) - vertical_offset
        base_row_y = content_area_y + base_row_y_in_content_area

        bg_color = ROW_ALT_COLOR_1 if idx % 2 == 0 else ROW_ALT_COLOR_2
        pygame.draw.rect(screen, bg_color, (0, base_row_y, w - SCROLLBAR_WIDTH, ROW_HEADER_HEIGHT))

        # Calculate the normal resting y position for the checkbox
        normal_box_y = base_row_y + (ROW_HEADER_HEIGHT - BOX_SIZE) // 2

        # Determine hover state
        mouse_pos = pygame.mouse.get_pos()
        checkbox_rect = pygame.Rect(PADDING * 2, normal_box_y, BOX_SIZE, BOX_SIZE)
        is_hovering = checkbox_rect.collidepoint(mouse_pos)

        # Update target y position based on hover state
        target_box_y = normal_box_y - CHECKBOX_ANIMATION_OFFSET if is_hovering else normal_box_y

        # Ensure the animation state list has an entry for this index
        while len(checkbox_animation_state) <= idx:
            checkbox_animation_state.append(normal_box_y) # Initialize with resting position

        # Only animate if we're hovering, otherwise snap to normal position
        if is_hovering:
            checkbox_animation_state[idx] += (target_box_y - checkbox_animation_state[idx]) * CHECKBOX_HOVER_ANIMATION_SPEED
        else:
            checkbox_animation_state[idx] = normal_box_y

        # Use the animated y position for drawing
        animated_box_y = checkbox_animation_state[idx]

        # Determine checkbox color based on state and hover
        if checked[idx]:
            box_color = CHECKBOX_CHECKED_HOVER if is_hovering else CHECKBOX_CHECKED
        else:
            box_color = CHECKBOX_HOVER_BG if is_hovering else CHECKBOX_BG

        # Draw the rounded, anti-aliased checkbox
        draw_rounded_anti_aliased_rect(screen, box_color, pygame.Rect(PADDING * 2, animated_box_y, BOX_SIZE, BOX_SIZE), radius=2)

        # Draw cell text
        for i, col_name in enumerate(headers):
            row = i // columns_per_row
            col = i % columns_per_row
            x = 50 + col * column_widths[i]
            y = base_row_y + row * ROW_HEADER_HEIGHT + PADDING
            
            val = rows[idx][col_name]
            draw_wrapped_text(
                surface=screen,
                text=val,
                x=x + PADDING,
                y=y,
                width=column_widths[i] - 2 * PADDING,
                font=FONT,
                color=TEXT_COLOR
            )

    # Clear clipping area
    screen.set_clip(None)

    # Draw scrollbar with gradient background
    scrollbar_x = w - SCROLLBAR_WIDTH
    scrollbar_y_start = TITLEBAR_HEIGHT
    scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y_start, SCROLLBAR_WIDTH, h - scrollbar_y_start)

    # Draw gradient background for scrollbar
    for y in range(scrollbar_rect.top, scrollbar_rect.bottom):
        # Calculate gradient color based on position
        gradient_progress = (y - scrollbar_rect.top) / scrollbar_rect.height
        current_color = tuple(
            int(SCROLLBAR_BG[i] + (SCROLLBAR_BG_GRADIENT[i] - SCROLLBAR_BG[i]) * gradient_progress)
            for i in range(3)
        )
        pygame.draw.line(screen, current_color, (scrollbar_x, y), (scrollbar_x + SCROLLBAR_WIDTH, y))

    # Calculate thumb dimensions and position
    if len(rows) <= max_visible_rows:
        thumb_height = scrollbar_rect.height
    else:
        thumb_height = max(
            int(scrollbar_rect.height * max_visible_rows / len(rows)),
            25
        )

    if len(rows) > max_visible_rows:
        thumb_y = scrollbar_rect.y + (
            (scrollbar_rect.height - thumb_height) * scroll_y
            / (len(rows) - max_visible_rows)
        )
    else:
        thumb_y = scrollbar_rect.y

    # Determine thumb color based on hover state
    mouse_pos = pygame.mouse.get_pos()
    full_width_thumb_rect = pygame.Rect(scrollbar_x, int(thumb_y), SCROLLBAR_WIDTH, thumb_height)

    if full_width_thumb_rect.collidepoint(mouse_pos):
        thumb_color = SCROLLBAR_HOVER_FG
    else:
        thumb_color = SCROLLBAR_FG

    # Calculate the drawing rectangle for the thumb with padding
    thumb_draw_width = SCROLLBAR_WIDTH - 2 * THUMB_PADDING
    thumb_draw_x = scrollbar_x + THUMB_PADDING
    thumb_draw_rect = pygame.Rect(thumb_draw_x, int(thumb_y), thumb_draw_width, thumb_height)

    # Draw the rounded, anti-aliased thumb
    draw_rounded_anti_aliased_rect(screen, thumb_color, thumb_draw_rect, radius=int(thumb_draw_width / 2))

    pygame.display.flip()
    return max_visible_rows, full_width_thumb_rect, scrollbar_rect, min_rect, max_rect, close_rect, total_rows, thumb_height, pygame.Rect(0, 0, 0, 0)  # Return empty rect when no load button is shown

# ──────────────────────────────────────────────────────────────────────────────
# 6) MAIN LOOP
# ──────────────────────────────────────────────────────────────────────────────

def main():
    global scroll_y, checked
    
    window_manager = WindowManager()
    clock = pygame.time.Clock()
    running = True
    dragging_scrollbar = False
    drag_offset = 0
    scroll_y = 0.0
    target_scroll_y = 0.0
    scroll_speed = 0.2  # Changed back to 0.2 for smooth scrolling

    # Initialize checkbox animation state (list of current y positions)
    checkbox_animation_state = [] # This will be populated in draw_all

    # Load application icon
    try:
        app_icon_surface = pygame.image.load(APP_ICON_FILE).convert_alpha()
        app_icon_surface = pygame.transform.scale(app_icon_surface, (35, 35))
    except pygame.error as e:
        print(f"Warning: Could not load application icon {APP_ICON_FILE}: {e}")
        app_icon_surface = None

    # Initialize variables
    max_visible_rows = 0
    max_scroll = 0.0
    thumb_height = 0

    while running:
        w, h = screen.get_size()
        # Pass the animation state list to draw_all
        max_visible_rows, thumb_rect, scrollbar_rect, min_btn, max_btn, close_btn, total_rows, thumb_height, load_button_rect = draw_all(screen, window_manager, app_icon_surface, checkbox_animation_state)

        max_scroll = max(0.0, len(rows) - max_visible_rows)
        scroll_y = max(0.0, min(scroll_y, max_scroll))
        target_scroll_y = max(0.0, min(target_scroll_y, max_scroll))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if window_manager.handle_event(event):
                scroll_y = target_scroll_y
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mx, my = event.pos

                    # Check if load button was clicked
                    if not headers and load_button_rect.collidepoint(mx, my):
                        try:
                            # Create a file dialog using win32ui
                            dlg = win32ui.CreateFileDialog(
                                1,  # 1 for open, 0 for save
                                "csv",  # default extension
                                None,  # default filename
                                win32con.OFN_FILEMUSTEXIST | win32con.OFN_PATHMUSTEXIST,
                                "CSV Files (*.csv)|*.csv|All Files (*.*)|*.*||"
                            )
                            dlg.SetOFNTitle("Select CSV File")
                            
                            if dlg.DoModal() == win32con.IDOK:
                                filepath = dlg.GetPathName()
                                # Load the CSV file
                                with open(filepath, newline="", encoding="utf-8-sig") as f:
                                    reader = csv.DictReader(f)
                                    # Clear existing data
                                    headers.clear()
                                    rows.clear()
                                    checked.clear()
                                    # Load new data
                                    headers.extend(reader.fieldnames[:])
                                    rows.extend([row for row in reader])
                                    checked.extend([False] * len(rows))
                            
                        except Exception as e:
                            print(f"Error opening file dialog: {e}")

                    # Window control buttons
                    # Check if window control buttons were clicked - ensure this happens AFTER load button check
                    elif close_btn.collidepoint(mx, my):
                        window_manager.close_window()
                        running = False
                    elif max_btn.collidepoint(mx, my):
                        window_manager.maximize_window()
                    elif min_btn.collidepoint(mx, my):
                        window_manager.minimize_window()

                    # Scrollbar and checkbox handling
                    elif my > TITLEBAR_HEIGHT:
                        if thumb_rect.collidepoint(event.pos):
                            dragging_scrollbar = True
                            drag_offset = my - thumb_rect.y
                        elif scrollbar_rect.collidepoint(mx, my):
                            scrollbar_track_height = scrollbar_rect.height - thumb_height
                            if len(rows) > max_visible_rows and scrollbar_track_height > 0:
                                rel_y_in_track = my - scrollbar_rect.y - thumb_rect.height / 2.0
                                rel_y_in_track = max(0.0, min(rel_y_in_track, scrollbar_track_height))
                                target_scroll_y = (rel_y_in_track / scrollbar_track_height) * (len(rows) - max_visible_rows)

                        if PADDING * 2 <= mx <= PADDING * 2 + BOX_SIZE:
                            header_height_total_for_click = ROW_HEADER_HEIGHT * total_rows
                            content_area_y_start = TITLEBAR_HEIGHT + header_height_total_for_click + SHADOW_HEIGHT + SHADOW_BLUR_HEIGHT
                            content_area_y_end = h - SCROLLBAR_WIDTH
                            
                            if my >= content_area_y_start and my <= content_area_y_end:
                                # Calculate which row was clicked
                                rel_y = my - content_area_y_start
                                row_height = ROW_HEADER_HEIGHT * total_rows
                                clicked_idx = int(scroll_y) + (rel_y // row_height) if row_height > 0 else 0
                                
                                if 0 <= clicked_idx < len(rows):
                                    # Check if click was in the first row of the entry
                                    row_in_entry = (rel_y % row_height) // ROW_HEADER_HEIGHT if row_height > 0 else 0
                                    if row_in_entry == 0:
                                        # Calculate checkbox position
                                        box_top_visual = content_area_y_start + row_height * (clicked_idx - scroll_y) + (ROW_HEADER_HEIGHT - BOX_SIZE) // 2
                                        
                                        # Get the animated position if available
                                        if 0 <= clicked_idx < len(checkbox_animation_state):
                                            animated_box_y = checkbox_animation_state[clicked_idx]
                                        else:
                                            animated_box_y = box_top_visual
                                        
                                        # Check if click was within checkbox bounds
                                        if my >= animated_box_y and my <= animated_box_y + BOX_SIZE:
                                            checked[clicked_idx] = not checked[clicked_idx]

                elif event.button == 4:
                    target_scroll_y = max(0.0, target_scroll_y - 1.0)
                elif event.button == 5:
                    target_scroll_y = min(len(rows) - max_visible_rows, target_scroll_y + 1.0)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_scrollbar = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_scrollbar:
                    scrollbar_track_height = scrollbar_rect.height - thumb_height
                    if len(rows) > max_visible_rows and scrollbar_track_height > 0:
                        rel_y_in_track = event.pos[1] - scrollbar_rect.y - thumb_rect.height / 2.0
                        rel_y_in_track = max(0.0, min(rel_y_in_track, scrollbar_track_height))
                        target_scroll_y = (rel_y_in_track / scrollbar_track_height) * (len(rows) - max_visible_rows)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    target_scroll_y = max(0.0, target_scroll_y - 1.0)
                elif event.key == pygame.K_DOWN:
                    target_scroll_y = min(len(rows) - max_visible_rows, target_scroll_y + 1.0)

        scroll_y += (target_scroll_y - scroll_y) * scroll_speed
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
