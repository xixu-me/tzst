import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-dialog';

// State
let currentView = 'create';
let commandHistory = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initSettings();
    initCreateView();
    initExtractView();
    initListView();
    initTestView();
    loadConfig();
});

// Navigation
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });
}

function switchView(view) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Update views
    document.querySelectorAll('.view').forEach(v => {
        v.style.display = 'none';
    });
    document.getElementById(`${view}-view`).style.display = 'block';

    currentView = view;
}

// Settings
function initSettings() {
    document.getElementById('discover-btn').addEventListener('click', discoverTzst);
    document.getElementById('browse-btn').addEventListener('click', browseTzst);
    document.getElementById('theme-select').addEventListener('change', changeTheme);
    document.getElementById('language-select').addEventListener('change', changeLanguage);
}

async function discoverTzst() {
    const infoBox = document.getElementById('tzst-info');
    const pathInput = document.getElementById('tzst-path');

    try {
        infoBox.textContent = 'Discovering tzst...';
        infoBox.className = 'info-box';

        const info = await invoke('discover_tzst');

        pathInput.value = info.path;
        infoBox.textContent = `Found: ${info.path}\nVersion: ${info.version}`;
        infoBox.className = 'info-box success';

        await invoke('set_tzst_path', { path: info.path });
    } catch (error) {
        infoBox.textContent = `Error: ${error}`;
        infoBox.className = 'info-box error';
        pathInput.value = '';
    }
}

async function browseTzst() {
    try {
        // Open file dialog
        const selected = await open({
            multiple: false,
            directory: false,
            title: 'Select tzst executable',
        });

        if (!selected) return;

        const path = selected;
        const infoBox = document.getElementById('tzst-info');
        const pathInput = document.getElementById('tzst-path');

        infoBox.textContent = 'Validating...';
        infoBox.className = 'info-box';

        const info = await invoke('validate_tzst_path', { path });

        pathInput.value = info.path;
        infoBox.textContent = `Valid: ${info.path}\nVersion: ${info.version}`;
        infoBox.className = 'info-box success';

        await invoke('set_tzst_path', { path: info.path });
    } catch (error) {
        const infoBox = document.getElementById('tzst-info');
        infoBox.textContent = `Error: ${error}`;
        infoBox.className = 'info-box error';
    }
}

async function changeTheme() {
    const theme = document.getElementById('theme-select').value;
    document.documentElement.setAttribute('data-theme', theme);
    await saveConfig();
}

async function changeLanguage() {
    await saveConfig();
    // In a full implementation, this would update UI text
}

