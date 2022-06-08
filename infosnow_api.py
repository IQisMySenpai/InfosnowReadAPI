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


def get_infosnow_data (resort_id, season):
    """
    Gets Data from the Infosnow website.
    :param resort_id: ID of the resort you want to pull
    :param season: Season of the data you want to pull 1: Winter, 2: Summer
    :return: Dictionary filled with data on the stuff you requested.
    """
    rq = requests.get('https://www.infosnow.ch/~apgmontagne/',
                      params={'tab': 'web-js', 'lang': 'de', 'xid': resort_id, 'saison': season},
                      headers={'User-Agent': 'Totally Not a Bot'})

    if rq.status_code != 200:  # Return None if status code is not 200
        print('Request didn\'t return status 200')
        return None

    html = rq.content.decode("utf-8")  # Decodes request to readable text.
    data = {}  # Dictionary where information is stored

    position = html.find('class="isH1"')  # Searches for Headers
    while position > -1:
        # Isolates header
        position = html.find('>', position + 1)
        position = html.find('>', position + 1)
        end = html.find('</div>', position + 1)

        header = html[position + 1:end]

        if 'offen)' in header:  # Checks that the headers contain important information
            h_end = header.find(' (')
            header = remove_html_tags(header[:h_end])
        else:
            position = html.find('class="isH1"', position)
            continue

        entries = []  # List of Entries in the Header

        next_entry = html.find('<div class="isRec">', position)

        next_data = html.find('<div class="isBreakBox">', position)
        if next_data < 0:
            next_data = html.find('<img class="isAPG"', position)

        print(f'Started Header: {header}')
        while next_entry < next_data:  # Gets each entry and adds it's information to data
            next_entry = html.find('~apgmontagne/pub/pics/state/3/', next_entry)
            next_entry = html.find(' alt="', next_entry)
            status = remove_html_tags(html[next_entry + 6:html.find('" title="', next_entry)])

            next_entry = html.find('~apgmontagne/pub/pics/svg/', next_entry)
            next_entry = html.find(' alt="', next_entry)
            category = remove_html_tags(html[next_entry + 6:html.find('" title="', next_entry)])

            next_entry = html.find('<div class="isTxt">', next_entry)
            text_end = html.find('</div>', next_entry)
            span = html.find('<span', next_entry)
            if 0 < span < text_end:
                name = remove_html_tags(html[next_entry + 19:span])
                span = html.find('>', span)
                span_end = html.find('</span>', span)
                length = remove_html_tags(html[span + 2:span_end - 1])
            else:
                name = remove_html_tags(html[next_entry + 19:text_end])
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

            next_entry = html.find('<div class="isRec">', next_entry)
            if next_entry < 0:
                break

        position = html.find('class="isH1"', position)
        data[header] = entries

    return data  # Returns Data
