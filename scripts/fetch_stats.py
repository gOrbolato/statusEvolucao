import os
import requests
import json
from datetime import datetime


def get_brasilia_time():
    return datetime.now(tz.gettz('America/Sao_Paulo')).strftime("%d/%m/%Y %H:%M")

def get_last_repo_data(username):
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Busca o último repositório não-fork
    repos = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers=headers,
        params={
            "sort": "updated",
            "direction": "desc",
            "per_page": 1
        }
    ).json()
    
    if not repos:
        return None
    
    last_repo = repos[0]
    languages = requests.get(last_repo['languages_url'], headers=headers).json()
    total_bytes = sum(languages.values())
    
    return {
        "updated_at": get_brasilia_time(),
        "repo_name": last_repo['name'],
        "repo_url": last_repo['html_url'],
        "main_language": max(languages.items(), key=lambda x: x[1])[0] if languages else None,
        "language_percent": round(max(languages.values())/total_bytes*100, 1) if languages else None
    }

if __name__ == "__main__":
    data = get_last_repo_data("gOrbolato")
    with open("repo_stats.json", "w") as f:
        json.dump(data, f, indent=2)