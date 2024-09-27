# -*- coding: utf-8 -*-
"""Hopin class file."""
import requests


class Hopin:
    """Hopin class."""

    def __init__(self, token):
        """Initialize a class instance."""
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json",
        }
        self.base_url = "https://api.hopin.com/v1"

        self.event_id = "uOWSaHxaRtjBBIsMLGQzMGxnK"
        self.organization_id = "moDz7NUY5qBaZnDP1QcgsUV5Q"
        self.ticket_id = "mVEJ1B4Y8RWcQ6nDATsMGecVT"

    def get_list(self, url, params={}):
        """Return a response from a paginated list."""
        response = requests.get(url, headers=self.headers, params=params).json()
        items = response.get("data", [])
        while response["links"].get("next"):
            url = response["links"]["next"]
            response = requests.get(url, headers=self.headers).json()
            items += response.get("data", [])
        return items

    # Events
    def get_registrations(self):
        """Return a list of registrations."""
        url = f"{self.base_url}/events/{self.event_id}/registrations"
        return self.get_list(url)

    def get_registrations_by_email(self):
        """Return a dict of registrations by Email."""
        registrations = {}
        for r in self.get_registrations():
            if r["attributes"]["refunded"]:
                continue
            email = r["attributes"]["email"]
            if email not in registrations:
                registrations[email] = r
            else:
                print(f"Duplicate registration email: {email}")
        return registrations

    # Organizations
    def get_organizations(self):
        """Return a list of organizations."""
        url = f"{self.base_url}/organizations"
        return self.get_list(url)

    def get_events(self):
        """Return a list of events for the organization."""
        url = f"{self.base_url}/organizations/{self.organization_id}/events"
        return self.get_list(url)

    # Tickets
    def create_magic_link(self, email, first_name, last_name):
        """Return a magic link for a user."""
        url = f"{self.base_url}/tickets/{self.ticket_id}/magicLinks"
        body = {
            "data": {
                "type": "magicLink",
                "attributes": {
                    "email": email,
                    # "extraFields": {
                    #     "property1": "string",
                    #     "property2": "string"
                    # },
                    "firstName": first_name,
                    # "headline": "string",
                    "lastName": last_name,
                    # "metadata": {
                    #     "property1": "string",
                    #     "property2": "string"
                    # },
                    # "registrationId": "string"
                }
            }
        }
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_magic_links(self):
        """Return a list of magic links for the ticket."""
        url = f"{self.base_url}/tickets/{self.ticket_id}/magicLinks"
        return self.get_list(url)

    def get_magic_links_by_email(self):
        """Return a dict of magic links by email address."""
        magic_links = {}
        for ml in self.get_magic_links():
            email = ml["attributes"]["email"]
            if email not in magic_links:
                magic_links[email] = ml
            else:
                print(f"Duplicate magic link email: {email}")
        return magic_links

    def get_tickets(self):
        """Return a list of tickets."""
        url = f"{self.base_url}/events/{self.event_id}/tickets"
        return self.get_list(url)
