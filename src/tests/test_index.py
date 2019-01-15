import unittest

from .. import index as main


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.mail_info = {
            "name": "user",
            "text": "I want to ask one question. Are you hangry?",
            "email": "example@example.com"
        }

        self.envs = {
            'CompanyMailAddress': 'example@example.com',
            'CompanyName': 'company',
            'CorporateSiteDomain': 'example.com'
        }

    def test_build_mail_info_to_company(self):
        expect = {
            "fa": self.envs['company_mail_address'],
            "da": self.envs['company_mail_address'],
            "rta": self.mail_info["email"],
            "title": f"{self.envs['corporate_site_domain']}へのお問い合わせ",
            "body": f"<html><body><h3>{self.mail_info['name']}様からのお問い合わせ</h3><p>メールアドレス：{self.mail_info['email']}</p><p>本文：{self.mail_info['text']}</p></body></html>",
        }
        self.assertEqual(main.build_mail_info_to_company(
            self.mail_info["name"], self.mail_info["text"], self.mail_info["email"], self.envs), expect)

    def test_build_mail_info_to_customer(self):
        expect = {
            "fa": self.envs["company_mail_address"],
            "da": self.mail_info["email"],
            "title": "お問い合わせありがとうございます。",
            "body": (f"<b>{self.mail_info['name']}様</b><br><br>"
                     f"こんにちは、{self.envs['company_name']}。<br>"
                     "この度は弊社コーポレートサイトにてお問い合わせいただき、誠にありがとうございます。<br>"
                     "以下の通り承りましたことをご連絡させていただきます。<br>"
                     "担当者が確認し次第、折り返しご連絡いたしますので、今しばらくお待ち下さい。<br><br>"
                     "----<br>"
                     f"{self.mail_info['text']}<br>"
                     "----<br>")
        }
        self.assertEqual(main.build_mail_info_to_customer(
            self.mail_info["name"], self.mail_info["text"], self.mail_info["email"], self.envs), expect)


if __name__ == "__main__":
    unittest.main()
