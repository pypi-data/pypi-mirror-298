import os
import subprocess

# Define the expected repositories
EXPECTED_REPOS = [
    "lcdm",
    "mnu",
    "mnu-3states",
    "ede",
    "neff",
    "wcdm"
]

# Base URL for the repositories
BASE_URL = "https://github.com/cosmopower-organization/"

def check_repos_in_dir(directory):
    """Check if all expected repositories are present in the directory."""
    return all(os.path.exists(os.path.join(directory, repo)) for repo in EXPECTED_REPOS)

def set_cosmopower_env(path):
    """Set the PATH_TO_COSMOPOWER_ORGANIZATION environment variable."""
    os.environ["PATH_TO_COSMOPOWER_ORGANIZATION"] = path
    print(f"PATH_TO_COSMOPOWER_ORGANIZATION is set to {path}")

def delete_pkl_files(directory):
    """Recursively find and delete all .pkl files in the directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pkl"):
                file_path = os.path.join(root, file)
                print(f"Deleting: {file_path}")
                os.remove(file_path)
                
def set():
    # Check if PATH_TO_COSMOPOWER_ORGANIZATION is already set
    path_to_cosmopower = os.getenv("PATH_TO_COSMOPOWER_ORGANIZATION")

    if path_to_cosmopower:
        # Avoid appending 'cosmopower-organization' multiple times
        if not path_to_cosmopower.endswith("cosmopower-organization"):
            path_to_cosmopower = os.path.join(path_to_cosmopower, "cosmopower-organization")
        print(f"Using PATH_TO_COSMOPOWER_ORGANIZATION: {path_to_cosmopower}")

        # Check if the directory exists; if not, fall back to default
        if not os.path.exists(path_to_cosmopower):
            print(f"Directory {path_to_cosmopower} does not exist. Falling back to default path.")
            path_to_cosmopower = None
    else:
        print("PATH_TO_COSMOPOWER_ORGANIZATION not set.")

    # If no valid path is set or if the path didn't exist, fall back to the default
    if not path_to_cosmopower:
        home_dir = os.path.expanduser("~")
        path_to_cosmopower = os.path.join(home_dir, "cosmopower-organization")
        print(f"Defaulting to: {path_to_cosmopower}")

    # Now check if the cosmopower-organization directory exists and contains the expected repositories
    if os.path.exists(path_to_cosmopower) and check_repos_in_dir(path_to_cosmopower):
        print(f"Found cosmopower-organization directory with all repositories at: {os.path.realpath(path_to_cosmopower)}")
        
        # Set the environment variable if it's not already set
        current_path = os.getenv("PATH_TO_COSMOPOWER_ORGANIZATION")
        if current_path != path_to_cosmopower:
            print("PATH_TO_COSMOPOWER_ORGANIZATION is not correctly set. Setting it now...")
            set_cosmopower_env(path_to_cosmopower)
        else:
            print("PATH_TO_COSMOPOWER_ORGANIZATION is already correctly set.")
    else:
        print("--> cosmopower-organization directory or repositories not found. Cloning repositories in your system!")

        # Create the cosmopower-organization directory if it doesn't exist
        if not os.path.exists(path_to_cosmopower):
            os.mkdir(path_to_cosmopower)

        os.chdir(path_to_cosmopower)

        # Clone all repositories using EXPECTED_REPOS and BASE_URL
        for repo in EXPECTED_REPOS:
            repo_url = os.path.join(BASE_URL, f"{repo}.git")
            subprocess.run(["git", "clone", repo_url])

        # After cloning, delete all .pkl files
        for repo in EXPECTED_REPOS:
            repo_path = os.path.join(path_to_cosmopower, repo)
            delete_pkl_files(repo_path)

        # Set the environment variable
        set_cosmopower_env(path_to_cosmopower)
