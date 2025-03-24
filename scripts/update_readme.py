import json

def update_readme():
    with open("repo_stats.json") as f:
        stats = json.load(f)
    
    if not stats:
        return

    with open("README.md", "r") as f:
        content = f.read()
    
    # Gera o badge da linguagem
    if stats["main_language"]:
        lang_badge = (
            f"![{stats['main_language']}]"
            f"(https://img.shields.io/badge/{stats['main_language']}-{stats['language_percent']}%25-blue)"
        )
    else:
        lang_badge = "No language detected"

    updated_content = content.replace(
        "<!-- LAST_UPDATE -->", stats["updated_at"]
    ).replace(
        "<!-- REPO_INFO -->",
        f"**[{stats['repo_name']}]({stats['repo_url']})** | {lang_badge}"
    )
    
    with open("README.md", "w") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()