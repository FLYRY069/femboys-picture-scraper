from tls_client import Session

class DiscordSession:
    """
    Cookies.

    Attributes:
        session (Session): An instance of tls_client

    Methods:
        __init__: Initializes, with a gven client identifier and random tls extension order. (If provided)
        get_cookies: Retrieves cookies from the Discord API session.

    """

    def __init__(self, client_identifier="chrome_115", random_tls_extension_order=True):
        """
        Initializes a new DiscordSession.

        Parameters:
            client_identifier (str): The client identifier to use for the session; Default is chrome_115
            random_tls_extension_order (bool): Flag to randomize tls order. Default is true
        """
        self.session = Session(client_identifier=client_identifier, random_tls_extension_order=random_tls_extension_order)

    def get_cookies(self) -> tuple:
        """
        Get cookies from the session.

        Returns:
            tuple: Tuple containing (__dcfduid, __sdcfduid, __cfruid)

        """
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.5",
            "connection": "keep-alive",
            "host": "canary.discord.com",
            "referer": "https://canary.discord.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
            "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
        }
        response = self.session.get(
            "https://canary.discord.com/api/v9/experiments", headers=headers
        )
        x = response.cookies.get("__dcfduid")
        y = response.cookies.get("__sdcfduid")
        z = response.cookies.get("__cfruid")
        return x, y, z


def get_cookies() -> tuple:
    session = DiscordSession()
    x, y, z = session.get_cookies()
    return x, y, z

if __name__ == "__main__":
    cookies = DiscordSession().get_cookies()
    print(cookies)