import json
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests


class MastoAPI:
    client_id = None
    client_secret = None
    grant_token = None
    instance_url = None

    def __init__(self):
        self.access_token = None
        self.api_keys = None
        self.read_config()

    def get_grant_token(self) -> None:
        url = f"{self.instance_url}/oauth/authorize?client_id={self.client_id}&scope=read+write+follow&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code"  # noqa: E501
        webbrowser.open_new_tab(url)

    def write_config(self) -> None:
        with open(Path(__file__).parent / "api_keys.json", "w") as f:
            self.api_keys["client_id"] = self.client_id
            self.api_keys["client_secret"] = self.client_secret
            self.api_keys["grant_token"] = self.grant_token
            self.api_keys["instance_url"] = self.instance_url
            self.api_keys["access_token"] = self.access_token
            json.dump(self.api_keys, f)

    def read_config(self) -> None:
        try:
            with open(Path(__file__).parent / "api_keys.json", "r") as f:
                self.api_keys = json.load(f)
        except FileNotFoundError:
            self.api_keys = {}
        self.client_id = self.api_keys.get("client_id")
        self.client_secret = self.api_keys.get("client_secret")
        self.grant_token = self.api_keys.get("grant_token")
        self.instance_url = self.api_keys.get("instance_url")
        if self.instance_url and not self.instance_url.startswith("https://"):
            self.instance_url = f"https://{self.instance_url}"
        self.access_token = self.api_keys.get("access_token")

    def verify_keys(self) -> bool:
        return self.api_keys and all(self.api_keys[elem] for elem in self.api_keys)

    def get_home_timeline(
        self, load_from: Optional[str] = None
    ) -> List[Dict[str, str]]:
        if load_from is not None:
            payload = {
                "max_id": load_from,
            }
        else:
            payload = {}
        resp = requests.get(
            f"{self.instance_url}/api/v1/timelines/home",
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_public_timeline(
        self,
        load_from: Optional[str] = None,
        local: bool = True,
    ) -> List[Dict[str, str]]:
        if local:
            url = f"{self.instance_url}/api/v1/timelines/public?local=true"
        else:
            url = f"{self.instance_url}/api/v1/timelines/public"
        if load_from is not None:
            payload = {
                "max_id": load_from,
            }
        else:
            payload = {}
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_local_timeline(
        self, load_from: Optional[str] = None
    ) -> List[Dict[str, str]]:
        return self.get_public_timeline()

    def get_global_timeline(
        self, load_from: Optional[str] = None
    ) -> List[Dict[str, str]]:
        return self.get_public_timeline(local=False)

    def get_access_token(self) -> None:
        url = f"{self.instance_url}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "code": self.grant_token,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "read write follow",
        }
        _, response = self.__call_url_post(url=url, data=data)
        self.api_keys["access_token"] = response.get("access_token")
        self.access_token = response.get("access_token")
        self.write_config()

    def __call_url_post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Union[str, Any, None]]] = None,
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        response = requests.post(
            url=url, headers={"Authorization": f"Bearer {self.access_token}"}, data=data
        )
        return response.status_code, response.json()

    def __call_url_get(self, url: str, headers: Optional[Dict[str, str]] = None):
        response = requests.get(
            url=url, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        return response.status_code, response.json()

    def favourite_post(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/favourite"
        return self.__call_url_post(url=url)

    def boost_post(self, post_id: str) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/reblog"
        return self.__call_url_post(url=url)

    def unfavourite_post(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/unfavourite"
        return self.__call_url_post(url=url)

    def unboost_post(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/unreblog"
        return self.__call_url_post(url=url)

    def bookmark_post(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/bookmark"
        return self.__call_url_post(url=url)

    def unbookmark_post(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/unbookmark"
        return self.__call_url_post(url=url)

    def get_account_by_id(self, account_id: str) -> Dict[str, str]:
        url = f"{self.instance_url}/api/v1/accounts/{account_id}"
        return self.__call_url_get(url=url)

    def get_post_by_id(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}"
        return self.__call_url_get(url=url)

    def get_post_context(
        self, post_id: str
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses/{post_id}/context"
        return self.__call_url_get(url=url)

    def add_post(
        self,
        post_content: str,
        visibility: str,
        sensitive: bool = False,
        content_warning: Optional[str] = None,
        poll_options: Optional[List[str]] = None,
        multiple_choice: bool = False,
        hide_total: bool = False,
        poll_expiration: int = 300,
        in_reply_to: Optional[str] = None,
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/statuses"
        data: Dict[str, Union[str, Any, None]] = {
            "status": post_content,
            "visibility": visibility,
        }
        if sensitive:
            data["sensitive"] = sensitive
            data["spoiler_text"] = content_warning
        if poll_options:
            data["poll[options][]"] = poll_options
            data["poll[expires_in]"] = poll_expiration
            data["poll[hide_totals]"] = hide_total
        if in_reply_to is not None:
            data["in_reply_to_id"] = in_reply_to
        return self.__call_url_post(url=url, data=data)

    def get_trending_posts(
        self,
        offset: Optional[int] = 0,
    ) -> List[Dict[str, str]]:
        url = f"{self.instance_url}/api/v1/trends/statuses"
        payload = {
            "offset": offset,
        }
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_posts_with_tag(
        self,
        tag_name: str,
        load_from: Optional[int] = None,
    ) -> List[Dict[str, str]]:
        if load_from is not None:
            payload = {
                "max_id": load_from,
            }
        else:
            payload = {}
        resp = requests.get(
            f"{self.instance_url}/api/v1/timelines/tag/{tag_name}",
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_trending_tags(
        self,
        offset: Optional[int] = 0,
    ) -> List[Dict[str, str]]:
        url = f"{self.instance_url}/api/v1/trends/tags"
        payload = {
            "offset": offset,
        }
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_trending_links(
        self,
        offset: Optional[int] = 0,
    ) -> List[Dict[str, str]]:
        url = f"{self.instance_url}/api/v1/trends/links"
        payload = {
            "offset": offset,
        }
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            params=payload,
        )
        return resp.json()

    def get_instance_status_limit(self) -> int:
        url = f"{self.instance_url}/api/v1/instance"
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        response = r.json()
        return response["configuration"]["statuses"]["max_characters"]

    def vote_in_poll(
        self, poll_id: int, votes: List[int]
    ) -> Tuple[int, Dict[str, Union[str, Any, None]]]:
        url = f"{self.instance_url}/api/v1/polls/{poll_id}/votes"
        data: Optional[Dict[str, Union[str, Any, None]]] = {"choices[]": votes}
        return self.__call_url_post(url=url, data=data)


if __name__ == "__main__":
    api = MastoAPI()
