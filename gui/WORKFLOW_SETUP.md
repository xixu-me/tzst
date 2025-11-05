# CI/CD Workflow Setup Instructions

## ⚠️ Important: Manual Setup Required

The GitHub Actions workflow file **cannot be automatically pushed** due to GitHub App permissions. The workflow configuration is ready but needs manual addition to your repository.

## Workflow File Location

The complete workflow is located at:
```
.github/workflows/build-gui.yml
```

This file exists in your local repository but is **untracked** in Git.

## How to Add the Workflow

### Option 1: Via GitHub Web Interface (Recommended)

1. Open `.github/workflows/build-gui.yml` in your local editor
2. Copy its entire contents
3. Go to your GitHub repository
4. Navigate to **Actions** tab → **New workflow** → **set up a workflow yourself**
5. Name it `build-gui.yml`
6. Paste the contents
7. Commit directly to `main` or your feature branch

### Option 2: Manual Git Push (Requires Direct Access)

If you have direct repository write access (not via GitHub App):

```bash
git add .github/workflows/build-gui.yml
git commit -m "Add GUI build workflow"
git push
```

### Option 3: Include in Pull Request

When you create a pull request from branch `claude/tauri-tzst-gui-011CUpAYMKfKZFeTyxvQi1DV`:

1. Manually add the workflow file via GitHub's web interface after creating the PR
2. Or ask a repository maintainer with appropriate permissions to add it

## What the Workflow Does

### Unsigned Builds (Runs on Every Push)
- **Windows**: MSI and NSIS installers (x64)
- **macOS**: APP bundles (Intel x64, Apple Silicon ARM64)
- **Linux**: DEB and AppImage packages (x64)
- Generates SHA256 checksums for all artifacts
- Uploads build artifacts to GitHub

### Signed Builds (Runs on Release Tags)
- Same as unsigned builds, plus:
- **Windows**: Code-signed installers
- **macOS**: Signed, notarized, and stapled builds
- Creates GitHub Release draft with all artifacts

## Required GitHub Secrets (For Signed Builds)

Configure these in **Settings** → **Secrets and variables** → **Actions**:

### Windows Code Signing
```
WINDOWS_CERTIFICATE          # Base64-encoded .pfx file
WINDOWS_CERTIFICATE_PASSWORD # Certificate password
```

### macOS Signing & Notarization
```
APPLE_CERTIFICATE            # Base64-encoded .p12 file
APPLE_CERTIFICATE_PASSWORD   # Certificate password
APPLE_ID                     # Your Apple ID email
APPLE_PASSWORD               # App-specific password
APPLE_TEAM_ID                # Developer Team ID (10 chars)
```

### How to Encode Certificates

**Windows (.pfx to base64):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("cert.pfx")) | Out-File cert.txt
```

**macOS (.p12 to base64):**
```bash
base64 -i cert.p12 -o cert.txt
```

## Testing Without Secrets

The workflow will run successfully without secrets configured:
- Unsigned builds will be created
- All platforms will build and test
- Artifacts will be uploaded
- Only signing/notarization steps will be skipped

## Triggering Builds

### Development Builds (Unsigned)
Any push to `main` or PR will trigger:
```bash
git push origin your-branch
```

### Release Builds (Signed)
Create and push a tag starting with `gui-v`:
```bash
git tag -a gui-v1.0.0 -m "Release GUI v1.0.0"
git push origin gui-v1.0.0
```

This will:
1. Build unsigned artifacts on all platforms
2. Build signed artifacts on Windows and macOS (if secrets are configured)
3. Create a draft GitHub Release with all artifacts
4. Generate and include checksums

## Platform Dependencies

The workflow automatically installs required dependencies:

- **Ubuntu**: WebKit2GTK, build tools, libraries
- **macOS**: Xcode Command Line Tools (pre-installed on GitHub runners)
- **Windows**: Visual Studio Build Tools (pre-installed on GitHub runners)

## Troubleshooting

### Workflow Not Appearing in Actions Tab
- Ensure the file is at `.github/workflows/build-gui.yml`
- Check the file has correct YAML syntax
- Workflow files must be in the default branch to appear

### Build Failures
- Check the "Actions" tab for detailed logs
- Common issues:
  - Missing dependencies (usually auto-fixed by install steps)
  - Rust compilation errors (check Cargo.toml)
  - Icon files missing (ensure all icons are committed)

### Signing Failures
- Verify secrets are correctly configured
- Check certificate hasn't expired
- For macOS: Ensure Apple Developer account is active
- Review signing logs in failed workflow run

## File Structure

```
.github/
└── workflows/
    └── build-gui.yml          # ← This needs manual addition
gui/
├── src/                       # Frontend (HTML/CSS/JS)
├── src-tauri/                 # Rust backend
│   ├── src/                   # Rust source
│   ├── icons/                 # App icons
│   └── Cargo.toml            # Dependencies
├── README.md                  # User documentation
├── OPS_GUIDE.md              # Operations guide
└── WORKFLOW_SETUP.md         # This file
```

## Next Steps After Adding Workflow

1. ✅ Add workflow file to repository (manual step above)
2. Verify workflow appears in "Actions" tab
3. Make a test commit to trigger a build
4. Review build artifacts
5. Configure signing secrets (optional, for production)
6. Test signed builds with a release tag

## Support

For issues with:
- **Workflow setup**: See this guide
- **Building locally**: See `gui/README.md`
- **Signing/packaging**: See `gui/OPS_GUIDE.md`
- **App functionality**: See `gui/README.md`

---

**Note**: Once a maintainer with `workflows` permission adds this file, all future updates can be made through normal pull requests.
