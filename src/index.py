import boto3
import json
import os

'''
fa : from address
da : destination address
rta : replay to address
title : the title of the email
body : the main contents of the email
'''


def build_mail_info_to_company(name, text, email, envs):
    return {
        "fa": envs['CompanyMailAddress'],
        "da": envs['CompanyMailAddress'],
        "rta": email,
        "title": f"{envs['CorporateSiteDomain']}へのお問い合わせ",
        "body": f"<html><body><h3>{name}様からのお問い合わせ</h3><p>メールアドレス：{email}</p><p>本文：{text}</p></body></html>",
    }


def build_mail_info_to_customer(name, text, email, envs):
    return {
        "fa": envs['CompanyMailAddress'],
        "da": email,
        "title": "お問い合わせありがとうございます。",
        "body": (f"<b>{name}様</b><br><br>"
                 f"こんにちは、{envs['CompanyName']}です。<br>"
                 "この度は弊社コーポレートサイトにてお問い合わせいただき、誠にありがとうございます。<br>"
                 "以下の通り承りましたことをご連絡させていただきます。<br>"
                 "担当者が確認し次第、折り返しご連絡いたしますので、今しばらくお待ち下さい。<br><br>"
                 "----<br>"
                 f"{text}<br>"
                 "----<br>")
    }


def send_mail(mail_info, endpoint_url):
    client = boto3.client("ses", region_name="us-east-1",
                          endpoint_url=endpoint_url)

    is_email_verified = mail_info["fa"] in client.list_identities(
        IdentityType='EmailAddress')['Identities']

    if not is_email_verified:
        client.verify_email_identity(EmailAddress=mail_info["fa"])

    if mail_info.get("rta") is None:

        return client.send_email(
            Source=mail_info["fa"],
            Destination={'ToAddresses': [mail_info["da"]]},
            Message={
                'Subject': {
                    'Data': mail_info["title"]
                },
                'Body': {
                    'Html': {
                        'Data': mail_info["body"]
                    }
                }
            },
        )
    else:
        return client.send_email(
            Source=mail_info["fa"],
            Destination={'ToAddresses': [mail_info["da"]]},
            Message={
                'Subject': {
                    'Data': mail_info["title"]
                },
                'Body': {
                    'Html': {
                        'Data': mail_info["body"]
                    }
                }
            },
            ReplyToAddresses=[mail_info["rta"]]
        )


def getEnvs():
    return {
        'CompanyMailAddress': os.environ['CompanyMailAddress'],
        'CompanyName': os.environ['CompanyName'],
        'CorporateSiteDomain': os.environ['CorporateSiteDomain'],
        "SesEndpointUrl": os.environ['SesEndpointUrl']
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        envs = getEnvs()

        send_mail(build_mail_info_to_company(
            body['name'], body['text'], body['email'], envs), envs['SesEndpointUrl'])

        send_mail(build_mail_info_to_customer(
            body['name'], body['text'], body['email'], envs), envs['SesEndpointUrl'])

        return {'body': 'success', 'statusCode': 200}
    except:
        import traceback
        traceback.print_exc()
        return {'body': 'internal server error', 'statusCode': 500}
