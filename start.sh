#!/usr/bin/env bash
set -e

echo "Starting application..."

# Go to project root
cd "$(dirname "$0")"

# If backend folder exists, use it
if [ -d "backend" ]; then
  echo "Backend folder found"
  cd backend

  # Node.js backend
  if [ -f package.json ]; then
    echo "Node.js backend detected"
    npm install
    npm start

  # Python backend
  elif [ -f app.py ] || [ -f main.py ]; then
    echo "Python backend detected"
    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi
    python app.py || python main.py
  else
    echo "No start file found in backend"
    exit 1
  fi

else
  echo "Backend folder not found"
  exit 1
fi
