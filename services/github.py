import requests


def get_branch_info(repo, branch_name):
    url = (
        f"https://api.github.com/repos/s1mbi0se/{repo}/branches/{branch_name}"
    )
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Bearer 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",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        branch_data = response.json()
        author = branch_data["commit"]["author"]["login"]
        return get_real_name(author)
    else:
        return None, None


def get_real_name(name):
    if name == "rafaelmgbh":
        return "Rafael Santos"
    elif name == "joaokax":
        return "Jõao Lucas"
    elif name == "carlosjeff":
        return "Carlos Jefferson"
    elif name == "PauloFMartins485":
        return "Paulo Martins"
    else:
        return "Não foi possível obter o nome do autor"
