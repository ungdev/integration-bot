import re
import unicodedata


def slugify(text):
    # Supprimer les accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Mettre en minuscules, remplacer les espaces et retirer les caractères non autorisés
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s]+', '-', text)