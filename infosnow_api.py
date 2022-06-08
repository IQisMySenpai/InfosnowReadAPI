import requests


def remove_html_tags(text: str):
    text = text.replace('&auml;', 'ä').replace('&ouml;', 'ö').replace('&uuml;', 'ü')
    text = text.replace('&Auml;', 'Ä').replace('&Ouml;', 'Ö').replace('&Uuml;', 'Ü')
    text = text.replace('&egrave;', 'è').replace('&Egrave;', 'È')
    text = text.replace('&eacute;', 'é').replace('&Eacute;', 'É')
    text = text.replace('&agrave;', 'à').replace('&Agrave;', 'À')
    text = text.replace('&ecirc;', 'ê').replace('&Ecirc;', 'Ê')
    text = text.replace('&ccedil', 'ç').replace('&Ccedil', 'Ç')

    return text.strip()


class API:
    url = 'https://www.infosnow.ch/~apgmontagne/'
    data = {}
    html = ''

    def __init__(self, resort_id, season):
        self.resort_id = resort_id
        self.season = season
        self.load_data()
        self.read_data()

    def load_data(self):
        rq = requests.get(self.url, params={'tab': 'web-js', 'lang': 'de', 'xid': self.resort_id, 'saison': self.season},
                          headers={'User-Agent': 'Totally Not a Bot'})

        self.html = rq.content.decode("utf-8")

    def read_data(self):
        position = self.html.find('class="isH1"')
        while position > -1:
            position = self.html.find('>', position + 1)
            position = self.html.find('>', position + 1)
            end = self.html.find('</div>', position + 1)

            header = self.html[position + 1:end]

            if 'offen)' in header:
                h_end = header.find(' (')
                header = remove_html_tags(header[:h_end])
            else:
                position = self.html.find('class="isH1"', position)
                continue

            entries = []

            next_entry = self.html.find('<div class="isRec">', position)

            next_data = self.html.find('<div class="isBreakBox">', position)
            if next_data < 0:
                next_data = self.html.find('<img class="isAPG"', position)

            print(f'Started Header: {header}')
            while next_entry < next_data:
                next_entry = self.html.find('~apgmontagne/pub/pics/state/3/', next_entry)
                next_entry = self.html.find(' alt="', next_entry)
                status = remove_html_tags(self.html[next_entry + 6:self.html.find('" title="', next_entry)])

                next_entry = self.html.find('~apgmontagne/pub/pics/svg/', next_entry)
                next_entry = self.html.find(' alt="', next_entry)
                category = remove_html_tags(self.html[next_entry + 6:self.html.find('" title="', next_entry)])

                next_entry = self.html.find('<div class="isTxt">', next_entry)
                text_end = self.html.find('</div>', next_entry)
                span = self.html.find('<span', next_entry)
                if 0 < span < text_end:
                    name = remove_html_tags(self.html[next_entry + 19:span])
                    span = self.html.find('>', span)
                    span_end = self.html.find('</span>', span)
                    length = remove_html_tags(self.html[span + 2:span_end - 1])
                else:
                    name = remove_html_tags(self.html[next_entry + 19:text_end])
                    length = None

                if ' &bull; ' in name:
                    point = name.find(' &bull; ')
                    label = name[:point]
                    name = name[point + 8:]
                else:
                    label = None

                doc = {'name': name, 'status': status, 'type': category}

                if label is not None:
                    doc['label'] = label

                if length is not None:
                    doc['length'] = length
                entries.append(doc)

                next_entry = self.html.find('<div class="isRec">', next_entry)
                if next_entry < 0:
                    break

            position = self.html.find('class="isH1"', position)
            self.data[header] = entries


api = API(54, 1)
print(api.data)
    