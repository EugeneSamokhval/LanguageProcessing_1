import nltk
import docx
import json
import copy
from nltk.corpus import stopwords


UNSHIPHER = {
    "CC": "союз",
    "CD": "кардинальное число",
    "DT": "определитель",
    "EX": 'существование там',
    "FW": "иностранное слово",
    "IN": "предлог/подчинительный союз",
    "JJ": 'прилагательное "большой"',
    "VP": "глагольная группа",
    "JJR": 'прилагательное, сравнительная степень "больше"',
    "JJS": 'прилагательное, превосходная степень "самый большой"',
    "LS": "маркер списка  1)",
    "MD": "модальный глагол  мог, будет",
    "NN": 'существительное, единственное число',
    "NNS": 'существительное, множественное число  "столы"',
    "PP": "предложная группа",
    "NNP": 'имя собственное, единственное число',
    "NNPS": 'имя собственное, множественное число',
    "PDT": 'предопределитель  "все дети"',
    "POS": "притяжательное окончание  родителя",
    "PRP": "личное местоимение  я, он, она",
    "PRP$": "притяжательное местоимение  мой, его, ее",
    "RB": "наречие  очень, тихо,",
    "RBR": "наречие, сравнительная степень  лучше",
    "RBS": "наречие, превосходная степень  лучший",
    "RP": "частица  сдаться",
    "S": "Простое повествовательное предложение",
    "SBAR": "Предложение, введенное (возможно пустым) подчинительным союзом",
    "SBARQ": "Прямой вопрос, введенный вопросительным словом или вопросительной группой.",
    "SINV": "Инвертированное повествовательное предложение, т.е. такое, в котором подлежащее следует за глаголом в прошедшем времени или модальным глаголом.",
    "SQ": "Инвертированный вопрос да/нет, или главное предложение вопроса, следующее за вопросительной группой в SBARQ.",
    "SYM": "Символ",
    "VBD": "глагол, прошедшее время  взял",
    "VBG": "глагол, герундий/презенс-партицип  берущий",
    "VBN": "глагол, прошедшее причастие  взятый",
    "VBP": "глагол, настоящее время, ед. число, не 3-е лицо  беру",
    "VBZ": "глагол, настоящее время, 3-е лицо, ед. число  берет",
    "WDT": "вопросительный определитель  который",
    "WP": "вопросительное местоимение кто, что",
    "WP$": "притяжательное вопросительное местоимение чей",
    "WRB": "вопросительное наречие  где, когда",
    "TO": 'to  идти "в" магазин.',
    "UH": "междометие",
    "VB": "глагол, исходная форма",
}


signs = "!~@#$%^&*()_+<>?:.,;[]\\|'\"–«"


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
    stop_words = set(stopwords.words("english"))
    for sign in signs:
        stop_words.add(sign)
    word_tokens = nltk.tokenize.word_tokenize(raw_data)
    tagged_word_tokens = nltk.pos_tag(word_tokens)
    final_table = []
    for token in tagged_word_tokens:
        if token[0].lower() not in stop_words:
            final_table.append(token)
    for token in range(len(final_table)):
        buffer = final_table[token][0]
        final_table[token] = (buffer, UNSHIPHER.get(final_table[token][1]))
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
