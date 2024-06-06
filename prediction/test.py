import pickle
import matplotlib.pyplot as plt

# Charger le fichier history_0.pkl
with open('old_model_2/history_3.pkl', 'rb') as f:
    history = pickle.load(f)

# Afficher les clés disponibles dans l'historique
print(history.keys())

# Extraire les données d'historique
loss = history['loss']
# Ajouter d'autres métriques si elles sont disponibles dans votre fichier history_0.pkl

# Extraire les données d'historique
val_loss = history['val_loss']

# Plot
plt.plot(loss, label='Perte (loss)')
plt.plot(val_loss, label='Perte (val_loss)')
# Ajouter d'autres métriques si elles sont disponibles dans votre fichier history_0.pkl

plt.xlabel('Epochs')
plt.ylabel('Valeurs')
plt.title('Évolution de la perte (loss) au cours des epochs')
plt.legend()
plt.show()
