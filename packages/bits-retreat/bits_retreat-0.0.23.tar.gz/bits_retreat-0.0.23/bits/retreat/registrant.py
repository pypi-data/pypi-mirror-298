# -*- coding: utf-8 -*-
"""Helpers module for Get Swoogo Data cloud function."""
import logging


class Registrant:
    """Registrant class."""

    def __init__(self, registrant, config):
        """Initialize a Registrant class instance."""
        self.config = config
        self.registrant = registrant

        # initialize registrant
        self.approval = None
        self.emplid = None
        self.ippia_response = None
        self.person = None
        self.status = None

        # initialize registration
        self.registration = {
            # email doamain
            "domain": None,

            # workday info
            "broad_email": None,
            "emplid": None,
            "job_class": None,
            "terminated": None,
            "title": None,
            "username": None,
            "workday_home_institution": None,
            "worker_status": None,
            "worker_sub_type": None,
            "worker_type": None,

            # ippia info
            "ippia_response": None,

            # approval status
            "status": None,
        }

        # add config fields from registrant to registration dict
        self.get_config_fields()

        # set registration data
        self.id = str(self.registration["id"])
        self.email = self.registration["email"].lower()
        self.registration["domain"] = self.get_domain()

        # get judge and poster data
        # self.registration["judge_categories"] = self.get_judge_categories()
        self.registration["poster_authors"] = self.get_poster_authors()
        self.registration["poster_presenters"] = self.get_poster_presenters()

    def get_approval_data(self, approvals):
        """Add approval data."""
        if self.id in approvals:
            self.approval = approvals[self.id]

    def get_config_fields(self):
        """Populate registration dict with config fields from registrant."""
        # add basic fields
        for key in self.config["basic_fields"]:
            if key == "reg_type_id":
                self.registration["personal_statement"] = self.registrant[key]["value"]
            else:
                self.registration[key] = self.registrant[key]

        # add poster and registration fields
        for section in ["poster_fields", "registration_fields"]:
            for param in self.config[section]:
                data = self.config[section][param]
                key = data["key"]
                if data["type"] in ["textArea", "textInput", "checkboxList"]:
                    self.registration[param] = self.registrant[key]
                else:
                    self.registration[param] = self.registrant[key]["value"]

    def get_domain(self):
        """Return the domain of the registrant's email address."""
        hostname = self.email.split("@")[1]
        return ".".join(hostname.split(".")[-2:])

    def get_gaia_people_data(self, emails):
        """Add gaia people data for this registrant."""
        if not self.email or self.email not in emails:
            # print(f"Person not found: {self.email}")
            return
        self.person = emails[self.email]
        self.emplid = self.person["emplid"]

        # set people fields
        self.registration["broad_email"] = self.person["email_username"]
        self.registration["emplid"] = self.emplid
        self.registration["job_class"] = self.person["job_class"]
        self.registration["terminated"] = self.person["terminated"]
        self.registration["title"] = self.person["title"]
        self.registration["username"] = self.person["username"]
        self.registration["workday_home_institution"] = self.person["home_institution"]
        self.registration["worker_status"] = self.person["worker_status"]
        self.registration["worker_sub_type"] = self.person["worker_sub_type"]
        self.registration["worker_type"] = self.person["worker_type"]

    def get_ippia_data(self, emplids):
        """Add IPPIA data for this registrant."""
        if not self.emplid or self.emplid not in emplids:
            return
        self.ippia_response = emplids[self.emplid]["Response"]
        self.registration["ippia_response"] = self.ippia_response

    def get_judge_categories(self):
        """Return the judge categories for the registrant."""
        categories = []
        for cat in self.registration["judge_categories"]:
            name = cat["value"]
            if name:
                categories.append(name)
        return categories

    def get_poster_authors(self):
        """Return the poster authors for a registrant."""
        authors = []
        for line in self.registration["poster_authors"].split("\n"):
            for author in line.split(","):
                for name in author.split(" and "):
                    name = name.strip()
                    if name:
                        authors.append(name.strip())
        return authors

    def get_poster_presenters(self):
        """Return the poster presenters for a registrant."""
        presenters = []
        for line in self.registration["poster_presenters"].split("\n"):
            for presenter in line.split(","):
                for name in presenter.split(" and "):
                    name = name.strip()
                    if name:
                        presenters.append(name.strip())
        return presenters

    def get_status(self):
        """Return the approval status of the registrant."""
        if self.person:

            # pre-approve broadies in any of these job classes
            if self.person["job_class"] in [
                "Affiliate Member",
                "Associate Member",
                "Core Member",
                "Employee",
                "Institute Member",
                "Senior Associate Member",
            ] and not self.person["terminated"]:
                self.status = "Pre-Approved"

            # pre-approve paid affiliates
            elif (self.registration["personal_statement"] == "I am a Broad Employee."
                    and self.person["worker_type"] == "Employee"
                    and self.person["worker_sub_type"] == "Paid Affiliate (Fixed Term)"
                    and self.ippia_response == "Accepted"
                    and not self.person["terminated"]):
                self.status = "Pre-Approved"

            # alert about terminated folks
            elif self.person["terminated"] and "@broadinstitute.org" in self.email and self.registration["registration_status"] in ["attended", "confirmed"]:
                logging.error("Terminated Broad Person: {}".format(self.email))

            elif self.person["terminated"] and self.registration["registration_status"] in ["attended", "confirmed"]:
                logging.warning("Former Broad Person: {}".format(self.email))

        # overide status with saved approval status
        if self.approval:
            self.status = self.approval["status"]

        self.registration["status"] = self.status

    def to_dict(self):
        """Return a dict of the Registrant."""
        return self.registration
