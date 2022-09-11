import train
import generate


class Model:
    def __init__(self, model_dir, len_prefix=2):
        self.model_dir = model_dir

        if len_prefix > 0:
            self.len_prefix = len_prefix
        else:
            raise ValueError("Incorrect value of len_prefix")

    def fit(self, input_dir):
        train.train(self, input_dir)

    def generate(self, prefix=None, length=100):

        if not (prefix is None) and len(prefix.split()) != self.len_prefix:
            raise ValueError("Incorrect value of prefix")
        elif length <= 0:
            raise ValueError("Incorrect value of length")
        else:
            generate.generate(self, prefix, length)
