"""PointSetManager module for managing PointSet objects."""

import os
import re
import urllib.request as req
from urllib.error import URLError


from .pointset import PointSet

RE_UUID = re.compile(r"^[0-9a-fA-F-]{36}$")

class PointSetManager:
    """Manager for PointSet objects, allowing storage and retrieval by ID."""

    @staticmethod
    def get_point_set(point_set_id: str) -> PointSet:
        """Retrieve a PointSet by its ID.

        Args:
            point_set_id (str): The ID of the PointSet to retrieve.

        Returns:
            PointSet: The PointSet associated with the given ID.

        """
        if not RE_UUID.match(point_set_id):
            raise ValueError(f"Malformed point set ID: {point_set_id}")
        
        api_base_url = os.getenv("POINTSET_API_URL")
        if api_base_url is None:
            raise RuntimeError("POINTSET_API_URL environment variable is not set.")
        
        url = f"{api_base_url.rstrip('/')}/pointset/{point_set_id}"
        try:
            with req.urlopen(url) as response:
                if response.status//100 == 5:
                    message = response.read().decode('utf-8')
                    raise RuntimeError(f"Database is currently unavailable: {message}")
                if response.status//100 == 4:
                    message = response.read().decode('utf-8')
                    raise KeyError(f"The requested resource '{point_set_id}' could not be found")
                if response.status != 200:
                    message = response.read().decode('utf-8')
                    raise RuntimeError(f"Failed to retrieve PointSet: {message}")
                data = response.read()
                return PointSet.from_bytes(data)
        except URLError as e:
            raise ConnectionError(f"Failed to connect to the PointSet API: {e.reason}") from e