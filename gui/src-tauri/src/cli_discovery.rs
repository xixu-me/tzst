use crate::TzstInfo;
use anyhow::{anyhow, Result};
use std::path::{Path, PathBuf};
use std::process::Command;

/// Discover tzst on the system PATH
pub fn discover_tzst() -> Result<TzstInfo, String> {
    // Try to find tzst in PATH
    match which::which("tzst") {
        Ok(path) => validate_tzst_path(&path),
        Err(_) => {
            // On Windows, also try with extensions
            #[cfg(target_os = "windows")]
            {
                for ext in &["exe", "cmd", "bat"] {
                    let name = format!("tzst.{}", ext);
                    if let Ok(path) = which::which(&name) {
                        return validate_tzst_path(&path);
                    }
                }
            }
            Err("tzst not found in PATH".to_string())
        }
    }
}

/// Validate a given tzst path
pub fn validate_tzst_path(path: &Path) -> Result<TzstInfo, String> {
    if !path.exists() {
        return Err(format!("Path does not exist: {}", path.display()));
    }

    // Check if it's executable (Unix) or has proper extension (Windows)
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let metadata = std::fs::metadata(path).map_err(|e| e.to_string())?;
        let permissions = metadata.permissions();
        if permissions.mode() & 0o111 == 0 {
            return Err(format!("File is not executable: {}", path.display()));
        }
    }

    #[cfg(windows)]
    {
        let ext = path.extension().and_then(|s| s.to_str()).unwrap_or("");
        if !["exe", "cmd", "bat"].contains(&ext.to_lowercase().as_str()) {
            return Err(format!(
                "File does not have a valid executable extension: {}",
                path.display()
            ));
        }
    }

    // Try to get version
    match get_version(path) {
        Ok(version) => Ok(TzstInfo {
            path: path.to_string_lossy().to_string(),
            version,
            is_valid: true,
        }),
        Err(e) => Err(format!("Failed to get version: {}", e)),
    }
}

/// Get tzst version
pub fn get_version(path: &Path) -> Result<String, String> {
    let output = Command::new(path)
        .arg("--version")
        .output()
        .map_err(|e| format!("Failed to execute tzst: {}", e))?;

    if !output.status.success() {
        return Err(format!(
            "tzst --version failed with exit code: {}",
            output.status
        ));
    }

    let version = String::from_utf8_lossy(&output.stdout)
        .trim()
        .to_string();

    Ok(version)
}

#[cfg(target_os = "macos")]
pub fn get_path_additions() -> Vec<PathBuf> {
    // On macOS, GUI apps don't inherit the full PATH from the terminal
    // Add common locations where tzst might be installed
    vec![
        PathBuf::from("/usr/local/bin"),
        PathBuf::from("/opt/homebrew/bin"),
        PathBuf::from("/opt/local/bin"),
        PathBuf::from(format!("{}/.local/bin", std::env::var("HOME").unwrap_or_default())),
    ]
}

#[cfg(not(target_os = "macos"))]
pub fn get_path_additions() -> Vec<PathBuf> {
    vec![]
}
