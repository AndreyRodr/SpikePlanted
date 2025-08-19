import requests
from bs4 import BeautifulSoup
import traceback

def get_group_standings(url):
    """
    Extracts group stage standings (teams and their records) from a VLR.gg URL.
    Returns a list of dictionaries, with each dictionary representing a group.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    standings_data = []
    
    try:
        # Find all the main group blocks on the page
        group_blocks = soup.find_all('div', class_='wf-card')
        
        for block in group_blocks:
            group_data = {}
            
            # Find the group name
            group_name_element = block.find('div', class_='event-groups-header-title')
            group_name = group_name_element.text.strip() if group_name_element else 'N/A'
            
            # Find all the team items within this group block
            team_items = block.find_all('a', class_='event-group-item')
            
            teams = []
            for item in team_items:
                team = {}
                
                # Extract team name
                team_name_element = item.find('div', class_='event-group-item-name')
                team['name'] = team_name_element.text.strip() if team_name_element else 'N/A'
                
                # Extract stats (W-L, Map Diff, Round Diff)
                stats_elements = item.find_all('div', class_='event-group-item-record')
                if stats_elements:
                    # Get the W-L record
                    team['record'] = stats_elements[0].text.strip()
                    # Get the Map and Round difference
                    if len(stats_elements) > 1:
                        team['map_diff'] = stats_elements[1].text.strip()
                    if len(stats_elements) > 2:
                        team['round_diff'] = stats_elements[2].text.strip()
                
                teams.append(team)
            
            group_data['group_name'] = group_name
            group_data['teams'] = teams
            standings_data.append(group_data)
            
    except Exception as e:
        print(f"HTML parsing error: {e}")
        traceback.print_exc()
        return None
        
    return standings_data

# Test block: This runs only when the file is executed directly.
if __name__ == '__main__':
    test_url = "https://www.vlr.gg/event/2498/vct-2025-emea-stage-2/group-stage"
    print("Executing group standings scraping test...")
    standings = get_group_standings(test_url)
    
    if standings:
        print("\nSuccessfully extracted group standings:")
        print(standings)
    else:
        print("\nFailed to extract group standings.")
