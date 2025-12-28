import requests
import re
from typing import Optional

def get_gfg_profile(username: str, session: Optional[requests.Session] = None):
    """
    Fetch GfG profile data for a user using optimized regex extraction
    
    Args:
        username: GfG username to fetch
        session: Optional session (kept for API compatibility)
    
    Returns:
        Dictionary with profile data or None if not found
    """
    url = f"https://www.geeksforgeeks.org/profile/{username}?tab=activity"
    
    # Use provided session or create a new one
    if session is None:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    try:
        response = session.get(url, timeout=15)
        if response.status_code != 200:
            return None

        html_content = response.text
        
        # Strategy 1: Look for simple "userData": { ... } block (Old/Standard format)
        # This is what we originally optimized for
        start_pos = html_content.find('"userData":{')
        if start_pos != -1:
            end_pos = html_content.find('"error"', start_pos)
            if end_pos == -1:
                end_pos = start_pos + 5000
            else:
                end_pos += 200
            user_section = html_content[start_pos:end_pos]
        else:
            # Strategy 2: Look for Next.js encoded data (New format seen in user's HTML)
            # The data is inside self.__next_f.push([1,"... \"userData\":{\"message\":\"...\",\"data\":{ ... }} ... "])
            # We search for the pattern: \"userData\":{...} but it might be esaped
            
            # Simple fallback: Just search the entire HTML for the keys since we can't easily parse the Next.js stream
            # but we limit detection to the area around "userData"
            
            # Find any occurrence of "userData"
            ud_idx = html_content.find('userData')
            if ud_idx != -1:
                # Take a large chunk around it
                user_section = html_content[ud_idx:ud_idx+5000]
            else:
                # Last resort: use the whole HTML but it might be slow
                user_section = html_content

        # Helper function to extract values
        def extract_value(pattern, is_int=False):
            # We need to handle both escaped \"name\":\"Value\" and double escaped \\"name\\":\\"Value\\"
            # becuase Next.js sometimes double escapes inside the pushed string
            
            # Try double escaped first (common in embedded JSON strings)
            # Pattern: \\"key\\":\\"value\\"
            match = re.search(pattern, user_section)
            if match:
                value = match.group(1)
                if not is_int:
                    value = value.replace('\\\\', '\\').replace('\\"', '"')
                return int(value) if is_int else value
                
            # Try single escaped (standard JSON)
            # Pattern: "key":"value" - we adjust the pattern to remove double backslashes
            simple_pattern = pattern.replace(r'\\"', '"')
            match = re.search(simple_pattern, user_section)
            if match:
                value = match.group(1)
                return int(value) if is_int else value
                
            return 0 if is_int else ""
        
        # Extract fields
        name = extract_value(r'\\"name\\":\\"([^\\"]+)\\"')
        # ... logic continues ...
        
        # Need to re-implement field extraction to use new helper
        # Let's write the extraction logic more cleanly
        
        # Numeric fields
        overall_score = extract_value(r'\\"score\\\":(\d+)', is_int=True)
        monthly_score = extract_value(r'\\"monthly_score\\\":(\d+)', is_int=True)
        problems_solved = extract_value(r'\\"total_problems_solved\\\":(\d+)', is_int=True)
        institute_rank = extract_value(r'\\"institute_rank\\\":(\d+)', is_int=True)
        
        # If still failed, try the "Coding Score" fallback for text scraping
        if overall_score == 0 and "Coding Score" in html_content:
            # Fallback text scraping could go here but let's stick to JSON regex first
            pass

        profile_image = extract_value(r'\\"profile_image_url\\":\\"([^\\"]+)\\"')
        institution = extract_value(r'\\"institute_name\\":\\"([^\\"]*)\\"')
        organization = extract_value(r'\\"organization_name\\":\\"([^\\"]*)\\"')
        designation = extract_value(r'\\"designation\\":\\"([^\\"]*)\\"')
        school = extract_value(r'\\"school\\":\\"([^\\"]*)\\"')
        
        pod_current_streak = extract_value(r'\\"pod_solved_current_streak\\\":(\d+)', is_int=True)
        pod_longest_streak = extract_value(r'\\"pod_solved_longest_streak\\\":(\d+)', is_int=True)
        pod_global_longest = extract_value(r'\\"pod_solved_global_longest_streak\\\":(\d+)', is_int=True)
        pod_submissions = extract_value(r'\\"pod_correct_submissions_count\\\":(\d+)', is_int=True)
        created_date = extract_value(r'\\"created_date\\":\\"([^\\"]*)\\"')
        
        # Check campus ambassador
        is_campus_ambassador = False
        if '"is_campus_ambassador":true' in user_section or '\\"is_campus_ambassador\\":true' in user_section:
            is_campus_ambassador = True

        # Verify essential data
        if problems_solved == 0 and overall_score == 0 and not name:
            # Try one more pattern for Next.js specific "score":2 structure without quotes
            # seen in the user provided HTML: "score":2
            # Note: The user HTML showed: "score":2
            
            # Let's add direct JSON patterns
            if overall_score == 0:
                m = re.search(r'"score":(\d+)', user_section)
                if m: overall_score = int(m.group(1))
            
            if problems_solved == 0:
                m = re.search(r'"total_problems_solved":(\d+)', user_section)
                if m: problems_solved = int(m.group(1))
                
            if not name:
                m = re.search(r'"name":"([^"]+)"', user_section)
                if m: name = m.group(1)

        # Build response
        if not name and problems_solved == 0:
            return None
            
        data = {
            "username": username,
            "profile_url": url,
            "name": name,
            "profile_image_url": profile_image,
            "institution": institution,
            "organization": organization,
            "designation": designation,
            "school": school if school else None,
            "overall_coding_score": overall_score,
            "monthly_score": monthly_score,
            "total_problems_solved": problems_solved,
            "institute_rank": institute_rank,
            "pod_solved_current_streak": pod_current_streak,
            "pod_solved_longest_streak": pod_longest_streak,
            "pod_solved_global_longest_streak": pod_global_longest,
            "pod_correct_submissions_count": pod_submissions,
            "is_campus_ambassador": is_campus_ambassador,
            "created_date": created_date,
        }
        
        return data

    except Exception as e:
        print(f"Error fetching profile: {str(e)}")
        return None
