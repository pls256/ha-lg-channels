# LG Channels Web Scraper and Home Assistant Dashboard Generator

## Overview

This project includes a Python-based web scraper designed to extract TV channel information from the LG Channels webpage, alongside a script to generate a YAML dashboard for Home Assistant. The project fetches details like category, brand, channel number, channel name, and description, saves the data in a JSON file, and downloads the associated brand images to a specified directory. It also generates a structured Home Assistant dashboard in YAML format, allowing users to interact with their LG TVs directly from Home Assistant.

This project uses the [webostv integration](https://www.home-assistant.io/integrations/webostv/) in Home Assistant to enable communication with LG webOS TVs.

## Features

- Scrapes TV channel information and organizes it into structured JSON format.
- Downloads brand images to a local directory.
- Generates a Home Assistant YAML dashboard with views for multiple TVs and categorized channels.
- Modular code with separate functions for web scraping, image downloading, and YAML generation.
- Easy to customize for your TVs and channels.

## Requirements

- Python 3.7 or later
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `PyYAML`
  - `os`
  - `json`

![LG Dashboard Example](assets/lg-dash-board.png)

## Usage

1. Prepare Input Data:
Before running the script, ensure you have a JSON file (lg-channels.json) containing the extracted channel data. This file can be created using the LG Channels Web Scraper script.

```bash
python lg_channel_scraper.py
```

2. Configure Media Players:
Edit the media_players dictionary in the script to include your Home Assistant media player entities. For example:

```python
media_players = {
    "Office TV": "media_player.office_tv",
    "Lounge TV": "media_player.lounge_tv"
}
```

3. Generate YAML Dashboard:
Run the script to generate the Home Assistant dashboard YAML file: 

```bash
python generate_dashboard_yaml.py
```

4. Configure Home Assistant:
COpy and Paste the generated YAML file (home_assistant_dashboard.yaml) to your Home Assistant dashboard raw edit.

Ensure the images referenced in the JSON data are available in the /local/images/lg-channels/ directory.

## How It Works

### JSON to YAML Conversion:
- Loads channel data from a JSON file.
- Groups channels by category.
- Creates views for each media player, with grid layouts for channels.

### Dashboard Configuration:

- Configures picture cards for each channel.

- Enables channel switching using the webostv.command service.

<HR>

### Notes
- The script assumes the existence of a JSON file created using the LG Channels Web Scraper script.

- Make sure the images are correctly placed in your Home Assistant's /www directory.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing
Feel free to contribute by submitting issues or pull requests. Any enhancements or bug fixes are welcome!