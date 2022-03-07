from spellchecker import SpellChecker
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import np



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
    # cleaned_instructions = instructions.apply(
    #     lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    # cleaned_instructions = cleaned_instructions.apply(lambda s: s.lower())
    # cleaned_instructions = cleaned_instructions.apply(
    #     lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # clean ingredients #
    # punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^_`{|}~/"
    # cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    # cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    # cleaned_ingredients = cleaned_ingredients.apply(
    #     lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))
    # make new csv dataset #
    cleaned_csv_data = {"id": id, "Title": cleaned_title, "Instructions": instructions,
                        "Image_Name": image_name, "Ingredients": ingredients, "cleaned_ingredients": "" }
    dataFrame = pd.DataFrame(data=cleaned_csv_data)

    cleaned_ingredients = cleaned_ingredient_for_suggestion(dataFrame)
    for i, row in cleaned_ingredients.iterrows():
        dataFrame.at[i, 'cleaned_ingredients'] = cleaned_ingredients.at[i, 'Ingredients_clean']

    print(dataFrame)

    try:
        print("data cleaned!")
        return dataFrame
    except:
        print("Error")

def exampleoutput(dataFrame):
    print("create example output...")
    data = dataFrame
    tempJson = []
    for i in range(8):
    #   data.at[i, 'Image_Name'] = data.at[i, 'Image_Name'] + ".jpg"
    #   tempJson.append([[data.at[i, 'id']],[data.at[i, 'Title']],[data.at[i, 'Image_Name']]])
        tempJson.append({"id": data.at[i, 'id'],
                         "Title": data.at[i, 'Title'],
                         "Image_Name": data.at[i, 'Image_Name']})

    print('success create json example')
    return tempJson
    # df = pd.DataFrame(tempJson, columns=["no","artist","songname","lyric"])

def searchtfidf(inputword,df_new,where):
    print("TF-IDF is running...")
    df = df_new
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(df[where].values.astype('U'))
    print(X.shape)
    query = inputword
    query_vec = vectorizer.transform([query])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    tfidfJson = []
    for i in results.argsort()[::-1]:
        if results[i] > 0:
            tfidfJson.append({"id": df_new.iloc[i, 0],
                             "foodTitle": df_new.iloc[i, 1],
                             "foodPicture": df_new.iloc[i, 3]})
    return tfidfJson

def favoritesearchtfidf(inputword,df_new):
    print("TF-IDF is running...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(df_new['foodTitle'])
    print(X.shape)
    query = inputword
    query_vec = vectorizer.transform([query])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    tfidfJson = []
    for i in results.argsort()[::-1]:
        print(results[i])
        if results[i] > 0:
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
    # text = fooddetails[0]["Ingredients"]
    # text = wordsuggestion(text)
    # fooddetails[0]["Ingredients"] = text
    # text = fooddetails[0]["Instructions"]
    # text = wordsuggestion(text)
    # fooddetails[0]["Instructions"] = text
    # print(fooddetails[0])
    return fooddetails[0]

def currentpage(currentpage, allpage):
    previouspage = True
    nextpage = True
    if currentpage-1 >= 0:
        previouspage = True
    else:
        previouspage = False
    if currentpage+1 < allpage:
        nextpage = True
    else:
        nextpage = False
    return [{'previouspage': previouspage,'nextpage': nextpage}]

def pagination(datainput,page):
    page = page-1
    dataperpage = 12
    result = len(datainput)
    data = []
    point = 0
    if result/dataperpage <= 1:
        data.append(datainput)
        return data
    else:
        pagenumber = result//dataperpage
        print('have: ',pagenumber,' page')
        for i in range(pagenumber+1):
            if point < result:
                datatemp = []
                for j in range(dataperpage):
                    if point < result:
                        datatemp.append(datainput[point])
                        point = point+1
                data.append(datatemp)
        print(data[page])
        return data
    # dict(zip(datainpage,))
    #         for j in range(dataperpage):
    #             if data[dataat]:
    #                 datainpage[i].append({"data": data[dataat]})
    #                 dataat = dataat+1
    # print(datainpage[15])
    # print(datainpage[page-1])
    # return datainpage[page]


def cleaned_ingredient_for_suggestion(data):
    data = data
    data = data.replace('#NAME?', np.nan)
    data = data.dropna()

    # clean ingredients #
    ingredients = data['Ingredients'].astype(str)
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    cleaned_ingredients = {"Ingredients_clean": cleaned_ingredients}
    dataFrame = pd.DataFrame(data=cleaned_ingredients)

    for i, row in dataFrame.iterrows():
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('sliced', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('tsp.', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('divided', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('Tbsp.', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('cups', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('cup', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('pounds', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('pound', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('teaspoons', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('teaspoon', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('tablespoons', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('tablespoon', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('tsp', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('lb', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('oz', '')

        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('½', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('¾', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('⅓', '')
        dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace('¼', '')


        for digit in dataFrame.at[i, 'Ingredients_clean']:
            if digit.isdigit():
                dataFrame.at[i, 'Ingredients_clean'] = dataFrame.at[i, 'Ingredients_clean'].replace(digit, '')

    dataFrame["Ingredients_clean"] = dataFrame["Ingredients_clean"].str.replace('[^\w\s]','')
    dataFrame["Ingredients_clean"] = dataFrame["Ingredients_clean"].str.replace('  ',' ')
    dataFrame["Ingredients_clean"] = dataFrame["Ingredients_clean"].str.replace('   ',' ')




    return dataFrame
