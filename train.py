from re import sub
from pickle import dump
from os import listdir
import argparse
import Model


def read_books(input_dir):
    """
    :param input_dir: директория, в которой содержатся все книги в формате .txt
    :return: список из слов этих книг
    """
    book_names = listdir(input_dir)
    book_texts = []
    for book_name in book_names:
        if len(book_name) >= 4 and book_name[-4:] == '.txt':
            file = open(input_dir + book_name, encoding='utf-8')
            book_texts.extend(words_tokenize(file.read()))
            file.close()
    return book_texts


def words_tokenize(book_text):
    """
    :param book_text: текст книги
    :return: преобразованный список слов
    """
    book_text = sub(r'[^A-Za-z. ]', '', book_text)
    return book_text.lower().split()


def save_file(data, model_dir):
    with open(model_dir, 'wb') as f:
        dump(data, f)


def generate_ngrams(words_tokens, model):
    """
    :param words_tokens: список слов, получившихся из всех книг
    :param model: экземпляр класса Model

    функция сохраняет файл в указанной директории
    """
    print(f'Count words:{len(words_tokens)}')
    print('Training...')
    ngrams = {}
    for i in range(len(words_tokens) - model.len_prefix):
        """
        seq - строка, в которой и находятся model.len_prefix слов, разделенных пробелом
        формат словаря: {'seq': {предполагаемое слово: кол-во таких слов в тексте, ...}, ...}
        """
        seq = ' '.join(words_tokens[i:i + model.len_prefix])
        if seq not in ngrams.keys():
            ngrams[seq] = {}
        if words_tokens[i + model.len_prefix] not in ngrams[seq].keys():
            ngrams[seq][words_tokens[i + model.len_prefix]] = 0

        count = ngrams[seq][words_tokens[i + model.len_prefix]] + 1
        ngrams[seq][words_tokens[i + model.len_prefix]] = count
    save_file(ngrams, model.model_dir)
    print("Training was successful")


def train(model, input_dir):
    """
    :param model: экземпляр класса Model
    :param input_dir: директория, в которой содержатся книги в формате .txt
    """
    words_tokens = read_books(input_dir)
    generate_ngrams(words_tokens, model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir',
                        dest='input_dir',
                        type=str,
                        help='Input dir for data',
                        required=True)
    parser.add_argument('--len-prefix',
                        dest='len_prefix',
                        type=int,
                        help='Input length of prefix. Default prefix length is 2',
                        default=2)
    parser.add_argument('--model',
                        dest="model_dir",
                        type=str,
                        help='Input dir for model. By default creates a file in this directory named "model.pickle"',
                        default='model.pkl')

    args = parser.parse_args()
    args.input_dir = args.input_dir.replace('\\', '\\\\') + '\\\\'
    args.model_dir = args.model_dir.replace('\\', '\\\\')

    model = Model.Model(args.model_dir, args.len_prefix)
    model.fit(args.input_dir)
