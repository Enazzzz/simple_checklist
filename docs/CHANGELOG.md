# Changelog

All notable changes to the CSV Checklist Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-07-21

### Fixed
- Fixed asset loading for PyInstaller builds: all icons and images are now reliably bundled and found at runtime.
- Improved resource path handling for compatibility between development and frozen (executable) environments.
- Updated build script and spec file for robust asset inclusion.

---

## [1.0.0] - 2025-01-XX

### Added
- **Initial Release** - Complete CSV checklist application
- **Modern Dark Theme UI** with professional color palette
- **Custom Frameless Window** with rounded corners and native controls
- **Smooth Animations** for checkboxes and hover effects
- **Physics-based Scrolling** with momentum and acceleration
- **Multi-column CSV Support** with automatic text wrapping
- **Interactive Checkboxes** with hover animations and reliable click detection
- **Window Management** - draggable, resizable, minimize/maximize/close
- **Native File Dialog** for CSV file loading
- **Keyboard Navigation** support (arrow keys for scrolling)
- **High DPI Support** for modern displays
- **Anti-aliased UI Elements** throughout the interface
- **Gradient Scrollbar** with hover effects
- **Professional Icon System** with multi-size ICO support

### Technical Features
- **Pygame-based Rendering** with custom drawing functions
- **Windows Native Integration** via pywin32
- **PyInstaller Build System** with complete asset inclusion
- **Icon Creation Utility** for custom application icons
- **Windows Icon Cache Management** for proper icon display
- **Comprehensive Error Handling** and logging
- **Responsive Layout** that adapts to content and window size

### Build & Distribution
- **Automated Build Scripts** for easy compilation
- **GitHub Actions Workflow** for continuous integration
- **Complete Documentation** including README, CONTRIBUTING, and LICENSE
- **Issue Templates** for bug reports and feature requests
- **Professional Project Structure** ready for open source

### Files Included
- Main application (`checklist.py`)
- PyInstaller configuration (`checklist.spec`)
- Build automation (`build.bat`, `install.bat`)
- Icon utilities (`create_icon.py`, `refresh_icons.bat`)
- Documentation (`README.md`, `CONTRIBUTING.md`, `LICENSE`)
- Sample data (`sample_data.csv`)
- Dependencies (`requirements.txt`)
- GitHub integration (`.github/` folder)

---

## Version History

### Version 1.0.0
- **Initial stable release**
- Complete feature set for CSV checklist management
- Professional UI with modern design
- Full Windows integration
- Ready for production use 