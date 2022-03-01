import string
import pandas as pd



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
    punctuation = "!\"#$%&'()*+,-.:;<=>?@[\]^_`{|}~/or"
    cleaned_ingredients = ingredients.apply(lambda s: s.translate(str.maketrans('', '', punctuation + u'\xa0')))
    cleaned_ingredients = cleaned_ingredients.apply(lambda s: s.lower())
    cleaned_ingredients = cleaned_ingredients.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    # make new csv dataset #
    cleaned_csv_data = {"id": id, "Title": cleaned_title, "Instructions": cleaned_instructions,
                        "Image_Name": image_name, "Ingredients": cleaned_ingredients}
    dataFrame = pd.DataFrame(data=cleaned_csv_data)

    try:
        dataFrame.to_csv("src/resource/Food Recipe.csv", encoding="utf8", index=False)
        print("Generate new csv")
    except:
        print("Error")


