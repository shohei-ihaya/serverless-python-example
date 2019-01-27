# Serverless-python-template

## Caution

現在、codebuild 上で `sam local invoke` がうまく動かない問題が発生しているので、codebuild 上で実行するコマンド群を書き記した `buildspec.yml` からインテグレーションテストのコマンドは抜いてある。
ローカルだと普通に動く。

## Outline

このリポジトリは、lambda 関数の unit テスト、インテグレーションテスト、デプロイを自動化するテンプレートして作成されたものです。
主に使用している技術は以下です。

- Codebuild

  - github や bitbackt のリポジトリ上のコードを使って CI&CD を実現する。
  - AWS 内部のサービスなので、AWS のみ使うときは、circle ci とかよりも認証周りが楽な気もする。
  - code build local というものもあるので、実際 buildspec.yml を手元で動かすことができる。

- sam local

  - ローカルで lambda サーバーを立ち上げることができるもの。

- localstack

  - ローカルで AWS の各コンポーネントを docker 上に立ち上げることができる。
  - lambda 以外と連携する lamnda 関数のインテグレーションテストに使用できる。

- pipenv

  - Python のライブラリの管理ツール

- bats

  - shell コマンドでテストをかけるライブラリ。

## Setup

```bash
# Clone repo to your local environment
git clone [url of this repo]

# Install dependency of python
pipenv install

# Run test
pipenv run python -B -m unittest src/tests/test_index.py
pipenv run bats ./integration_test.sh

# Create Service role and codebuild project(including webhook settings)
bash ./codebuild_project/setup_codebuild_build_project.sh

# Run codebuild locally(Usually for debugging of buildspec.yml)
bash ./codebuild_build.sh -i aws/codebuild/python:3.7.1 -a artifact

# Deploy from local(Usually this isn't needed)
bash ./deploy.sh
```

## Requirements

- bats
- pipenv
- sam
- jq
- docker-componse

## Env variables

- FunctionName
- BucketName
- CompanyMailAddress
- CompanyName
- CorporateSiteDomain
- SesEndpointUrl(Currently, `https://email.us-east-1.amazonaws.com` )

### Local

We use `.env` file when deploy.
However, you should deploy from codebuild or other ci tool.

### CI

You can set env variables at each CI project.
