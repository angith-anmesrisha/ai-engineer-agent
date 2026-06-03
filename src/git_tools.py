import os
import subprocess
from github import Github

class JarvisGitEngine:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.github_token = os.getenv("GITHUB_TOKEN")
        # Extract owner/repo from path if needed, fallback to active default
        self.repo_name = os.getenv("GITHUB_REPO", "angith-anmesrisha/ai-engineer-agent")

    def deploy_patch_to_remote_cluster(self, branch_name: str, commit_message: str):
        """[Reactive Mode Fallback] Stages, commits, and pushes to a specific branch on the core agent repo."""
        print(f"🚀 [JARVIS Git] Securing localized snapshot tracking lines on branch: {branch_name}...")
        try:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True, cwd=self.repo_path)
            subprocess.run(["git", "add", "."], check=True, cwd=self.repo_path)
            subprocess.run(["git", "commit", "-m", commit_message], check=True, cwd=self.repo_path)
            subprocess.run(["git", "push", "-u", "origin", branch_name], check=True, cwd=self.repo_path)
            print("✅ [JARVIS Git] Branch updates synced successfully upstream.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git tracking command sequence rejected. Forcing alternative execution parameters: {e}")

    def submit_pull_request(self, branch_name: str, title: str, description: str):
        """[Reactive Mode Fallback] Files a Pull Request specifically against the master branch of the agent repo."""
        if not self.github_token:
            return None
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        try:
            pr = repo.create_pull(title=title, body=description, head=branch_name, base="master")
            return pr.html_url
        except Exception as api_err:
            print(f"⚠️ PR tracking bypass: {api_err}")
            return None

    def initialize_and_push_new_repo(self, local_project_path: str, repo_name: str, description: str) -> str:
        """
        [PROACTIVE CREATOR MODE] Creates a brand-new repository on your personal GitHub account,
        initializes local git completely isolated from the agent, and pushes directly to 'main'.
        """
        if not self.github_token:
            raise Exception("CRITICAL: GITHUB_TOKEN missing from system environment matrices.")

        g = Github(self.github_token)
        user = g.get_user()
        clean_repo_name = repo_name.replace(" ", "-").replace(":", "").lower()

        # 1. Create the brand-new repository on your cloud profile
        try:
            print(f"🌐 [JARVIS Cloud] Instantiating a pristine GitHub repository: '{clean_repo_name}'...")
            repo = user.create_repo(name=clean_repo_name, description=description, private=False, auto_init=False)
            repo_html_url = repo.html_url
        except Exception as e:
            print(f"ℹ️ Repository might already exist online, fetching data node references... {e}")
            repo = user.get_repo(clean_repo_name)
            repo_html_url = repo.html_url

        # 2. Initialize isolated local git variables inside the creation target path
        print(f"🏗️ [JARVIS Git] Executing local Git initialization for isolated scope at: {local_project_path}")
        try:
            # Reconstruct the remote authenticated path safely
            authenticated_url = f"https://{self.github_token}@github.com/{user.login}/{clean_repo_name}.git"
            
            subprocess.run(["git", "init"], check=True, cwd=local_project_path, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True, cwd=local_project_path, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, cwd=local_project_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"feat(jarvis): initial release architecture for {repo_name}"], check=True, cwd=local_project_path, capture_output=True)
            
            # Check if remote origin already exists, reset it if true, else add it cleanly
            check_remote = subprocess.run(["git", "remote"], cwd=local_project_path, capture_output=True, text=True)
            if "origin" in check_remote.stdout:
                subprocess.run(["git", "remote", "set-url", "origin", authenticated_url], check=True, cwd=local_project_path, capture_output=True)
            else:
                subprocess.run(["git", "remote", "add", "origin", authenticated_url], check=True, cwd=local_project_path, capture_output=True)
                
            print(f"🛰️ [JARVIS Cloud] Pushing core code matrix directly to remote tracking repository link...")
            subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True, cwd=local_project_path, capture_output=True)
            
            return repo_html_url
        except subprocess.CalledProcessError as err:
            raise Exception(f"Isolated shell Git runtime sequence rejected: {err.stderr.decode('utf-8', errors='ignore')}")