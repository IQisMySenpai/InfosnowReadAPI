# InfosnowReadAPI

## Table of Contents

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Example](#example)
   - [Requesting Data](#requesting-data)
   - [Data Format](#data-format)
3. [Comments on the License](#comments-on-the-license)

## About The Project

I needed code to get me information on the current open lifts and slops of a ski area. I requested read access to the infosnow API, however wasn't given it.

Please read [Comments on the License](#comments-on-the-license) before using my project.

### Built With

* [Python3.9]([www.jquery.com](https://www.python.org/downloads/release/python-390/))

## Example

Some examples on how to use the code and how the returned data is formated

### Requesting Data

You will need to import the get_infosnow_data function.
This function takes two parameters. The first being the id of the
resort that you are collecting data from. The second being the season, you would like data on. 1 - Winter, 2 - Summer.

```python
from infosnow_api import get_infosnow_data

data = get_infosnow_data('54', '1')
```


### Data Format

The return data is structured as followed.

The outer dictionary contains the different categories of entries. 
Some examples for the winter season would be:
- Anlagen
- Pisten
- Funparks
- Schlittelpisten

Each of these categories have an array of entries. Each entry is a dict with following keys:
- *name*: String with the name of the entry
- *status*: String if the current entry is open
- *type*: String with the type of the entry
- *label* (optional): String with the short label. For example "12 - Kanonenrohr", the 12 would be the label and Kanonenrohr the name.
- *length* (optional): String with the length in km

Example of the structure:
```json
{
   "Pisten": [
      {
         "name": "Tunnel Westseite", 
         "status": "ausser Betrieb", 
         "type": "Skipiste - schwarz", 
         "label": "1", 
         "length": "3.3 km"
      }
   ]
}
```

## Comments on the License

While I have released my code under the MIT License, I do have to note that the web-crawler returns data gathered and owned by [APG|SGA Out of Home Media](https://www.apgsga.ch/en/).
This means that (including but not limited to) publishing, distributing, selling, and/or using acquired data gathered by my software has to happen following 
[APG|SGA Out of Home Media's](https://www.apgsga.ch/en/) copyright and licensing for their data and not my open-source software.

In no event will I be liable or responsible for data that you collected, and its safe storage.