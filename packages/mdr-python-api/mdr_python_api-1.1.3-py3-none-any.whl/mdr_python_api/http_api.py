from typing import Tuple
import requests

HOST = "http://localhost"  # Standard loopback interface address (localhost)
PORT = 443  # Port to listen on (non-privileged ports are > 1023)


def encode(string: str):
    return string.replace("/", chr(0xFF))


class ApiImpl:
    def init(new_host, new_port=443):
        global HOST
        global PORT
        HOST = new_host
        PORT = new_port

    def add_dependencies(
        label: str,
        version: str,
        dependencies: list[Tuple[str, str, str]],
        input_dep: bool,
    ):
        for dep in dependencies:
            dep_label, dep_version, tag = dep
            input_dep_str = "false"
            if input_dep:
                input_dep_str = "true"

            url = f"{HOST}:{PORT}/dependency"
            params = {
                "label": label,
                "version": version,
                "dep_label": dep_label,
                "dep_version": dep_version,
                "tag": tag,
                "input_dep": input_dep_str,
            }
            requests.request(method="post", url=url, params=params)

    def register_meta_data(
        label: str, version: str, owner: str, url: str, md: str
    ) -> str:
        url = f"{HOST}:{PORT}/register"
        params = {
            "label": label,
            "version": version,
            "owner": owner,
            "url": url,
            "md": md,
        }
        response = requests.request(method="post", url=url, params=params)

        return response.text

    def search_meta_data(search_string: str):
        url = f"{HOST}:{PORT}/search"
        params = {
            "label_regex": search_string,
            "version_regex": "*",
            "dependencies": "false",
        }
        response = requests.request(method="get", url=url, params=params)
        delimiter = chr(0xFF)
        results = response.text.split(delimiter)
        return results

    def search_dependencies(search_string: str):
        url = f"{HOST}:{PORT}/search"
        params = {
            "label_regex": search_string,
            "version_regex": "*",
            "dependencies": "true",
        }
        response = requests.request(method="get", url=url, params=params)
        delimiter = chr(0xFF)
        results = response.text.split(delimiter)
        return results

    def health_check():
        url = f"{HOST}:{PORT}/health"
        print(f"URL = {url}")
        try:
            response = requests.request(method="get", url=url)
            result = response.text
        except Exception:
            return False
        if result == "OK":
            return True
        return False
