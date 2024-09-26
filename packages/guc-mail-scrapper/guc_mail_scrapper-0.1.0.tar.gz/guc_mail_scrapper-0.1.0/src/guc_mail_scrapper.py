from bs4 import BeautifulSoup
import requests

BASE_URL = "https://mail.guc.edu.eg/owa/"


class InvalidCredentialsError(Exception):
    pass


class ForwardEmailError(Exception):
    pass


class GucMailScrapper:
    def __init__(self, authenticated_session: requests.Session):
        self.authenticated_session = authenticated_session

    def get_authenticated_session(username: str, password: str) -> requests.Session:
        session = requests.Session()

        session.post(
            BASE_URL + "auth.owa",
            data={
                "destination": BASE_URL,
                "flags": "4",
                "forcedownlevel": "0",
                "username": username,
                "password": password,
            },
        )

        if not GucMailScrapper.is_authenticated(session):
            raise InvalidCredentialsError()

        return session

    def is_authenticated(session: requests.Session) -> bool:
        req = session.get(BASE_URL, allow_redirects=False)
        return req.text.find("Inbox") != -1

    def count_mail_pages(self) -> int:
        res = self.authenticated_session.get(BASE_URL)
        soup = BeautifulSoup(res.text, "html.parser")
        pages = soup.select(".pTxt")
        return len(pages)

    def get_mail_ids(self, page: int) -> list[str]:
        res = self.authenticated_session.get(f"{BASE_URL}?pg={page}")
        soup = BeautifulSoup(res.text, "html.parser")

        mails = [checkbox["value"] for checkbox in soup.select('input[name="chkmsg"]')]

        return mails

    def forward_mail(self, mail_id: str, forward_to: str):
        url_encoded_mail_id = requests.utils.quote(mail_id)
        read_url = f"{BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Forward&id={url_encoded_mail_id}"
        response = self.authenticated_session.get(read_url)

        soup = BeautifulSoup(response.text, "html.parser")

        inputs = {
            input["name"]: input["value"]
            for input in soup.select("input")
            if input.has_attr("name") and input.has_attr("value")
        }

        inputs["txtbdy"] = soup.select_one("#txtbdyldr").text
        inputs["txtsbj"] = soup.select_one("#txtsbjldr")["value"]
        inputs["txtto"] = forward_to
        inputs["hidcmdpst"] = "snd"

        forward_url = f"{BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Send"
        response = self.authenticated_session.post(forward_url, data=inputs)

        if response.status_code != 200:
            raise ForwardEmailError()
