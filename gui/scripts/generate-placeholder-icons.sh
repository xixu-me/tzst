#!/bin/bash
# Generate placeholder icons for development
# Requires ImageMagick: sudo apt-get install imagemagick (Linux) or brew install imagemagick (macOS)

set -e

ICON_DIR="src-tauri/icons"
mkdir -p "$ICON_DIR"

# Create a simple colored square as base
# Using tzst brand color (blue)
COLOR="#2563eb"

echo "Generating placeholder icons..."

# Generate PNG icons
convert -size 32x32 xc:"$COLOR" -fill white -gravity center -pointsize 20 -annotate +0+0 "T" "$ICON_DIR/32x32.png"
convert -size 128x128 xc:"$COLOR" -fill white -gravity center -pointsize 80 -annotate +0+0 "T" "$ICON_DIR/128x128.png"
convert -size 256x256 xc:"$COLOR" -fill white -gravity center -pointsize 160 -annotate +0+0 "T" "$ICON_DIR/128x128@2x.png"
convert -size 512x512 xc:"$COLOR" -fill white -gravity center -pointsize 320 -annotate +0+0 "T" "$ICON_DIR/icon.png"

# Generate ICO for Windows (requires multiple sizes)
convert "$ICON_DIR/32x32.png" "$ICON_DIR/icon.png" "$ICON_DIR/icon.ico"

# Generate ICNS for macOS (requires iconutil on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    ICONSET_DIR="$ICON_DIR/icon.iconset"
    mkdir -p "$ICONSET_DIR"

    sips -z 16 16 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_16x16.png"
    sips -z 32 32 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_16x16@2x.png"
    sips -z 32 32 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_32x32.png"
    sips -z 64 64 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_32x32@2x.png"
    sips -z 128 128 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_128x128.png"
    sips -z 256 256 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_128x128@2x.png"
    sips -z 256 256 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_256x256.png"
    sips -z 512 512 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_256x256@2x.png"
    sips -z 512 512 "$ICON_DIR/icon.png" --out "$ICONSET_DIR/icon_512x512.png"
    cp "$ICON_DIR/icon.png" "$ICONSET_DIR/icon_512x512@2x.png"

    iconutil -c icns "$ICONSET_DIR" -o "$ICON_DIR/icon.icns"
    rm -rf "$ICONSET_DIR"
    echo "Generated macOS .icns file"
else
    echo "Skipping .icns generation (requires macOS)"
    # Create a dummy file for Linux builds
    touch "$ICON_DIR/icon.icns"
fi

echo "Placeholder icons generated successfully!"
echo "Note: These are development placeholders. Use proper icons for production."
