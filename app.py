import gradio as gr
from model import FootballPredictor
from model_tennis import TennisPredictor
import os
import matplotlib.pyplot as plt
import numpy as np

print("🚀 Démarrage de l'application Football & Tennis...")
print("=" * 60)

# Initialiser le prédicteur football
print("\n⚽ Initialisation du prédicteur football...")
predictor = FootballPredictor('data20202025.csv')

# Charger le modèle s'il existe, sinon l'entraîner
if os.path.exists('best_model.pth'):
    print("📦 Chargement du modèle football existant...")
    predictor.load_model('best_model.pth')
    print("✅ Modèle football chargé")
else:
    print("🎓 Entraînement du modèle football (première utilisation)...")
    predictor.train(epochs=150, batch_size=32, learning_rate=0.001)

# Initialiser le prédicteur tennis
print("\n🎾 Initialisation du prédicteur tennis...")
print("⏳ Chargement des données tennis (cela peut prendre 1-2 minutes)...")
tennis_predictor = TennisPredictor('datatenis20002025.csv')
tennis_predictor.load_and_prepare_data()
print(f"✅ Tennis prêt! {len(tennis_predictor.get_all_players())} joueurs chargés")



# Récupérer toutes les équipes
all_teams_raw = predictor.get_all_teams()

# Créer un mapping pour afficher des noms clairs
team_display_names = {}
team_real_names = {}

for team in all_teams_raw:
    if team == "Milan":
        display_name = "AC Milan"
    elif team == "Internazionale":
        display_name = "Inter Milan"
    else:
        display_name = team
    team_display_names[team] = display_name
    team_real_names[display_name] = team

# Liste des équipes pour l'interface (noms affichés)
all_teams = sorted(list(team_display_names.values()))

# Récupérer tous les joueurs de tennis
all_tennis_players = tennis_predictor.get_all_players()
tennis_surfaces = ['Hard', 'Clay', 'Grass', 'Carpet']

# ==================== FONCTIONS FOOTBALL ====================

def predict_match(team1, team2, venue):
    """Fonction de prédiction pour l'interface"""
    if team1 == team2:
        return "⚠️ Veuillez sélectionner deux équipes différentes!", None
    
    team1_real = team_real_names.get(team1, team1)
    team2_real = team_real_names.get(team2, team2)
    
    result = predictor.predict(team1_real, team2_real, venue)
    
    win_prob = result['win'] * 100
    draw_prob = result['draw'] * 100
    loss_prob = result['loss'] * 100
    
    max_prob = max(win_prob, draw_prob, loss_prob)
    if max_prob == win_prob:
        prediction = f"🏆 Victoire probable de {team1}"
    elif max_prob == draw_prob:
        prediction = "🤝 Match nul probable"
    else:
        prediction = f"🏆 Victoire probable de {team2}"
    
    result_text = f"""
# {prediction}

## 📊 Probabilités:

### ⚽ Victoire {team1}: **{win_prob:.1f}%**
### 🤝 Match nul: **{draw_prob:.1f}%**
### ⚽ Victoire {team2}: **{loss_prob:.1f}%**

---

**Lieu:** {"🏠 Domicile (" + team1 + ")" if venue == "Home" else "✈️ Extérieur (chez " + team2 + ")"}
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = [f'Victoire\n{team1}', 'Match\nNul', f'Victoire\n{team2}']
    probabilities = [win_prob, draw_prob, loss_prob]
    colors = ['#4CAF50', '#FFC107', '#FF5722']
    
    bars = ax.bar(categories, probabilities, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{prob:.1f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Probabilité (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Prédiction: {team1} vs {team2}', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    return result_text, fig

def get_team_stats(team):
    """Affiche les statistiques d'une équipe"""
    team_real = team_real_names.get(team, team)
    
    if team_real not in predictor.team_stats:
        return "❌ Équipe non trouvée dans la base de données", None
    
    stats = predictor.team_stats[team_real]
    
    stats_text = f"""
# 📈 Statistiques de {team}

## 🎯 Performance
- **Taux de victoire:** {stats['win_rate']*100:.1f}%
- **Forme récente:** {stats['recent_form']*100:.1f}%
- **Matchs joués:** {stats['total_games']}

## ⚽ Attaque
- **Buts marqués (moy.):** {stats['avg_gf']:.2f}
- **xG (Expected Goals):** {stats['avg_xg']:.2f}
- **Tirs (moy.):** {stats['avg_sh']:.1f}
- **Tirs cadrés (moy.):** {stats['avg_sot']:.1f}

## 🛡️ Défense
- **Buts encaissés (moy.):** {stats['avg_ga']:.2f}
- **xGA (Expected Goals Against):** {stats['avg_xga']:.2f}

## 📊 Possession
- **Possession moyenne:** {stats['avg_poss']:.1f}%
    """
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    categories = ['Attaque', 'Défense', 'Possession', 'Victoires', 'Forme']
    
    values = [
        min(stats['avg_gf'] / 3, 1),
        1 - min(stats['avg_ga'] / 3, 1),
        stats['avg_poss'] / 100,
        stats['win_rate'],
        stats['recent_form']
    ]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, color='#2196F3')
    ax.fill(angles, values, alpha=0.25, color='#2196F3')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_title(f'Profil de {team}', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True)
    
    plt.tight_layout()
    
    return stats_text, fig

