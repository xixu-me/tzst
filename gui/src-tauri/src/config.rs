use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AppConfig {
    pub tzst_path: Option<PathBuf>,
    pub theme: String,
    pub language: String,
    pub history_limit: usize,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            tzst_path: None,
            theme: "light".to_string(),
            language: "en".to_string(),
            history_limit: 100,
        }
    }
}

impl AppConfig {
    pub fn load() -> Result<Self> {
        let config_dir = Self::config_dir()?;
        let config_path = config_dir.join("config.json");

        if config_path.exists() {
            let content = std::fs::read_to_string(&config_path)?;
            let config: Self = serde_json::from_str(&content)?;
            Ok(config)
        } else {
            Ok(Self::default())
        }
    }

    pub fn save(&self) -> Result<()> {
        let config_dir = Self::config_dir()?;
        std::fs::create_dir_all(&config_dir)?;

        let config_path = config_dir.join("config.json");
        let content = serde_json::to_string_pretty(self)?;
        std::fs::write(&config_path, content)?;

        Ok(())
    }

    fn config_dir() -> Result<PathBuf> {
        let dir = if cfg!(target_os = "macos") {
            let home = std::env::var("HOME")?;
            PathBuf::from(home).join("Library/Application Support/tzst-gui")
        } else if cfg!(target_os = "windows") {
            let appdata = std::env::var("APPDATA")?;
            PathBuf::from(appdata).join("tzst-gui")
        } else {
            // Linux and others
            let home = std::env::var("HOME")?;
            PathBuf::from(home).join(".config/tzst-gui")
        };

        Ok(dir)
    }
}
