import pickle


class Pickler:
    @staticmethod
    def save_obj(obj, path):
        with open(path, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)




    @staticmethod
    def load_obj(path):
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
        except ImportError:
            return None
        except TypeError:
            return None
