"""
Exemple d'utilisation du prédicteur de matchs Serie A
"""

from model import FootballPredictor

# Initialiser le prédicteur
predictor = FootballPredictor('data20202025.csv')

# Charger le modèle pré-entraîné (ou entraîner si nécessaire)
try:
    predictor.load_model('best_model.pth')
    print("✅ Modèle chargé avec succès!\n")
except:
    print("🎓 Entraînement du modèle...\n")
    predictor.train(epochs=150, batch_size=32, learning_rate=0.001)

# Récupérer toutes les équipes disponibles
teams = predictor.get_all_teams()
print(f"📋 {len(teams)} équipes disponibles:")
for team in teams[:10]:  # Afficher les 10 premières
    print(f"   - {team}")
print("   ...\n")

# Exemple 1: Prédire Milan vs Juventus à domicile
print("=" * 60)
print("🏟️  EXEMPLE 1: Milan vs Juventus (à domicile)")
print("=" * 60)
result = predictor.predict('Milan', 'Juventus', 'Home')
print(f"⚽ Victoire Milan:    {result['win']*100:5.1f}%")
print(f"🤝 Match nul:        {result['draw']*100:5.1f}%")
print(f"⚽ Victoire Juventus: {result['loss']*100:5.1f}%")
print()

# Exemple 2: Prédire Napoli vs Inter à l'extérieur
print("=" * 60)
print("✈️  EXEMPLE 2: Napoli vs Inter (à l'extérieur)")
print("=" * 60)
result = predictor.predict('Napoli', 'Internazionale', 'Away')
print(f"⚽ Victoire Napoli: {result['win']*100:5.1f}%")
print(f"🤝 Match nul:       {result['draw']*100:5.1f}%")
print(f"⚽ Victoire Inter:  {result['loss']*100:5.1f}%")
print()

# Exemple 3: Afficher les statistiques d'une équipe
print("=" * 60)
print("📊 EXEMPLE 3: Statistiques de l'AC Milan")
print("=" * 60)
milan_stats = predictor.team_stats.get('Milan', {})
if milan_stats:
    print(f"🎯 Taux de victoire:     {milan_stats['win_rate']*100:.1f}%")
    print(f"📈 Forme récente:        {milan_stats['recent_form']*100:.1f}%")
    print(f"⚽ Buts marqués (moy):    {milan_stats['avg_gf']:.2f}")
    print(f"🛡️  Buts encaissés (moy): {milan_stats['avg_ga']:.2f}")
    print(f"📊 Possession (moy):     {milan_stats['avg_poss']:.1f}%")
    print(f"🎮 Matchs joués:         {milan_stats['total_games']}")
print()

# Exemple 4: Comparer plusieurs matchs
print("=" * 60)
print("🔄 EXEMPLE 4: Comparaison de plusieurs matchs")
print("=" * 60)
matches = [
    ('Milan', 'Juventus', 'Home'),
    ('Juventus', 'Milan', 'Home'),
    ('Napoli', 'Roma', 'Home'),
    ('Internazionale', 'Atalanta', 'Home')
]

for team1, team2, venue in matches:
    result = predictor.predict(team1, team2, venue)
    winner = "Nul" if max(result.values()) == result['draw'] else team1 if result['win'] > result['loss'] else team2
    confidence = max(result.values()) * 100
    print(f"{team1} vs {team2} ({venue:4s}): {winner:20s} ({confidence:5.1f}%)")
print()

# Exemple 5: Fonction utilitaire pour prédire un match complet
def predict_and_display(team1, team2, venue='Home'):
    """Fonction helper pour afficher une prédiction complète"""
    print("\n" + "=" * 60)
    print(f"🎯 PRÉDICTION: {team1} vs {team2}")
    print(f"📍 Lieu: {'🏠 Domicile' if venue == 'Home' else '✈️ Extérieur'} (perspective {team1})")
    print("=" * 60)
    
    result = predictor.predict(team1, team2, venue)
    
    # Déterminer le favori
    probs = [
        (result['win'], f"Victoire {team1}"),
        (result['draw'], "Match nul"),
        (result['loss'], f"Victoire {team2}")
    ]
    probs.sort(reverse=True)
    
    print(f"\n🏆 Résultat le plus probable: {probs[0][1]} ({probs[0][0]*100:.1f}%)")
    print(f"\n📊 Probabilités détaillées:")
    print(f"   1. {probs[0][1]:20s} {probs[0][0]*100:5.1f}%")
    print(f"   2. {probs[1][1]:20s} {probs[1][0]*100:5.1f}%")
    print(f"   3. {probs[2][1]:20s} {probs[2][0]*100:5.1f}%")
    
    # Niveau de confiance
    confidence_gap = (probs[0][0] - probs[1][0]) * 100
    if confidence_gap > 15:
        print(f"\n💪 Confiance: FORTE (écart de {confidence_gap:.1f}%)")
    elif confidence_gap > 8:
        print(f"\n👍 Confiance: MOYENNE (écart de {confidence_gap:.1f}%)")
    else:
        print(f"\n🤷 Confiance: FAIBLE (écart de {confidence_gap:.1f}%) - Match serré!")

# Utiliser la fonction helper
predict_and_display('Roma', 'Lazio', 'Home')
predict_and_display('Atalanta', 'Internazionale', 'Home')

print("\n" + "=" * 60)
print("✅ Exemples terminés!")
print("💡 Lancez 'python app.py' pour l'interface graphique complète")
print("=" * 60)