def compare_teams(team1, team2):
    """Compare deux équipes"""
    if team1 == team2:
        return "⚠️ Veuillez sélectionner deux équipes différentes!", None
    
    team1_real = team_real_names.get(team1, team1)
    team2_real = team_real_names.get(team2, team2)
    
    if team1_real not in predictor.team_stats or team2_real not in predictor.team_stats:
        return "❌ Une ou plusieurs équipes non trouvées", None
    
    stats1 = predictor.team_stats[team1_real]
    stats2 = predictor.team_stats[team2_real]
    
    comparison_text = f"""
# ⚔️ Comparaison: {team1} vs {team2}

| Statistique | {team1} | {team2} |
|-------------|---------|---------|
| **Taux de victoire** | {stats1['win_rate']*100:.1f}% | {stats2['win_rate']*100:.1f}% |
| **Forme récente** | {stats1['recent_form']*100:.1f}% | {stats2['recent_form']*100:.1f}% |
| **Buts marqués (moy.)** | {stats1['avg_gf']:.2f} | {stats2['avg_gf']:.2f} |
| **Buts encaissés (moy.)** | {stats1['avg_ga']:.2f} | {stats2['avg_ga']:.2f} |
| **xG** | {stats1['avg_xg']:.2f} | {stats2['avg_xg']:.2f} |
| **xGA** | {stats1['avg_xga']:.2f} | {stats2['avg_xga']:.2f} |
| **Possession (moy.)** | {stats1['avg_poss']:.1f}% | {stats2['avg_poss']:.1f}% |
| **Tirs (moy.)** | {stats1['avg_sh']:.1f} | {stats2['avg_sh']:.1f} |
    """
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    categories = ['Victoires', 'Forme', 'Attaque', 'Défense', 'Possession']
    team1_values = [
        stats1['win_rate'] * 100,
        stats1['recent_form'] * 100,
        (stats1['avg_gf'] / 3) * 100,
        (1 - min(stats1['avg_ga'] / 3, 1)) * 100,
        stats1['avg_poss']
    ]
    team2_values = [
        stats2['win_rate'] * 100,
        stats2['recent_form'] * 100,
        (stats2['avg_gf'] / 3) * 100,
        (1 - min(stats2['avg_ga'] / 3, 1)) * 100,
        stats2['avg_poss']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, team1_values, width, label=team1, color='#2196F3', alpha=0.8)
    bars2 = ax.bar(x + width/2, team2_values, width, label=team2, color='#FF5722', alpha=0.8)
    
    ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparaison: {team1} vs {team2}', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    
    return comparison_text, fig

# ==================== FONCTIONS TENNIS ====================

