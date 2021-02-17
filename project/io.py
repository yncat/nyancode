class IO:
    def dump(self, filename, content):
        with open(filename, "w", encoding="UTF-8") as f:
            f.write(content)

    def load(self, path):
        with open(path, "r", encoding="UTF-8") as f:
            c = f.read()
        # end with
        return c
