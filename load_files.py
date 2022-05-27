import xml.sax


class TableHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.CurrentData = ""
        self.records = []
        self.one_record = []
        self.name = ''
        self.score = ''
        self.wave = ''

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if self.CurrentData == "record":
            pass

    def characters(self, content):
        if self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "score":
            self.score = content
        elif self.CurrentData == "wave":
            self.wave = content

    def endElement(self, tag):
        if self.CurrentData == "name":
            self.one_record.append(self.name)
        elif self.CurrentData == "score":
            self.one_record.append(self.score)
        elif self.CurrentData == 'wave':
            self.one_record.append(self.wave)
        if len(self.one_record) == 3:
            self.records.append(self.one_record)
            self.one_record = []
            self.name = ''
            self.score = ''
            self.wave = ''
            self.CurrentData = ''
