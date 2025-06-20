# 📝 simple\_checklist

**simple\_checklist** is a customizable, frameless desktop checklist application I built using **Pygame**, designed for productivity and flexibility. It lets me (or you!) load CSV files as interactive task tables with smooth scrolling, animated UI elements, and fully custom window controls.

I made this project to emphasize clean design, animation-rich interaction, and native usability without relying on traditional OS window frames.

---

## 🔧 Features

* **Frameless Window Design**

  * Custom title bar with manual drag & resize behavior
  * Fully custom buttons: Minimize, Maximize/Restore, Close

* **Data-Driven Task Management**

  * Load CSV files via a native file explorer popup
  * Display tasks as a scrollable, wrap-enabled table
  * Checkboxes to mark tasks complete, saved in memory

* **Smooth UI & Visual Effects**

  * Gradient vertical scrollbar with hover behavior
  * Button animations with color transitions
  * Text wrapping for long entries in each cell

* **Keyboard & Mouse Friendly**

  * Scrollwheel support for long lists
  * Hover-based UI highlighting for interactive elements

---

## 📦 Prerequisites

Make sure Python 3.6 or newer is installed, along with these packages:

```bash
pip install pygame pywin32
```

> I use `pywin32` for handling Windows API functions that control the window behavior.

---

## ▶️ How I Run the App

1. I install Python and the required packages.
2. Then I clone or download the repo to my machine.
3. I place the following image assets in the same folder as `checklist.py`:

```
checklist.png
close_black.png
close_white.png
maximize_black.png
maximize_white.png
minimize_white.png
minimize-black.png
restore_black.png
restore_white.png
```

4. I launch the script from my terminal or command prompt:

```bash
python checklist.py
```

---

## 🛠️ How I Build a Standalone Executable (Windows)

To turn the script into a `.exe` (no terminal window), here’s what I do:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. (Optional) I create a `.ico` file for the app icon (like `checklist.ico`).

3. Then I run this build command:

```bash
python -m PyInstaller --onefile --noconsole --icon=checklist.ico \
--add-data "checklist.png;." \
--add-data "close_black.png;." --add-data "close_white.png;." \
--add-data "maximize_black.png;." --add-data "maximize_white.png;." \
--add-data "minimize_white.png;." --add-data "minimize-black.png;." \
--add-data "restore_black.png;." --add-data "restore_white.png;." \
checklist.py
```

4. The final executable shows up in the `dist/` folder.

---

## 🖼️ Required Image Assets

Here’s a list of the image files I include for the UI:

```
checklist.png             # App icon/logo
close_black.png           # Close button (dark mode)
close_white.png           # Close button (light mode)
maximize_black.png        # Maximize button (dark mode)
maximize_white.png        # Maximize button (light mode)
minimize_white.png        # Minimize button (light mode)
minimize-black.png        # Minimize button (dark mode)
restore_black.png         # Restore button (dark mode)
restore_white.png         # Restore button (light mode)
```

All of these go in the same folder as `checklist.py`, or I include them with `--add-data` when using PyInstaller.

---

## 💡 Potential Improvements

Here’s what I might add in future versions:

* Dark mode toggle
* Theme and color customization
* Drag-and-drop task ordering
* CSV editing and saving
* Configurable column widths
* Auto-save checkbox states

---

## 📜 License

I’m using the [MIT License](https://opensource.org/licenses/MIT) for this project.

---

## 🙌 Credits

This project was built by me — **Zane** — a student and aspiring software engineer who loves Python and making things simple and intuitive.

---

## 🔗 Related Tools

* [Pygame Documentation](https://www.pygame.org/docs/)
* [PyInstaller Docs](https://pyinstaller.org/en/stable/)
* [pywin32 on PyPI](https://pypi.org/project/pywin32/)

---
