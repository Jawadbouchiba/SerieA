#!/usr/bin/env python3
"""
Advanced Betting Strategy Module for Sports Betting
Implements best practices for profitable sports betting
"""

import numpy as np
from model import FootballPredictor


class BettingStrategy:
    """Stratégies avancées pour les paris sportifs"""
    
    def __init__(self, predictor, initial_bankroll=1000):
        self.predictor = predictor
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.bet_history = []
        
    def evaluate_match(self, team1, team2, venue, bookmaker_odds, 
                      min_confidence=0.65, min_edge=0.08, max_stake=0.05):
        """
        Évalue un match et retourne une recommandation de pari
        
        Args:
            team1: Équipe 1
            team2: Équipe 2
            venue: 'Home' ou 'Away'
            bookmaker_odds: dict avec 'win', 'draw', 'loss'
            min_confidence: Seuil minimal de confiance (défaut: 65%)
            min_edge: Avantage minimal requis (défaut: 8%)
            max_stake: Mise maximale en % du bankroll (défaut: 5%)
        
        Returns:
            dict avec recommandation complète
        """
        # Obtenir la prédiction
        prediction = self.predictor.predict(team1, team2, venue, use_neural_network=True)
        
        # Analyse de valeur
        betting_analysis = self.predictor.calculate_betting_value(prediction, bookmaker_odds)
        
        # Vérifier les conditions
        should_bet, reason = self.predictor.should_bet(
            prediction, bookmaker_odds, 
            min_confidence=min_confidence, 
            min_edge=min_edge
        )
        
        recommendation = {
            'match': f"{team1} vs {team2}",
            'venue': venue,
            'prediction': prediction,
            'betting_analysis': betting_analysis,
            'should_bet': should_bet,
            'reason': reason,
            'bankroll': self.current_bankroll
        }
        
        if should_bet and betting_analysis['best_bet']:
            best = betting_analysis['outcomes'][betting_analysis['best_bet']]
            stake_pct = min(best['kelly_stake'], max_stake)
            stake_amount = self.current_bankroll * stake_pct
            
            recommendation['bet_details'] = {
                'outcome': betting_analysis['best_bet'],
                'stake_pct': stake_pct,
                'stake_amount': stake_amount,
                'odds': bookmaker_odds[betting_analysis['best_bet']],
                'expected_value': best['expected_value'],
                'edge': best['edge']
            }
        
        return recommendation
    
    def simulate_bet(self, recommendation, actual_result):
        """
        Simule un pari et met à jour le bankroll
        
        Args:
            recommendation: Recommandation de pari
            actual_result: 'win', 'draw', ou 'loss'
        
        Returns:
            dict avec résultats du pari
        """
        if not recommendation['should_bet']:
            return {
                'bet_placed': False,
                'profit': 0,
                'new_bankroll': self.current_bankroll
            }
        
        bet_details = recommendation['bet_details']
        stake = bet_details['stake_amount']
        odds = bet_details['odds']
        predicted_outcome = bet_details['outcome']
        
        # Calculer le résultat
        if predicted_outcome == actual_result:
            profit = stake * (odds - 1)
            won = True
        else:
            profit = -stake
            won = False
        
        # Mettre à jour le bankroll
        self.current_bankroll += profit
        
        # Enregistrer dans l'historique
        bet_record = {
            'match': recommendation['match'],
            'predicted': predicted_outcome,
            'actual': actual_result,
            'stake': stake,
            'odds': odds,
            'profit': profit,
            'won': won,
            'new_bankroll': self.current_bankroll,
            'bankroll_after': self.current_bankroll,
            'roi': (profit / stake) * 100 if stake > 0 else 0
        }
        self.bet_history.append(bet_record)
        
        return bet_record
    
    def get_performance_stats(self):
        """Retourne les statistiques de performance"""
        if not self.bet_history:
            return None
        
        total_bets = len(self.bet_history)
        wins = sum(1 for bet in self.bet_history if bet['won'])
        total_staked = sum(bet['stake'] for bet in self.bet_history)
        total_profit = sum(bet['profit'] for bet in self.bet_history)
        
        win_rate = (wins / total_bets) * 100 if total_bets > 0 else 0
        roi = (total_profit / total_staked) * 100 if total_staked > 0 else 0
        bankroll_growth = ((self.current_bankroll - self.initial_bankroll) / self.initial_bankroll) * 100
        
        return {
            'total_bets': total_bets,
            'wins': wins,
            'losses': total_bets - wins,
            'win_rate': win_rate,
            'total_staked': total_staked,
            'total_profit': total_profit,
            'roi': roi,
            'initial_bankroll': self.initial_bankroll,
            'current_bankroll': self.current_bankroll,
            'bankroll_growth': bankroll_growth,
            'avg_stake': total_staked / total_bets if total_bets > 0 else 0,
            'avg_profit_per_bet': total_profit / total_bets if total_bets > 0 else 0
        }
    
    def print_performance_report(self):
        """Affiche un rapport de performance détaillé"""
        stats = self.get_performance_stats()
        
        if not stats:
            print("❌ Aucun pari dans l'historique")
            return
        
        print("\n" + "="*60)
        print("📊 RAPPORT DE PERFORMANCE DES PARIS")
        print("="*60)
        print(f"\n💰 Bankroll:")
        print(f"   Initial: ${stats['initial_bankroll']:.2f}")
        print(f"   Actuel:  ${stats['current_bankroll']:.2f}")
        print(f"   Croissance: {stats['bankroll_growth']:+.2f}%")
        
        print(f"\n📈 Statistiques:")
        print(f"   Total de paris: {stats['total_bets']}")
        print(f"   Victoires: {stats['wins']} ({stats['win_rate']:.1f}%)")
        print(f"   Défaites: {stats['losses']}")
        
        print(f"\n💵 Finances:")
        print(f"   Total misé: ${stats['total_staked']:.2f}")
        print(f"   Profit total: ${stats['total_profit']:+.2f}")
        print(f"   ROI: {stats['roi']:+.2f}%")
        print(f"   Mise moyenne: ${stats['avg_stake']:.2f}")
        print(f"   Profit moyen par pari: ${stats['avg_profit_per_bet']:+.2f}")
        
        print("\n" + "="*60)
        
        # Afficher les derniers paris
        if len(self.bet_history) > 0:
            print("\n📜 Derniers paris (max 10):")
            for bet in self.bet_history[-10:]:
                result_icon = "✅" if bet['won'] else "❌"
                print(f"   {result_icon} {bet['match']}: {bet['predicted']} @ {bet['odds']:.2f}")
                print(f"      Mise: ${bet['stake']:.2f} | Profit: ${bet['profit']:+.2f} | ROI: {bet['roi']:+.1f}%")


