# 📦 pack-repo-4ai

**Stop copy-pasting files manually.**
`pack-repo-4ai` is a CLI tool that compresses your codebase into a single, AI-optimized context file and copies it to your clipboard.

Designed specifically for **DeepSeek R1**, **Claude 3.5**, and **OpenAI o1**.

## 🚀 Why use this?
When you paste 10 different files into ChatGPT, it gets confused.
`pack-repo-4ai` wraps your code in XML tags (`<file path="...">`), which Reasoning Models use to understand your project structure perfectly.

## ⚡ Quick Start

1. **Install**
   ```bash
   pip install pack-repo-4ai
2. **Run**
    (inside your project)
    pack-repo
    (Note: The result is automatically copied to your clipboard)
3. **Paste**
    Go to DeepSeek/Claude and hit Cmd+V. Your entire codebase is now in the chat context.

## 🛡️ Bullet-Proof Features
- Auto-Clipboard: No manual selecting. It's already copied.
- Smart Ignores: Automatically ignores node_modules, .venv, yarn.lock, and binary files to save tokens.
- Security: Blocks system folders and hidden secrets (.env) by default.
- XML Formatting: Proven to increase accuracy in Reasoning Models.

## 📝 Options
# Print to screen instead of copying
pack-repo --print

# Scan a specific folder
pack-repo /path/to/my/project

## License
MIT