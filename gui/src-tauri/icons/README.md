# Icons

This directory should contain application icons in the following formats:

## Required Icons

- `32x32.png` - Small icon (32x32 pixels)
- `128x128.png` - Medium icon (128x128 pixels)
- `128x128@2x.png` - Medium icon for HiDPI (256x256 pixels)
- `icon.icns` - macOS icon bundle
- `icon.ico` - Windows icon

## Generating Icons

You can use the `@tauri-apps/cli` to generate icons from a source PNG:

```bash
npm run tauri icon /path/to/source-icon.png
```

The source icon should be at least 1024x1024 pixels for best results.

## Placeholder Icons

For development, you can use simple colored PNG files. The build system will use these
as-is, though production builds should use properly designed icons.

## Icon Design Guidelines

- Use the tzst logo or branding
- Ensure good contrast for both light and dark backgrounds
- Keep designs simple and recognizable at small sizes
- Follow platform-specific design guidelines:
  - macOS: Rounded square with subtle gradient
  - Windows: Flat or slightly 3D design
  - Linux: Flat design with good contrast