def predict_tennis_match(player1, player2, surface):
    """Fonction de prédiction pour les matchs de tennis"""
    if player1 == player2:
        return "⚠️ Veuillez sélectionner deux joueurs différents!", None
    
    result = tennis_predictor.predict(player1, player2, surface)
    
    prob1 = result['player1_win'] * 100
    prob2 = result['player2_win'] * 100
    
    if prob1 > prob2:
        prediction = f"🏆 Victoire probable de {player1}"
    else:
        prediction = f"🏆 Victoire probable de {player2}"
    
    result_text = f"""
# {prediction}

## 🎾 Probabilités:

### 🏆 Victoire {player1}: **{prob1:.1f}%**
### 🏆 Victoire {player2}: **{prob2:.1f}%**

---

**Surface:** {surface}
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = [f'{player1}', f'{player2}']
    probabilities = [prob1, prob2]
    colors = ['#4CAF50', '#FF5722']
    
    bars = ax.bar(categories, probabilities, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{prob:.1f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Probabilité de victoire (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Prédiction Tennis: {player1} vs {player2}', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    return result_text, fig

def get_tennis_player_stats(player):
    """Affiche les statistiques d'un joueur de tennis"""
    info = tennis_predictor.get_player_info(player)
    
    if info is None:
        return "❌ Joueur non trouvé dans la base de données", None
    
    stats_text = f"""
# 🎾 Statistiques de {player}

## 🎯 Performance Globale
- **Taux de victoire:** {info['win_rate']*100:.1f}%
- **Forme récente:** {info['recent_form']*100:.1f}%
- **Classement moyen:** {info['avg_rank']:.0f}
- **Matchs joués:** {info['total_matches']}
- **Victoires totales:** {info['total_wins']}

## 🎾 Performance par Surface
"""
    
    for surface, surface_stats in info['surfaces'].items():
        stats_text += f"- **{surface}:** {surface_stats['win_rate']*100:.1f}% ({surface_stats['total_matches']} matchs)\n"
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    categories = ['Taux de\nvictoire', 'Forme\nrécente']
    values = [info['win_rate'] * 100, info['recent_form'] * 100]
    colors = ['#4CAF50', '#2196F3']
    
    bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_ylabel('Performance (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Performance Globale', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    surfaces = []
    surface_values = []
    for surface, surface_stats in info['surfaces'].items():
        if surface_stats['total_matches'] > 0:
            surfaces.append(surface)
            surface_values.append(surface_stats['win_rate'] * 100)
    
    if surfaces:
        bars2 = ax2.bar(surfaces, surface_values, color='#FF9800', alpha=0.8, edgecolor='black', linewidth=2)
        for bar, val in zip(bars2, surface_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}%',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax2.set_ylabel('Taux de victoire (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Performance par Surface', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_axisbelow(True)
    
    plt.tight_layout()
    
    return stats_text, fig

def compare_tennis_players(player1, player2):
    """Compare deux joueurs de tennis"""
    if player1 == player2:
        return "⚠️ Veuillez sélectionner deux joueurs différents!", None
    
    info1 = tennis_predictor.get_player_info(player1)
    info2 = tennis_predictor.get_player_info(player2)
    
    if info1 is None or info2 is None:
        return "❌ Un ou plusieurs joueurs non trouvés", None
    
    comparison_text = f"""
# ⚔️ Comparaison: {player1} vs {player2}

| Statistique | {player1} | {player2} |
|-------------|-----------|-----------|
| **Taux de victoire** | {info1['win_rate']*100:.1f}% | {info2['win_rate']*100:.1f}% |
| **Forme récente** | {info1['recent_form']*100:.1f}% | {info2['recent_form']*100:.1f}% |
| **Classement moyen** | {info1['avg_rank']:.0f} | {info2['avg_rank']:.0f} |
| **Matchs joués** | {info1['total_matches']} | {info2['total_matches']} |
| **Victoires totales** | {info1['total_wins']} | {info2['total_wins']} |

## Performance par Surface:
"""
    
    for surface in ['Hard', 'Clay', 'Grass', 'Carpet']:
        stats1 = info1['surfaces'].get(surface, {'win_rate': 0, 'total_matches': 0})
        stats2 = info2['surfaces'].get(surface, {'win_rate': 0, 'total_matches': 0})
        comparison_text += f"- **{surface}:** {stats1['win_rate']*100:.1f}% vs {stats2['win_rate']*100:.1f}%\n"
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    categories = ['Victoires', 'Forme', 'Hard', 'Clay', 'Grass', 'Carpet']
    
    player1_values = [
        info1['win_rate'] * 100,
        info1['recent_form'] * 100,
        info1['surfaces'].get('Hard', {'win_rate': 0})['win_rate'] * 100,
        info1['surfaces'].get('Clay', {'win_rate': 0})['win_rate'] * 100,
        info1['surfaces'].get('Grass', {'win_rate': 0})['win_rate'] * 100,
        info1['surfaces'].get('Carpet', {'win_rate': 0})['win_rate'] * 100
    ]
    
    player2_values = [
        info2['win_rate'] * 100,
        info2['recent_form'] * 100,
        info2['surfaces'].get('Hard', {'win_rate': 0})['win_rate'] * 100,
        info2['surfaces'].get('Clay', {'win_rate': 0})['win_rate'] * 100,
        info2['surfaces'].get('Grass', {'win_rate': 0})['win_rate'] * 100,
        info2['surfaces'].get('Carpet', {'win_rate': 0})['win_rate'] * 100
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, player1_values, width, label=player1, color='#2196F3', alpha=0.8)
    bars2 = ax.bar(x + width/2, player2_values, width, label=player2, color='#FF5722', alpha=0.8)
    
    ax.set_ylabel('Taux de victoire (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparaison Tennis: {player1} vs {player2}', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    
    return comparison_text, fig

# ==================== INTERFACE GRADIO ====================

with gr.Blocks(title="⚽🎾 Prédicteur Football & Tennis", css="") as app:

    gr.Markdown("""
    # ⚽🎾 Prédicteur de Matchs avec réseau neuronal
    ## 🧠 Intelligence Artificielle avec PyTorch

    Prédisez les résultats des matchs de **Serie A** et de **Tennis** basés sur les données historiques
    """)

    with gr.Tabs():

        # ==================== SECTION FOOTBALL ====================
        with gr.Tab("⚽ FOOTBALL - Serie A"):
            with gr.Tabs():

                with gr.Tab("🎯 Prédiction"):
                    gr.Markdown("### Sélectionnez deux équipes et le lieu du match")

                    with gr.Row():
                        with gr.Column():
                            team1_input = gr.Dropdown(choices=all_teams, label="🏠 Équipe à domicile",
                                                      value=all_teams[0] if all_teams else None)
                        with gr.Column():
                            team2_input = gr.Dropdown(choices=all_teams, label="✈️ Équipe à l'extérieur",
                                                      value=all_teams[1] if len(all_teams) > 1 else None)

                    venue_input = gr.Radio(choices=["Home", "Away"], label="📍 Perspective de prédiction",
                                          value="Home",
                                          info="'Home' = probabilités pour l'équipe à domicile, 'Away' = pour l'équipe à l'extérieur")

                    predict_button = gr.Button("🔮 Prédire le résultat", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            prediction_output = gr.Markdown()
                        with gr.Column():
                            prediction_plot = gr.Plot()

                    predict_button.click(fn=predict_match,
                                         inputs=[team1_input, team2_input, venue_input],
                                         outputs=[prediction_output, prediction_plot])

                with gr.Tab("📊 Statistiques"):
                    gr.Markdown("### Consultez les statistiques détaillées d'une équipe")

                    team_stats_input = gr.Dropdown(choices=all_teams, label="Sélectionnez une équipe",
                                                   value=all_teams[0] if all_teams else None)
                    stats_button = gr.Button("📈 Voir les statistiques", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            stats_output = gr.Markdown()
                        with gr.Column():
                            stats_plot = gr.Plot()

                    stats_button.click(fn=get_team_stats, inputs=[team_stats_input],
                                       outputs=[stats_output, stats_plot])

                with gr.Tab("⚔️ Comparaison"):
                    gr.Markdown("### Comparez deux équipes côte à côte")

                    with gr.Row():
                        compare_team1 = gr.Dropdown(choices=all_teams, label="Équipe 1",
                                                    value=all_teams[0] if all_teams else None)
                        compare_team2 = gr.Dropdown(choices=all_teams, label="Équipe 2",
                                                    value=all_teams[1] if len(all_teams) > 1 else None)

                    compare_button = gr.Button("⚖️ Comparer", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            compare_output = gr.Markdown()
                        with gr.Column():
                            compare_plot = gr.Plot()

                    compare_button.click(fn=compare_teams,
                                         inputs=[compare_team1, compare_team2],
                                         outputs=[compare_output, compare_plot])

        # ==================== SECTION TENNIS ====================
        with gr.Tab("🎾 TENNIS"):
            with gr.Tabs():

                with gr.Tab("🎯 Prédiction"):
                    gr.Markdown("### Sélectionnez deux joueurs et la surface")

                    with gr.Row():
                        with gr.Column():
                            tennis_player1 = gr.Dropdown(choices=all_tennis_players, label="🎾 Joueur 1",
                                                         value=all_tennis_players[0] if all_tennis_players else None)
                        with gr.Column():
                            tennis_player2 = gr.Dropdown(choices=all_tennis_players, label="🎾 Joueur 2",
                                                         value=all_tennis_players[1] if len(all_tennis_players) > 1 else None)

                    tennis_surface = gr.Radio(choices=tennis_surfaces, label="🎾 Surface", value="Hard",
                                             info="Choisissez la surface du court")

                    tennis_predict_button = gr.Button("🔮 Prédire le résultat", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            tennis_prediction_output = gr.Markdown()
                        with gr.Column():
                            tennis_prediction_plot = gr.Plot()

                    tennis_predict_button.click(fn=predict_tennis_match,
                                                inputs=[tennis_player1, tennis_player2, tennis_surface],
                                                outputs=[tennis_prediction_output, tennis_prediction_plot])

                with gr.Tab("📊 Statistiques"):
                    gr.Markdown("### Consultez les statistiques détaillées d'un joueur")

                    tennis_stats_input = gr.Dropdown(choices=all_tennis_players, label="Sélectionnez un joueur",
                                                     value=all_tennis_players[0] if all_tennis_players else None)
                    tennis_stats_button = gr.Button("📈 Voir les statistiques", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            tennis_stats_output = gr.Markdown()
                        with gr.Column():
                            tennis_stats_plot = gr.Plot()

                    tennis_stats_button.click(fn=get_tennis_player_stats, inputs=[tennis_stats_input],
                                              outputs=[tennis_stats_output, tennis_stats_plot])

                with gr.Tab("⚔️ Comparaison"):
                    gr.Markdown("### Comparez deux joueurs côte à côte")

                    with gr.Row():
                        tennis_compare_player1 = gr.Dropdown(choices=all_tennis_players, label="Joueur 1",
                                                             value=all_tennis_players[0] if all_tennis_players else None)
                        tennis_compare_player2 = gr.Dropdown(choices=all_tennis_players, label="Joueur 2",
                                                             value=all_tennis_players[1] if len(all_tennis_players) > 1 else None)

                    tennis_compare_button = gr.Button("⚖️ Comparer", variant="primary", size="lg")

                    with gr.Row():
                        with gr.Column():
                            tennis_compare_output = gr.Markdown()
                        with gr.Column():
                            tennis_compare_plot = gr.Plot()

                    tennis_compare_button.click(fn=compare_tennis_players,
                                                inputs=[tennis_compare_player1, tennis_compare_player2],
                                                outputs=[tennis_compare_output, tennis_compare_plot])

      

    gr.Markdown("""
    ---
    <div style="text-align: center;">
        <p>🚀 Développé avec PyTorch & Gradio | 📊 Données 2000-2025</p>
    </div>
    """)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 Lancement de l'interface Gradio...")
    print("=" * 60)
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)