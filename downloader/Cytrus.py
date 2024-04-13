import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import requests
import settings
from data_models import CytrusModel


class Cytrus:
    def __init__(self):
        self._initialized = False
        self._base_url = "https://launcher.cdn.ankama.com/"
        self.cytrus_data = None
        self._files = []
        self._files_to_retry = []
        self._files_to_download_count = 0
        self._downloaded_files = 0

    def initialize(self):
        if self._initialized:
            return

        print("Initializing Cytrus...")
        response = requests.get(self._base_url + "cytrus.json")
        self.cytrus_data = CytrusModel(**response.json())

        self._initialized = True
        print("Cytrus initialized!")

    async def download_game(self, game, platform, build, version):
        self.print_game(game, platform, build, version)
        game_path = f"./{game}_{platform}_{build}_{version}/"
        os.makedirs(game_path, exist_ok=True)

        response = requests.get(f"{self._base_url}{game}/releases/{build}/{platform}/{version}.json")
        if response.status_code != 200:
            print(f"Failed to download game {game} with build {build} and version {version}.")
            print(f"URL: {self._base_url}{game}/releases/{build}/{platform}/{version}.json")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            return
        doc = response.json()
        for path, content in doc.items():
            for filename, file_info in content["files"].items():
                self._files.append(
                    {"path": os.path.join(game_path, filename), "hash": file_info["hash"], "size": file_info["size"]}
                )

        self._files = {f["path"]: f for f in self._files}.values()
        self._files_to_download_count = len(self._files)

        with ThreadPoolExecutor(max_workers=settings.max_concurrency) as executor:
            executor.map(lambda f: self.download_file(f, game), self._files)

        while self._files_to_retry:
            with ThreadPoolExecutor(max_workers=settings.max_concurrency) as executor:
                executor.map(lambda f: self.download_file(f, game, True), self._files_to_retry)

        print(
            f"Download finished! All {self._downloaded_files}/{self._files_to_download_count} files were downloaded."
        )
        self._files.clear()

    def download_file(self, file_info, game, retry=False):
        url = f"{self._base_url}{game}/hashes/{file_info['hash'][:2]}/{file_info['hash']}"
        os.makedirs(os.path.dirname(file_info["path"]), exist_ok=True)

        print(
            f"[Progress: {self._downloaded_files} files downloaded out of {self._files_to_download_count}] Downloading {file_info['path']} ..."
        )
        try:
            response = requests.get(url)
            with open(file_info["path"], "wb") as f:
                f.write(response.content)

            with Lock():
                if retry:
                    self._files_to_retry = [x for x in self._files_to_retry if x["path"] != file_info["path"]]
                self._downloaded_files += 1
                if sys.platform == "win32":
                    os.system(f"title [{self._downloaded_files}/{self._files_to_download_count}] downloaded")

        except Exception as e:
            print(f"Caught exception while downloading file {file_info['path']}: {e}. Will try to redownload it later")
            if not retry:
                self._files_to_retry.append(file_info)

    @staticmethod
    def print_game(game, platform, build, version):
        print("Downloading ", end="")
        print(f"\033[96m{game}\033[0m", end=" ")  # Cyan
        print("in platform ", end="")
        print(f"\033[91m{platform}\033[0m", end=" ")  # Dark Red
        print("with build ", end="")
        print(f"\033[93m{build}\033[0m", end=" ")  # Yellow
        print("of version ", end="")
        print(f"\033[95m{version}\033[0m")  # Magenta
        sys.stdout.flush()


if __name__ == "__main__":
    cytrus = Cytrus()
    cytrus.initialize()
