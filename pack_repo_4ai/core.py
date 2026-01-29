import os
import sys
import argparse
import fnmatch
import pyperclip

# --- CONFIG ---
MAX_FILES = 300
MAX_FILE_SIZE_KB = 500
# --------------

def get_ignore_patterns(root_dir):
    patterns = [
        # 1. PYTHON & VIRTUAL ENVIRONMENTS
        '.venv', 'venv', 'env', '.env', '.pytest_cache', '__pycache__', 
        '*.pyc', '*.pyo', '*.pyd', '.coverage', '*.egg-info',

        # 2. JAVASCRIPT / WEB TRASH
        'node_modules', 'bower_components', 'jspm_packages', 
        '.npm', '.yarn', 'yarn.lock', 'package-lock.json', 'pnpm-lock.yaml',
        '.next', '.nuxt', '.cache', 'dist', 'build', 'out', # Build folders
        'coverage', # Test coverage reports

        # 3. COMPILED / BINARY / EXECUTABLES
        '*.exe', '*.dll', '*.so', '*.dylib', '*.bin', 
        '*.class', '*.jar', '*.war', '*.ear', # Java
        'target', # Rust/Java build folder
        
        # 4. IDEs & EDITORS (The "Silent Token Eaters")
        '.git', '.svn', '.hg', '.idea', '.vscode', '.vs', 
        '.settings', '.project', '.classpath', # Eclipse
        '*.swp', '*.swo', '*~', # Vim/Emacs swap files
        '.DS_Store', 'Thumbs.db', # OS Junk

        # 5. MEDIA & DOCUMENTS (Not Code)
        '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico', '*.webp',
        '*.mp4', '*.mov', '*.avi', '*.mkv', '*.mp3', '*.wav', '*.flac',
        '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
        '*.zip', '*.tar', '*.gz', '*.7z', '*.rar', '*.iso',
        '*.ttf', '*.otf', '*.woff', '*.woff2', # Fonts

        # 6. LOGS & DATABASES
        '*.log', '*.sqlitedb', '*.db', '*.sqlite',
        
        # 7. SYSTEM CRITICAL (Anti-Root Guard)
        'Library', 'Applications', 'System', 'Users', 'Desktop', 'Downloads',
        
        # 8. SELF (Prevents tool from scanning itself)
        'packer.py', 'core.py', 'repo_packer'
    ]
    
    # Add .gitignore rules if they exist
    gitignore_path = os.path.join(root_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def is_ignored(path, ignore_patterns):
    name = os.path.basename(path)
    for pattern in ignore_patterns:
        # Match filenames (e.g., "*.pyc")
        if fnmatch.fnmatch(name, pattern): 
            return True
        # Match full paths for safety
        if fnmatch.fnmatch(path, pattern): 
            return True
        # Match Directories explicitly (e.g. "dist/")
        if pattern in path.split(os.sep):
            return True
            
    return False

def pack_repo(root_dir, print_to_terminal=False):
    abs_root = os.path.abspath(root_dir)
    print(f"📂 Scanning: {abs_root}...")
    
    output = ["<context_manifest>"]
    output.append(f"  <project_root>{abs_root}</project_root>")
    
    ignore_patterns = get_ignore_patterns(root_dir)
    file_count = 0
    skipped_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), ignore_patterns)]
        
        for filename in filenames:
            if file_count >= MAX_FILES: break
            
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)
            
            if is_ignored(file_path, ignore_patterns):
                continue
            
            try:
                # SKIP LARGE FILES
                if os.path.getsize(file_path) > (MAX_FILE_SIZE_KB * 1024):
                    skipped_count += 1
                    continue 

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    output.append(f'  <file path="{rel_path}">')
                    output.append(content)
                    output.append('  </file>')
                    file_count += 1
            except Exception:
                pass
        
        if file_count >= MAX_FILES: break

    output.append("</context_manifest>")
    final_text = "\n".join(output)

    # --- ACTION BLOCK ---
    if print_to_terminal:
        print(final_text)
    else:
        try:
            pyperclip.copy(final_text)
            print(f"\n✅ SUCCESS! {file_count} files copied to clipboard.")
            print(f"👉 Go to your AI model and paste")
        except Exception as e:
            print(f"\n❌ Clipboard Error: {e}")
            print("Printing to screen instead...")
            print(final_text)

def main():
    parser = argparse.ArgumentParser(description="Pack repository for AI context")
    parser.add_argument("path", nargs="?", default=".", help="Folder to scan")
    parser.add_argument("--print", action="store_true", help="Print to screen instead of clipboard")
    args = parser.parse_args()
    
    pack_repo(args.path, args.print)

if __name__ == "__main__":
    main()