import hashlib
import json

import mailchimp_marketing as MailchimpMarketing
from decouple import config
from mailchimp_marketing.api_client import ApiClientError


class Newsletter:
    """
    newsletter class using mailchimp.

    Read mailchimp docs to know the required
    fields in member_info so as to know the
    keyword arguments to use.
    """

    @staticmethod
    def get_email_hash(email):
        """returns MD5 hash of the lowercase version of the email address."""
        email_hash = hashlib.md5(email.encode("utf-8").lower()).hexdigest()
        return email_hash

    @staticmethod
    def serialize_error(error: ApiClientError) -> dict:
        """
        convert apiclient error to dict
        type(error.text) -> str so it has to be converted to dict
        to access the key and values
        """
        return json.loads(error.text)

    def __init__(self, list_id: str) -> None:
        """initialize connection to mailchimp"""
        self.mailchimp = MailchimpMarketing.Client()
        self.mailchimp.set_config(
            {"api_key": config("MAILCHIMP_KEY"), "server": config("MAILCHIMP_SERVER")}
        )
        self.list_id = list_id

    def __str__(self) -> str:
        """string representation of the newsletter object"""
        return f"Newsletter object for {self.list_id}"

    def __eq__(self, other_object) -> bool:
        """compares  two newsletter objects"""
        if isinstance(other_object, Newsletter):
            return self.list_id == other_object.list_id
        return False

    def add_member(self, is_exist_subscribe: bool = True, **member_info):
        """
        adds member to the audience list with the member_info.

        is_exist_subscribe determines whether user whose email_address
        already exist in the list should be updated to change their status to
        subscribed. This is useful as users who have unsubscribed might want
        to subscribe back. Moreso, when a user unsubsribed their email_address
        isn't removed from the list only their status is changed.

        More info on mailchimp docs as regards status and removing members.
        """
        try:
            response = self.mailchimp.lists.add_list_member(self.list_id, member_info)
            return "added"
        except ApiClientError as error:
            response = self.get_member_info(
                self.get_email_hash(member_info["email_address"])
            )
            error = Newsletter.serialize_error(error)
            if (
                error["title"] == "Member Exists"
                and response["status"] == "unsubscribed"
            ):
                if is_exist_subscribe:
                    return self.subscribe(response["contact_id"])
            return error["title"]

    def get_all_members(self):
        """gets all the members in a list"""
        try:
            response = self.mailchimp.lists.get_list_members_info(self.list_id)
            return response
        except ApiClientError as error:
            error = Newsletter.serialize_error(error)
            return error

    def get_member_info(self, member_email_hash):
        """gets info of a specific member"""
        try:
            response = self.mailchimp.lists.get_list_member(
                self.list_id, member_email_hash
            )
            return response
        except ApiClientError as error:
            error = Newsletter.serialize_error(error)
            return error

    def update_contact(self, member_email_hash, **member_info):
        """update the member info of the member that owns the email_hash"""
        try:
            response = self.mailchimp.lists.update_list_member(
                self.list_id, member_email_hash, member_info
            )
            return "updated"
        except ApiClientError as error:
            error = Newsletter.serialize_error(error)
            return error

    def subscribe(self, member_email_hash):
        """change a specific member status to subscribed"""
        return self.update_contact(member_email_hash, status="subscribed")

    def unsubscribe(self, member_email_hash):
        """change a specific member status to unsubscribed"""
        return self.update_contact(member_email_hash, status="unsubscribed")


list_id = "a8eb3204d1"
newsletter = Newsletter(list_id)
