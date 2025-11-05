#!/usr/bin/env python3
"""Generate placeholder icons for development."""

import os
from pathlib import Path

# Simple 32x32 PNG (blue square with white border)
PNG_32x32 = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000002000000020080200000073f5f2"
    "640000000467414d410000b18f0bfc610500000009704859730000177000001770"
    "01686f7768620000001c49444154785eed94010d00000c02a0ffaf8f1d64740000"
    "00000000be230d820a01b3cb87c70000000049454e44ae426082"
)

# Simple 128x128 PNG
PNG_128x128 = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000008000000080080200000053df1f"
    "e50000000467414d410000b18f0bfc610500000009704859730000177000001770"
    "01686f7768620000005a49444154785eedd4410a80200c0050bfe733a31d7ff2"
    "f22b4004a10a7c8c0eb8e07a20c80100000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000000000000000"
    "00000000000000f80bea020ea3c2f3d10000000049454e44ae426082"
)

def create_icon_files():
    """Create placeholder icon files."""
    icon_dir = Path("src-tauri/icons")
    icon_dir.mkdir(parents=True, exist_ok=True)

    # Create PNG files
    files = {
        "32x32.png": PNG_32x32,
        "128x128.png": PNG_128x128,
        "128x128@2x.png": PNG_128x128,  # Reuse 128 for now
        "icon.png": PNG_128x128,
    }

    for filename, data in files.items():
        filepath = icon_dir / filename
        filepath.write_bytes(data)
        print(f"Created {filepath}")

    # Create minimal ICO file (Windows)
    ico_path = icon_dir / "icon.ico"
    ico_path.write_bytes(PNG_32x32)  # Simple fallback
    print(f"Created {ico_path}")

    # Create minimal ICNS file (macOS)
    icns_path = icon_dir / "icon.icns"
    icns_path.write_bytes(PNG_128x128)  # Simple fallback
    print(f"Created {icns_path}")

    print("\nPlaceholder icons generated!")
    print("Note: These are minimal placeholders. Use proper icons for production.")
    print("      Run 'npm run tauri icon <source.png>' with a 1024x1024 PNG for real icons.")

if __name__ == "__main__":
    create_icon_files()
