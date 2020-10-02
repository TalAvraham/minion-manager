"""
    Author  : Tal Avraham
    Created : 5/16/2020
    Purpose : Install files from a Github repository.
"""


# === Imports === #
from github import Github, GithubException
import config
import logging
import base64

# === Constants === #
ROOT_DIRECTORY = '.'


# === Exceptions === #
class RepoInstallError(BaseException):
    pass


# === Classes === #
class GithubRepoInstaller:
    """Github repository installer."""

    IGNORED_FILES = ["README.md", "config.py"]

    def __init__(self, github_repo_name, local_install_dir):
        self._github = Github(config.GITHUB_TOKEN)
        self._user = self._github.get_user()
        self._repo = self._get_repo(github_repo_name)
        self._install_dir = local_install_dir

    def install_latest_files(self):
        logging.info(f"Installing latest {self._repo.name} files from github.")
        try:
            self._install_repo()
            logging.info(f"Successfully installed {self._repo.name}.")
        except RepoInstallError:
            logging.error(f"Failed to install {self._repo.name}.")
            raise RepoInstallError

    def _get_repo(self, name):
        for repo in self._user.get_repos():
            if repo.name == name:
                return repo
        raise ValueError

    def _install_repo(self):
        for content_file in self._repo.get_contents(path=ROOT_DIRECTORY):
            try:
                self._process_content_file(content_file)
            except (GithubException, IOError) as error:
                logging.error(f"Error processing {content_file.path}: {error}")
                raise RepoInstallError

    def _process_content_file(self, content_file):
        logging.debug(f"Processing {content_file.path}.")
        if content_file.name not in self.IGNORED_FILES:
            self._install_content_file(content_file)

    def _get_install_path(self, content_file):
        return f"{self._install_dir}\\{content_file.path}"

    def _install_content_file(self, content_file):
        data = base64.b64decode(content_file.content)
        with open(self._get_install_path(content_file), "wb") as output_file:
            output_file.write(data)
