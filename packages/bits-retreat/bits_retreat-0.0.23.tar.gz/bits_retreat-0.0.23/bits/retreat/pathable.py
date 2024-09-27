# -*- coding: utf-8 -*-
"""Pathable class file."""
import os
import requests

from bits.pathable import Pathable as Client

PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')


class Pathable:
    """Pathable class."""

    def __init__(self, api_key, community_id="JwWkx4QL5sxFgy229"):
        """Initialize a new Pathable instance."""
        self.api_key = api_key
        self.client = Client(api_key)
        self.community_id = community_id

    def create_pathable_person(self, r):
        """Create a person in pathable."""
        email = r["email"]
        first_name = r["first_name"]
        last_name = r["last_name"]
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }
        params = {}
        body = {
            "_email": email,
            "_profile": {
                "firstName": first_name,
                "lastName": last_name,
                "_templateId": "xWCj6xgHu6TXveybt",
            }
        }
        try:
            response = requests.post(
                "https://api.pathable.co/v1/people",
                json=body,
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            print(response.json())
        except Exception as e:
            print(f"ERROR: Failed to create person: {email} [{e}]")

    def create_pathable_profile(self, r):
        """Create a profile in pathable."""
        email = r["email"]
        first_name = r["first_name"]
        last_name = r["last_name"]
        person_id = r["person_id"]
        p = Pathable(self.api_key)
        body = {
            "firstName": first_name,
            "lastName": last_name,
            "personId": person_id,
            "communityId": self.community_id,
            "_templateId": "xWCj6xgHu6TXveybt",
        }
        try:
            # print(f"Skipping creating profile: {email}...")
            print(p.create_profile(body))
        except Exception as e:
            print(f"ERROR: Failed to create profile: {email} [{e}]")

    def get_pathable_people(self):
        """Return a dict of pathable people by email."""
        p = Pathable(self.api_key)
        people = {}
        for person in p.get_people():
            if "email" not in person:
                continue
            email = person["email"]
            people[email] = person
        return people

    def get_pathable_profiles(self):
        """Return a dict of pathable profiles by email."""
        profiles = {}
        p = Pathable(self.api_key)
        for profile in p.get_profiles():
            if "email" not in profile:
                continue
            email = profile["email"]
            profiles[email] = profile
        return profiles

    def update_pathable_people(self, registrants):
        """Update the people in Pathable."""
        print(f"Registrants: {len(registrants)}")

        pathable_people = self.get_pathable_people()
        print(f"Pathable People: {len(pathable_people)}")

        # group the registrants by status
        approved = []
        rejected = []
        terms = []
        unapproved = []
        for email in registrants:
            r = registrants[email]
            emplid = r["emplid"]
            status = r["status"]
            terminated = r["terminated"]

            # skip terminated broadies
            if "@broadinstitute.org" in email and emplid and terminated:
                print(f"Terminated Broadie: {email}")
                terms.append(email)
                continue

            # skip rejected registrants
            if status in ["Rejected"]:
                rejected.append(email)
                continue

            # skip un-approved registrants
            if not status or status in ["Needs Update", "Updated"]:
                unapproved.append(email)
                continue

            # find approved folks
            if status in ["Approved", "Pre-Approved"]:
                approved.append(email)
            else:
                print(f"ERROR: Unknown status for {email}: {status}")
                import json
                print(json.dumps(r, indent=2, sort_keys=True))

        # get pathable people to add
        add_people = []
        add_profiles = []
        for email in approved:
            r = registrants[email]
            if email not in pathable_people:
                add_people.append(r)
            elif self.community_id not in [profile["communityId"] for profile in pathable_people[email]["profiles"]]:
                r["person_id"] = pathable_people[email]["_id"]
                add_profiles.append(r)

        # get pathable_people to remove
        pathable_staff = []
        projection_staff = []
        remove = []
        unregistered = []
        for email in pathable_people:
            p = pathable_people[email]
            if email in approved:
                continue
            if self.community_id not in [profile["communityId"] for profile in p["profiles"]]:
                continue
            if "@pathable.com" in email:
                pathable_staff.append(email)
            elif "@projection.com" in email:
                projection_staff.append(email)
            elif email not in registrants:
                unregistered.append(email)
            else:
                status = remove.append(email)

        # output people to add
        output = f"\nPeople to Add: {len(add_people)}\n"
        for r in sorted(add_people, key=lambda x: x["email"]):
            output += f"   + {r['email']}\n"
            self.create_pathable_person(r)

        # output profiles to add
        output += f"\nProfiles to Add: {len(add_profiles)}\n"
        for r in sorted(add_profiles, key=lambda x: x["email"]):
            output += f"   + {r['email']}\n"
            self.create_pathable_profile(r)

        # output people to remove
        output += f"\nRemove: {len(remove)}\n"
        for email in sorted(remove):
            note = "Unknown"
            if email in registrants:
                status = registrants[email]["status"]
                if status:
                    note = status
                else:
                    note = "Needs Approval"
            output += f"   - {email} ({note})\n"

        # output unregistered profiles
        output += f"\nUnregistered: {len(unregistered)}\n"
        for email in sorted(unregistered):
            output += f"   - {email}\n"

        # output pathable staff
        output += f"\nPathable Staff: {len(pathable_staff)}\n"
        for email in sorted(pathable_staff):
            output += f"   * {email}\n"

        # output projection staff
        output += f"\nProjection Staff: {len(projection_staff)}\n"
        for email in sorted(projection_staff):
            output += f"   * {email}\n"

        print(output)
        return output
