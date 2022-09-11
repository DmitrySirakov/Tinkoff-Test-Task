from random import randrange, choices
from pickle import load
import argparse

import Model


def generate_start_seq(ngrams):
    """
    :param ngrams: словарь, в котором содержатся все ngrams
    :return: строку, с которой начнется наш текст
    """
    save_dict = list(ngrams.keys())
    start_frase = save_dict[randrange(len(save_dict))]
    return start_frase


def load_file(model):
    with open(model, 'rb') as f:
        return load(f)


def generate_text(ngrams, prefix, length):
    """
    :param ngrams: словарь со всеми ngrams
    :param prefix: стартовая фраза, с которой начнется текст
    :param length: кол-во слов в тексте, который нужно сгенерировать
    :return: сгенерированный текст
    """
    len_prefix = len(prefix.split())
    output = prefix
    for i in range(length):
        if prefix in ngrams.keys():
            """
            словарь ngrams имеет вид: {'prefix': {предполагаемое слово: кол-во таких слов в тексте, ...}..}
            считаем сумму кол-ва предполагаемых слов и создаем список, в котором содержатся вероятности 
            выбора следующего слова.
            у самых часто встречающихся слов - большая вероятность, у самых редких слов - меньшая
            """
            count_words = sum(ngrams[prefix].values())
            keys = list(ngrams[prefix].keys())
            possible_words = keys

            total_chance = [ngrams[prefix][x] / count_words for x in keys]
            next_word = choices(possible_words, weights=total_chance)[0]

            output += ' ' + next_word
            seq_words = output.split()
            prefix = ' '.join(seq_words[len(seq_words) - len_prefix:len(seq_words)])
        else:
            print('No such prefix found. Try another')
    return output


def generate(model, prefix, length):
    """
    :param model: экземпляр класса Model
    :param prefix: стартовая фраза текста
    :param length: кол-во слов, которые нужно сгенировать

    функция печатает в консоли сгенерированный текст
    """
    ngrams = load_file(model.model_dir)
    if prefix is None:
        prefix = generate_start_seq(ngrams)

    print(generate_text(ngrams, prefix, length))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',
                        dest='model_dir',
                        type=str,
                        help='Input dir for model',
                        required=True)
    parser.add_argument('--prefix',
                        dest='prefix',
                        type=str,
                        help='Input start prefix for text. Default prefix is random',
                        default=None)
    parser.add_argument('--length',
                        dest='length',
                        type=int,
                        help='Input count words of text. Default counts words are 100',
                        default=100)
    args = parser.parse_args()
    args.model_dir = args.model_dir.replace('\\', '\\\\')
    model = Model.Model(args.model_dir)
    model.generate(args.prefix, args.length)
