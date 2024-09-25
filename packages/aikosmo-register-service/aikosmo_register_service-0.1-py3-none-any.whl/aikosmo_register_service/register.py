import os
import asyncio
from supabase import create_client, Client
from typing import Optional

def get_cloud_run_url() -> Optional[str]:
    service_name = os.environ.get('K_SERVICE')
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    if service_name and project_id:
        return f"https://{service_name}-{project_id}.run.app"
    return None

def initialize_supabase() -> Optional[Client]:
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        return create_client(supabase_url, supabase_key)
    return None

async def login_and_upsert_url(supabase: Client, url: str, service_name: str):
    email = os.environ.get('SUPABASE_EMAIL')
    password = os.environ.get('SUPABASE_PASSWORD')

    if not (email and password):
        print("Supabase email or password not found in environment variables")
        return

    try:
        await supabase.auth.sign_in_with_password({"email": email, "password": password})

        data, error = await supabase.table('microservices').upsert({
            'url': url,
            'name': service_name
        }, on_conflict='name').execute()

        if error:
            print(f"Error upserting data: {error}")
        else:
            print(f"Successfully upserted URL for service {service_name}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

async def register_service():
    url = get_cloud_run_url()
    if not url:
        print("Not running on Cloud Run or unable to determine the URL")
        return

    supabase = initialize_supabase()
    if not supabase:
        print("Unable to initialize Supabase client")
        return

    service_name = os.environ.get('K_SERVICE')
    if not service_name:
        print("K_SERVICE environment variable not found")
        return

    await login_and_upsert_url(supabase, url, service_name)

def register():
    asyncio.run(register_service())
