import requests
import os
import sys

def get_organizations(api_token, api_version):
    """Fetches all organizations the user has access to."""
    url = f"https://api.snyk.io/rest/orgs?version={api_version}"
    headers = {
        "Authorization": api_token,
        "Accept": "application/vnd.api+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return [{"id": org["id"], "name": org["attributes"]["name"]} for org in data]
    else:
        print(f"Error fetching organizations: {response.status_code}")
        return None

def snyk_cleanup():
    # 1. Setup Configuration
    api_token = os.getenv('SNYK_TOKEN')
    if not api_token:
        print("Error: Please set the SNYK_TOKEN environment variable.")
        sys.exit(1)

    api_version = "2024-10-15"
    
    # Check for Dry Run flag
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("🛠 DRY RUN MODE ENABLED: No targets will be deleted.")

    # 2. Select Organization
    orgs = get_organizations(api_token, api_version)
    if not orgs:
        print("No organizations found or failed to authenticate.")
        return

    print("\nAvailable Organizations:")
    for idx, org in enumerate(orgs, 1):
        print(f"{idx}. {org['name']} ({org['id']})")

    try:
        choice = int(input(f"\nSelect an organization (1-{len(orgs)}): "))
        selected_org = orgs[choice - 1]
        org_id = selected_org['id']
        print(f"Selected: {selected_org['name']}")
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        return

    # 3. Fetch All Targets
    headers = {
        "Authorization": api_token,
        "Accept": "application/vnd.api+json"
    }
    
    base_url = f"https://api.snyk.io/rest/orgs/{org_id}/targets"
    target_list = []
    next_url = f"{base_url}?version={api_version}&limit=100"

    print(f"\nFetching targets for {selected_org['name']}...")
    
    while next_url:
        if not next_url.startswith("http"):
            next_url = f"https://api.snyk.io{next_url}"

        response = requests.get(next_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching targets: {response.status_code}")
            break
            
        json_data = response.json()
        for item in json_data.get('data', []):
            target_list.append({
                "id": item['id'],
                "name": item['attributes'].get('display_name', 'Unknown')
            })
        next_url = json_data.get('links', {}).get('next')

    if not target_list:
        print("No targets found in this organization.")
        return

    # 4. Confirmation and Deletion
    print("\n" + "!" * 40)
    if dry_run:
        print(f"DRY RUN: Would have deleted {len(target_list)} targets in {selected_org['name']}.")
        for target in target_list:
            print(f"  [WOULD DELETE] {target['name']}")
        print("\nDry run complete. No changes were made.")
        return

    print(f"DANGER: You are about to DELETE ALL {len(target_list)} targets")
    print(f"in organization: {selected_org['name']}")
    confirm = input("Are you sure? (type 'yes' to proceed): ")
    print("!" * 40 + "\n")

    if confirm.lower() == 'yes':
        for target in target_list:
            print(f"Deleting {target['name']}...", end=" ", flush=True)
            delete_url = f"{base_url}/{target['id']}?version={api_version}"
            del_response = requests.delete(delete_url, headers=headers)
            
            if del_response.status_code == 204:
                print("✅ Success")
            else:
                print(f"❌ Failed ({del_response.status_code})")
        print("\nCleanup finished.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    snyk_cleanup()
