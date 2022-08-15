import settings
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.git.models import GitBaseVersionDescriptor
from azure.devops.v6_0.git.models import GitTargetVersionDescriptor
from azure.devops.v6_0.git.models import GitCommitDiffs
from azure.devops.v6_0.git.models import GitRepository
from azure.devops.v6_0.git.models import GitPullRequest
from logging import getLogger

logger = getLogger(__name__)

settings_data=settings.get_settings_app_data()

personal_access_token = settings_data['ads']['pw']
organization = settings_data['ads']['organization']
project=settings_data['ads']['project']
url_core=settings_data['ads']['url_core']
organization_url=url_core + organization

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
git_client = connection.clients.get_git_client()

def get_repo_id(repo_id :str) -> str:
    repo:GitRepository = git_client.get_repository(
        repository_id=repo_id, 
        project=project 
    )
    return repo.id


def get_repo_name(repo_id :str) -> str:
    repo:GitRepository = git_client.get_repository(
        repository_id=repo_id, 
        project=project 
    )
    return repo.name

def print_pr(pr_id:int):
    pr:GitPullRequest = git_client.get_pull_request_by_id(
        project=project, 
        pull_request_id=pr_id
    )
    print(str(pr.pull_request_id) + ': ' + pr.source_ref_name + ' => ' + pr.target_ref_name)

def print_repos():
    repos = git_client.get_repositories(project)
    for repo in repos:
        print(repo.id + ':' + repo.name)


def print_diffs(repo_id:str, base_version:str, target_version:str):
    diffs:GitCommitDiffs = git_client.get_commit_diffs( 
        repository_id=repo_id, 
        project=project, 
        top=100000, 
        base_version_descriptor=GitBaseVersionDescriptor(base_version=base_version),
        target_version_descriptor=GitTargetVersionDescriptor(target_version=target_version))

    changes = diffs.changes

    for change in changes:
        print(change['changeType'] + ':' + change['item']['path'])
    
