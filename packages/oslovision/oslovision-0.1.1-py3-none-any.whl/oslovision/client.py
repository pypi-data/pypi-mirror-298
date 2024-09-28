import requests
from typing import Dict, Union, Optional
from io import IOBase


class OsloVision:
    def __init__(self, token: str):
        self.base_url = "https://app.oslo.vision/api/v1"
        self.headers = {"Authorization": f"Bearer {token}"}

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response

    def test_api(self) -> Dict[str, str]:
        """Test if the API is up and running and the token is valid."""
        response = self._make_request("GET", "/")
        return response.json()

    def add_image(
        self,
        project_identifier: str,
        image: Union[str, IOBase],
        split: str = "train",
        status: str = "pending",
    ) -> Dict:
        """Add an image to the project."""
        data = {
            "project_identifier": project_identifier,
            "split": split,
            "status": status,
        }
        files = None

        if isinstance(image, str):
            data["url"] = image
        else:
            files = {"image": image}

        response = self._make_request("POST", "/images", data=data, files=files)
        return response.json()

    def create_annotation(
        self,
        project_identifier: str,
        image_identifier: str,
        label: str,
        x0: float,
        y0: float,
        width_px: float,
        height_px: float,
    ) -> Dict:
        """Create a new annotation."""
        data = {
            "project_identifier": project_identifier,
            "image_identifier": image_identifier,
            "label": label,
            "x0": x0,
            "y0": y0,
            "width_px": width_px,
            "height_px": height_px,
        }
        response = self._make_request("POST", "/annotations", json=data)
        return response.json()

    def download_export(self, project_identifier: str, version: int) -> str:
        """Download an export from the dataset."""
        params = {"project_identifier": project_identifier}
        response = self._make_request(
            "GET", f"/exports/{version}", params=params, allow_redirects=False
        )

        if response.status_code == 302:
            return response.headers["Location"]
        else:
            raise Exception("Export not found or not ready")


# Usage example:
# if __name__ == "__main__":
#     api = OsloAPI("https://app.oslo.vision/api/v1", "your_token_here")

#     # Test API
#     print(api.test_api())

#     # Add image
#     with open("image.jpg", "rb") as img_file:
#         image_data = api.add_image("project_id", img_file)
#     print(image_data)

#     # Create annotation
#     annotation = api.create_annotation(
#         "project_id", image_data["id"], "cat", 10, 20, 100, 150
#     )
#     print(annotation)

#     # Download export
#     download_url = api.download_export("project_id", 1)
#     print(f"Download URL: {download_url}")
