#!/usr/bin/env python3
"""Development script for building and serving documentation locally."""

import argparse
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""    try:
        result = subprocess.run(
            cmd, shell=True, check=True, cwd=cwd,
            capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def clean_build(build_dir):
    """Clean the build directory."""
    if build_dir.exists():
        print(f"Cleaning {build_dir}")
        shutil.rmtree(build_dir)


def build_docs(source_dir, build_dir, watch=False):
    """Build the documentation."""
    if watch:
        print("Starting live reload server...")
        print("Visit http://localhost:8000 to view the documentation")
        print("Press Ctrl+C to stop the server")
        
        cmd = f"sphinx-autobuild {source_dir} {build_dir} --host 0.0.0.0 --port 8000"
        success, stdout, stderr = run_command(cmd)
        
        if not success:
            print("Failed to start live reload server.")
            print("Make sure sphinx-autobuild is installed: pip install sphinx-autobuild")
            return False
    else:
        print(f"Building documentation: {source_dir} -> {build_dir}")
        cmd = f"python -m sphinx -b html {source_dir} {build_dir}"
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print("Documentation built successfully!")
            index_file = build_dir / "index.html"
            print(f"Open {index_file} in your browser to view the documentation")
            return True
        else:
            print("Build failed!")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False


def serve_docs(build_dir, port=8000):
    """Serve the built documentation locally."""
    if not build_dir.exists():
        print(f"Build directory {build_dir} does not exist. Build the docs first.")
        return False
    
    print(f"Serving documentation at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    cmd = f"python -m http.server {port}"
    success, stdout, stderr = run_command(cmd, cwd=build_dir)
    
    return success


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import sphinx
        print(f"Sphinx version: {sphinx.__version__}")
    except ImportError:
        print("Sphinx is not installed. Install with: pip install sphinx")
        return False
    
    try:
        import tzst
        print(f"tzst version: {tzst.__version__}")
    except ImportError:
        print("tzst package is not installed. Install with: pip install -e ..")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Build and serve tzst documentation")
    parser.add_argument(
        "command", 
        choices=["build", "clean", "serve", "watch", "check"],
        help="Command to execute"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port for serving documentation (default: 8000)"
    )
    parser.add_argument(
        "--open", "-o",
        action="store_true",
        help="Open documentation in browser after building/serving"
    )
    
    args = parser.parse_args()
    
    # Get directories
    script_dir = Path(__file__).parent
    source_dir = script_dir
    build_dir = script_dir / "_build"
    
    if args.command == "check":
        success = check_dependencies()
        sys.exit(0 if success else 1)
    
    elif args.command == "clean":
        clean_build(build_dir)
        
    elif args.command == "build":
        if not check_dependencies():
            sys.exit(1)
        
        success = build_docs(source_dir, build_dir)
        
        if success and args.open:
            index_file = build_dir / "index.html"
            webbrowser.open(f"file://{index_file.absolute()}")
        
        sys.exit(0 if success else 1)
    
    elif args.command == "watch":
        if not check_dependencies():
            sys.exit(1)
        
        success = build_docs(source_dir, build_dir, watch=True)
        sys.exit(0 if success else 1)
    
    elif args.command == "serve":
        success = serve_docs(build_dir, args.port)
        
        if args.open:
            webbrowser.open(f"http://localhost:{args.port}")
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
