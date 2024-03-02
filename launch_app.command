# Get the absolute directory of the script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

chmod +x "$SCRIPT_DIR/app_view.py"

# Launch the application
python3 "$SCRIPT_DIR/app_view.py"