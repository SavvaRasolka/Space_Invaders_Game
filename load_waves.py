import xml.sax


class WavesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.CurrentData = ""
        self.mobs = []
        self.one_mob = []
        self.name = ''
        self.hp = ''
        self.sprite = ''
        self.cost = ''

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if self.CurrentData == "mob":
            pass

    def characters(self, content):
        if self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "hp":
            self.hp = content
        elif self.CurrentData == "sprite":
            self.sprite = content
        elif self.CurrentData == "cost":
            self.cost = content

    def endElement(self, tag):
        if self.CurrentData == "name":
            self.one_mob.append(self.name)
        elif self.CurrentData == "hp":
            self.one_mob.append(self.hp)
        elif self.CurrentData == "sprite":
            self.one_mob.append(self.sprite)
        elif self.CurrentData == "cost":
            self.one_mob.append(self.cost)
        if len(self.one_mob) == 4:
            self.mobs.append(self.one_mob)
            self.one_mob = []
            self.name = ''
            self.hp = ''
            self.sprite = ''
            self.cost = ''
            self.CurrentData = ''
