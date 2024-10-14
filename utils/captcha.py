import httpx
import time
from .logger import Logger


class TaskPayload:
    """
    For the request payload for captcha solving

    Attributes:
        solver (str): The client key for capmonster.
        rqdata (dict): Request data required for solving the captcha.
        site_key (str): The site key of the website.
        websiteURL (str): The url of the website.
        useragent (str): The user agent to be used.
    """

    def __init__(self, solver, rqdata, site_key, websiteURL, useragent):
        """
        Initializes the TaskPayload object.

        Args:
            solver (str): The client key for capmonster.
            rqdata (dict): Request data required for solving the captcha.
            site_key (str): The site key of the website.
            websiteURL (str): The url of the website.
            useragent (str): The user agent to be used.
        """
        self.solver = solver
        self.rqdata = rqdata
        self.site_key = site_key
        self.websiteURL = websiteURL
        self.useragent = useragent

    def to_dict(self):
        """
        Convert task payload to dict

        Returns:
            dict: A dictionary for task payload.
        """
        return {
            "clientKey": self.solver,
            "task": {
                "type": "HCaptchaTaskProxyless",
                "isInvisible": True,
                "data": self.rqdata,
                "websiteURL": self.websiteURL,
                "websiteKey": self.site_key,
                "userAgent": self.useragent,
            },
        }


class CaptchaWrapper:
    """
    Handler/Wrapper
    """

    def __init__(self):
        """
        Initializes
        """
        self.logger = Logger()

    def solve(self, task_payload, log=True) -> str:
        """
        Solve capcha

        Args:
            task_payload (TaskPayload): Payload for captcha solver
            log (bool): Flag to debug the solvers output

        Returns:
            str: The solved captcha token.
        """
        key = None
        with httpx.Client(
            headers={"content-type": "application/json", "accept": "application/json"},
            timeout=30,
        ) as client:
            task_id = client.post(
                f"https://api.capmonster.cloud/createTask", json=task_payload.to_dict()
            ).json()["taskId"]
            get_task_payload = {
                "clientKey": task_payload.solver,
                "taskId": task_id,
            }

            while key is None:
                response = client.post(
                    "https://api.capmonster.cloud/getTaskResult", json=get_task_payload
                ).json()
                try:
                    if response["status"] == "ready":
                        key = response["solution"]["gRecaptchaResponse"]
                        if log:
                            self.logger.inf(
                                "Solved a captcha",
                                solution=f"{key[:min(len(token), 40)]}******",
                            )
                    else:
                        time.sleep(1)
                except Exception as e:
                    self.logger.err(
                        "Error solving captcha",
                        err=e,
                    )
                    return None

        return key


def solve(solver, rqdata, site_key, websiteURL, useragent, log=True) -> str:
    """
    Function to solve a captcha.

    Args:
        solver (str): The client key for capmonster.
        rqdata (dict): Request data required for solving the captcha.
        site_key (str): The site key of the website.
        websiteURL (str): The url of the website.
        useragent (str): The user agent to be used.
        log (bool): Flag indicating whether to log solving process or not. Default is True.

    Returns:
        str: Captcha key
    """
    payload = TaskPayload(solver, rqdata, site_key, websiteURL, useragent)
    wrapper = CaptchaWrapper()
    return wrapper.solve(payload, log)

if __name__ == "__main__":
    solve("1123", "1123", "1123", "1123", "1123")