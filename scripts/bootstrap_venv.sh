#!/usr/bin/env bash

# --- Bootstrap Python Virtual Environment ---
echo "[INFO] Bootstrapping virtual environment..."

# Step 1: Check if Python is available
if ! command -v python &>/dev/null; then
  echo "[FAIL] Python not found. Please install Python 3.x first."
  exit 1
fi

# Step 2: Create .venv if missing
if [ ! -d ".venv" ]; then
  echo "[INFO] Creating .venv..."
  python -m venv .venv || { echo "[FAIL] Failed to create virtual environment"; exit 1; }
else
  echo "[OK] .venv already exists."
fi

# Step 3: Activate the environment (POSIX-compatible shells only)
if [ -f ".venv/Scripts/activate" ]; then
  echo "[INFO] Activating .venv..."
  source .venv/Scripts/activate
else
  echo "[WARN] Activation script not found. Please activate manually."
fi

# Step 4: Install requirements (optional)
if [ -f "requirements.txt" ]; then
  echo "[INFO] Installing dependencies from requirements.txt..."
  .venv/Scripts/pip install -r requirements.txt
else
  echo "[WARN] No requirements.txt found."
fi

echo "[DONE] Environment setup complete."
