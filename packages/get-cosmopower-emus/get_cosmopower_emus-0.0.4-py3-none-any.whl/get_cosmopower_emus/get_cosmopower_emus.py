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

def check_repos_in_dir(directory):
    """Check if all expected repositories are present in the directory."""
    return all(os.path.exists(os.path.join(directory, repo)) for repo in EXPECTED_REPOS)

def set_cosmopower_env(path):
    """Set the PATH_TO_COSMOPOWER_ORGANIZATION environment variable and save it to a file."""
    # Set the environment variable
    os.environ["PATH_TO_COSMOPOWER_ORGANIZATION"] = path

    # # Write environment setup to a file
    # mdir = os.path.dirname(os.path.realpath(__file__))
    # with open(os.path.join(mdir, "..", "set_class_sz_env.sh"), "w") as f:
    #     f.write(f"export PATH_TO_COSMOPOWER_ORGANIZATION={path}\n")

    print(f"PATH_TO_COSMOPOWER_ORGANIZATION is set to {path}")

def set():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Look for the cosmopower-organization directory in the home directory
    cosmopower_dir = os.path.join(home_dir, "cosmopower-organization")

    if os.path.exists(cosmopower_dir) and check_repos_in_dir(cosmopower_dir):
        print(f"Found cosmopower-organization directory with all repositories at: {os.path.realpath(cosmopower_dir)}")
        path_to_cosmopower = os.path.realpath(cosmopower_dir)

        # Check if PATH_TO_COSMOPOWER_ORGANIZATION is already set correctly
        current_path = os.getenv("PATH_TO_COSMOPOWER_ORGANIZATION")
        if current_path != path_to_cosmopower:
            print("PATH_TO_COSMOPOWER_ORGANIZATION is not correctly set. Setting it now...")
            print(f"Current PATH_TO_COSMOPOWER_ORGANIZATION: {current_path}")
            print(f"New PATH_TO_COSMOPOWER_ORGANIZATION: {path_to_cosmopower}")
            set_cosmopower_env(path_to_cosmopower)
        else:
            print("PATH_TO_COSMOPOWER_ORGANIZATION is already correctly set.")
    else:
        print("--> cosmopower-organization directory or repositories not found. Cloning repositories in your home directory!")

        # Create the cosmopower-organization directory if it doesn't exist
        if not os.path.exists(cosmopower_dir):
            os.mkdir(cosmopower_dir)

        os.chdir(cosmopower_dir)

        # Clone all repositories
        repos = [
            "https://github.com/cosmopower-organization/lcdm.git",
            "https://github.com/cosmopower-organization/mnu.git",
            "https://github.com/cosmopower-organization/mnu-3states.git",
            "https://github.com/cosmopower-organization/ede.git",
            "https://github.com/cosmopower-organization/neff.git",
            "https://github.com/cosmopower-organization/wcdm.git"
        ]

        for repo in repos:
            subprocess.run(["git", "clone", repo])

        # After cloning, set the environment variable
        path_to_cosmopower = os.path.realpath(cosmopower_dir)
        set_cosmopower_env(path_to_cosmopower)

# if __name__ == "__main__":
#     main()
