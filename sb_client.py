import json
from supabase import create_client, Client

def create_supabase_client() -> Client:
    with open('supabase.json', 'r') as supabase_json:
        supabase_data = json.load(supabase_json)
    
    supabase = create_client(supabase_data['supabase_url'], supabase_data['supabase_key'])
    return supabase