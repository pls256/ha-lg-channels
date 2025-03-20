import json
import yaml  # Use PyYAML to write structured YAML content

# Paths to input and output
json_file = "lg-channels.json"  # JSON file containing channel data
yaml_file = "home_assistant_dashboard.yaml"  # YAML file to generate

# Load JSON data
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Define the media players and their corresponding views -- UPDATE THESE TO YOUR TV --
media_players = {
    "Office TV": "media_player.office_tv",
    "Lounge TV": "media_player.lounge_tv",
    "Man Cave Top TV": "media_player.man_cave_tv_top",
    "Man Cave Bottom TV": "media_player.man_cave_tv_bottom"
}

# Start building the overall YAML structure for the dashboard
dashboard_yaml = {
    "title": "LG Channels Dashboard",
    "views": []
}

# Group channels by category
categories = {}
for item in data:
    category_name = item["Category"]
    if category_name not in categories:
        categories[category_name] = []
    categories[category_name].append(item)

# Create a separate view for each media player
for tv_name, entity_id in media_players.items():
    view = {
        "title": tv_name,
        "path": tv_name.lower().replace(" ", "_"),  # Generate a valid path for the view
        "panel": False,
        "cards": []
    }

    # Add a grid for each category in this TV's view
    for category, channels in categories.items():
        grid_card = {
            "type": "grid",
            "title": f"{category} Channels",
            "columns": 3,  # Grid width of 5
            "square": False,  # Render cards with flexible dimensions
            "cards": []
        }

        # Add Picture Cards for each channel in the category
        for channel in channels:
            image_name = channel["Brand Image URL"].split("/")[-1]  # Extract image file name
            channel_number = channel["Channel"]  # Get the integer channel number

            grid_card["cards"].append({
                "type": "picture",
                "image": f"/local/images/lg-channels/{image_name}",  # Path to the image in Home Assistant
                "alt_text": channel["Channel Name"],  # Add channel name as alt_text
                "tap_action": {
                    "action": "call-service",
                    "service": "webostv.command",
                    "service_data": {
                        "entity_id": entity_id,
                        "command": "tv/openChannel",
                        "payload": {
                            "channelMode": "Terrestrial",
                            "channelNumber": channel_number
                        }
                    }
                }
            })

        # Add the grid card to the view
        view["cards"].append(grid_card)

    # Add the view to the dashboard
    dashboard_yaml["views"].append(view)

# Write YAML content to file
with open(yaml_file, "w", encoding="utf-8") as file:
    yaml.dump(dashboard_yaml, file, default_flow_style=False, allow_unicode=True)

print(f"Home Assistant dashboard YAML has been written to {yaml_file}")
