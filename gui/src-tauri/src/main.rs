// Prevents console window from appearing on Windows in release builds
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod cli_discovery;
mod command_builder;
mod config;

use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::sync::Mutex;
use tauri::State;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct TzstInfo {
    path: String,
    version: String,
    is_valid: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct TaskConfig {
    operation: String,
    archive_path: String,
    target_paths: Vec<String>,
    output_dir: Option<String>,
    compression_level: Option<u8>,
    streaming: bool,
    verbose: bool,
    filter: Option<String>,
    dry_run: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct TaskResult {
    success: bool,
    exit_code: i32,
    stdout: String,
    stderr: String,
    duration_ms: u64,
}

struct AppState {
    tzst_path: Mutex<Option<PathBuf>>,
    config: Mutex<config::AppConfig>,
}

#[tauri::command]
async fn discover_tzst() -> Result<TzstInfo, String> {
    cli_discovery::discover_tzst()
}

#[tauri::command]
async fn validate_tzst_path(path: String) -> Result<TzstInfo, String> {
    cli_discovery::validate_tzst_path(&PathBuf::from(path))
}

#[tauri::command]
async fn get_tzst_version(state: State<'_, AppState>) -> Result<String, String> {
    let path_guard = state.tzst_path.lock().unwrap();
    if let Some(path) = path_guard.as_ref() {
        cli_discovery::get_version(path)
    } else {
        Err("tzst path not configured".to_string())
    }
}

#[tauri::command]
async fn set_tzst_path(path: String, state: State<'_, AppState>) -> Result<(), String> {
    let path_buf = PathBuf::from(path);
    cli_discovery::validate_tzst_path(&path_buf)?;

    let mut path_guard = state.tzst_path.lock().unwrap();
    *path_guard = Some(path_buf.clone());

    let mut config = state.config.lock().unwrap();
    config.tzst_path = Some(path_buf);
    config.save().map_err(|e| e.to_string())?;

    Ok(())
}

#[tauri::command]
async fn build_command(task: TaskConfig, state: State<'_, AppState>) -> Result<Vec<String>, String> {
    let path_guard = state.tzst_path.lock().unwrap();
    let tzst_path = path_guard.as_ref().ok_or("tzst path not configured")?;

    command_builder::build_command(tzst_path, &task)
}

#[tauri::command]
async fn execute_task(
    task: TaskConfig,
    state: State<'_, AppState>,
) -> Result<TaskResult, String> {
    let path_guard = state.tzst_path.lock().unwrap();
    let tzst_path = path_guard.as_ref().ok_or("tzst path not configured")?.clone();
    drop(path_guard);

    command_builder::execute_task(tzst_path, task).await
}

#[tauri::command]
async fn get_config(state: State<'_, AppState>) -> Result<config::AppConfig, String> {
    let config = state.config.lock().unwrap();
    Ok(config.clone())
}

#[tauri::command]
async fn save_config(config: config::AppConfig, state: State<'_, AppState>) -> Result<(), String> {
    let mut state_config = state.config.lock().unwrap();
    *state_config = config.clone();
    config.save().map_err(|e| e.to_string())
}

fn main() {
    // Load configuration
    let config = config::AppConfig::load().unwrap_or_default();
    let tzst_path = config.tzst_path.clone();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .manage(AppState {
            tzst_path: Mutex::new(tzst_path),
            config: Mutex::new(config),
        })
        .invoke_handler(tauri::generate_handler![
            discover_tzst,
            validate_tzst_path,
            get_tzst_version,
            set_tzst_path,
            build_command,
            execute_task,
            get_config,
            save_config,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
