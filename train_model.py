#!/usr/bin/env python3
"""Script pour réentraîner le modèle avec les nouvelles améliorations"""

from model import FootballPredictor
import os

# Supprimer l'ancien modèle
if os.path.exists('best_model.pth'):
    os.remove('best_model.pth')
    print("🗑️ Ancien modèle supprimé")

# Créer et entraîner le nouveau modèle
print("🎓 Début de l'entraînement du nouveau modèle...")
print("⚡ Architecture: Réseau plus simple avec régularisation")
print("📊 Features: Statistiques d'équipe + Head-to-Head")
print("🔧 Optimizations: Label smoothing + Weight decay\n")

predictor = FootballPredictor('data20202025.csv')
history = predictor.train(epochs=100, batch_size=32, learning_rate=0.0005)

print("\n✅ Entraînement terminé!")
print(f"📈 Meilleure précision: {max(history['test_acc']):.2f}%")
print("💾 Modèle sauvegardé dans best_model.pth")
