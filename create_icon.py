#!/usr/bin/env python3
"""
Icon Creator Script
Creates a proper multi-size ICO file from a large source image.
"""

from PIL import Image
import os
import sys

def create_icon_from_image(source_image_path, output_ico_path="checklist.ico"):
    """
    Create a multi-size ICO file from a source image.
    
    Args:
        source_image_path (str): Path to the source image (PNG, JPG, etc.)
        output_ico_path (str): Path for the output ICO file
    """
    
    # Standard Windows icon sizes
    icon_sizes = [
        (16, 16),    # Taskbar, file list
        (24, 24),    # Taskbar (high DPI)
        (32, 32),    # File explorer, desktop
        (48, 48),    # Desktop, file explorer
        (64, 64),    # Desktop (high DPI)
        (96, 96),    # Desktop (very high DPI)
        (128, 128),  # File properties
        (256, 256),  # File properties, modern Windows
    ]
    
    try:
        # Open the source image
        print(f"Opening source image: {source_image_path}")
        source_image = Image.open(source_image_path)
        
        # Convert to RGBA if not already (for transparency support)
        if source_image.mode != 'RGBA':
            source_image = source_image.convert('RGBA')
        
        print(f"Source image size: {source_image.size}")
        print(f"Source image mode: {source_image.mode}")
        
        # Create the ICO file with all sizes
        print(f"Creating ICO file with {len(icon_sizes)} sizes...")
        source_image.save(
            output_ico_path,
            format='ICO',
            sizes=icon_sizes,
            optimize=True
        )
        
        # Get file size
        file_size = os.path.getsize(output_ico_path)
        print(f"✅ Successfully created: {output_ico_path}")
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: Source image not found: {source_image_path}")
        return False
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        return False

def main():
    """Main function to handle command line usage."""
    
    if len(sys.argv) < 2:
        print("Icon Creator Script")
        print("Usage: python create_icon.py <source_image_path> [output_ico_path]")
        print("\nExample:")
        print("  python create_icon.py checklist_large.png")
        print("  python create_icon.py checklist_large.png my_icon.ico")
        print("\nThe script will create a multi-size ICO file with all standard Windows icon sizes.")
        return
    
    source_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "checklist.ico"
    
    success = create_icon_from_image(source_path, output_path)
    
    if success:
        print("\n🎉 Icon creation completed successfully!")
        print("You can now use this ICO file in your PyInstaller spec file.")
    else:
        print("\n💥 Icon creation failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 