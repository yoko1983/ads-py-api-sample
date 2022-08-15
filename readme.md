# 準備
GitHubよりcloneし、プログラムを実行できるように準備を行う

`cd [work_dir]`

`git clone https://github.com/yoko1983/ads-py-api-sample.git`

`cd azuredevops/`

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

# トークンを作成
AzureDevOps上で、WorkItem/GitRepoの参照・更新権のトークンを作成する

# アプリケーション設定ファイルを作成
settings_app.jsonを作成する。

`vi [work_dir]/azuredevops/settings_app.json`


```
{
    "ads": {
        "url_core": "https://dev.azure.com/",
        "organization": "xxxx",
        "project": "yyyy",
        "id": "zzzzz",
        "pw": "tttttttttttttttttttttttttttttt",
        "api_version": "6.0"
    } 
}
```

# 実行
```python3 ./work_item.py```