async function loadConfig() {
    try {
        const config = await invoke('get_config');

        if (config.tzst_path) {
            document.getElementById('tzst-path').value = config.tzst_path;
            const info = await invoke('get_tzst_version');
            const infoBox = document.getElementById('tzst-info');
            infoBox.textContent = `Configured: ${config.tzst_path}\nVersion: ${info}`;
            infoBox.className = 'info-box success';
        }

        document.getElementById('theme-select').value = config.theme;
        document.getElementById('language-select').value = config.language;
        document.documentElement.setAttribute('data-theme', config.theme);
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

async function saveConfig() {
    try {
        const config = {
            tzst_path: document.getElementById('tzst-path').value || null,
            theme: document.getElementById('theme-select').value,
            language: document.getElementById('language-select').value,
            history_limit: 100
        };
        await invoke('save_config', { config });
    } catch (error) {
        console.error('Failed to save config:', error);
    }
}

// Create View
function initCreateView() {
    document.getElementById('create-execute').addEventListener('click', executeCreate);
    document.getElementById('create-clear').addEventListener('click', () => {
        document.getElementById('create-archive-path').value = '';
        document.getElementById('create-files').value = '';
        document.getElementById('create-level').value = '3';
        document.getElementById('create-verbose').checked = false;
        hideOutput('create');
    });
}

async function executeCreate() {
    const archivePath = document.getElementById('create-archive-path').value.trim();
    const filesText = document.getElementById('create-files').value.trim();
    const level = parseInt(document.getElementById('create-level').value);
    const verbose = document.getElementById('create-verbose').checked;

    if (!archivePath || !filesText) {
        showOutput('create', false, 'Please provide archive path and files to add');
        return;
    }

    const targetPaths = filesText.split('\n').map(l => l.trim()).filter(l => l);

    const task = {
        operation: 'a',
        archive_path: archivePath,
        target_paths: targetPaths,
        output_dir: null,
        compression_level: level,
        streaming: false,
        verbose: verbose,
        filter: null,
        dry_run: false
    };

    await executeTask('create', task);
}

// Extract View
function initExtractView() {
    document.getElementById('extract-execute').addEventListener('click', executeExtract);
    document.getElementById('extract-clear').addEventListener('click', () => {
        document.getElementById('extract-archive-path').value = '';
        document.getElementById('extract-output').value = '';
        document.getElementById('extract-files').value = '';
        document.getElementById('extract-filter').value = 'data';
        document.getElementById('extract-streaming').checked = false;
        document.getElementById('extract-verbose').checked = false;
        hideOutput('extract');
    });
}

async function executeExtract() {
    const archivePath = document.getElementById('extract-archive-path').value.trim();
    const outputDir = document.getElementById('extract-output').value.trim();
    const filesText = document.getElementById('extract-files').value.trim();
    const filter = document.getElementById('extract-filter').value;
    const streaming = document.getElementById('extract-streaming').checked;
    const verbose = document.getElementById('extract-verbose').checked;

    if (!archivePath) {
        showOutput('extract', false, 'Please provide archive path');
        return;
    }

    const targetPaths = filesText ? filesText.split('\n').map(l => l.trim()).filter(l => l) : [];

    const task = {
        operation: 'x',
        archive_path: archivePath,
        target_paths: targetPaths,
        output_dir: outputDir || null,
        compression_level: null,
        streaming: streaming,
        verbose: verbose,
        filter: filter,
        dry_run: false
    };

    await executeTask('extract', task);
}

// List View
function initListView() {
    document.getElementById('list-execute').addEventListener('click', executeList);
    document.getElementById('list-clear').addEventListener('click', () => {
        document.getElementById('list-archive-path').value = '';
        document.getElementById('list-verbose').checked = true;
        document.getElementById('list-streaming').checked = false;
        hideOutput('list');
    });
}

async function executeList() {
    const archivePath = document.getElementById('list-archive-path').value.trim();
    const verbose = document.getElementById('list-verbose').checked;
    const streaming = document.getElementById('list-streaming').checked;

    if (!archivePath) {
        showOutput('list', false, 'Please provide archive path');
        return;
    }

    const task = {
        operation: 'l',
        archive_path: archivePath,
        target_paths: [],
        output_dir: null,
        compression_level: null,
        streaming: streaming,
        verbose: verbose,
        filter: null,
        dry_run: false
    };

    await executeTask('list', task);
}

// Test View
function initTestView() {
    document.getElementById('test-execute').addEventListener('click', executeTest);
    document.getElementById('test-clear').addEventListener('click', () => {
        document.getElementById('test-archive-path').value = '';
        document.getElementById('test-streaming').checked = false;
        hideOutput('test');
    });
}

async function executeTest() {
    const archivePath = document.getElementById('test-archive-path').value.trim();
    const streaming = document.getElementById('test-streaming').checked;

    if (!archivePath) {
        showOutput('test', false, 'Please provide archive path');
        return;
    }

    const task = {
        operation: 't',
        archive_path: archivePath,
        target_paths: [],
        output_dir: null,
        compression_level: null,
        streaming: streaming,
        verbose: false,
        filter: null,
        dry_run: false
    };

    await executeTask('test', task);
}

// Execute task
async function executeTask(viewName, task) {
    const executeBtn = document.getElementById(`${viewName}-execute`);
    executeBtn.disabled = true;
    executeBtn.innerHTML = '<span class="spinner"></span> Executing...';

    try {
        const result = await invoke('execute_task', { task });

        let output = '';
        if (result.stdout) output += result.stdout;
        if (result.stderr) output += '\n' + result.stderr;

        const statusText = result.success
            ? `Success (${result.duration_ms}ms)`
            : `Failed with exit code ${result.exit_code} (${result.duration_ms}ms)`;

        showOutput(viewName, result.success, output, statusText);

        // Add to history
        addToHistory(task, result);
    } catch (error) {
        showOutput(viewName, false, `Error: ${error}`);
    } finally {
        executeBtn.disabled = false;
        executeBtn.textContent = {
            create: 'Create Archive',
            extract: 'Extract Archive',
            list: 'List Contents',
            test: 'Test Archive'
        }[viewName];
    }
}

// Output display
function showOutput(viewName, success, content, statusText = null) {
    const outputSection = document.getElementById(`${viewName}-output`);
    outputSection.className = 'output-section visible';

    const status = statusText || (success ? 'Success' : 'Error');
    const statusClass = success ? 'success' : 'error';

    outputSection.innerHTML = `
        <div class="output-header">
            <span class="output-status ${statusClass}">${status}</span>
        </div>
        <div class="output-content">${escapeHtml(content)}</div>
    `;
}

function hideOutput(viewName) {
    const outputSection = document.getElementById(`${viewName}-output`);
    outputSection.className = 'output-section';
    outputSection.innerHTML = '';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// History
function addToHistory(task, result) {
    const historyItem = {
        timestamp: new Date().toISOString(),
        task: task,
        result: result
    };

    commandHistory.unshift(historyItem);
    if (commandHistory.length > 100) {
        commandHistory.pop();
    }

    updateHistoryView();
}

function updateHistoryView() {
    const historyList = document.getElementById('history-list');

    if (commandHistory.length === 0) {
        historyList.innerHTML = '<p class="empty-state">No commands executed yet</p>';
        return;
    }

    historyList.innerHTML = commandHistory.map(item => {
        const time = new Date(item.timestamp).toLocaleString();
        const statusClass = item.result.success ? 'success' : 'error';
        const status = item.result.success ? 'Success' : 'Failed';

        return `
            <div class="history-item">
                <div class="history-header">
                    <span class="output-status ${statusClass}">${status}</span>
                    <span class="history-time">${time}</span>
                </div>
                <div class="history-command">
                    ${item.task.operation} ${item.task.archive_path}
                    ${item.result.duration_ms ? `(${item.result.duration_ms}ms)` : ''}
                </div>
            </div>
        `;
    }).join('');
}
