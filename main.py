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

    # in the word data, find pairs of words that differ by only one phoneme. For example, the words "so" and "su" differ
    # by only one phoneme. The same applies to the words "koko" and "kolo". The words "koko" and "kolo" would thus be
    # considered a pair.
    # For each pair, find the phoneme that is different between the two words. In the case of "koko" and "kolo", the
    # phoneme that is different is "k". The phoneme "k" is thus the phoneme in question. Build a dictionary with the
    # phonemes as keys and the pairs as values. The phoneme that is different is a new key for a dictionary in which
    # the pair is stored as a list item. For instance, the pair "koko" and "kolo" would result in the following entry
    # for "k": {"k": {"l": ["koko", "kolo"]}}. The pair "so" and "su" would result in the following entry for "u":
    # {"u": {"o": ["so", "su"]}}. The pair "musomani" and "musomanu" would result in the following entry for "i":
    # {"i": {"u": ["musomani", "musomanu"]}}.
    pairs = {}
    for word in words:
        for other_word in words:
            if word != other_word:
                if len(word) == len(other_word):
                    different_phonemes = 0
                    for i in range(len(word)):
                        if word[i] != other_word[i]:
                            different_phonemes += 1
                    if different_phonemes == 1:
                        for i in range(len(word)):
                            if word[i] != other_word[i]:
                                if word[i] not in pairs.keys():
                                    pairs[word[i]] = {}
                                if other_word[i] not in pairs[word[i]].keys():
                                    pairs[word[i]][other_word[i]] = []
                                pairs[word[i]][other_word[i]].append(word)
                                pairs[word[i]][other_word[i]].append(other_word)

    for key in pairs.keys():
        for other_key in pairs[key].keys():
            pairs[key][other_key] = list(set(pairs[key][other_key]))

    for phoneme in pairs:
        print(phoneme, pairs[phoneme])

    # Write an xlsx file with a matrix of all possible pairs. The matrix should have the phonemes as column headers and
    # row headers.

    workbook = xlsxwriter.Workbook("pairs.xlsx")
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    for key in pairs.keys():
        worksheet.write(row, col, key)
        row += 1

    row = 0
    col = 1
    for key in pairs.keys():
        worksheet.write(row, col, key)
        col += 1

    # now we have a matrix with the phonemes as column headers and row headers. We need to fill in the matrix with the
    # pairs. For each pair, we need to find the column and row header that corresponds to the phoneme that is different
    # between the two words.
    for index, key in enumerate(pairs.keys()):
        for other_index, other_key in enumerate(pairs.keys()):
            if other_key in pairs[key].keys():
                worksheet.write(index + 1, other_index + 1, ", ".join(pairs[key][other_key]))

    workbook.close()

    # save the sheet to the desktop, overwrite if it already exists
    if os.path.exists(desktop + "/pairs.xlsx"):
        os.remove(desktop + "/pairs.xlsx")
    shutil.move("pairs.xlsx", desktop + "/pairs.xlsx")


calculate_combinations()
