import requests
import json

# Define your Airtable and Meta Ads API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = 'patGOAwLj5ybiak3V.ea941e120e717cc7fe3ce6979a4bdeee3fb105d0588f84a7c7d8b5b06c562ce1'
AIRTABLE_BASE_ID = 'appptfrZU0B5ztVSQ'
AIRTABLE_TABLE_NAME = 'Performance-KPI'
META_ACCESS_TOKEN = 'EAAM2gsgkLtkBO6OCmqrpWAFKbUYKUtiHq7yWumIqgleU7GGHPss4G38x8ru7DxLUXCPTSY507ZAialeysqVZBFS7ko8evppXQWonISA6yq80CHsaMUw7iLCoDKD6FPoYYX4XA9WZAzYFLpgPP4yJru7UNxXCOyUqsCXN8qCwMOrdDNModeRkUfYNkUZD'
META_AD_ACCOUNT_ID = 'act_3439696339428833'

# URLs for API requests
AIRTABLE_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
META_URL = f'https://graph.facebook.com/v14.0/{META_AD_ACCOUNT_ID}/insights'

# Headers for Airtable API
airtable_headers = {
    'Authorization': f'Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

from datetime import datetime, timedelta

from datetime import datetime, timedelta

# Calcola l'intervallo di date per il giorno precedente
today = datetime.now()
yesterday = today - timedelta(days=1)

# Converti le date in stringhe nel formato richiesto per prendere solo il giorno precedente
since = yesterday.strftime('%Y-%m-%d')
until = yesterday.strftime('%Y-%m-%d')

# Parameters for Meta Ads API request
meta_params = {
    'access_token': META_ACCESS_TOKEN,
    'fields': 'campaign_name,impressions,clicks,spend',  # Define the fields you need
    'time_range': json.dumps({'since': since, 'until': until}),
    'level': 'campaign'  # Assicurati di includere 'level' per richiedere i dati a livello di campagna
}

# Get data from Meta Ads API
response = requests.get(META_URL, params=meta_params)
if response.status_code == 200:
    meta_data = response.json()
    
    # Loop through each campaign and add data to Airtable
    for campaign in meta_data.get('data', []):
        airtable_data = {
            'fields': {
                'Campaign Name': campaign.get('campaign_name'),
                'Impressions': int(campaign.get('impressions', 0)),
                'Clicks': int(campaign.get('clicks', 0)),
                'Spend': float(campaign.get('spend', 0.0))
                'Date': yesterday.strftime('%Y-%m-%d')  # Aggiungi la data del giorno precedente
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
