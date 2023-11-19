from action import Action

class Actions:
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith("#") or line.startswith("//"):
                    continue
                yield Action.fromLine(line)

