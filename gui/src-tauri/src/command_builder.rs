use crate::{TaskConfig, TaskResult};
use std::path::PathBuf;
use std::process::Stdio;
use std::time::Instant;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;

/// Build tzst command arguments safely (no shell injection)
pub fn build_command(tzst_path: &PathBuf, task: &TaskConfig) -> Result<Vec<String>, String> {
    let mut args = vec![task.operation.clone()];

    // Add archive path
    args.push(task.archive_path.clone());

    // Add target paths for create/extract operations
    if !task.target_paths.is_empty() {
        args.extend(task.target_paths.clone());
    }

    // Add options
    if let Some(output_dir) = &task.output_dir {
        args.push("-o".to_string());
        args.push(output_dir.clone());
    }

    if let Some(level) = task.compression_level {
        args.push("-l".to_string());
        args.push(level.to_string());
    }

    if task.streaming {
        args.push("--streaming".to_string());
    }

    if task.verbose {
        args.push("-v".to_string());
    }

    if let Some(filter) = &task.filter {
        args.push("--filter".to_string());
        args.push(filter.clone());
    }

    Ok(args)
}

/// Execute tzst task asynchronously
pub async fn execute_task(
    tzst_path: PathBuf,
    task: TaskConfig,
) -> Result<TaskResult, String> {
    let args = build_command(&tzst_path, &task)?;

    let start = Instant::now();

    let mut child = Command::new(&tzst_path)
        .args(&args)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn process: {}", e))?;

    let stdout = child
        .stdout
        .take()
        .ok_or("Failed to capture stdout")?;
    let stderr = child
        .stderr
        .take()
        .ok_or("Failed to capture stderr")?;

    let mut stdout_reader = BufReader::new(stdout).lines();
    let mut stderr_reader = BufReader::new(stderr).lines();

    let mut stdout_lines = Vec::new();
    let mut stderr_lines = Vec::new();

    // Read stdout and stderr concurrently
    let stdout_task = tokio::spawn(async move {
        let mut lines = Vec::new();
        while let Ok(Some(line)) = stdout_reader.next_line().await {
            lines.push(line);
        }
        lines
    });

    let stderr_task = tokio::spawn(async move {
        let mut lines = Vec::new();
        while let Ok(Some(line)) = stderr_reader.next_line().await {
            lines.push(line);
        }
        lines
    });

    stdout_lines = stdout_task.await.map_err(|e| e.to_string())?;
    stderr_lines = stderr_task.await.map_err(|e| e.to_string())?;

    let status = child.wait().await.map_err(|e| e.to_string())?;
    let duration = start.elapsed();

    Ok(TaskResult {
        success: status.success(),
        exit_code: status.code().unwrap_or(-1),
        stdout: stdout_lines.join("\n"),
        stderr: stderr_lines.join("\n"),
        duration_ms: duration.as_millis() as u64,
    })
}
