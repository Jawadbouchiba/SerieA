# 🚀 DÉMARRER LE PROJET - INTERFACE WEB

## ✨ **UNE SEULE COMMANDE POUR TOUT LANCER :**

```bash
cd /Users/jawadbouchiba/SerieA && source .venv/bin/activate && python3 app.py
```

Cela lancera une **interface web** sur **http://localhost:7860** avec :

1. 🎯 **Prédiction de Match Unique** - Analysez un match avec tous les détails de paris
2. 📊 **Matchs Multiples** - Analysez plusieurs matchs en lot
3. 📈 **Statistiques d'Équipe** - Consultez les stats détaillées des équipes

---

## 📝 **Étape par Étape :**

### 1. Ouvrir le Terminal

### 2. Exécuter cette Commande :
```bash
cd /Users/jawadbouchiba/SerieA
source .venv/bin/activate
python3 app.py
```

### 3. Ouvrir le Navigateur
Aller sur : **http://localhost:7860**

### 4. Utiliser l'Interface
- Choisissez un onglet (Match Unique, Matchs Multiples, ou Stats d'Équipe)
- Entrez les équipes et les cotes
- Cliquez sur le bouton pour obtenir les prédictions !

---

## 🎯 **Comment Utiliser Chaque Onglet :**

### Onglet 1 : Match Unique 🎯
1. Sélectionnez l'Équipe à Domicile et l'Équipe Visiteuse dans les listes déroulantes
2. Choisissez le Lieu (Domicile/Extérieur)
3. Entrez les cotes du bookmaker (format décimal comme 2.10, 3.40, 3.50)
4. Définissez votre bankroll
5. Cliquez sur "🔮 Prédire"
6. Obtenez une analyse complète avec recommandation de pari !

### Onglet 2 : Matchs Multiples 📊
1. Entrez les matchs, un par ligne, dans ce format :
   ```
   Juventus, Milan, Home, 2.10, 3.40, 3.50
   Inter, Napoli, Home, 1.85, 3.60, 4.20
   Roma, Lazio, Away, 2.50, 3.20, 2.90
   ```
2. Définissez votre bankroll
3. Cliquez sur "🔮 Analyser Tout"
4. Obtenez des recommandations en lot avec la mise totale !

### Onglet 3 : Stats d'Équipe 📈
1. Sélectionnez n'importe quelle équipe dans la liste déroulante
2. Cliquez sur "📊 Analyser"
3. Consultez les statistiques détaillées et les évaluations !

---

## 🛑 **Pour Arrêter le Serveur :**

Appuyez sur `Ctrl+C` dans le terminal

---

## 📱 **Accès depuis un Téléphone/Autre Appareil :**

Si vous souhaitez y accéder depuis un autre appareil sur le même réseau :

```bash
# Lancer avec le partage activé
cd /Users/jawadbouchiba/SerieA
source .venv/bin/activate
python3 -c "
import gradio as gr
from app import app
app.launch(server_name='0.0.0.0', server_port=7860, share=True)
"
```

Cela vous donne une URL publique accessible depuis n'importe où !

---

## ✅ **Ce que Vous Obtenez :**

✅ Belle interface web  
✅ Les 3 modes de prédiction en un seul endroit  
✅ Listes déroulantes interactives pour les équipes  
✅ Recommandations de paris automatiques  
✅ Calcul de mise selon le Critère de Kelly  
✅ Analyse de la valeur espérée  
✅ Score de confiance  
✅ Pas de ligne de commande nécessaire - juste des clics !  

---

## 🆘 **Dépannage :**

### Port déjà utilisé ?
```bash
# Utiliser un port différent
python3 app.py --server-port 7861
```

### Module introuvable ?
```bash
source .venv/bin/activate  # Ne pas oublier cette étape !
pip install gradio
```

### Impossible d'accéder depuis le navigateur ?
- Vérifiez que vous voyez "Running on http://localhost:7860"
- Essayez http://127.0.0.1:7860 à la place
- Vérifiez les paramètres du pare-feu

---

## 🎓 **Conseils Pro :**

1. **Mettez la page en favori** (http://localhost:7860) pour un accès rapide
2. **Gardez le terminal ouvert** pendant l'utilisation du site
3. **Plusieurs prédictions à la fois** - Utilisez l'onglet "Matchs Multiples"
4. **Comparer les équipes** - Utilisez l'onglet "Stats d'Équipe" avant de parier
5. **Sauvegarder les résultats** - Copiez-collez l'analyse dans vos notes

---

## 📚 **Exemple de Flux de Travail :**

1. **Matin :** Lancer le serveur web
   ```bash
   cd /Users/jawadbouchiba/SerieA && source .venv/bin/activate && python3 app.py
   ```

2. **Consulter les matchs du jour :** Utiliser l'onglet "Matchs Multiples" avec les cotes du jour

3. **Analyse approfondie :** Utiliser "Match Unique" pour une analyse détaillée des matchs prometteurs

4. **Recherche sur les équipes :** Utiliser "Stats d'Équipe" avant de décider

5. **Placer les paris :** Suivre les recommandations (commencez avec de petites mises !)

6. **Soir :** Arrêter le serveur avec Ctrl+C

---

## 🎉 **Vous Êtes Prêt !**

Exécutez simplement :
```bash
cd /Users/jawadbouchiba/SerieA && source .venv/bin/activate && python3 app.py
```

Puis ouvrez **http://localhost:7860** dans votre navigateur !

**Bonne chance ! 🍀⚽**
