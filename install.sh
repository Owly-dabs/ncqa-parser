#!/usr/bin/env sh
set -e

REPO_URL="https://github.com/Owly-dabs/ncqa-parser"
INSTALL_DIR="$HOME/.ncqa-parser"
CLI_FILE="ncqa-cli.py"

echo "🚀 Installing ncqa-parser..."

# Detect OS
OS="$(uname | tr '[:upper:]' '[:lower:]')"

# Pick correct pip command
if [ "$OS" = "darwin" ]; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

# Check for Git
if ! command -v git >/dev/null 2>&1; then
    echo "❌ git not found. Please install it first."
    exit 1
fi

# Clone or update repo
if [ -d "$INSTALL_DIR" ]; then
    echo "🔁 Existing installation found, updating..."
    git -C "$INSTALL_DIR" pull --quiet || echo "⚠️ Could not update, using existing copy."
else
    echo "📦 Cloning repository..."
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

# Check for pip command
if ! command -v "$PIP_CMD" >/dev/null 2>&1; then
    echo "❌ $PIP_CMD not found."
    if [ "$OS" = "darwin" ]; then
        echo "👉 Install Python 3 via Homebrew: brew install python"
    else
        echo "👉 Install pip via: sudo apt install python3-pip"
    fi
    exit 1
fi

# Install dependencies
echo "📚 Installing Python dependencies..."
$PIP_CMD install --upgrade pip >/dev/null
$PIP_CMD install -r "$INSTALL_DIR/requirements.txt" >/dev/null

# Make CLI executable
chmod +x "$INSTALL_DIR/$CLI_FILE"

# Detect shell rc file
case "$SHELL" in
  */zsh)  SHELL_RC="$HOME/.zshrc" ;;
  */bash) SHELL_RC="$HOME/.bashrc" ;;
  *)      SHELL_RC="$HOME/.profile" ;;
esac

# Add to PATH if missing
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo "🔧 Adding $INSTALL_DIR to PATH in $SHELL_RC..."
    printf '\n# Added by ncqa-parser installer\nexport PATH="$PATH:%s"\n' "$INSTALL_DIR" >> "$SHELL_RC"
    echo "✅ PATH updated. Restart your terminal or run: source $SHELL_RC"
else
    echo "✅ PATH already contains $INSTALL_DIR"
fi

echo "🎉 Installation complete! Restart your terminal and run:"
echo ""
echo "    ncqa-cli.py [options]"
echo ""