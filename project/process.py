from spellchecker import SpellChecker
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re



def get_and_clean_data():
    data = pd.read_csv('src/resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')

    id = data['No']
    title = data['Title'].astype(str)
    ingredients = data['Cleaned_Ingredients'].astype(str)
    instructions = data['Instructions'].astype(str)
    image_name = data['Image_Name'].astype(str)

    # clean title #
    cleaned_title = title.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_title = cleaned_title.apply(lambda s: s.lower())
    cleaned_title = cleaned_title.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # clean instructions #
    cleaned_instructions = instructions.apply(
        lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_instructions = cleaned_instructions.apply(lambda s: s.lower())
    cleaned_instructions = cleaned_instructions.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # clean ingredients #
    punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^_`{|}~/"
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # make new csv dataset #
    cleaned_csv_data = {"id": id, "Title": cleaned_title, "Instructions": cleaned_instructions,
                        "Image_Name": image_name, "Ingredients": cleaned_ingredients}
    dataFrame = pd.DataFrame(data=cleaned_csv_data)
    findfooddetails(dataFrame, "apples and oranges")
    try:
        # dataFrame.to_csv("src/resource/Food Recipe.csv", encoding="utf8", index=False)
        print("data cleaned!")
        return dataFrame
    except:
        print("Error")

def exampleoutput(dataFrame):
    print("create example output...")
    data = dataFrame
    tempJson = []
    for i in range(10):
        data.at[i, 'Image_Name'] = data.at[i, 'Image_Name'] + ".jpg"
    #     tempJson.append([[data.at[i, 'id']],[data.at[i, 'Title']],[data.at[i, 'Image_Name']]])
        tempJson.append({"id": data.at[i, 'id'],
                         "Title": data.at[i, 'Title'],
                         "Image_Name": data.at[i, 'Image_Name']})

    print('success create json example')
    return tempJson
    # df = pd.DataFrame(tempJson, columns=["no","artist","songname","lyric"])

def favoritesearchtfidf(inputword,df_new):
    print("TF-IDF is running...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(df_new['foodTitle'])
    print(X.shape)
    query = inputword
    query_vec = vectorizer.transform([query])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    tfidfJson = []
    for i in results.argsort()[-10:][::-1]:
        print(results[i])
        tfidfJson.append({"id": df_new.iloc[i, 0],
                         "foodTitle": df_new.iloc[i, 1],
                         "foodPicture": df_new.iloc[i, 2]})
    return tfidfJson

def wordsuggestion(inputword):
    spell = SpellChecker()
    input = inputword.split()
    wordtemp = []
    for word in input:
        wordtemp.append(spell.correction(word))
    wordtemp=wordtemp
    wordtemp = ' '.join(wordtemp)
    if wordtemp == inputword:
        return inputword
    else:
        return wordtemp

def findfooddetails(dataframe, inputword):
    print("Search food details is running...")
    data = dataframe
    foodname = inputword
    print(foodname)
    fooddetails = []
    for i, row in data.iterrows():
        if data.at[i, 'Title'] == foodname:
            fooddetails.append({"Title" : data.at[i, 'Title'],
                                "Instructions": data.at[i, 'Instructions'],
                                "Ingredients": data.at[i, 'Ingredients'],
                                "Image_Name": data.at[i, 'Image_Name']})

    # fooddetails[0]["Ingredients"] = re.split(r"\.", fooddetails[0]["Ingredients"])
    text = fooddetails[0]["Ingredients"]
    text = wordsuggestion(text)
    fooddetails[0]["Ingredients"] = text
    text = fooddetails[0]["Instructions"]
    text = wordsuggestion(text)
    fooddetails[0]["Instructions"] = text
    # print(fooddetails[0])
    return fooddetails[0]