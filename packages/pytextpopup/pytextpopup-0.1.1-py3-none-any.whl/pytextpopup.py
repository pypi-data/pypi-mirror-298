import tkinter as tk
from screeninfo import get_monitors

def text_popup(text, fontname="Arial", color="white", scrollspeed=5):
    """
    Displays a floating text window at the cursor position on the screen with scrolling text.
    The window width adjusts based on the length of the text, but does not exceed 90% of the screen width.

    Args:
        text (str): The text to display.
        fontname (str): The font name to use for the text (default: "Arial").
        color (str): The color of the text (default: "white").
        scrollspeed (int): The speed at which the text scrolls (default: 5).
    """
    # Create the main window
    root = tk.Tk()

    # Get the cursor position
    cursor_x = root.winfo_pointerx()
    cursor_y = root.winfo_pointery()

    # Detect which monitor the cursor is in
    monitor = None
    for m in get_monitors():
        if m.x <= cursor_x <= m.x + m.width and m.y <= cursor_y <= m.y + m.height:
            monitor = m
            break

    # Set default to the main monitor if none found (just a precaution)
    if monitor is None:
        monitor = get_monitors()[0]

    # Set the maximum width to 90% of the screen width
    max_window_width = int(monitor.width * 0.9)

    # Calculate a dynamic width based on the length of the text, up to the maximum allowed width
    char_width = 10  # Estimated average character width in pixels (can vary with the font)
    calculated_width = min(len(text) * char_width, max_window_width)

    # Set the window width and height dynamically based on the calculated width
    window_width = calculated_width
    window_height_percent = 0.1  # 10% of the screen height
    window_height = int(monitor.height * window_height_percent)

    # Calculate the desired position for the window (above the cursor)
    window_x = cursor_x - window_width // 2
    window_y = cursor_y - window_height - 20  # Move up 20 pixels from the cursor

    # Adjust to ensure the window stays within screen bounds for the selected monitor
    if window_x < monitor.x:
        window_x = monitor.x  # Ensure it doesn't go off the left edge of the monitor
    if window_x + window_width > monitor.x + monitor.width:
        window_x = monitor.x + monitor.width - window_width  # Ensure it doesn't go off the right edge

    if window_y < monitor.y:
        window_y = monitor.y  # Ensure it doesn't go off the top of the screen
    if window_y + window_height > monitor.y + monitor.height:
        window_y = monitor.y + monitor.height - window_height  # Ensure it doesn't go off the bottom

    # Configure window properties
    root.attributes('-transparentcolor', 'black')
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
    
    # Set the window's background color (black will become transparent)
    root.config(bg='black')
    canvas = tk.Canvas(root, bg='black', height=window_height, width=window_width, highlightbackground='black')
    canvas.pack()

    # Scale the font size based on the window height
    font_size = int(window_height * 0.4)  # Adjust the scaling factor as needed
    font = (fontname, font_size)  # Change the font name as needed
    
    # Create text on the canvas with the provided color
    text_id = canvas.create_text(window_width, window_height // 2, text=text, font=font, fill=color, anchor='w')

    # Get the width of the text (important for determining when scrolling is complete)
    canvas.update_idletasks()  # Force update to get correct text width
    text_width = canvas.bbox(text_id)[2]  # bbox returns a tuple (x1, y1, x2, y2), we need x2 (the right side)

    # Define scrolling function
    def scroll_text():
        # Move the text by the specified increment to the left
        canvas.move(text_id, -scrollspeed, 0)  # Negative value to move left
        canvas.update()

        # Check if the text has scrolled off the window
        text_pos = canvas.bbox(text_id)[2]  # Get the right side of the text
        if text_pos < 0:
            root.destroy()  # Close the window if the text has fully scrolled off
        else:
            # Adjust the delay to control scrolling speed (lower means faster)
            canvas.after(10, scroll_text)  # 10 milliseconds delay for smoother animation

    # Start scrolling the text
    scroll_text()
    root.mainloop()

# Example usage: This can be removed or modified as needed.
if __name__ == "__main__":
    text_popup(
        text="This is a long text popup example. This text adjusts the window width based on its length, and it scrolls across the screen.",
        fontname="Orbitron-Regular",
        color="white",   # Text color
        scrollspeed=10    # Scrolling speed
    )
