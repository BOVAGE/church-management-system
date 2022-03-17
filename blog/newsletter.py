import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from decouple import config

def subscribe(email):
    mailchimp = MailchimpMarketing.Client()
    mailchimp.set_config({
    "api_key": config('MAILCHIMP_KEY'),
    "server": config('MAILCHIMP_SERVER')
    })

    list_id = 'a8eb3204d1'

    member_info = {
        'email_address': email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("Response: {}".format(response))
        return 'added'
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return 'failed'
