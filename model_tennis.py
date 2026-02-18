import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

class TennisPredictor:
    def __init__(self, csv_path='datatenis20002025.csv'):
        self.csv_path = csv_path
        self.player_stats = {}
        self.h2h_stats = {}
        self.surface_stats = {}
        
    def load_and_prepare_data(self):
        """Charge et prépare les données de tennis"""
        print("🎾 Chargement des données tennis...")
        df = pd.read_csv(self.csv_path, low_memory=False)
        
        # Nettoyer les données
        print("🧹 Nettoyage des données tennis...")
        df = df.dropna(subset=['Player_1', 'Player_2', 'Winner'])
        
        # Remplacer les valeurs -1 par NaN puis par la médiane
        # Convertir d'abord en numérique pour éviter les erreurs
        numeric_cols = ['Rank_1', 'Rank_2', 'Odd_1', 'Odd_2']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].replace(-1, np.nan)
            df[col] = df[col].fillna(df[col].median())
        
        print(f"✅ Données nettoyées: {len(df)} matchs")
        
        # Calculer les statistiques
        self.calculate_player_stats(df)
        self.calculate_h2h_stats(df)
        self.calculate_surface_stats(df)
        
        return df
    
    def calculate_player_stats(self, df):
        """Calcule les statistiques par joueur"""
        print("📊 Calcul des statistiques des joueurs...")
        
        all_players = set(df['Player_1'].unique()) | set(df['Player_2'].unique())
        
        for player in all_players:
            # Matchs où le joueur a participé
            p1_matches = df[df['Player_1'] == player].copy()
            p2_matches = df[df['Player_2'] == player].copy()
            
            # Victoires
            p1_wins = len(p1_matches[p1_matches['Winner'] == player])
            p2_wins = len(p2_matches[p2_matches['Winner'] == player])
            total_wins = p1_wins + p2_wins
            total_matches = len(p1_matches) + len(p2_matches)
            
            if total_matches == 0:
                continue
            
            win_rate = total_wins / total_matches
            
            # Forme récente (10 derniers matchs)
            all_matches = pd.concat([p1_matches, p2_matches]).sort_values('Date')
            recent_matches = all_matches.tail(10)
            recent_wins = len(recent_matches[recent_matches['Winner'] == player])
            recent_form = recent_wins / len(recent_matches) if len(recent_matches) > 0 else 0.5
            
            # Ranking moyen
            p1_ranks = p1_matches['Rank_1'].replace(-1, np.nan)
            p2_ranks = p2_matches['Rank_2'].replace(-1, np.nan)
            all_ranks = pd.concat([p1_ranks, p2_ranks]).dropna()
            avg_rank = all_ranks.mean() if len(all_ranks) > 0 else 500
            
            self.player_stats[player] = {
                'win_rate': win_rate,
                'recent_form': recent_form,
                'avg_rank': avg_rank,
                'total_matches': total_matches,
                'total_wins': total_wins
            }
    
    def calculate_h2h_stats(self, df):
        """Calcule les statistiques head-to-head"""
        print("⚔️ Calcul des statistiques H2H tennis...")
        
        for player in self.player_stats.keys():
            p1_matches = df[df['Player_1'] == player]
            p2_matches = df[df['Player_2'] == player]
            
            # Pour chaque adversaire
            opponents_1 = p1_matches['Player_2'].unique()
            opponents_2 = p2_matches['Player_1'].unique()
            all_opponents = set(opponents_1) | set(opponents_2)
            
            for opponent in all_opponents:
                if player == opponent:
                    continue
                
                # Matchs directs
                direct_p1 = p1_matches[p1_matches['Player_2'] == opponent]
                direct_p2 = p2_matches[p2_matches['Player_1'] == opponent]
                all_direct = pd.concat([direct_p1, direct_p2])
                
                if len(all_direct) == 0:
                    continue
                
                h2h_key = f"{player}_vs_{opponent}"
                
                wins = len(all_direct[all_direct['Winner'] == player])
                total = len(all_direct)
                
                self.h2h_stats[h2h_key] = {
                    'win_rate': wins / total if total > 0 else 0.5,
                    'total_matches': total
                }
    
    def calculate_surface_stats(self, df):
        """Calcule les statistiques par surface pour chaque joueur"""
        print("🎾 Calcul des statistiques par surface...")
        
        for player in self.player_stats.keys():
            player_surfaces = {}
            
            for surface in ['Hard', 'Clay', 'Grass', 'Carpet']:
                # Matchs sur cette surface
                p1_matches = df[(df['Player_1'] == player) & (df['Surface'] == surface)]
                p2_matches = df[(df['Player_2'] == player) & (df['Surface'] == surface)]
                
                wins_p1 = len(p1_matches[p1_matches['Winner'] == player])
                wins_p2 = len(p2_matches[p2_matches['Winner'] == player])
                total_wins = wins_p1 + wins_p2
                total_matches = len(p1_matches) + len(p2_matches)
                
                if total_matches > 0:
                    player_surfaces[surface] = {
                        'win_rate': total_wins / total_matches,
                        'total_matches': total_matches
                    }
                else:
                    player_surfaces[surface] = {
                        'win_rate': 0.5,
                        'total_matches': 0
                    }
            
            self.surface_stats[player] = player_surfaces
    
    def predict(self, player1, player2, surface='Hard'):
        """Prédit le résultat d'un match de tennis"""
        
        # Récupérer les stats des joueurs
        stats1 = self.player_stats.get(player1, {})
        stats2 = self.player_stats.get(player2, {})
        
        if not stats1 or not stats2:
            # Valeurs par défaut si joueur inconnu
            return {
                'player1_win': 0.5,
                'player2_win': 0.5
            }
        
        # Stats générales
        win_rate1 = stats1.get('win_rate', 0.5)
        win_rate2 = stats2.get('win_rate', 0.5)
        
        form1 = stats1.get('recent_form', 0.5)
        form2 = stats2.get('recent_form', 0.5)
        
        # Ranking (plus le ranking est bas, mieux c'est)
        rank1 = stats1.get('avg_rank', 500)
        rank2 = stats2.get('avg_rank', 500)
        
        # Convertir le ranking en score (inverser pour que meilleur rank = meilleur score)
        rank_score1 = 1.0 / (1.0 + rank1 / 100.0)
        rank_score2 = 1.0 / (1.0 + rank2 / 100.0)
        
        # Stats H2H
        h2h_key = f"{player1}_vs_{player2}"
        h2h_bonus = 0.0
        
        if h2h_key in self.h2h_stats:
            h2h_data = self.h2h_stats[h2h_key]
            h2h_win_rate = h2h_data.get('win_rate', 0.5)
            h2h_bonus = (h2h_win_rate - 0.5) * 0.2  # Bonus/malus basé sur H2H
        
        # Stats par surface
        surface_bonus1 = 0.0
        surface_bonus2 = 0.0
        
        if player1 in self.surface_stats and surface in self.surface_stats[player1]:
            surface_win_rate1 = self.surface_stats[player1][surface]['win_rate']
            surface_bonus1 = (surface_win_rate1 - win_rate1) * 0.15
        
        if player2 in self.surface_stats and surface in self.surface_stats[player2]:
            surface_win_rate2 = self.surface_stats[player2][surface]['win_rate']
            surface_bonus2 = (surface_win_rate2 - win_rate2) * 0.15
        
        # Calcul du score de "force"
        strength1 = (
            win_rate1 * 0.30 +
            form1 * 0.25 +
            rank_score1 * 0.20 +
            surface_bonus1
        )
        
        strength2 = (
            win_rate2 * 0.30 +
            form2 * 0.25 +
            rank_score2 * 0.20 +
            surface_bonus2
        )
        
        # Ajuster avec H2H
        strength1 += h2h_bonus
        
        # Calculer les probabilités
        total_strength = strength1 + strength2
        
        if total_strength > 0:
            prob1 = strength1 / total_strength
            prob2 = strength2 / total_strength
        else:
            prob1 = 0.5
            prob2 = 0.5
        
        # Limiter les probabilités extrêmes (min 15%, max 85%)
        prob1 = max(0.15, min(0.85, prob1))
        prob2 = max(0.15, min(0.85, prob2))
        
        # Renormaliser
        total = prob1 + prob2
        prob1 /= total
        prob2 /= total
        
        return {
            'player1_win': float(prob1),
            'player2_win': float(prob2)
        }
    
    def get_all_players(self):
        """Retourne la liste de tous les joueurs"""
        return sorted(list(self.player_stats.keys()))
    
    def get_player_info(self, player):
        """Retourne les informations d'un joueur"""
        if player not in self.player_stats:
            return None
        
        stats = self.player_stats[player]
        surface_info = self.surface_stats.get(player, {})
        
        return {
            'name': player,
            'win_rate': stats['win_rate'],
            'recent_form': stats['recent_form'],
            'avg_rank': stats['avg_rank'],
            'total_matches': stats['total_matches'],
            'total_wins': stats['total_wins'],
            'surfaces': surface_info
        }

if __name__ == "__main__":
    # Tester le modèle
    predictor = TennisPredictor('datatenis20002025.csv')
    predictor.load_and_prepare_data()
    
    # Afficher quelques joueurs
    players = predictor.get_all_players()
    print(f"\n✅ {len(players)} joueurs chargés")
    
    if len(players) >= 2:
        player1, player2 = players[0], players[1]
        result = predictor.predict(player1, player2, 'Hard')
        print(f"\n🎯 Prédiction {player1} vs {player2} (Hard):")
        print(f"   {player1}: {result['player1_win']*100:.2f}%")
        print(f"   {player2}: {result['player2_win']*100:.2f}%")
