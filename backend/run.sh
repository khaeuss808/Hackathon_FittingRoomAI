#!/bin/bash

echo "=== The Fitting Room Backend Setup ==="
echo ""

if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Seed database with sample data (run once)
if [ ! -f products.db ]; then
    echo ""
    echo "🌱 Seeding database with sample products..."
    python seed_data.py
else
    echo ""
    echo "✓ Database already exists. Skipping seed."
    echo "  (Delete products.db to reseed)"
fi

echo ""
echo "🚀 Starting Flask server..."
python main.py
