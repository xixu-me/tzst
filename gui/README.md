# tzst GUI

Cross-platform desktop application for managing tzst archives.

## Overview

This is a Tauri-based GUI client that provides a user-friendly interface for the `tzst` command-line tool. It discovers and executes the `tzst` CLI found on your system PATH, offering features like:

- **CLI Discovery & Validation**: Automatically finds tzst or lets you specify a custom path
- **Task Configuration**: Easy-to-use forms for create, extract, list, and test operations
- **Live Execution**: Real-time output streaming and progress tracking
- **Command History**: Track all executed commands
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Prerequisites

### Required

1. **tzst CLI**: The `tzst` command-line tool must be installed and available on your PATH
   - Install from PyPI: `pip install tzst`
   - Or download from [GitHub releases](https://github.com/xixu-me/tzst/releases)

2. **Development Tools** (for building from source):
   - Rust 1.70+ and Cargo
   - Node.js 18+ and npm
   - Platform-specific dependencies (see below)

### Platform-Specific Dependencies

#### Linux
```bash
sudo apt-get update
sudo apt-get install -y \
    libwebkit2gtk-4.1-dev \
    build-essential \
    curl \
    wget \
    file \
    libxdo-dev \
    libssl-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```

#### macOS
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

#### Windows
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Install [WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) (usually pre-installed on Windows 10/11)

## Development

### Setup

```bash
cd gui
npm install
```

### Run in Development Mode

```bash
npm run dev
```

This will start the app in development mode with hot-reload enabled.

### Build for Production

```bash
npm run build
```

Build artifacts will be created in `src-tauri/target/release/bundle/`.

## Installation

### From Binary Releases

Download the appropriate installer for your platform from the releases page:

- **Windows**: `.msi` or `.exe`
- **macOS**: `.dmg` or `.app`
- **Linux**: `.deb` or `.AppImage`

### Windows Installation

1. Download `tzst-gui_x.x.x_x64.msi`
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu

**Note**: Windows may show a SmartScreen warning on first run. Click "More info" → "Run anyway". This is normal for new applications without established reputation.

### macOS Installation

1. Download `tzst-gui_x.x.x_aarch64.dmg` (Apple Silicon) or `tzst-gui_x.x.x_x64.dmg` (Intel)
2. Open the DMG file
3. Drag the app to Applications folder
4. On first launch, right-click → "Open" to bypass Gatekeeper

**Important**: The app requires a notarized build to run without warnings. See [macOS Notarization](#macos-notarization) below.

### Linux Installation

#### Debian/Ubuntu (.deb)
```bash
sudo dpkg -i tzst-gui_x.x.x_amd64.deb
sudo apt-get install -f  # Install dependencies
```

#### AppImage
```bash
chmod +x tzst-gui_x.x.x_amd64.AppImage
./tzst-gui_x.x.x_amd64.AppImage
```

## Usage

### First Run

1. Launch the application
2. Navigate to **Settings**
3. Click **Auto Discover** to find tzst on your PATH
   - If tzst is not found, click **Browse** to manually select the executable
4. Verify the version information is displayed

### Creating an Archive

1. Navigate to **Create**
2. Enter the archive path (e.g., `/path/to/backup.tzst`)
3. Add files/directories to include (one per line)
4. Adjust compression level (1-22, default: 3)
5. Click **Create Archive**

### Extracting an Archive

1. Navigate to **Extract**
2. Enter the archive path
3. Specify output directory (optional)
4. Select security filter (default: "data" for maximum security)
5. Click **Extract Archive**

### Listing Archive Contents

1. Navigate to **List**
2. Enter the archive path
3. Enable verbose output for detailed information
4. Click **List Contents**

### Testing Archive Integrity

1. Navigate to **Test**
2. Enter the archive path
3. Click **Test Archive**

## Configuration

Configuration is stored in platform-specific locations:

- **Linux**: `~/.config/tzst-gui/config.json`
- **macOS**: `~/Library/Application Support/tzst-gui/config.json`
- **Windows**: `%APPDATA%\tzst-gui\config.json`

### Configuration Options

```json
{
  "tzst_path": "/usr/local/bin/tzst",
  "theme": "light",
  "language": "en",
  "history_limit": 100
}
```

## Troubleshooting

### tzst Not Found on PATH

**Symptoms**: "tzst not found in PATH" error on launch

**Solutions**:

1. **Verify tzst installation**:
   ```bash
   which tzst  # Linux/macOS
   where tzst  # Windows
   ```

2. **Add to PATH**:
   - Linux/macOS: Add to `~/.bashrc` or `~/.zshrc`:
     ```bash
     export PATH="$PATH:/path/to/tzst/directory"
     ```
   - Windows: Add to PATH via System Properties → Environment Variables

3. **macOS-specific**: GUI apps may not inherit terminal PATH
   - Use the manual browse option in Settings
   - Common locations: `/usr/local/bin/tzst`, `/opt/homebrew/bin/tzst`

4. **Manual configuration**:
   - Click **Browse** in Settings
   - Navigate to tzst executable
   - Select and confirm

### Windows Script Execution

If you have `tzst.cmd` or `tzst.bat` instead of `tzst.exe`:

1. The app will attempt to use it automatically
2. Ensure the script is on your PATH
3. You may need to specify the full path in Settings

### Permission Denied (Linux/macOS)

If you encounter permission errors:

```bash
# Make tzst executable
chmod +x /path/to/tzst

# Or reinstall with proper permissions
pip install --user tzst
```

### AppImage Won't Run (Linux)

```bash
# Enable execution
chmod +x tzst-gui_*.AppImage

# Install FUSE if needed
sudo apt-get install fuse libfuse2

# Run
./tzst-gui_*.AppImage
```

## Security

### Shell Command Execution

The app uses Tauri's shell plugin with strict allowlisting:

- Only `tzst` command is permitted
- All arguments are passed as arrays (no shell interpolation)
- User-provided paths are validated

### Content Security Policy

The web UI runs with a strict CSP:
```
default-src 'self';
style-src 'self' 'unsafe-inline';
script-src 'self' 'unsafe-inline'
```

### macOS Hardened Runtime

Production builds use Hardened Runtime with:
- Code signing
- Notarization
- Entitlements for necessary permissions

## Building for Distribution

### Windows Code Signing

1. Obtain a code signing certificate
2. Set environment variables:
   ```
   TAURI_SIGNING_PRIVATE_KEY=path/to/private-key.pfx
   TAURI_SIGNING_PRIVATE_KEY_PASSWORD=your-password
   ```
3. Build: `npm run build`

### macOS Notarization

1. Obtain an Apple Developer account
2. Create an App-Specific Password
3. Set environment variables:
   ```bash
   export APPLE_ID=your@apple.id
   export APPLE_PASSWORD=app-specific-password
   export APPLE_TEAM_ID=your-team-id
   ```
4. Build and notarize:
   ```bash
   npm run build
   xcrun notarytool submit src-tauri/target/release/bundle/macos/tzst-gui.app.zip \
     --apple-id "$APPLE_ID" \
     --password "$APPLE_PASSWORD" \
     --team-id "$APPLE_TEAM_ID" \
     --wait
   xcrun stapler staple src-tauri/target/release/bundle/macos/tzst-gui.app
   ```

### Linux Packaging

Builds automatically create:
- `.deb` for Debian/Ubuntu
- `.AppImage` for universal Linux

For `.rpm`:
```bash
# Install rpm tools
sudo apt-get install rpm

# Update tauri.conf.json to include "rpm" in bundle.targets
npm run build
```

## CI/CD

See `.github/workflows/build-gui.yml` for automated builds across all platforms.

The workflow:
1. Builds for Linux (x64, arm64)
2. Builds for macOS (x64, Apple Silicon)
3. Builds for Windows (x64, arm64)
4. Signs and notarizes (when credentials are available)
5. Creates release artifacts with checksums

## Architecture

### Backend (Rust)

- `src-tauri/src/main.rs`: Main entry point, Tauri commands
- `src-tauri/src/cli_discovery.rs`: PATH discovery and validation
- `src-tauri/src/command_builder.rs`: Safe command building and execution
- `src-tauri/src/config.rs`: Configuration management

### Frontend (Web)

- `src/index.html`: UI structure
- `src/styles.css`: Styling with light/dark theme support
- `src/main.js`: Application logic and Tauri API integration

### Communication

Frontend ↔ Tauri API ↔ Rust Backend ↔ tzst CLI

## License

BSD 3-Clause (same as tzst)

## Contributing

Contributions are welcome! Please see the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

For GUI-specific issues:
1. Check if it's a tzst CLI issue or GUI issue
2. Include OS version and desktop environment
3. Provide steps to reproduce
4. Include relevant logs from the app

## Acknowledgments

- [Tauri](https://tauri.app/) - The framework powering this app
- [tzst](https://github.com/xixu-me/tzst) - The underlying archive tool
