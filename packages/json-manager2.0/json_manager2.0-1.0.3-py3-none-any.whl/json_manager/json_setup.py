from json import load, dump
from os import path, getcwd

from .json_attributdict import AttributDict

class setup():



    def __init__(self, paths: dict[str: str], encode: str = 'utf-8', newline: str = ''):
        """
        Init datas
        :param paths:> ``key`` : str, ``value`` : path of the file.
        :param encode: File encoding for write and read. Default 'utf-8'
        :param newline: The new line in the file. Default ''
        """

        self.__proprietes_dynamiques = {}
        self.paths = paths
        self.encode = encode
        self.newline = newline

        for i in paths.keys():
            self.__load_json(i, paths[i])
        print(self.__proprietes_dynamiques)


    def __read_file(self, file_path):
        with open(file_path, 'r', encoding=self.encode, newline=self.newline, errors='ignore') as f:
            file = load(f)
            return file

    def __load_json(self, name, path_):
        global file_path

        if not path.isabs(path_):
            # Conserver le chemin relatif à l'utilisateur
            file_path = path.join(getcwd(), path_)
        else:
            # Utiliser directement le chemin absolu
            file_path = path_

        file = self.__read_file(file_path=file_path)

        self.__proprietes_dynamiques[name] = AttributDict(file)


    def __getattr__(self, key):

        # Cette méthode est appelée uniquement si l'attribut n'est pas trouvé normalement
        if key in self.__proprietes_dynamiques:
            return self.__proprietes_dynamiques[key]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")


    def __delattr__(self, item):
        if item in self.__proprietes_dynamiques:
            del self.__proprietes_dynamiques[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")


    def write(self):

        for i in self.paths.keys():

            if not path.isabs(self.paths[i]):
                # Conserver le chemin relatif à l'utilisateur
                file_path = path.join(getcwd(), self.paths[i])
            else:
                # Utiliser directement le chemin absolu
                file_path = self.paths[i]

            if self.__read_file(file_path) == self.__proprietes_dynamiques[i]:
                print('pass')
                pass

            else:
                with open(file_path, 'w', encoding=self.encode, newline=self.newline, errors='ignore') as f:
                    dump(self.__proprietes_dynamiques[i], f, indent=2)

        return True

