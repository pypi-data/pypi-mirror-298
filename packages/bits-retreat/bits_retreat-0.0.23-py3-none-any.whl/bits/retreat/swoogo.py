# -*- coding: utf-8 -*-
"""Swoogo class file."""

import requests


class Swoogo(object):
    """Swoogo class."""

    def __init__(self, api_key, api_secret, verbose=False):
        """Initialize a Swoogo class instance."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.verbose = verbose

        self.base_url = "https://www.swoogo.com/api/v1"

        self.access_token = self._get_access_token()

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

    def _get_access_token(self):
        """Return a bearer token for making authorized requests."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        url = f"{self.base_url}/oauth2/token.json"
        data = "grant_type=client_credentials"
        auth = (self.api_key, self.api_secret)
        response = requests.post(url, auth=auth, headers=headers, data=data, timeout=10)
        return response.json().get("access_token")

    def _get_list_items(self, url, headers, params):
        """Return the results from a paginated list."""
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response_data = response.json()
        items = response_data.get("items", [])

        next_url = response_data.get("_links", {}).get("next", {}).get("href")
        while next_url:
            response = requests.get(next_url, headers=headers, params=params, timeout=60)
            response_data = response.json()
            items.extend(response_data.get("items", []))
            next_url = response_data.get("_links", {}).get("next", {}).get("href")

        return items

    #
    # Events
    #
    def get_event(self, event_id):
        """Return a single Swoogo event."""
        url = f"{self.base_url}/events/{event_id}.json"
        params = {}
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        return response.json()

    def get_events(self):
        """Get all events from swoogo."""
        url = f"{self.base_url}/events.json"
        params = {}
        return self._get_list_items(url, headers=self.headers, params=params)

    #
    # Questions
    #
    def get_question(self, question_id):
        """Get a question from swoogo."""
        url = f"{self.base_url}/event-questions/{question_id}.json"
        params = {}
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        return response.json()

    def get_questions(self, event_id):
        """Get all questions from an event in swoogo."""
        url = f"{self.base_url}/event-questions.json"
        params = {
            "event_id": event_id,
            "fields": "id,name,attribute,type,page_id,sort",
            "per-page": 200,
        }
        return self._get_list_items(url, headers=self.headers, params=params)

    #
    # Registrants
    #
    def approve_swoogo_registration(self, rid, approval_field):
        """Approve a single registration in Swoogo."""
        url = f"{self.base_url}/registrants/update/{rid}.json"
        payload = {approval_field: "TRUE"}
        response = requests.put(url, headers=self.headers, json=payload, timeout=30)
        if response.status_code == 200:
            return True
        return False

    def cancel_swoogo_registration(self, rid):
        """Cancel a single registration in Swoogo."""
        url = f"{self.base_url}/registrants/update/{rid}.json"
        payload = {"registration_status": "cancelled"}
        response = requests.put(url, headers=self.headers, json=payload, timeout=30)
        if response.status_code == 200:
            return True
        return False

    def get_registrants(self, event_id, fields=None):
        """Get all registrants from an event in swoogo."""
        url = f"{self.base_url}/registrants.json"
        if not fields:
            fields = [
                "id",
                "first_name",
                "last_name",
                "email",
                "registration_status",
                "reg_type_id",
            ]
        params = {
            "event_id": event_id,
            "fields": ",".join(fields),
            "per-page": 200,
        }
        return self._get_list_items(url, headers=self.headers, params=params)

    def get_registrants_by_domain(self, event_id=None, registrants=None):
        """Return a dict of registrants by their email domain name."""
        if not event_id and not registrants:
            raise ValueError("Must provide either event_id or registrants")
        if not registrants:
            registrants = self.get_registrants(event_id)
        domains = {}
        for r in registrants:
            domain = r["domain"]
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(r)
        return domains

    def get_registrants_by_id(self, event_id=None, registrants=None):
        """Return a dict of registrants by their registration id."""
        if not event_id and not registrants:
            raise ValueError("Must provide either event_id or registrants")
        if not registrants:
            registrants = self.get_registrants(event_id)
        reg_ids = {}
        for r in registrants:
            rid = r["id"]
            reg_ids[rid] = r
        return reg_ids

    #
    # Get Registrant Types
    #
    def get_registrant_types(self, event_id):
        """Get all registrant types from an event in swoogo."""
        url = f"{self.base_url}/reg-types.json"
        params = {
            "event_id": event_id,
            "per-page": 200,
        }
        return self._get_list_items(url, headers=self.headers, params=params)

    def get_registrant_types_dict(self, event_id):
        """Return a dict of registrant types for the given event."""
        types = {}
        for reg_type in self.get_registrant_types(event_id):
            type_id = reg_type["id"]
            types[type_id] = reg_type
        return types
