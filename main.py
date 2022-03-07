import string
import nltk
import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_and_clean_data():
    data = pd.read_csv('src/resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    data = data.replace('#NAME?', np.nan)
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
    punctuation = "!\"#$%&()*+-:;<=>?@[]^_`{|}~"
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.replace('\', \'', ','))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.replace('tsp.', 'tsp.'))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.replace('tbsp.', 'tsp.'))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.replace('Tbsp.', 'tsp.'))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.replace('teaspoon', 'tsp.'))




    punctuation2 = "\'"
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation2 + u'\xa0')))

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


def tfidf_scoring_by_title():

    csv_file = "src/resource/Food Recipe.csv"
    data = pd.read_csv(csv_file)
    all_data = pd.DataFrame(data, columns=['Title', 'Instructions', 'Image_Name', 'Ingredients'])

    # Tf idf scoring #
    query = input("Enter food title: ")

    tfidf_data_ranking = []
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_data['Title'].apply(lambda x: np.str_(x)))
    query_vectorizer = vectorizer.transform([query])
    results = cosine_similarity(X, query_vectorizer).reshape((-1,))
    rank = 0
    for i in results.argsort()[-10:][::-1]:
        rank = rank + 1
        tfidf_data_ranking.append({
            "Rank": rank,
            "Title": all_data.iloc[i, 0],
            "Instructions": all_data.iloc[i, 1],
            "Image": all_data.iloc[i, 2] + ".jpg",
            "Ingredient": all_data.iloc[i, 3],
            "Score": results[i]
            }
        )

    return tfidf_data_ranking

def tfidf_scoring_by_ingredients():

    csv_file = "src/resource/Food Recipe.csv"
    data = pd.read_csv(csv_file)
    all_data = pd.DataFrame(data, columns=['Title', 'Image_Name', 'Ingredients'])

    # Tf idf scoring #
    query = input("Enter food ingredients: ")

    tfidf_data_ranking = []
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_data['Ingredients'].apply(lambda x: np.str_(x)))
    query_vectorizer = vectorizer.transform([query])
    results = cosine_similarity(X, query_vectorizer).reshape((-1,))
    rank = 0
    for i in results.argsort()[-10:][::-1]:
        rank = rank + 1
        tfidf_data_ranking.append({
            "Rank": rank,
            "Title": all_data.iloc[i, 0],
            "Image": all_data.iloc[i, 1] + ".jpg",
            "Ingredient": all_data.iloc[i, 2],
            "Score": results[i]
            }
        )

    return tfidf_data_ranking


def cleaned_ingredient_for_suggestion():
    data = pd.read_csv('src/resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    data = data.replace('#NAME?', np.nan)
    data = data.dropna()

    # clean ingredients #
    ingredients = data['Cleaned_Ingredients'].astype(str)
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    cleaned_ingredients = {"Ingredients": cleaned_ingredients}
    dataFrame = pd.DataFrame(data=cleaned_ingredients)

    for i, row in dataFrame.iterrows():
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('tsp', '')
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('lb', '')
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('oz', '')

        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('½', '')
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('¾', '')
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('⅓', '')
        dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace('¼', '')


        for digit in dataFrame.at[i, 'Ingredients']:
            if digit.isdigit():
                dataFrame.at[i, 'Ingredients'] = dataFrame.at[i, 'Ingredients'].replace(digit, '')

    dataFrame["Ingredients"] = dataFrame["Ingredients"].str.replace('[^\w\s]','')
    dataFrame["Ingredients"] = dataFrame["Ingredients"].str.replace('  ',' ')
    dataFrame["Ingredients"] = dataFrame["Ingredients"].str.replace('   ',' ')


    print(dataFrame.head(5).to_markdown())

    return dataFrame

def pagination(data,page):
    dataperpage = 12
    result = len(data)
    datainpage = []
    dataat = 0
    if result/dataperpage <= 1:
        return
    else:
        pagenumber = result/dataperpage
        for i in pagenumber:
            for j in dataperpage:
                if data[dataat]:
                    datainpage[i].append(data[dataat])
                    dataat = dataat+1
    return datainpage[page]