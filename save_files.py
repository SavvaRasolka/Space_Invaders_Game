import xml.etree.ElementTree as ET


class TableSaver:
    def __init__(self, data):
        self.data = data

    def save(self, path):
        root = ET.Element('data')
        for note in self.data:
            record = ET.Element('record')

            name = ET.Element('name')
            name.text = str(note)
            record.append(name)

            score = ET.Element('score')
            score.text = str(self.data[note][0])
            record.append(score)

            wave = ET.Element('wave')
            wave.text = str(self.data[note][1])
            record.append(wave)

            root.append(record)
        etree = ET.ElementTree(root)
        try:
            file_to_save = open(path + "\\record_table.xml", "wb")
            etree.write(file_to_save)
            file_to_save.close()
        except:
            return


def save_to_file(table):
    saving = TableSaver(table)
    saving.save('config')
