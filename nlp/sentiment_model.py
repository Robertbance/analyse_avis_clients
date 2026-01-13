from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

def preparer_donnees(textes, labels):
    """
    textes : liste de textes nettoyés
    labels : liste des sentiments
    """
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(textes).toarray()

    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    return X, y, vectorizer, encoder

textes = [
    "service rapide professionnel",
    "livraison lente mauvais"
]

labels = ["positif", "négatif"]

X, y, vectorizer, encoder = preparer_donnees(textes, labels)

print(X.shape)  # données numériques
print(y)        # labels encodés
