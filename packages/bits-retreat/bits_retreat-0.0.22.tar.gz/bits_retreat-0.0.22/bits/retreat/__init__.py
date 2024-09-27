# -*- coding: utf-8 -*-
"""Retreat class file."""
import os
import requests

from google.cloud import secretmanager_v1


class Retreat:
    """Retreat class."""

    def __init__(self):
        """Initialize a new Retreat instance."""
        self.project = None

    def firestore(self):
        """Return a Retreat Firestore object."""
        from bits.retreat.firestore import Firestore
        return Firestore()

    def get_domains(self, registrants):
        """Return a dict or domains."""
        domains = {}
        for r in registrants:
            domain = r["domain"]
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(r)
        return domains

    def get_project(self):
        """Return the project ID of the current environment."""
        if "GCP_PROJECT" in os.environ:
            return os.environ["GCP_PROJECT"]
        if "GOOGLE_CLOUD_PROJECT" in os.environ:
            return os.environ["GOOGLE_CLOUD_PROJECT"]
        return requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"},
        ).text

    def get_secret(self, name):
        """Return the auth data from the request_json."""
        if not self.project:
            self.project = self.get_project()
        client = secretmanager_v1.SecretManagerServiceClient()
        secret_path = client.secret_version_path(self.project, name, "latest")
        request = {"name": secret_path}
        return client.access_secret_version(request=request).payload.data.decode("utf-8")

    def swoogo(self):
        """Connect to Swoogo API."""
        from bits.retreat.swoogo import Swoogo
        params = {
            "api_key": os.environ.get("SWOOGO_API_KEY"),
            "api_secret": self.get_secret("swoogo-api-secret"),
        }
        return Swoogo(**params)
