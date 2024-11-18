import threading
import server
from server import message_queue
import curses
import math
from collections import defaultdict
from typing import Dict, Tuple
import time


client_data: Dict[str, Dict] = defaultdict(lambda: {
    'cpu_percent': 0,
    'ram_used': 0,
    'ram_total': 0,
    'last_update': 0
})

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)    

def draw_circle(stdscr, center_y, center_x, radius, percentage=0):
    angle_threshold = -90 + (percentage * 360 / 100)
    points = {}
    
    for angle in range(-90, 270):
        radian = math.radians(angle)
        y = center_y + round(radius * math.sin(radian))
        x = center_x + round(radius * 2 * math.cos(radian))
        
        color = curses.color_pair(3) if angle <= angle_threshold else curses.color_pair(2)
        points[(y, x)] = color
    
    for (y, x), color in points.items():
        try:
            stdscr.addstr(y, x, "█", color)
        except curses.error:
            pass

def draw_client_panel(stdscr, hostname: str, data: dict, start_y: int, start_x: int, width: int, height: int):
    for y in range(start_y, start_y + height):
        stdscr.addch(y, start_x, '│')
        stdscr.addch(y, start_x + width - 1, '│')
    for x in range(start_x + 1, start_x + width - 1):
        stdscr.addch(start_y, x, '─')
        stdscr.addch(start_y + height - 1, x, '─')
    
    stdscr.addch(start_y, start_x, '┌')
    stdscr.addch(start_y, start_x + width - 1, '┐')
    stdscr.addch(start_y + height - 1, start_x, '└')
    stdscr.addch(start_y + height - 1, start_x + width - 1, '┘')

    hostname_x = start_x + (width - len(hostname)) // 2
    stdscr.addstr(start_y + 1, hostname_x, hostname, curses.color_pair(5))

    circle_center_y = start_y + (height // 2)
    circle_center_x = start_x + (width // 2)
    radius = min(height // 4, width // 6)
    draw_circle(stdscr, circle_center_y, circle_center_x, radius, data['cpu_percent'])
    
    cpu_text = f"{data['cpu_percent']}%"
    stdscr.addstr(circle_center_y, circle_center_x - len(cpu_text) // 2, cpu_text, curses.color_pair(1))

    ram_y = circle_center_y + radius + 1
    ram_text = f"{data['ram_used']:.1f}/{data['ram_total']:.1f}GB"
    stdscr.addstr(ram_y, circle_center_x - len(ram_text) // 2, ram_text, curses.color_pair(1))
    
    bar_width = width - 10
    bar_start_x = start_x + 5
    ram_percent = (data['ram_used'] / data['ram_total']) * 100 if data['ram_total'] > 0 else 0
    used_bar_length = int((ram_percent / 100) * bar_width)
    
    for x in range(bar_start_x, bar_start_x + used_bar_length):
        stdscr.addch(ram_y + 1, x, '█', curses.color_pair(3))
    for x in range(bar_start_x + used_bar_length, bar_start_x + bar_width):
        stdscr.addch(ram_y + 1, x, '█', curses.color_pair(4))

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(200)
    init_colors()
    
    scroll_position = 0
    
    while True:
        while not message_queue.empty():
            message = message_queue.get()
            try:
                hostname, cpu_usage, ram_usage = message.split()
                cpu_percent = int(cpu_usage.strip('%'))
                ram_used, ram_total = ram_usage.split('/')
                ram_used = float(ram_used.strip('GB'))
                ram_total = float(ram_total.strip('GB'))
                
                client_data[hostname].update({
                    'cpu_percent': cpu_percent,
                    'ram_used': ram_used,
                    'ram_total': ram_total,
                    'last_update': time.time()
                })
            except ValueError:
                continue

        stdscr.clear()
        stdscr.border(0)

        max_rows, max_cols = stdscr.getmaxyx()
        panel_width = max_cols // 2 - 2
        panel_height = 15
        panels_per_row = max(1, (max_cols - 4) // panel_width)
        
        current_time = time.time()
        inactive_clients = [
            hostname for hostname, data in client_data.items()
            if current_time - data['last_update'] > 10
        ]
        for hostname in inactive_clients:
            del client_data[hostname]

        active_clients = sorted(client_data.keys())
        total_rows = math.ceil(len(active_clients) / panels_per_row)
        
        max_scroll = max(0, total_rows - (max_rows - 2) // panel_height)
        scroll_position = min(max_scroll, max(0, scroll_position))

        for i, hostname in enumerate(active_clients):
            row = i // panels_per_row - scroll_position
            col = i % panels_per_row
            
            panel_y = 1 + (row * panel_height)
            panel_x = 2 + (col * panel_width)
            
            if 0 <= panel_y < max_rows - panel_height:
                draw_client_panel(
                    stdscr, hostname, client_data[hostname],
                    panel_y, panel_x, panel_width, panel_height
                )

        if max_scroll > 0:
            if scroll_position > 0:
                stdscr.addstr(0, max_cols // 2 - 1, "▲", curses.color_pair(1))
            if scroll_position < max_scroll:
                stdscr.addstr(max_rows - 1, max_cols // 2 - 1, "▼", curses.color_pair(1))

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            scroll_position = max(0, scroll_position - 1)
        elif key == curses.KEY_DOWN:
            scroll_position = min(max_scroll, scroll_position + 1)

        stdscr.refresh()

server_thread = threading.Thread(target=server.start_server)
server_thread.daemon = True
server_thread.start()


curses.wrapper(draw_dashboard)