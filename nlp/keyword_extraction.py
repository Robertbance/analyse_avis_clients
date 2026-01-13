from sklearn.feature_extraction.text import TfidfVectorizer

def extraire_mots_cles(textes, top_n=5):
    """
    textes : liste de textes nettoyés
    top_n : nombre de mots-clés à extraire
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textes)

    mots = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    mots_scores = list(zip(mots, scores))
    mots_scores = sorted(mots_scores, key=lambda x: x[1], reverse=True)

    mots_cles = [mot for mot, score in mots_scores[:top_n]]
    return mots_cles
