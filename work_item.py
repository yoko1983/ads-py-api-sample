import datetime
import settings
import urllib
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import WorkItem
from azure.devops.v6_0.work_item_tracking.models import WorkItemRelation
from azure.devops.v6_0.work_item_tracking.models import WorkArtifactLink
from logging import getLogger

logger = getLogger(__name__)

settings_data=settings.get_settings_app_data()

personal_access_token = settings_data['ads']['pw']
organization = settings_data['ads']['organization']
project=settings_data['ads']['project']
url_core=settings_data['ads']['url_core']
organization_url=url_core + organization

work_item_field_date='Microsoft.VSTS.CodeReview.AcceptedDate'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
wit_client = connection.clients.get_work_item_tracking_client()

def convert_str_to_datetime(str: str) -> datetime:
    """

    文字列のISO8601のUTC（協定世界時）をdatetimeに変換

    Args:
        str (str): ISO8601のUTC（協定世界時）の文字列

    Returns:
        datetime

    """    
    # yyyymmddhhmmss.を設定
    yyyymmddhhmmss= str[:20]
    # SZ/SSZ/SSSZのうちZをトリムし、S/SS/SSSに対して固定値3桁でゼロパティングして設定
    sss=str[20:].replace('Z', '').rjust(3, '0')
    # yyyymmddhhmmss.SSS+00:00を返却
    return datetime.datetime.fromisoformat(yyyymmddhhmmss + sss + '+00:00')
    

def get_nowdate(work_item_id: int) -> datetime:
    """

    日付を取得する。

    Args:
        work_item_id (int): WorkItemのID

    Raises:
        RequestException: HttpRequestに失敗した場合

    Returns:
        datetime: 取得した日付

    """

    wi:WorkItem = wit_client.get_work_item(
        project=project,
        id=work_item_id)
    return wi.fields[work_item_field_date]

logger.info(get_nowdate(3))

def get_pr_id_dict(work_item_id: int) -> dict:
    """

    PRリンクよりPR辞書を取得する。

    Args:
        work_item_id (int): WorkItemのID

    Raises:
        RequestException: HttpRequestに失敗した場合

    Returns:
        PRID-リポジトリID辞書(key:pr_id(int), value:repo_id(str))

    """

    wi:WorkItem = wit_client.get_work_item(
        project=project,
        id=work_item_id,
        expand='all'
    )
    pr_dict = {}
    for relation in wi.relations:
        relation:WorkItemRelation =relation
        if relation.rel == 'ArtifactLink':
            rel:WorkArtifactLink = relation.rel
            if relation.attributes['name'] == 'Pull Request':
                pr_url = relation.url
                pr_url_base_len=len("vstfs:///Git/PullRequestId/")
                pr_url_parts = urllib.parse.unquote(pr_url[pr_url_base_len:])
                pr = pr_url_parts.split('/')
                pr_id=int(pr[2])
                repo_id=pr[1]
                pr_dict[pr_id] = repo_id

    return pr_dict

logger.info(get_pr_id_dict(3))