import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


class FootballDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class FootballNN(nn.Module):
    def __init__(self, input_size):
        super(FootballNN, self).__init__()
     
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.4),
            
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            nn.Linear(32, 3)  # 3 outputs: Win, Draw, Loss probabilities
        )
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.network(x)
        return self.softmax(x)

class FootballPredictor:
    def __init__(self, csv_path='data20202025.csv'):
        self.csv_path = csv_path
        self.model = None
        self.scaler = StandardScaler()
        self.team_encoder = LabelEncoder()
        self.team_stats = {}
        self.h2h_stats = {}  # Stocker les statistiques H2H
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def load_and_prepare_data(self):
        """Charge et prépare les données"""
        print("📊 Chargement des données...")
        df = pd.read_csv(self.csv_path)
        
        # Nettoyer les données
        print("🧹 Nettoyage des données...")
        # Remplir les valeurs manquantes avec la médiane
        numeric_columns = ['gf', 'ga', 'xg', 'xga', 'sh', 'sot', 'poss']
        for col in numeric_columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Supprimer les lignes avec des valeurs infinies ou NaN restantes
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(subset=numeric_columns)
        
        print(f"✅ Données nettoyées: {len(df)} matchs")
        
        # Préparation des features (chronologique)
        X, y = self.prepare_features(df)
        
        # Calcul des statistiques finales pour les prédictions futures
        self.calculate_team_stats(df)
        self.calculate_h2h_stats(df)
        
        return X, y
    
    def calculate_team_stats(self, df):
        """Calcule les statistiques moyennes par équipe"""
        print("📈 Calcul des statistiques des équipes...")
        
        for team in df['team'].unique():
            team_data = df[df['team'] == team]
            
            # Statistiques d'attaque
            avg_gf = team_data['gf'].mean()
            avg_xg = team_data['xg'].mean()
            avg_sh = team_data['sh'].mean()
            avg_sot = team_data['sot'].mean()
            
            # Statistiques de défense
            avg_ga = team_data['ga'].mean()
            avg_xga = team_data['xga'].mean()
            
            # Possession
            avg_poss = team_data['poss'].mean()
            
            # Résultats
            wins = len(team_data[team_data['result'] == 'W'])
            draws = len(team_data[team_data['result'] == 'D'])
            losses = len(team_data[team_data['result'] == 'L'])
            total_games = len(team_data)
            
            win_rate = wins / total_games if total_games > 0 else 0
            
            # Forme récente (derniers 5 matchs)
            recent_games = team_data.tail(5)
            recent_wins = len(recent_games[recent_games['result'] == 'W'])
            recent_form = recent_wins / len(recent_games) if len(recent_games) > 0 else 0
            
            self.team_stats[team] = {
                'avg_gf': avg_gf,
                'avg_ga': avg_ga,
                'avg_xg': avg_xg,
                'avg_xga': avg_xga,
                'avg_sh': avg_sh,
                'avg_sot': avg_sot,
                'avg_poss': avg_poss,
                'win_rate': win_rate,
                'recent_form': recent_form,
                'total_games': total_games
            }
    
    def calculate_h2h_stats(self, df):
        """Calcule les statistiques des confrontations directes"""
        print("⚔️ Calcul des statistiques head-to-head...")
        
        for team in df['team'].unique():
            team_matches = df[df['team'] == team]
            
            for opponent in df['team'].unique():
                if team == opponent:
                    continue
                
                # Matchs où team joue
                direct = team_matches[team_matches['opponent'] == opponent]
                
                if len(direct) == 0:
                    continue
                
                h2h_key = f"{team}_vs_{opponent}"
                
                wins = len(direct[direct['result'] == 'W'])
                draws = len(direct[direct['result'] == 'D'])
                losses = len(direct[direct['result'] == 'L'])
                total = len(direct)
                
                avg_gf = direct['gf'].mean()
                avg_ga = direct['ga'].mean()
                avg_gd = avg_gf - avg_ga
                
                self.h2h_stats[h2h_key] = {
                    'win_rate': wins / total if total > 0 else 0.33,
                    'avg_gd': avg_gd,
                    'recent_form': wins / min(3, total) if total > 0 else 0.33,
                    'total_matches': total
                }
    
    def get_team_features(self, team):
        """Récupère les features d'une équipe"""
        if team not in self.team_stats:
            # Valeurs par défaut si l'équipe n'existe pas
            return [1.0, 1.0, 1.0, 1.0, 10.0, 5.0, 50.0, 0.33, 0.33]
        
        stats = self.team_stats[team]
        return [
            stats['avg_gf'],
            stats['avg_ga'],
            stats['avg_xg'],
            stats['avg_xga'],
            stats['avg_sh'],
            stats['avg_sot'],
            stats['avg_poss'],
            stats['win_rate'],
            stats['recent_form']
        ]
    
    def prepare_features(self, df):
        """Prépare les features pour l'entraînement de manière chronologique"""
        print("🔧 Préparation des features (chronologique)...")
        
        # Trier par date pour traitement chronologique
        df = df.sort_values('date').reset_index(drop=True)
        
        X = []
        y = []
        
        # Statistiques évolutives par équipe (mises à jour après chaque match)
        team_history = {}
        # Historique des confrontations directes
        h2h_history = {}
        
        for idx, row in df.iterrows():
            team = row['team']
            opponent = row['opponent']
            venue = 1 if row['venue'] == 'Home' else 0
            
            # Initialiser l'historique si nécessaire
            if team not in team_history:
                team_history[team] = {
                    'matches': [],
                    'results': []
                }
            if opponent not in team_history:
                team_history[opponent] = {
                    'matches': [],
                    'results': []
                }
            
            # Calculer les features AVANT le match (avec données passées uniquement)
            team_features = self.get_historical_features(team_history[team])
            opponent_features = self.get_historical_features(team_history[opponent])
            
            # Ajouter les statistiques head-to-head
            h2h_key = f"{team}_vs_{opponent}"
            h2h_reverse = f"{opponent}_vs_{team}"
            h2h_features = self.get_h2h_features(h2h_history, h2h_key, h2h_reverse)
            
            # Combiner toutes les features
            features = team_features + opponent_features + [venue] + h2h_features
            X.append(features)
            
            # Label (résultat)
            if row['result'] == 'W':
                y.append([1, 0, 0])  # Victoire
            elif row['result'] == 'D':
                y.append([0, 1, 0])  # Nul
            else:
                y.append([0, 0, 1])  # Défaite
            
            # Mettre à jour l'historique APRÈS avoir créé les features
            team_history[team]['matches'].append({
                'gf': row['gf'],
                'ga': row['ga'],
                'xg': row['xg'],
                'xga': row['xga'],
                'sh': row['sh'],
                'sot': row['sot'],
                'poss': row['poss'],
                'result': row['result']
            })
            team_history[team]['results'].append(row['result'])
            
            # Mettre à jour l'historique H2H
            if h2h_key not in h2h_history:
                h2h_history[h2h_key] = []
            h2h_history[h2h_key].append({
                'result': row['result'],
                'gf': row['gf'],
                'ga': row['ga']
            })
        
        return np.array(X), np.array(y)
    
    def get_historical_features(self, history):
        """Calcule les features basées sur l'historique passé d'une équipe"""
        matches = history['matches']
        results = history['results']
        
        if len(matches) == 0:
            # Valeurs par défaut pour les équipes sans historique
            return [1.0, 1.0, 1.0, 1.0, 10.0, 5.0, 50.0, 0.33, 0.33]
        
        # Calculer les moyennes sur tous les matchs passés
        avg_gf = np.mean([m['gf'] for m in matches])
        avg_ga = np.mean([m['ga'] for m in matches])
        avg_xg = np.mean([m['xg'] for m in matches])
        avg_xga = np.mean([m['xga'] for m in matches])
        avg_sh = np.mean([m['sh'] for m in matches])
        avg_sot = np.mean([m['sot'] for m in matches])
        avg_poss = np.mean([m['poss'] for m in matches])
        
        # Taux de victoire
        wins = results.count('W')
        win_rate = wins / len(results) if len(results) > 0 else 0.33
        
        # Forme récente (derniers 5 matchs)
        recent_results = results[-5:] if len(results) >= 5 else results
        recent_wins = recent_results.count('W')
        recent_form = recent_wins / len(recent_results) if len(recent_results) > 0 else 0.33
        
        return [
            avg_gf, avg_ga, avg_xg, avg_xga,
            avg_sh, avg_sot, avg_poss,
            win_rate, recent_form
        ]
    
    def get_h2h_features(self, h2h_history, h2h_key, h2h_reverse):
        """Calcule les features basées sur l'historique des confrontations directes"""
        # Récupérer les matchs directs
        direct_matches = h2h_history.get(h2h_key, [])
        reverse_matches = h2h_history.get(h2h_reverse, [])
        
        if len(direct_matches) == 0 and len(reverse_matches) == 0:
            # Pas d'historique : valeurs neutres
            return [0.33, 0.0, 0.0]
        
        # Compter les victoires dans les matchs directs
        wins = sum(1 for m in direct_matches if m['result'] == 'W')
        draws = sum(1 for m in direct_matches if m['result'] == 'D')
        
        # Compter les défaites (= victoires de l'adversaire)
        losses = sum(1 for m in reverse_matches if m['result'] == 'W')
        reverse_draws = sum(1 for m in reverse_matches if m['result'] == 'D')
        
        total_matches = len(direct_matches) + len(reverse_matches)
        total_draws = draws + reverse_draws
        
        if total_matches == 0:
            return [0.33, 0.0, 0.0]
        
        # Taux de victoire en H2H
        h2h_win_rate = wins / total_matches if total_matches > 0 else 0.33
        
        # Différence de buts moyenne en H2H
        all_gf = [m['gf'] for m in direct_matches] + [m['ga'] for m in reverse_matches]
        all_ga = [m['ga'] for m in direct_matches] + [m['gf'] for m in reverse_matches]
        
        if len(all_gf) > 0:
            avg_gd = float(np.mean(np.array(all_gf) - np.array(all_ga)))
            # Limiter pour éviter des valeurs extrêmes
            avg_gd = np.clip(avg_gd, -5.0, 5.0)
        else:
            avg_gd = 0.0
        
        # Forme récente H2H (derniers 3 matchs)
        recent_h2h_direct = direct_matches[-3:] if len(direct_matches) >= 3 else direct_matches
        recent_h2h_wins = sum(1 for m in recent_h2h_direct if m['result'] == 'W')
        recent_total = min(3, len(direct_matches) + len(reverse_matches))
        recent_h2h_form = recent_h2h_wins / recent_total if recent_total > 0 else 0.33
        
        return [float(h2h_win_rate), float(avg_gd), float(recent_h2h_form)]
    
    def train(self, epochs=100, batch_size=32, learning_rate=0.001):
        """Entraîne le modèle"""
        print(f"🚀 Démarrage de l'entraînement sur {self.device}...")
        
        # Charger et préparer les données
        X, y = self.load_and_prepare_data()
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalisation
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        # Créer les datasets
        train_dataset = FootballDataset(X_train, y_train)
        test_dataset = FootballDataset(X_test, y_test)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size)
        
        # Initialiser le modèle
        input_size = X_train.shape[1]
        self.model = FootballNN(input_size).to(self.device)
        
        # Loss et optimizer avec label smoothing pour réduire la confiance excessive
        criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=1e-4)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=10, factor=0.5)
        
        # Entraînement
        best_test_loss = float('inf')
        history = {'train_loss': [], 'test_loss': [], 'test_acc': []}
        
        for epoch in range(epochs):
            # Phase d'entraînement
            self.model.train()
            train_loss = 0
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            
            # Phase de validation
            self.model.eval()
            test_loss = 0
            correct = 0
            total = 0
            
            with torch.no_grad():
                for batch_X, batch_y in test_loader:
                    batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                    outputs = self.model(batch_X)
                    loss = criterion(outputs, batch_y)
                    test_loss += loss.item()
                    
                    # Calculer l'accuracy
                    _, predicted = outputs.max(1)
                    _, labels = batch_y.max(1)
                    total += labels.size(0)
                    correct += predicted.eq(labels).sum().item()
            
            test_loss /= len(test_loader)
            test_acc = 100. * correct / total
            
            scheduler.step(test_loss)
            
            history['train_loss'].append(train_loss)
            history['test_loss'].append(test_loss)
            history['test_acc'].append(test_acc)
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{epochs}] - "
                      f"Train Loss: {train_loss:.4f}, "
                      f"Test Loss: {test_loss:.4f}, "
                      f"Test Acc: {test_acc:.2f}%")
            
            # Sauvegarder le meilleur modèle
            if test_loss < best_test_loss:
                best_test_loss = test_loss
                self.save_model('best_model.pth')
        
        print(f"\n✅ Entraînement terminé! Meilleure précision: {max(history['test_acc']):.2f}%")
        return history
    
    def predict(self, team1, team2, venue='Home', use_neural_network=True):
        """Prédit le résultat d'un match avec une approche hybride
        
        Args:
            team1: Nom de l'équipe à domicile
            team2: Nom de l'équipe à l'extérieur
            venue: 'Home' ou 'Away'
            use_neural_network: Si True, utilise le réseau de neurones. Si False, utilise uniquement les heuristiques
        
        Returns:
            dict avec 'win', 'draw', 'loss' probabilities et 'confidence' score
        """
        if self.model is None:
            raise ValueError("Le modèle n'est pas entraîné. Appelez train() d'abord.")
        
        # Récupérer les statistiques des équipes
        stats1 = self.team_stats.get(team1, {})
        stats2 = self.team_stats.get(team2, {})
        
        # Statistiques de base
        win_rate1 = stats1.get('win_rate', 0.33)
        win_rate2 = stats2.get('win_rate', 0.33)
        
        form1 = stats1.get('recent_form', 0.33)
        form2 = stats2.get('recent_form', 0.33)
        
        # Statistiques offensives/défensives
        attack1 = stats1.get('avg_gf', 1.0) / max(stats1.get('avg_ga', 1.0), 0.5)
        attack2 = stats2.get('avg_gf', 1.0) / max(stats2.get('avg_ga', 1.0), 0.5)
        
        # xG ratio
        xg1 = stats1.get('avg_xg', 1.0)
        xga1 = stats1.get('avg_xga', 1.0)
        xg2 = stats2.get('avg_xg', 1.0)
        xga2 = stats2.get('avg_xga', 1.0)
        
        # Avantage domicile/extérieur
        home_advantage = 0.08 if venue == 'Home' else -0.05
        
        # Historique H2H
        h2h_key = f"{team1}_vs_{team2}"
        h2h_reverse = f"{team2}_vs_{team1}"
        h2h_bonus = 0.0
        
        if h2h_key in self.h2h_stats:
            h2h_data = self.h2h_stats[h2h_key]
            h2h_win_rate = h2h_data.get('win_rate', 0.33)
            h2h_bonus = (h2h_win_rate - 0.33) * 0.15
        
        # Calcul des forces relatives
        strength1 = (win_rate1 * 0.35 + form1 * 0.25 + min(attack1/2, 0.5) * 0.2 + (xg1 - xga1) * 0.05)
        strength2 = (win_rate2 * 0.35 + form2 * 0.25 + min(attack2/2, 0.5) * 0.2 + (xg2 - xga2) * 0.05)
        
        # Ajuster avec H2H et avantage domicile
        strength1 += home_advantage + h2h_bonus
        
        # Calculer les probabilités brutes
        total_strength = strength1 + strength2
        if total_strength > 0:
            base_win = strength1 / total_strength
            base_loss = strength2 / total_strength
        else:
            base_win = 0.4
            base_loss = 0.4
        
        # Probabilité de match nul basée sur les stats historiques
        # Plus les équipes sont proches en niveau, plus le nul est probable
        strength_diff = abs(strength1 - strength2)
        draw_prob = max(0.15, min(0.35, 0.30 - strength_diff * 0.3))
        
        # Normaliser les probabilités
        remaining = 1.0 - draw_prob
        win_prob = base_win * remaining
        loss_prob = base_loss * remaining
        
        # Calcul des probabilités via réseau de neurones si demandé
        if use_neural_network:
            # Préparer les features pour le modèle
            team1_features = self.get_team_features(team1)
            team2_features = self.get_team_features(team2)
            venue_encoded = 1 if venue == 'Home' else 0
            
            # H2H features
            h2h_key = f"{team1}_vs_{team2}"
            h2h_reverse = f"{team2}_vs_{team1}"
            h2h = self.h2h_stats.get(h2h_key, {})
            h2h_rev = self.h2h_stats.get(h2h_reverse, {})
            
            if h2h:
                h2h_features = [
                    h2h.get('win_rate', 0.33),
                    h2h.get('avg_gd', 0.0),
                    h2h.get('recent_form', 0.33)
                ]
            else:
                h2h_features = [0.33, 0.0, 0.33]
            
            features = np.array([team1_features + team2_features + [venue_encoded] + h2h_features])
            features_scaled = self.scaler.transform(features)
            
            with torch.no_grad():
                X_tensor = torch.FloatTensor(features_scaled).to(self.device)
                nn_output = self.model(X_tensor)
                nn_probs = nn_output.cpu().numpy()[0]
            
            # Combiner les probabilités du réseau avec les heuristiques (70% NN, 30% heuristique)
            win_prob = 0.7 * nn_probs[0] + 0.3 * win_prob
            draw_prob = 0.7 * nn_probs[1] + 0.3 * draw_prob
            loss_prob = 0.7 * nn_probs[2] + 0.3 * loss_prob
        
        # Renormaliser pour que le total = 1
        total = win_prob + draw_prob + loss_prob
        win_prob /= total
        draw_prob /= total
        loss_prob /= total
        
        # Calculer le score de confiance (basé sur l'entropie et la distance au 33%)
        max_prob = max(win_prob, draw_prob, loss_prob)
        entropy = -(win_prob * np.log(win_prob + 1e-10) + 
                   draw_prob * np.log(draw_prob + 1e-10) + 
                   loss_prob * np.log(loss_prob + 1e-10))
        max_entropy = -np.log(1/3)  # Entropie maximale pour 3 classes
        
        # Score de confiance : 1.0 = très confiant, 0.0 = incertain
        confidence = 1.0 - (entropy / max_entropy)
        
        # Ajuster la confiance en fonction du nombre de matchs disponibles
        total_games = min(stats1.get('total_games', 0), stats2.get('total_games', 0))
        if total_games < 10:
            confidence *= 0.6  # Réduire la confiance si peu de données
        elif total_games < 20:
            confidence *= 0.8
        
        return {
            'win': float(win_prob),
            'draw': float(draw_prob),
            'loss': float(loss_prob),
            'confidence': float(confidence),
            'max_prob': float(max_prob)
        }
    
    def save_model(self, filename='football_model.pth'):
        """Sauvegarde le modèle"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'team_stats': self.team_stats,
            'h2h_stats': self.h2h_stats
        }, filename)
    
    def load_model(self, filename='football_model.pth'):
        """Charge le modèle"""
        checkpoint = torch.load(filename, map_location=self.device, weights_only=False)
        
        # Déterminer la taille d'entrée
        input_size = 22  # 9 features par équipe + 1 venue + 3 H2H features
        self.model = FootballNN(input_size).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.scaler = checkpoint['scaler']
        self.team_stats = checkpoint['team_stats']
        self.h2h_stats = checkpoint.get('h2h_stats', {})
        self.model.eval()
    
    def get_all_teams(self):
        """Retourne la liste de toutes les équipes"""
        return sorted(list(self.team_stats.keys()))
    
    def calculate_betting_value(self, prediction, bookmaker_odds):
        """Calcule la valeur d'un pari selon les cotes du bookmaker
        
        Args:
            prediction: dict avec 'win', 'draw', 'loss', 'confidence'
            bookmaker_odds: dict avec 'win', 'draw', 'loss' (cotes décimales)
        
        Returns:
            dict avec recommandations de paris et expected value
        """
        results = {}
        
        for outcome in ['win', 'draw', 'loss']:
            prob = prediction[outcome]
            odds = bookmaker_odds.get(outcome, 0)
            
            if odds <= 1.0:
                results[outcome] = {
                    'bet': False,
                    'reason': 'Invalid odds',
                    'expected_value': 0,
                    'kelly_stake': 0
                }
                continue
            
            # Expected Value = (Probabilité * Cote) - 1
            expected_value = (prob * odds) - 1
            
            # Kelly Criterion: f = (bp - q) / b
            # où f = fraction du bankroll, b = cote - 1, p = prob de gagner, q = prob de perdre
            b = odds - 1
            kelly_fraction = (b * prob - (1 - prob)) / b if b > 0 else 0
            
            # Limiter Kelly à 5% maximum (fractional Kelly: 25% de Kelly complet)
            kelly_stake = max(0, min(kelly_fraction * 0.25, 0.05))
            
            # Conditions pour parier
            should_bet = (
                expected_value > 0.05 and  # Au moins 5% d'EV positif
                prediction['confidence'] > 0.6 and  # Confiance minimale de 60%
                prob > 0.35 and  # Probabilité minimale de 35%
                kelly_stake > 0.005  # Mise Kelly > 0.5% du bankroll
            )
            
            results[outcome] = {
                'bet': should_bet,
                'expected_value': float(expected_value),
                'kelly_stake': float(kelly_stake),
                'implied_prob': float(1/odds),
                'model_prob': float(prob),
                'edge': float(prob - 1/odds)
            }
        
        # Trouver le meilleur pari
        best_bet = None
        best_ev = -1
        
        for outcome, data in results.items():
            if data['bet'] and data['expected_value'] > best_ev:
                best_ev = data['expected_value']
                best_bet = outcome
        
        return {
            'outcomes': results,
            'best_bet': best_bet,
            'confidence': prediction['confidence']
        }
    
    def should_bet(self, prediction, bookmaker_odds, min_confidence=0.65, min_edge=0.08):
        """Décide si un pari vaut la peine d'être placé
        
        Args:
            prediction: dict avec probabilités prédites
            bookmaker_odds: dict avec cotes du bookmaker
            min_confidence: Seuil minimal de confiance (0-1)
            min_edge: Avantage minimal requis (edge)
        
        Returns:
            bool: True si le pari est recommandé
        """
        if prediction['confidence'] < min_confidence:
            return False, "Confidence trop faible"
        
        betting_analysis = self.calculate_betting_value(prediction, bookmaker_odds)
        
        if not betting_analysis['best_bet']:
            return False, "Aucune valeur positive détectée"
        
        best = betting_analysis['outcomes'][betting_analysis['best_bet']]
        
        if best['edge'] < min_edge:
            return False, f"Edge insuffisant ({best['edge']:.2%} < {min_edge:.2%})"
        
        return True, f"Parier sur {betting_analysis['best_bet']} (EV: {best['expected_value']:.2%}, Edge: {best['edge']:.2%})"
    
    def calibration_curve(self, X_test, y_test, n_bins=10):
        """Calcule la courbe de calibration du modèle pour vérifier la fiabilité des probabilités
        
        Returns:
            dict avec les probabilités prédites vs observées
        """
        if self.model is None:
            raise ValueError("Le modèle n'est pas entraîné.")
        
        self.model.eval()
        X_test_scaled = self.scaler.transform(X_test)
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X_test_scaled).to(self.device)
            predictions = self.model(X_tensor).cpu().numpy()
        
        # Extraire les prédictions pour la classe "Win"
        pred_probs = predictions[:, 0]
        true_labels = y_test[:, 0]
        
        # Créer les bins
        bins = np.linspace(0, 1, n_bins + 1)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        observed_freqs = []
        for i in range(n_bins):
            mask = (pred_probs >= bins[i]) & (pred_probs < bins[i+1])
            if mask.sum() > 0:
                observed_freqs.append(true_labels[mask].mean())
            else:
                observed_freqs.append(0)
        
        return {
            'predicted': bin_centers.tolist(),
            'observed': observed_freqs,
            'bins': bins.tolist()
        }

if __name__ == "__main__":
    # Entraîner le modèle
    predictor = FootballPredictor('data20202025.csv')
    history = predictor.train(epochs=150, batch_size=32, learning_rate=0.001)
    
    # Tester une prédiction avec analyse de paris
    teams = predictor.get_all_teams()
    if len(teams) >= 2:
        team1, team2 = teams[0], teams[1]
        result = predictor.predict(team1, team2, 'Home', use_neural_network=True)
        
        print(f"\n🎯 Prédiction {team1} vs {team2} (à domicile):")
        print(f"   Victoire {team1}: {result['win']*100:.2f}%")
        print(f"   Match nul: {result['draw']*100:.2f}%")
        print(f"   Victoire {team2}: {result['loss']*100:.2f}%")
        print(f"   Confiance: {result['confidence']*100:.1f}%")
        
        # Exemple d'analyse de paris avec cotes fictives
        bookmaker_odds = {
            'win': 2.10,
            'draw': 3.40,
            'loss': 3.50
        }
        
        print(f"\n💰 Analyse de paris (Cotes: Win={bookmaker_odds['win']}, Draw={bookmaker_odds['draw']}, Loss={bookmaker_odds['loss']}):")
        betting_analysis = predictor.calculate_betting_value(result, bookmaker_odds)
        
        for outcome, data in betting_analysis['outcomes'].items():
            if data['bet']:
                print(f"   ✅ {outcome.upper()}: Parier {data['kelly_stake']*100:.2f}% du bankroll")
                print(f"      EV: {data['expected_value']*100:.2f}% | Edge: {data['edge']*100:.2f}%")
            else:
                print(f"   ❌ {outcome.upper()}: Pas de valeur (EV: {data['expected_value']*100:.2f}%)")
        
        if betting_analysis['best_bet']:
            print(f"\n🎲 Meilleur pari: {betting_analysis['best_bet'].upper()}")
        else:
            print(f"\n⚠️ Aucun pari recommandé")
