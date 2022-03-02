import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_and_clean_data():
    data = pd.read_csv('src/resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    data = data.dropna()

    title = data['Title'].astype(str)
    image_name = data['Image_Name'].astype(str)

    # clean title #
    cleaned_title = title.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_title = cleaned_title.apply(lambda s: s.lower())
    cleaned_title = cleaned_title.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # clean instructions #
    instructions = data['Instructions'].astype(str)
    punctuation = "!\"#$%&'*+,-:<=>?@[]^_`{|}~"
    cleaned_instructions = instructions.apply(
        lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    cleaned_instructions = cleaned_instructions.apply(lambda s: s.lower())
    cleaned_instructions = cleaned_instructions.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # clean ingredients #
    ingredients = data['Cleaned_Ingredients'].astype(str)
    punctuation = "!\"#$%&'()*+,-:;<=>?@[]^_`{|}~"
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # make new csv dataset #
    cleaned_csv_data = {"Title": cleaned_title, "Instructions": cleaned_instructions,
                        "Image_Name": image_name, "Ingredients": cleaned_ingredients}
    dataFrame = pd.DataFrame(data=cleaned_csv_data)
    dataFrame.dropna()
    dataFrame.reset_index(inplace=True)
    del dataFrame['index']
    try:
        dataFrame.to_csv("src/resource/Food Recipe.csv", encoding="utf8")
        print("Generate new csv")
    except:
        print("Error")


def tfidf_scoring():

    csv_file = "src/resource/Food Recipe.csv"
    data = pd.read_csv(csv_file)
    all_data = pd.DataFrame(data, columns=['Title', 'Image_Name', 'Ingredients'])
