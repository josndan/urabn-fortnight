class Posting:
    def __init__(self, id, data, positions):
        self.docId = id
        self.data = data
        self.positions = positions

    def getTermCount(self):
        return len(self.positions)

    def getDocId(self):
        return self.docId

    def getPositions(self):
        return self.positions

    def __repr__(self):
        return f"{self.docId} : {self.data} : {self.positions}"

