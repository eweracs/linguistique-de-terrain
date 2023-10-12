# This is a sample Python script.
import numpy

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

words = [
    "maħamadu",
    "initʃe",
    "ikakɛnɛ",
    "netɔgɔ",
    "musomani",
    "nedẽmuso",
    "musomanju",
    "ãu",
    "ã",
    "i",
    "e",
    "etɔgɔ",
    "muso",
    "musow",
    "walãba",
    "walãni",
    "tʃɛmãni",
    "nedeʧɛ",
    "tʃɛmãnju",
    "tʃɛ",
    "namasa",
    "pɔmu",
    "mɔbili",
    "ala",
    "ɲɛnamaja",
    "dunja",
    "dʒi",
    "aɾidʒinɛ",
    "hakɛto",
    "teɾi",
    "teɾimuso",
    "teɾitʃɛ",
    "teɾtʃɛw",
    "teɾimusou",
    "finiti",
    "musomanifiniti",
    "faː",
    "fa",
    "so",
    "so",
    "kulu",
    "jiɾi",
    "dʒiɾi",
    "sã",
    "sã",
    "balemakɛ",
    "balematʃe",
    "kaadũ",
    "taːma",
    "tagama",
    "bagã",
    "dō",
    "plaʒida",
    "mɔkɛ",
    "fini",
    "fini",
    "finju",
    "su",
    "su",
    "su",
    "suu",
    "bagãu",
    "ba",
    "mɔmuso",
    "kasunɔgɔ",
    "ziɾi",
    "bamuso",
    "faʧɛ",
    "fakɛ",
    "inisoɣoma",
    "inisogoma",
    "kalã",
    "nekafinju",
    "sodẽ",
    "dʒiɾi",
    "jiɾi",
    "kaboli",
    "kaːkalã",
    "ekafinju",
    "sɛbẽnikɛ̃lã",
    "kãlimu",
    "koko",
    "gabugu",
    "ɲɛ̃naʤɛ",
    "ɲinɛ",
    "kɔnɔ",
    "so",
    "nekapɔmu",
    "nekapɔmu",
    "kalãso",
    "mpalã",
    "nekampalãw",
    "nekampalã",
    "ajehakɛto",
    "a",
    "a",
    "da",
    "ko",
    "sãnakalãso",
    "sãnakalãsow",
    "sã",
    "kakɛafɛ",
    "kakɛkalãfɛ",
    "mbɛndɔgɔnife",
    "sɛbɛ̃fŭɾa",
    "ʤiɾibulu",
    "kɔɾɔmuso",
    "ʤifile",
    "kuluː",
    "ɲɛda",
    "ɲɛkɛnɛ",
    "sãnakalãsokadineje",
    "sãnakalãkadineje",
    "nekɔɾɔmusow",
    "ɑ̃kafinju",
    "mɔʧɛ",
    "kalãdẽkagafe",
    "dʒiflẽw",
    "mbɛpatidũ",
    "gafe",
    "gafew",
    "bilemã",
    "mbɛnipɔmudu"
]


def calculate_combinations():
    # collect all existing letters in the words
    # if a letter is followed by the "ː" character. So aː would be considered one single letter. The same applies to the "̃" character.
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
    # based on the words. If a letter before is one of the combining characters, then it is considered as part of the
    # letter. So the letter before will also be taken into account.
    combinations = {}
    for letter in letters:
        combinations[letter] = {"before": [], "after": []}
        for word in words:
            if letter in word:
                if word.index(letter) > 0:
                    if word[word.index(letter) - 1] in combining_characters:
                        combinations[letter]["before"].append(word[word.index(letter) - 2] + word[word.index(letter) - 1])
                    else:
                        combinations[letter]["before"].append(word[word.index(letter) - 1])
                if word.index(letter) < len(word) - 1:
                    if word[word.index(letter) + 1] in combining_characters:
                        combinations[letter]["after"].append(word[word.index(letter) + 1] + word[word.index(letter) + 2])
                    else:
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