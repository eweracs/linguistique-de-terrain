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

    # for each letter, collect all existing combinations. Each list entry needs to consist of the phoneme, the phoneme
    # that precedes it and which phoneme supersedes it, as well as the word in which this combination was found. The
    # phoneme in question is marked with an underscore. Make a dictionary with the letters as keys and the combinations
    # as values. So, for example, for the word "etɔgɔ", I would expect an entry like this: {"t": ["e_ɔ", "etetɔgɔ"]]}.
    # When a different word contains t, like the word "ajehakɛto", I expect the entry for "t" to be updated to include
    # the new combination: {"t": ["e_ɔ", "etetɔgɔ", "ɛ_o", "ajehakɛto"]}. When a phoneme is the first letter of a word,
    # the preceding phoneme is an empty string, which is marked with "#". When a phoneme is the last letter of a word,
    # the superseding phoneme is likewise an empty string, which is marked with "#". The word "teɾimuso" would thus
    # result in the following entry for "t": {"t": ["#_e", "teɾimuso"]}. Don't forget that a word can also be just one
    # letter long, like the word "a". In this case, the preceding and superseding phonemes are both empty strings.
    # The underscore is used to separate the preceding and superseding phonemes from the phoneme in question. The
    # underscore thus marks the phoneme in question. The word "a" would thus result in the following entry for "a":
    # {"a": ["#_#"]}. The word "ãu" would result in the following entry for "ã": {"ã": ["#_u", "ãu"]}. The word "ana"
    # would result in the following entry for "a": {"a": ["#_n", "ana"], ["n_#", "ana"}. The word "auana" would result
    # in the following entry for "a": {"a": ["#_u", "auana"], ["u_n", "auana"], ["n_#", "auana"]}.
    # The word "musomani" would result in the following entry for "m": {"m": ["#_u", "musomani"], ["o_a", "musomani"]}

    combinations_dictionary = {}
    for letter in letters:
        for word in words:
            if letter in word:
                if letter not in combinations_dictionary.keys():
                    combinations_dictionary[letter] = []
                if word.index(letter) == 0:
                    if word.index(letter) < len(word) - 1:
                        if word[word.index(letter) + 1] in combining_characters:
                            combinations_dictionary[letter].append(
                                ["#_" + word[word.index(letter) + 1], word])
                        else:
                            combinations_dictionary[letter].append(["#_" + word[word.index(letter) + 1], word])
                    else:
                        combinations_dictionary[letter].append(["#_#", word])

    # print(combinations_dictionary)

    # transform the combinations into an xlsx file.
    import xlsxwriter
    workbook = xlsxwriter.Workbook("combinations.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for key in combinations_dictionary.keys():
        worksheet.write(row, col, key)
        for item in combinations_dictionary[key]:
            worksheet.write(row, col + 1, item[0])
            worksheet.write(row, col + 2, item[1])
            row += 1
    workbook.close()

    # save the sheet to the desktop, overwrite if it already exists
    import os
    import shutil
    desktop = "/Users/sebastiancarewe/Desktop"
    if os.path.exists(desktop + "/combinations.xlsx"):
        os.remove(desktop + "/combinations.xlsx")
    shutil.move("combinations.xlsx", desktop + "/combinations.xlsx")


calculate_combinations()