def analyze_betting_conditions(predictor, team1, team2, venue='Home'):
    """
    Analyse approfondie des conditions de pari pour un match
    
    Affiche:
    - Prédictions du modèle
    - Statistiques des équipes
    - Recommandations de seuils
    """
    print(f"\n{'='*70}")
    print(f"🔍 ANALYSE APPROFONDIE: {team1} vs {team2} ({venue})")
    print(f"{'='*70}")
    
    # Prédiction
    pred = predictor.predict(team1, team2, venue, use_neural_network=True)
    
    print(f"\n📊 Prédictions du modèle:")
    print(f"   Victoire {team1}: {pred['win']*100:.2f}%")
    print(f"   Match nul: {pred['draw']*100:.2f}%")
    print(f"   Victoire {team2}: {pred['loss']*100:.2f}%")
    print(f"   Confiance: {pred['confidence']*100:.1f}%")
    print(f"   Probabilité max: {pred['max_prob']*100:.1f}%")
    
    # Statistiques des équipes
    stats1 = predictor.team_stats.get(team1, {})
    stats2 = predictor.team_stats.get(team2, {})
    
    print(f"\n📈 Statistiques {team1}:")
    print(f"   Taux de victoire: {stats1.get('win_rate', 0)*100:.1f}%")
    print(f"   Forme récente: {stats1.get('recent_form', 0)*100:.1f}%")
    print(f"   Buts marqués (moy): {stats1.get('avg_gf', 0):.2f}")
    print(f"   Buts encaissés (moy): {stats1.get('avg_ga', 0):.2f}")
    print(f"   xG (moy): {stats1.get('avg_xg', 0):.2f}")
    print(f"   Total matchs: {stats1.get('total_games', 0)}")
    
    print(f"\n📈 Statistiques {team2}:")
    print(f"   Taux de victoire: {stats2.get('win_rate', 0)*100:.1f}%")
    print(f"   Forme récente: {stats2.get('recent_form', 0)*100:.1f}%")
    print(f"   Buts marqués (moy): {stats2.get('avg_gf', 0):.2f}")
    print(f"   Buts encaissés (moy): {stats2.get('avg_ga', 0):.2f}")
    print(f"   xG (moy): {stats2.get('avg_xg', 0):.2f}")
    print(f"   Total matchs: {stats2.get('total_games', 0)}")
    
    # H2H
    h2h_key = f"{team1}_vs_{team2}"
    h2h = predictor.h2h_stats.get(h2h_key, {})
    
    if h2h:
        print(f"\n⚔️ Head-to-Head:")
        print(f"   Taux de victoire {team1}: {h2h.get('win_rate', 0)*100:.1f}%")
        print(f"   Différence de buts (moy): {h2h.get('avg_gd', 0):+.2f}")
        print(f"   Total matchs H2H: {h2h.get('total_matches', 0)}")
    
    # Recommandations de cotes
    print(f"\n💡 Cotes minimales recommandées (pour EV positif):")
    print(f"   Victoire {team1}: {1/pred['win']:.2f}")
    print(f"   Match nul: {1/pred['draw']:.2f}")
    print(f"   Victoire {team2}: {1/pred['loss']:.2f}")
    
    # Seuils de confiance
    if pred['confidence'] >= 0.75:
        conf_msg = "🟢 EXCELLENTE - Prédiction très fiable"
    elif pred['confidence'] >= 0.65:
        conf_msg = "🟡 BONNE - Prédiction fiable"
    elif pred['confidence'] >= 0.50:
        conf_msg = "🟠 MOYENNE - Prudence recommandée"
    else:
        conf_msg = "🔴 FAIBLE - Éviter de parier"
    
    print(f"\n🎯 Niveau de confiance: {conf_msg}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    # Exemple d'utilisation
    print("📥 Chargement du modèle...")
    predictor = FootballPredictor('data20202025.csv')
    predictor.load_model('best_model.pth')
    
    teams = predictor.get_all_teams()
    if len(teams) >= 2:
        # Analyse détaillée
        analyze_betting_conditions(predictor, teams[0], teams[1], 'Home')
        
        # Exemple de stratégie de paris
        strategy = BettingStrategy(predictor, initial_bankroll=1000)
        
        # Évaluer un match avec cotes fictives
        bookmaker_odds = {'win': 2.10, 'draw': 3.40, 'loss': 3.50}
        recommendation = strategy.evaluate_match(
            teams[0], teams[1], 'Home', bookmaker_odds,
            min_confidence=0.65,
            min_edge=0.08
        )
        
        print(f"\n💰 Recommandation de pari:")
        print(f"   Match: {recommendation['match']}")
        print(f"   Parier? {recommendation['should_bet']}")
        print(f"   Raison: {recommendation['reason']}")
        
        if recommendation['should_bet']:
            details = recommendation['bet_details']
            print(f"\n✅ Détails du pari recommandé:")
            print(f"   Issue: {details['outcome']}")
            print(f"   Mise: ${details['stake_amount']:.2f} ({details['stake_pct']*100:.2f}% du bankroll)")
            print(f"   Cote: {details['odds']:.2f}")
            print(f"   EV: {details['expected_value']*100:+.2f}%")
            print(f"   Edge: {details['edge']*100:+.2f}%")
