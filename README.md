# CSV Checklist Application

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

A modern, custom-framed desktop checklist application built with Pygame for Windows. Features a sleek dark theme with smooth animations and professional UI elements.

## ✨ Features

### 🎨 **Modern UI Design**
- **Dark theme** with professional color palette
- **Custom frameless window** with rounded corners
- **Smooth animations** for checkboxes and hover effects
- **Gradient scrollbar** with physics-based scrolling
- **Anti-aliased rounded rectangles** throughout the interface

### 🖱️ **Interactive Elements**
- **Draggable window** with custom title bar
- **Resizable window** with edge detection
- **Custom window controls** (minimize, maximize/restore, close)
- **Interactive checkboxes** with hover animations
- **Smooth scrolling** with mouse wheel and momentum

### 📊 **Data Management**
- **CSV file loading** via native file dialog
- **Multi-column data display** with automatic text wrapping
- **Responsive layout** that adapts to content
- **Checkbox state tracking** for each row

### 🎯 **User Experience**
- **Professional appearance** suitable for business use
- **Intuitive controls** with visual feedback
- **Keyboard navigation** support (arrow keys for scrolling)
- **High DPI support** for modern displays

## 🚀 Quick Start

### Prerequisites
- **Python 3.6+**
- **Pygame**: `pip install pygame`
- **pywin32**: `pip install pywin32`
- **PyInstaller** (for building): `pip install pyinstaller`

### Running the Application
```bash
python checklist.py
```

### Building the Executable
```bash
# Option 1: Use the provided batch file
scripts/build.bat

# Option 2: Run PyInstaller directly
python -m PyInstaller checklist.spec
```

The executable will be created in the `dist/` folder as `checklist.exe`.

## 🎨 Customization

### Color Scheme
The application uses a professional dark theme with these colors:
- **Background**: Dark grays (20-65 range)
- **Text**: Light grays to white (200-255 range)
- **Accent**: Green for checkboxes (50-220 range)
- **Highlights**: Red for close button

### Icon Customization
To use your own icon:
1. Create a large image (256x256 or larger)
2. Run the icon creation script:
   ```bash
   python scripts/create_icon.py your_large_image.png
   ```
3. Rebuild the executable

## 📁 Project Structure

```
simple_checklist/
├── checklist.py          # Main application
├── checklist.spec        # PyInstaller configuration
├── requirements.txt      # Python dependencies
├── sample_data.csv      # Sample CSV data
├── VERSION              # Version file
├── LICENSE              # MIT License
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── assets/              # Images and icons
│   ├── checklist.ico    # Application icon
│   ├── checklist.png    # App icon (PNG)
│   └── *.png           # Window control icons
├── scripts/             # Build and utility scripts
│   ├── build.bat        # Build script
│   ├── install.bat      # Installation script
│   ├── refresh_icons.bat # Windows icon cache refresh
│   └── create_icon.py   # Icon creation utility
├── docs/                # Documentation
│   ├── CHANGELOG.md     # Version history
│   └── CONTRIBUTING.md  # Contribution guidelines
├── .github/             # GitHub configuration
├── build/               # PyInstaller build output
└── dist/                # Distribution files
```

## 🔧 Development

### Key Components
- **WindowManager**: Handles window dragging, resizing, and controls
- **CSV Loading**: Native file dialog integration
- **Rendering Engine**: Custom drawing functions with anti-aliasing
- **Animation System**: Smooth checkbox and scroll animations
- **Event Handling**: Comprehensive mouse and keyboard input

### Build System
- **PyInstaller spec file** with all dependencies included
- **Automatic data file inclusion** for all required assets
- **Icon embedding** with multi-size support
- **Clean build process** with proper caching

## 📋 Required Files

### Core Application
- `checklist.py` - Main application code
- `checklist.spec` - PyInstaller configuration

### Assets
- `assets/checklist.ico` - Application icon (multi-size)
- `assets/checklist.png` - Application icon (PNG format)
- Window control icons:
  - `assets/close_white.png`, `assets/close_black.png`
  - `assets/maximize_white.png`, `assets/maximize_black.png`
  - `assets/minimize_white.png`, `assets/minimize_black.png`
  - `assets/restore_white.png`, `assets/restore_black.png`

### Build Tools
- `scripts/build.bat` - Automated build script
- `scripts/create_icon.py` - Icon creation utility
- `scripts/refresh_icons.bat` - Windows icon cache management

## 🐛 Troubleshooting

### Icon Not Displaying
If the custom icon doesn't appear:
1. Run `scripts/refresh_icons.bat` to clear Windows icon cache
2. Copy the executable to a different location
3. Create a desktop shortcut to test

### Build Issues
- Ensure all PNG files are present in the project directory
- Use `python -m PyInstaller` instead of `pyinstaller` command
- Run with `--clean` flag to force rebuild

## 📄 License

This project is open source and available under the MIT License.

## 📋 Release Notes

### Version 1.0.1 (2025-07-20)
- **Fixed asset loading for PyInstaller builds:** All icons and images are now reliably bundled and found at runtime, preventing missing file errors in the executable.
- **Improved resource path handling:** Compatibility between development and frozen (executable) environments, so assets always load correctly.
- **Build process improvements:** Updated build script and `.spec` file for robust asset inclusion and easier future maintenance.

### Version 1.0.0 (Initial Release- 2025-07-19)
- **Complete CSV checklist application** with modern UI
- **Professional dark theme** with smooth animations
- **Custom frameless window** with native controls
- **Multi-column data support** with automatic text wrapping
- **Interactive checkboxes** with reliable click detection
- **Physics-based scrolling** with momentum
- **Windows integration** with proper icon support
- **Build automation** with PyInstaller
- **Complete documentation** and GitHub integration

For detailed changes, see [CHANGELOG.md](docs/CHANGELOG.md).
