class Reaction:
    def __init__(self, name, profile_url, reaction):
        """
            Parameters:
                - name String
                - profile_url String
                - reaction String
        """
        self.name = name
        self.profile_url = profile_url
        self.reaction = reaction

    def __repr__(self):
        return  self.name + ',' + self.profile_url + ',' + self.reaction

    def __iter__(self):
        self.count = 0
        self.list = [self.name, self.profile_url, self.reaction]
        return self

    def __next__(self):
        if self.count == len(self.list):
            raise StopIteration
        self.count += 1
        return self.list[self.count - 1]