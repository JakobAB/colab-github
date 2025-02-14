import os
import sys
from google.colab import drive

def github_auth(persistent_key: bool):
  """
  Authenticate with GitHub to access private repo. This function will 
  detect if there is `id_ed25519` key SSH profile. If not, it will create
  one. 
  - `persistent_key`: Store private key in Google Drive.
  """
  
  os.system("mkdir -p ~/.ssh")

  if persistent_key:
    drive.mount('/content/drive/')
    private_key_dir = "/content/drive/MyDrive/.colab-github"
    os.system(f"mkdir -p {private_key_dir}")
  else:
    private_key_dir = "~/.ssh"

  private_key_path = private_key_dir + "/id_ed25519"
  public_key_path = private_key_path + ".pub"

  if not os.path.exists(os.path.expanduser(private_key_path)):
    fresh_key = True
    os.system(f"ssh-keygen -t ed25519 -f {private_key_path} -N ''")
  else:
    fresh_key = False

  if persistent_key:
    os.system("rm -f ~/.ssh/id_ed25519")
    os.system("rm -f ~/.ssh/id_ed25519.pub")
    os.system(f"cp -s {private_key_path} ~/.ssh/id_ed25519")
    os.system(f"cp -s {public_key_path} ~/.ssh/id_ed25519.pub")

  with open(os.path.expanduser(public_key_path), "r") as f:
    public_key = f.read()
    if fresh_key:
      print("Please go to https://github.com/settings/ssh/new to upload the following key: ")
      print("After adding the key to github, please re-execute this code!")
    else:
      print("Looks like a private key was already created. If you already entered it into github, no action is required."
      "\n Otherwise, Please go to https://github.com/settings/ssh/new and upload the following key: ")
    print(public_key)

  # add github to known hosts (you may hardcode it to prevent MITM attacks)
  os.system("ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts")

  os.system("chmod go-rwx ~/.ssh/id_ed25519")


def validate_repositories(repositories: list):
  assert isinstance(repositories, list), f"repositories has to be a list, not {type(repositories)=}"
  for repo in repositories:
    assert isinstance(repo, str), f"repository list elements have to be strings, not {type(repo)=}"


def clone_repositories(repositories: list):
  for repo in repositories:
    print(f"Cloning {repo}...")
    repo_addr = f"git@github.com:{repo}.git" # use SSH method to clone repo
    os.system(f"git clone {repo_addr}")


def add_repositories_to_path(repositories: list):
  print("Add repositories to path...")
  for repo in repositories:
    github_user, repo_name = repo.split("/")
    sys.path.insert(0, f'/content/{repo_name}')


def setup(repositories):
  github_auth(persistent_key=True)
  validate_repositories(repositories)
  clone_repositories(repositories)
  add_repositories_to_path(repositories)
  print("Finished setup!")
