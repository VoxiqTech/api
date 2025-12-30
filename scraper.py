import requests
import re
import concurrent.futures

def fetch_profile_data(username):
    """
    Fetches the main profile page and extracts data from the embedded 'userData' JSON using Regex.
    This is more reliable for Scores, Rank, and basic info than parsing HTML classes.
    """
    url = f"https://www.geeksforgeeks.org/profile/{username}?tab=activity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    
    # Default Structure
    data = {
        "username": username,
        "profile_url": url,
        "name": "",
        "institution": "N/A",
        "institute_rank": "N/A",
        "coding_score": 0,
        "total_problems_solved": 0,
        "monthly_coding_score": 0,
        "articles_published": 0,
        # Extra fields from user's regex
        "profile_image_url": "",
        "streak_current": 0,
        "streak_max": 0,
        "campus_ambassador": False,
        "html_fetch_success": False
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data["html_fetch_success"] = True
            html_content = response.text
            
            # --- User's Regex Logic ---
            # Locate userData block
            start_pos = html_content.find('"userData":{')
            user_section = ""
            if start_pos != -1:
                end_pos = html_content.find('"error"', start_pos)
                if end_pos == -1: end_pos = start_pos + 5000
                else: end_pos += 200
                user_section = html_content[start_pos:end_pos]
            else:
                ud_idx = html_content.find('userData')
                if ud_idx != -1: user_section = html_content[ud_idx:ud_idx+5000]
                else: user_section = html_content

            def extract_value(pattern, is_int=False):
                # Try complex pattern handling escaped quotes
                match = re.search(pattern, user_section)
                if match:
                    value = match.group(1)
                    if not is_int:
                        # Clean escaped chars
                        value = value.replace('\\\\', '\\').replace('\\"', '"')
                    return int(value) if is_int else value
                
                # Try simple pattern
                simple_pattern = pattern.replace(r'\\"', '"')
                match = re.search(simple_pattern, user_section)
                if match:
                    value = match.group(1)
                    return int(value) if is_int else value
                    
                return 0 if is_int else ""

            # Extraction
            data["name"] = extract_value(r'\\"name\\":\\"([^\\"]+)\\"')
            data["institution"] = extract_value(r'\\"institute_name\\":\\"([^\\"]*)\\"') or "N/A"
            data["institute_rank"] = extract_value(r'\\"institute_rank\\\":(\d+)', is_int=False) # Keep as string/int mixed
            if data["institute_rank"] == 0: data["institute_rank"] = "N/A"
            
            data["coding_score"] = extract_value(r'\\"score\\\":(\d+)', is_int=True)
            data["monthly_coding_score"] = extract_value(r'\\"monthly_score\\\":(\d+)', is_int=True)
            data["total_problems_solved"] = extract_value(r'\\"total_problems_solved\\\":(\d+)', is_int=True)
            data["articles_published"] = 0 # Not present in basic userData typically, keeps default
            
            data["profile_image_url"] = extract_value(r'\\"profile_image_url\\":\\"([^\\"]+)\\"')
            
            # Streaks
            data["streak_current"] = extract_value(r'\\"pod_solved_current_streak\\\":(\d+)', is_int=True)
            data["streak_max"] = extract_value(r'\\"pod_solved_longest_streak\\\":(\d+)', is_int=True)
            
            # Ambassador Check
            if '"is_campus_ambassador":true' in user_section or '\\"is_campus_ambassador\\":true' in user_section:
                data["campus_ambassador"] = True
            
            # Fallback for Total Solved if 0
            if data["total_problems_solved"] == 0:
                 m = re.search(r'"total_problems_solved":(\d+)', user_section)
                 if m: data["total_problems_solved"] = int(m.group(1))

        else:
            print(f"Profile fetch failed: {response.status_code}")
    except Exception as e:
        print(f"Profile fetch error: {e}")

    return data

def fetch_breakdown_api(username):
    """
    Fetches the Practice API to get detailed problem breakdown.
    """
    api_url = "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/"
    headers = {
        "Origin": "https://www.geeksforgeeks.org",
        "Referer": "https://www.geeksforgeeks.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {
        "handle": username,
        "requestType": "",
        "year": "",
        "month": ""
    }
    
    data = {
        "problems_solved_breakdown": {
            "school": 0,
            "basic": 0,
            "easy": 0,
            "medium": 0,
            "hard": 0
        },
        "api_total_count": 0,
        "api_fetch_success": False
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data["api_fetch_success"] = True
            api_data = response.json()
            
            if "result" in api_data:
                result = api_data["result"]
                for difficulty, problems in result.items():
                    diff_key = difficulty.lower()
                    if diff_key in data["problems_solved_breakdown"]:
                        data["problems_solved_breakdown"][diff_key] = len(problems)
            
            if "count" in api_data:
                data["api_total_count"] = int(api_data["count"])
        else:
            print(f"Breakdown API fetch failed: {response.status_code}")
    except Exception as e:
        print(f"Breakdown API error: {e}")

    return data

def get_gfg_profile(username):
    """
    Orchestrates parallel fetching:
    1. Profile Data (from Regex on HTML)
    2. Breakdown Data (from API)
    """
    
    # Parallel Execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_profile = executor.submit(fetch_profile_data, username)
        future_api = executor.submit(fetch_breakdown_api, username)
        
        # Wait for both
        profile_data = future_profile.result()
        api_data = future_api.result()

    # Merge: Breakdown into Profile
    if api_data["api_fetch_success"]:
        profile_data["problems_solved_breakdown"] = api_data["problems_solved_breakdown"]
        
        # Trust API total count if HTML missed it
        if profile_data["total_problems_solved"] == 0 and api_data["api_total_count"] > 0:
            profile_data["total_problems_solved"] = api_data["api_total_count"]

    return profile_data
