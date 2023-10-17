from data import words


def calculate_combinations():
    # collect all existing letters in the words
    # if a letter is followed by the "ː" character. So aː would be considered one single letter. The same applies to
    # the "̃" character.
    combining_characters = ["ː", "̃", "̆"]
    letters = []
    for word in words:
        for letter in word:
            if word.index(letter) < len(word) - 1:
                if word[word.index(letter) + 1] in combining_characters:
                    if letter + word[word.index(letter) + 1] not in letters:
                        letters.append(letter + word[word.index(letter) + 1])
                elif letter not in letters and letter not in combining_characters:
                    letters.append(letter)

    print(letters)

    # for each letter, collect all existing combinations: which letter can precede it, which can follow it,
    # based on the words. If the letter after the current letter is a combining character, it is ignored.
    combinations = {}
    for letter in letters:
        combinations[letter] = {"before": [], "after": []}
        for word in words:
            if letter in word:
                if word.index(letter) > 0:
                    if word[word.index(letter) - 1] not in combinations[letter]["before"]:
                        combinations[letter]["before"].append(word[word.index(letter) - 1])
                if word.index(letter) < len(word) - 1:
                    if word[word.index(letter) + 1] not in combining_characters:
                        if word[word.index(letter) + 1] not in combinations[letter]["after"]:
                            combinations[letter]["after"].append(word[word.index(letter) + 1])

    # transform the combinations into an xlsx file.
    # For each letter, create a sheet with the letters that can precede it and the letters that can follow it
    import xlsxwriter
    workbook = xlsxwriter.Workbook('combinations.xlsx')
    for letter in combinations:
        worksheet = workbook.add_worksheet(letter)
        worksheet.write(0, 0, "Before")
        worksheet.write(0, 1, "After")
        worksheet.write_column(1, 0, combinations[letter]["before"])
        worksheet.write_column(1, 1, combinations[letter]["after"])
    workbook.close()

    # save the sheet to the desktop, overwrite if it already exists
    import os
    import shutil
    desktop = "/Users/sebastiancarewe/Desktop"
    if os.path.exists(desktop + "/combinations.xlsx"):
        os.remove(desktop + "/combinations.xlsx")
    shutil.move("combinations.xlsx", desktop + "/combinations.xlsx")


calculate_combinations()
