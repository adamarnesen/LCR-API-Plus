# LCR API

Forked from: https://github.com/philipbl/LCR-API.

A Python API and some analytics for Leader and Clerk Resources for
[The Church of Jesus Christ of Latter-day Saints](https://www.churchofjesuschrist.org/?lang=eng).
I've only tested it with Python 3.5+.

The following calls are supported, which correspond to a page in LCR:

- Birthday list
- Members moved out
- Members moved in
- Member list
- Calling list
- Recommend Status

There is one additional call supported:

- Individual photo – Gets the photo for an individual. This is the same call that LCR uses to show a picture when you go to a member's page.

More calls will be supported as I have time. Pull requests are welcomed!

## Disclaimer

This code is rough around the edges. I don't handle any cases where a person using this code doesn't have permissions to access the reports, so I don't know what will happen.

## Setup

1. Install [Python 3.10](https://www.python.org/downloads/release/python-3100/)
1. Install and setup `pipenv`: `pip install pipenv`
1. Setup environment for this project
   1. From the root directory of the project (where the `Pipfile` file is
      located) run `pipenv install`
   1. Activate the environment using `pipenv shell`

## Usage

### Quarterly Reports Example

You can create a set of charts for multiple units (ex. in a stake) based on their quarterly
reports. You will need to have access to each unit in order to pull data.

To run analytics on the quarterly report, use `run_analytics.py`. To run this, you should place a
file called `profile.json` in the root directory of this project. The contents of that file should
contain the following.

```json
{
  "username": "<your lcr username>",
  "password": "<your lcr password>",
  "unit_number": 12345, // The unit you belong to. Can be a stake or ward.
  "unit_name": "<A name you want to use for your unit.>", // note this does not have to match the actual unit name.
  "units": [
    // specify as many units as you want that your LCR account has access to.
    {
      "name": "<unitName1>", // the name to show in analytics for this unit. Does not need to match the actual unit name.
      "number": 121314 // The unit number
    },
    {
      "name": "<unitName2>",
      "number": 151617
    },
    {
      "name": "<unitNameN>",
      "number": 181920
    }
  ]
}
```

Once you have this, run the following from the root directory of the project.
`python run_analytics.py`

This will pull the data from the specified units and produce a set of charts and graphs based on
quarterly reports. Charts will automatically open in your default browser.

### API Example

```python
from lcr import API as LCR

lcr = LCR("<LDS USERNAME>", "<LDS PASSWORD>", <UNIT NUMBER>)

months = 5
move_ins = lcr.members_moved_in(months)

for member in move_ins:
    print("{}: {}".format(member['spokenName'], member['textAddress']))
```

### To Do

- Add more tests
- Support more reports and calls
