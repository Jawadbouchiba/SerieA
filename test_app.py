#!/usr/bin/env python3
import sys
import traceback

try:
    print("🚀 Démarrage de l'application...")
    print("=" * 50)
    
    # Importer l'app
    print("📦 Import de app.py...")
    import app
    print("✅ Import réussi")
    
except Exception as e:
    print("❌ ERREUR:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\n📋 Traceback complet:")
    traceback.print_exc()
    sys.exit(1)
