import os
import random
from github import Github


def fetch_random_github_repo():
    # Get the GitHub token from the environment variable
    access_token = os.environ.get('GITHUB_TOKEN')

    # Create a PyGitHub instance using the access token
    g = Github(access_token)

    # Get the authenticated user
    user = g.get_user()

    # Fetch all repositories of the authenticated user
    repositories = user.get_repos()

    # Select a random repository
    selected_repo = random.choice(list(repositories))

    return selected_repo


def fetch_random_code_from_repo(repository):
    # Get the default branch of the repository
    default_branch = repository.default_branch

    # Get the contents of the default branch
    contents = repository.get_contents("", ref=default_branch)

    # Filter out non-code files
    code_files = [file for file in contents if file.type ==
                  "file" and file.path.endswith(".py")]

    # Select a random code file
    selected_file = random.choice(code_files)

    # Get the code from the selected file
    code = selected_file.decoded_content.decode()

    return code


def generate_haiku_from_github_repo():
    # Fetch a random GitHub repository
    selected_repo = fetch_random_github_repo()

    # Get random code from the repository
    code = fetch_random_code_from_repo(selected_repo)

    # Generate haiku using the code
    haiku = generate_haiku_from_code(code)

    return haiku
