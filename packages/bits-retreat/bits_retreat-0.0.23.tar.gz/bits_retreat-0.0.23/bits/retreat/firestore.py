# -*- coding: utf-8 -*-
"""Firestore class for Retreat app."""
import datetime
from google.cloud import firestore


class Firestore:
    """Firestore class."""

    def __init__(self):
        """Initialize a new Firestore instance."""
        self.client = firestore.Client()

    #
    # Firestore approvals
    #
    def approve_approval(self, rid, user):
        """Approve a single approval in Firestore."""
        self.update_approval_status(rid, "Approved", user)

    def reject_approval(self, rid, user):
        """Reject a single approval in Firestore."""
        self.update_approval_status(rid, "Rejected", user)

    def update_approval_status(self, rid, status, user):
        """Reject a single approval in Firestore."""
        updated = datetime.datetime.now()
        data = {
            "registrant_id": int(rid),
            "updated_by": user.email,
            "status": status,
            "updated": updated,
        }
        self.client.collection("approvals").document(rid).set(data)

    #
    # Firestore notes
    #
    def get_note(self, rid):
        """Return a single note from firestore."""
        return self.client.collection("notes").document(rid).get().to_dict()

    def get_notes_dict(self):
        """Return a dict of notes."""
        notes = {}
        for doc in self.client.collection("notes").stream():
            notes[doc.id] = doc.to_dict()
        return notes

    def update_note(self, rid, note):
        """Update a single note in firestore."""
        if not note:
            return
        ref = self.client.collection("notes").document(rid)
        doc = ref.get()
        if doc.exists:
            data = doc.to_dict()
            history = data.get("history", [])
            if "note" in data:
                history.append(data["note"])
            data["history"] = history
            data["note"] = note
        else:
            data = {"id": rid, "note": note, "history": []}
        ref.set(data)

    #
    # Firestore registrants
    #
    def approve_registrant(self, rid):
        """Approve a single registrant in Firestore."""
        self.update_registrant_status(rid, "Approved")

    def get_registrant(self, rid):
        """Return a single registrant."""
        return self.client.collection("registrants").document(rid).get().to_dict()

    def get_registrants(self, domain=None, status=None, registration_status=None):
        """Return a list of registrants."""
        registrants = []
        query = self.client.collection("registrants")
        if domain:
            query = query.where("domain", "==", domain)
        if status:
            query = query.where("status", "==", status)
        if registration_status:
            query = query.where("registration_status", "==", registration_status)
        for doc in query.stream():
            registrants.append(doc.to_dict())
        return registrants

    def reject_registrant(self, rid):
        """Reject a single registrant in Firestore."""
        self.update_registrant_status(rid, "Rejected")

    def update_registrant_status(self, rid, status):
        """Update a single registrant in Firestore."""
        ref = self.client.collection("registrants").document(rid)
        ref.update({"status": status})
