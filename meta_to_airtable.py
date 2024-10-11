import requests
import json

# Define your Airtable and Meta Ads API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = 'patEeGtwQq2jRDGoH'
AIRTABLE_BASE_ID = 'ptfrZU0B5ztVSQ'
AIRTABLE_TABLE_NAME = 'Performance-KPI'
META_ACCESS_TOKEN = 'EAAM2gsgkLtkBO6OCmqrpWAFKbUYKUtiHq7yWumIqgleU7GGHPss4G38x8ru7DxLUXCPTSY507ZAialeysqVZBFS7ko8evppXQWonISA6yq80CHsaMUw7iLCoDKD6FPoYYX4XA9WZAzYFLpgPP4yJru7UNxXCOyUqsCXN8qCwMOrdDNModeRkUfYNkUZD'
META_AD_ACCOUNT_ID = 'act_537133347493122'

# URLs for API requests
AIRTABLE_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
META_URL = f'https://graph.facebook.com/v14.0/{META_AD_ACCOUNT_ID}/insights'

# Headers for Airtable API
airtable_headers = {
    'Authorization': f'Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Parameters for Meta Ads API request
meta_params = {
    'access_token': META_ACCESS_TOKEN,
    'fields': 'impressions,clicks,spend',  # Define the fields you need
    'time_range': json.dumps({'since': '2024-01-01', 'until': '2024-12-31'})
}

# Get data from Meta Ads API
response = requests.get(META_URL, params=meta_params)
if response.status_code == 200:
    meta_data = response.json()
    
    # Loop through each campaign and add data to Airtable
    for campaign in meta_data.get('data', []):
        airtable_data = {
            'fields': {
                'Impressions': int(campaign.get('impressions', 0)),
                'Clicks': int(campaign.get('clicks', 0)),
                'Spend': float(campaign.get('spend', 0.0))
            }
        }

        # Post data to Airtable
        airtable_response = requests.post(AIRTABLE_URL, headers=airtable_headers, data=json.dumps(airtable_data))
        if airtable_response.status_code == 200:
            print(f"Successfully added campaign data for: {campaign.get('campaign_name')}")
        else:
            print(f"Failed to add campaign data for: {campaign.get('campaign_name')}, Error: {airtable_response.content}")
else:
    print(f"Failed to fetch data from Meta Ads API, Error: {response.content}")	
