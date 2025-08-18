import requests
from bs4 import BeautifulSoup

def get_match_data(url):
    """
    Extracts team names and match scores from a vlr.gg match page.
    Returns a dictionary with the data or None in case of an error.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Throws an exception for 4xx/5xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    match_data = {}

    try:
        team_names = soup.find_all('div', class_='wf-title-med')
        if len(team_names) >= 2:
            match_data['team_1'] = team_names[0].text.strip()
            match_data['team_2'] = team_names[1].text.strip()

        score_div = soup.find('div', class_='match-header-vs-score')
        if score_div:
            first_score_span = score_div.select_one('span:first-child')
            last_score_span = score_div.select_one('span:last-child')

            if first_score_span and last_score_span:
                match_data['score_1'] = first_score_span.text.strip()
                match_data['score_2'] = last_score_span.text.strip()
            else:
                match_data['score_1'] = "N/A"
                match_data['score_2'] = "N/A"

    except Exception as e:
        print(f"HTML parsing error: {e}")
        return None

    return match_data

# Test block: This code runs only when the file is executed directly.
if __name__ == '__main__':
    print("Executing scraping function tests...")

    # Test URL 1
    test_url_1 = "https://www.vlr.gg/511577/giantx-vs-team-heretics-vct-2025-emea-stage-2-w5"
    data_1 = get_match_data(test_url_1)
    if data_1 and data_1.get('team_1'):
        print("\nSuccessfully extracted data from match 1:")
        print(f"Match: {data_1.get('team_1')} {data_1.get('score_1')} vs {data_1.get('score_2')} {data_1.get('team_2')}")

    # Test URL 2
    test_url_2 = "https://www.vlr.gg/509831/mibr-vs-loud-vct-2025-americas-stage-2-w5"
    data_2 = get_match_data(test_url_2)
    if data_2 and data_2.get('team_1'):
        print("\nSuccessfully extracted data from match 2:")
        print(f"Match: {data_2.get('team_1')} {data_2.get('score_1')} vs {data_2.get('score_2')} {data_2.get('team_2')}")
    else:
        print("\nFailed to extract data from the match.")