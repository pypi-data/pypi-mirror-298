import os
import shutil
import time

from dulwich.errors import GitProtocolError, NotGitRepository
from dulwich.objects import Commit
from dulwich.porcelain import clone
from dulwich.repo import Repo
from dulwich.walk import Walker


class NullWriter:
    """A class to suppress standard output and standard error."""

    def write(self, s):
        pass

    def flush(self):
        pass


class CodeCommitListCommits:
    def __init__(self, username: str, password: str, region: str, target_dir: str = "./tmp"):
        self.username = username
        self.password = password
        self.region = region
        self.target_dir = target_dir

    def _clone_repository(self) -> None:
        """Clone the repository to the target directory."""
        repo_url = f"https://git-codecommit.{self.region}.amazonaws.com/v1/repos/{self.repository_name}"
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        try:
            null_writer = NullWriter()
            clone(
                repo_url,
                target=self.target_dir,
                username=self.username,
                password=self.password,
                outstream=null_writer,
                errstream=null_writer,
            )
        except GitProtocolError as e:
            if "403" in str(e):
                print(f"Authentication error: Please check your username and password. \n{e}")
            else:
                print(f"Network error: Please check your network access. \n{e}")
            raise
        except NotGitRepository as e:
            print(f"Repository not found: Please check the region and the repository name. \n{e}")
            raise
        except Exception as e:
            print(f"Failed to clone repository: {e}")
            raise

    def _delete_repository(self) -> None:
        """Delete the cloned repository."""
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)

    def _extract_commit_details(self, commit: Commit) -> dict[str, str | list[str]]:
        """Extract details from a commit."""
        committer_name, committer_email = commit.committer.decode("utf-8").split("<")
        author_name, author_email = commit.author.decode("utf-8").split("<")
        return {
            "commit_id": commit.id.decode("utf-8"),
            "tree_id": commit.tree.decode("utf-8"),
            "parent_ids": [parent.decode("utf-8") for parent in commit.parents],
            "author_name": author_name.strip(),
            "author_email": author_email.strip(">"),
            "author_date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(commit.commit_time)),
            "committer_name": committer_name.strip(),
            "committer_email": committer_email.strip(">"),
            "commit_date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(commit.commit_time)),
            "timezone_offset": commit.commit_timezone,
            "message": commit.message.decode("utf-8"),
        }

    def list_commits(self, repository_name: str, branch_name: str | None = None) -> list[dict[str, str | list[str]]]:
        self.repository_name = repository_name
        self._clone_repository()
        try:
            repo = Repo(self.target_dir)
            refs = repo.get_refs()
            if branch_name:
                branch_ref = f"refs/remotes/origin/{branch_name}".encode("utf-8")
                if branch_ref not in refs:
                    raise ValueError(f"Branch '{branch_name}' not found in the repository.")
                walker = Walker(repo, [refs[branch_ref]])
            else:
                walker = Walker(repo, [repo.head()])
            commits_list = [self._extract_commit_details(entry.commit) for entry in walker]
        except Exception as e:
            print(f"Failed to open repository: {e}")
            raise
        finally:
            self._delete_repository()
        return commits_list
