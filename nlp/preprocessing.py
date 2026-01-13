import spacy

nlp = spacy.load("fr_core_news_sm")

def nettoyer_texte(texte):
    """
    Nettoie un texte français :
    - minuscules
    - suppression ponctuation
    - suppression stop words
    - lemmatisation
    """
    doc = nlp(texte.lower())

    tokens_utiles = []

    for token in doc:
        if token.is_stop:
            continue
        if token.is_punct:
            continue
        if token.is_space:
            continue

        tokens_utiles.append(token.lemma_)

    return " ".join(tokens_utiles)
