import requests
from typing import Dict, Union, Optional
from io import IOBase, BytesIO
import os
import zipfile


class OsloVision:
    def __init__(
        self, token: str, base_url: Optional[str] = "https://app.oslo.vision/api/v1"
    ):
        self.base_url = base_url
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

    def download_export(
        self, project_identifier: str, version: int, output_dir: Optional[str] = "."
    ) -> str:
        """
        Download an export from the dataset, follow redirects, and unzip the contents.

        Args:
            project_identifier (str): The ID of the project
            version (int): The version number of the export
            output_dir (str): The directory where the unzipped files should be saved

        Returns:
            str: The path to the directory containing the unzipped files
        """
        params = {"project_identifier": project_identifier}
        response = self._make_request(
            "GET",
            f"/exports/{version}",
            params=params,
            allow_redirects=True,
            stream=True,
        )

        if response.status_code == 200:
            # Check if the response is a zip file
            if response.headers.get("Content-Type") == "application/zip":
                # Create a BytesIO object from the response content
                zip_content = BytesIO(response.content)

                # Create the output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                # Unzip the contents
                with zipfile.ZipFile(zip_content) as zip_ref:
                    zip_ref.extractall(output_dir)

                return output_dir
            else:
                raise ValueError("The downloaded content is not a zip file")
        else:
            raise Exception(f"Failed to download export: HTTP {response.status_code}")


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
