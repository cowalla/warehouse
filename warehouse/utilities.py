class ChoiceEnum(object):
    def __init__(self, names_enums):
        self.names_enums = names_enums

    def as_choices(self):
        return tuple(
            (enum, name)
            for name, enum in self.names_enums.iteritems()
        )

    def names(self):
        return self.names_enums.keys()

    def __getitem__(self, item):
        return self.names_enums[item]