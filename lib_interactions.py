import nltk
import docx
import json
import copy
import spacy
from nltk.corpus import stopwords
from nltk.parse.malt import MaltParser


UNSHIPHER = {
    "CC": "союз",
    "CD": "кардинальное число",
    "DT": "определитель",
    "EX": 'существование там',
    "FW": "иностранное слово",
    "IN": "предлог/подчинительный союз",
    "JJ": 'прилагательное',
    "VP": "глагольная группа",
    "JJR": 'прилагательное, сравнительная степень',
    "JJS": 'прилагательное, превосходная степень',
    "LS": "маркер списка  1)",
    "MD": "модальный глагол сосотавное сказуемое",
    "NN": 'существительное, единственное число',
    "NNS": 'существительное, множественное число',
    "PP": "предложная группа",
    "NNP": 'имя собственное, единственное число',
    "NNPS": 'имя собственное, множественное число',
    "PDT": 'предопределитель',
    "POS": "притяжательное окончание",
    "PRP": "личное местоимение, ",
    "PRP$": "притяжательное местоимение",
    "RB": "наречие",
    "RBR": "наречие, сравнительная степень",
    "RBS": "наречие, превосходная степень",
    "RP": "частица",
    "S": "Простое повествовательное предложение",
    "SBAR": "Предложение, введенное (возможно пустым) подчинительным союзом",
    "SBARQ": "Прямой вопрос, введенный вопросительным словом или вопросительной группой",
    "SINV": "Инвертированное повествовательное предложение, т.е. такое, в котором подлежащее следует за глаголом в прошедшем времени или модальным глаголом.",
    "SQ": "Инвертированный вопрос да/нет, или главное предложение вопроса, следующее за вопросительной группой в SBARQ",
    "SYM": "Символ",
    "VBD": "глагол, прошедшее время",
    "VBG": "глагол, герундий/презенс-партицип  берущий",
    "VBN": "глагол, прошедшее причастие  взятый",
    "VBP": "глагол, настоящее время, ед. число, не 3-е лицо  беру",
    "VBZ": "глагол, настоящее время, 3-е лицо, ед. число  берет",
    "WDT": "вопросительный определитель. Обстоятельство",
    "WP": "вопросительное местоимение. Обстоятельство",
    "WP$": "притяжательное вопросительное местоимение чей, ",
    "WRB": "вопросительное наречие",
    "TO": 'to  идти "в" магазин.',
    "UH": "междометие",
    "VB": "глагол, исходная форма",
}


signs = "!~@#$%^&*()_+<>?:.,;[]\\|'\"\'–«"


def load_file(path: str) -> list:
    opened_file = open(path, "rb")
    if '.doc' in path:
        current_file = docx.Document(opened_file)
        list_of_rows = [row.text for row in current_file.paragraphs]
        opened_file.close()
        raw_data = ""
        for row in list_of_rows:
            raw_data += row
    elif '.txt' in path:
        raw_data = ''
        for raw in opened_file:
            raw_data += raw
    else:
        raw_data = None
    return raw_data


def process_text(raw_data):
    nlp = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words("english"))
    for sign in signs:
        stop_words.add(sign)
    word_tokens = nltk.tokenize.word_tokenize(raw_data)
    tagged_word_tokens = nltk.pos_tag(word_tokens)
    sentences = nltk.sent_tokenize(raw_data)
    sentences = [nltk.tokenize.word_tokenize(
        sentence) for sentence in sentences]
    # sentences = [[word for word in sentence if word.lower() not in stop_words]
    #             for sentence in sentences]
    for sentence in range(len(sentences)):
        temp_sent = ''
        for word in sentences[sentence]:
            temp_sent += word + ' '
        sentences[sentence] = temp_sent
    tagged_sentences = [nlp(sentence)
                        for sentence in sentences]

    final_table = []
    for token in tagged_word_tokens:
        if token[0].lower() not in stop_words:
            final_table.append(token)
    for token in range(len(final_table)):
        buffer = final_table[token][0]
        final_table[token] = (buffer, UNSHIPHER.get(final_table[token][1]))
    synt_collection = dict()
    for sentence in tagged_sentences:
        struct_of_sentence = []
        podl_index = 0
        scaz_index = 0
        for token in sentence:
            struct_of_sentence.append({token.pos_})
        switch = False
        for index in range(len(struct_of_sentence)):
            if (struct_of_sentence[index] == {'NOUN'} or struct_of_sentence[index] == {'PROPN'} or struct_of_sentence[index] == {'PRON'}):
                for sub_index in range(index+1, len(struct_of_sentence)):
                    if (struct_of_sentence[sub_index] == {'NOUN'} or struct_of_sentence[sub_index] == {'PROPN'}):
                        break
                    if (struct_of_sentence[sub_index] == {'VERB'}):
                        podl_index = index
                        scaz_index = sub_index
                        struct_of_sentence[podl_index] = " ,Подлежащее"
                        for change_index in range(index+1, scaz_index+1):
                            struct_of_sentence[change_index] = " ,Сказуемое"
                        switch = True
                        break
            if switch:
                break
        for index in range(0, index):
            struct_of_sentence[index] = ' ,Обстоятельство времени или места'
        changer = ' ,Дополнение'
        for index in range(scaz_index+1, len(sentence)):
            if (struct_of_sentence[index] != {'NOUN'}) or (struct_of_sentence[index] != {'PROPN'}):
                changer = ' ,Обстоятельство'
            struct_of_sentence[index] = changer
        for entry in range(len(struct_of_sentence)):
            if sentence[entry].text.lower() not in stop_words:
                synt_collection[str(sentence[entry])
                                ] = struct_of_sentence[entry]
    print(len(synt_collection), len(final_table))
    for index in range(len(final_table)):
        if synt_collection.get(final_table[index][0]):
            final_table[index] = (final_table[index][0], str(final_table[index]
                                  [1] + synt_collection.get(final_table[index][0])))
    final_table = set(final_table)
    final_table = list(final_table)
    return final_table


def save_file(text: list, name: str):
    document = docx.Document()
    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "id"
    hdr_cells[1].text = "word"
    hdr_cells[2].text = "description"
    for id, word, description in text:
        if not description:
            continue
        row_cells = table.add_row().cells
        row_cells[0].text = str(id)
        row_cells[1].text = word
        row_cells[2].text = description

    document.add_page_break()

    document.save(name + ".docx")
