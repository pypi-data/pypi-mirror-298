from yaml import full_load as load_yaml_file


class Rulez:
    def __init__(self, file_):
        self.prop = {}
        with open(file_) as f:
            self.rulez = load_yaml_file(f)

    def __get(self, val, name):
        _max = len(val)
        obj = self.rulez
        for i in range(_max):
            if val[i] in obj:
                if i == _max - 1:
                    a = obj[val[i]]
                    self.prop[name] = a
                    return a
                else:
                    obj = obj[val[i]]
        return ""

    def get(self, item):
        if item in self.prop:
            return self.prop[item]

        val = item.split("/")
        if len(val) == 1 and val[0] == "":
            return self.rulez
        return self.__get(val, item)
