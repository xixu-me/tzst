# Operations Guide - tzst GUI

## Overview

This guide covers building, signing, packaging, and releasing the tzst GUI application for all supported platforms.

## Prerequisites

### Development Environment

All platforms require:
- Rust 1.70+ (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`)
- Node.js 18+ and npm
- Git

### Platform-Specific Tools

#### Linux Build Machine
```bash
# Ubuntu/Debian
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
    librsvg2-dev \
    rpm

# For AppImage
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

#### macOS Build Machine
```bash
# Install Xcode
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Windows Build Machine
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
   - Select "Desktop development with C++"
   - Include Windows 10/11 SDK
2. Install [WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/)
3. Install [WiX Toolset 3.11+](https://wixtoolset.org/releases/) for MSI creation

## Building

### Local Development Build

```bash
cd gui
npm install
npm run dev
```

### Production Build

```bash
cd gui
npm install
npm run build
```

Build artifacts location: `src-tauri/target/release/bundle/`

### Cross-Platform CI Builds

See `.github/workflows/build-gui.yml` for complete CI setup.

## Code Signing

### Windows Code Signing

#### Option 1: Using a .pfx Certificate

1. Obtain a code signing certificate from a CA (DigiCert, Sectigo, etc.)
2. Export as .pfx with password
3. Set environment variables:
   ```powershell
   $env:TAURI_SIGNING_PRIVATE_KEY="C:\path\to\cert.pfx"
   $env:TAURI_SIGNING_PRIVATE_KEY_PASSWORD="your-password"
   ```
4. Build: `npm run build`

#### Option 2: Using signtool (Manual)

```powershell
# After building
signtool sign /f "C:\path\to\cert.pfx" /p "password" /tr http://timestamp.digicert.com /td sha256 /fd sha256 "src-tauri\target\release\bundle\msi\tzst-gui_1.0.0_x64.msi"
```

#### CI/CD Setup

Store in GitHub Secrets:
- `WINDOWS_CERTIFICATE`: Base64-encoded .pfx
- `WINDOWS_CERTIFICATE_PASSWORD`: Certificate password

```yaml
# .github/workflows/build-gui.yml
- name: Decode certificate
  run: |
    $cert = [Convert]::FromBase64String("${{ secrets.WINDOWS_CERTIFICATE }}")
    [IO.File]::WriteAllBytes("cert.pfx", $cert)

- name: Build and sign
  env:
    TAURI_SIGNING_PRIVATE_KEY: cert.pfx
    TAURI_SIGNING_PRIVATE_KEY_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
  run: npm run build
```

#### SmartScreen Reputation

New certificates have no reputation, causing SmartScreen warnings:
- This is normal and expected
- Reputation builds over time (typically 3-6 months)
- Users can bypass: "More info" → "Run anyway"
- Consider EV certificate for immediate reputation

### macOS Code Signing and Notarization

#### Prerequisites

1. Apple Developer account ($99/year)
2. Developer ID Application certificate
3. App-specific password for notarization

#### Setup

```bash
# Install developer certificate in Keychain
# Download from developer.apple.com

# Create app-specific password
# Visit appleid.apple.com → Security → App-Specific Passwords

# Store credentials
export APPLE_ID="your@apple.id"
export APPLE_PASSWORD="xxxx-xxxx-xxxx-xxxx"  # App-specific password
export APPLE_TEAM_ID="XXXXXXXXXX"  # Find in developer.apple.com
```

#### Build and Sign

```bash
npm run build
```

Tauri automatically signs during build if certificate is in Keychain.

#### Notarization Process

```bash
# Archive the app
cd src-tauri/target/release/bundle/macos
ditto -c -k --keepParent "tzst GUI.app" tzst-gui.zip

# Submit for notarization
xcrun notarytool submit tzst-gui.zip \
  --apple-id "$APPLE_ID" \
  --password "$APPLE_PASSWORD" \
  --team-id "$APPLE_TEAM_ID" \
  --wait

# Check status (if needed)
xcrun notarytool history --apple-id "$APPLE_ID" --password "$APPLE_PASSWORD" --team-id "$APPLE_TEAM_ID"

# Get logs if failed
xcrun notarytool log <submission-id> --apple-id "$APPLE_ID" --password "$APPLE_PASSWORD" --team-id "$APPLE_TEAM_ID"

# Staple the notarization ticket
xcrun stapler staple "tzst GUI.app"

# Verify
spctl -a -vvv -t install "tzst GUI.app"
```

#### Create DMG

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "tzst GUI" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "tzst GUI.app" 200 190 \
  --hide-extension "tzst GUI.app" \
  --app-drop-link 600 185 \
  "tzst-gui_1.0.0_aarch64.dmg" \
  "tzst GUI.app"

# Notarize the DMG
xcrun notarytool submit tzst-gui_1.0.0_aarch64.dmg \
  --apple-id "$APPLE_ID" \
  --password "$APPLE_PASSWORD" \
  --team-id "$APPLE_TEAM_ID" \
  --wait

# Staple
xcrun stapler staple tzst-gui_1.0.0_aarch64.dmg
```

#### CI/CD Setup

Store in GitHub Secrets:
- `APPLE_CERTIFICATE`: Base64-encoded .p12 certificate
- `APPLE_CERTIFICATE_PASSWORD`: Certificate password
- `APPLE_ID`: Apple ID email
- `APPLE_PASSWORD`: App-specific password
- `APPLE_TEAM_ID`: Team ID

```yaml
# .github/workflows/build-gui.yml
- name: Import certificate
  run: |
    echo "${{ secrets.APPLE_CERTIFICATE }}" | base64 --decode > cert.p12
    security create-keychain -p actions build.keychain
    security default-keychain -s build.keychain
    security unlock-keychain -p actions build.keychain
    security import cert.p12 -k build.keychain -P "${{ secrets.APPLE_CERTIFICATE_PASSWORD }}" -T /usr/bin/codesign
    security set-key-partition-list -S apple-tool:,apple: -s -k actions build.keychain

- name: Build and notarize
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
    APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
  run: |
    npm run build
    # Notarization steps...
```

### Linux Signing (Optional)

Linux packages don't require signing, but you can sign .deb packages:

```bash
# Generate GPG key
gpg --gen-key

# Sign package
dpkg-sig --sign builder tzst-gui_1.0.0_amd64.deb

# Verify
dpkg-sig --verify tzst-gui_1.0.0_amd64.deb
```

## Packaging

### Windows

Builds produce:
- `tzst-gui_1.0.0_x64_en-US.msi` (recommended)
- `tzst-gui_1.0.0_x64-setup.exe` (NSIS installer)

### macOS

Builds produce:
- `tzst GUI.app` (application bundle)
- `tzst-gui_1.0.0_aarch64.dmg` (disk image for distribution)

### Linux

Builds produce:
- `tzst-gui_1.0.0_amd64.deb` (Debian/Ubuntu)
- `tzst-gui_1.0.0_amd64.AppImage` (universal)

For RPM:
1. Add `"rpm"` to `bundle.targets` in `tauri.conf.json`
2. Install `rpm`: `sudo apt-get install rpm`
3. Build: `npm run build`
4. Output: `tzst-gui-1.0.0-1.x86_64.rpm`

## Release Checklist

### Pre-Release

- [ ] Update version in `gui/package.json`
- [ ] Update version in `gui/src-tauri/Cargo.toml`
- [ ] Update version in `gui/src-tauri/tauri.conf.json`
- [ ] Update `CHANGELOG.md`
- [ ] Update documentation if needed
- [ ] Run full test suite
- [ ] Test on all target platforms

### Build

- [ ] Windows x64 build
- [ ] Windows ARM64 build (if supported)
- [ ] macOS x64 (Intel) build
- [ ] macOS ARM64 (Apple Silicon) build
- [ ] Linux x64 build
- [ ] Linux ARM64 build (optional)

### Sign and Notarize

- [ ] Sign Windows builds
- [ ] Sign macOS builds
- [ ] Notarize macOS builds
- [ ] Staple notarization to macOS builds
- [ ] Verify all signatures

### Package

- [ ] Create Windows installers (MSI + EXE)
- [ ] Create macOS DMGs
- [ ] Create Linux packages (DEB + AppImage + RPM)
- [ ] Generate SHA256 checksums for all artifacts

### Test

- [ ] Install and run on Windows 10/11
- [ ] Install and run on macOS 12+ (Intel and Apple Silicon)
- [ ] Install and run on Ubuntu 20.04/22.04
- [ ] Verify tzst discovery works
- [ ] Test all operations (create, extract, list, test)
- [ ] Check for security warnings/blocks

### Release

- [ ] Create Git tag: `git tag -a gui-v1.0.0 -m "Release v1.0.0"`
- [ ] Push tag: `git push origin gui-v1.0.0`
- [ ] Create GitHub release
- [ ] Upload all artifacts
- [ ] Include checksums file
- [ ] Write release notes
- [ ] Publish release

## Troubleshooting

### Build Failures

#### Windows: "Cannot find Visual Studio"
```powershell
# Verify installation
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"

# Set environment
$env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin"
```

#### macOS: "Code signing failed"
```bash
# List available identities
security find-identity -v -p codesigning

# Verify certificate is valid
security find-certificate -c "Developer ID Application" -p
```

#### Linux: "Cannot find webkit2gtk"
```bash
# Ensure packages are installed
sudo apt-get install -y libwebkit2gtk-4.1-dev

# Verify pkg-config can find it
pkg-config --modversion webkit2gtk-4.1
```

### Signing Issues

#### Windows: SmartScreen Warning
- Normal for new certificates
- No fix except time (3-6 months) or EV certificate
- Users can bypass safely

#### macOS: "App is damaged and can't be opened"
- Quarantine attribute issue
- Fix: `xattr -cr /path/to/app`
- Prevent: Ensure proper notarization

#### macOS: Notarization Fails
```bash
# Get detailed logs
xcrun notarytool log <submission-id> --apple-id "$APPLE_ID" --password "$APPLE_PASSWORD" --team-id "$APPLE_TEAM_ID" > notarization.log

# Common issues:
# 1. Hardened runtime not enabled → Check tauri.conf.json
# 2. Missing entitlements → Add to tauri.conf.json
# 3. Unsigned dependencies → All binaries must be signed
```

### Size Optimization

Current targets:
- Windows: < 80 MB
- macOS: < 60 MB
- Linux: < 60 MB

To reduce size:

1. **Enable stripping** (already in `Cargo.toml`):
   ```toml
   [profile.release]
   strip = true
   ```

2. **Optimize dependencies**:
   ```toml
   [profile.release]
   lto = true
   codegen-units = 1
   opt-level = "z"
   ```

3. **Exclude unnecessary files**:
   Update `bundle` in `tauri.conf.json`

## Monitoring and Telemetry

### Crash Reporting (Optional)

Consider integrating Sentry or similar:

```rust
// In main.rs
#[cfg(not(debug_assertions))]
fn init_sentry() {
    let _guard = sentry::init(("https://your-dsn@sentry.io/project", sentry::ClientOptions {
        release: sentry::release_name!(),
        ..Default::default()
    }));
}
```

### Update Checking

Tauri has built-in update support. To enable:

1. Add updater to `tauri.conf.json`
2. Set up update server
3. Sign updates with private key

## Security Considerations

### Release Signing Keys

- Store signing keys in secure vault (1Password, Azure Key Vault, etc.)
- Use separate keys for different platforms
- Rotate keys annually
- Never commit keys to repository
- Use GitHub Secrets for CI/CD

### Dependency Audits

```bash
# Rust dependencies
cargo audit

# npm dependencies
npm audit

# Fix automatically
npm audit fix
```

### Security Updates

- Monitor CVEs for Tauri, Rust, and Node.js
- Update dependencies monthly
- Test thoroughly after updates
- Release security patches quickly

## Resources

- [Tauri Documentation](https://tauri.app/v2/)
- [Tauri Code Signing Guide](https://tauri.app/v2/guides/distribution/sign/)
- [Apple Notarization Guide](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Windows Code Signing Best Practices](https://docs.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-best-practices)

## Support

For issues with builds or releases:
1. Check GitHub Issues
2. Review Tauri Discord
3. Consult this ops guide
4. Create detailed bug report with logs
