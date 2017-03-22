# This sample assumes a client object `service` has been created
# and your app has an access token to use on behalf of the user.
# To learn more about creating a client, see the OAuth 2.0 example:
#  https://developers.google.com/+/domains/authentication/

import pprint

# Set the user's ID to 'me': requires the plus.me scope
user_id = 'me'

# Insert an Activity
print('Insert activity')
result = service.activities().insert(
    userId = user_id,
    body = {
        'object' : {
            'originalContent' : 'Happy Monday! #caseofthemondays'
        },
        'access' : {
            'items' : [{
                'type' : 'domain'
            }],
            'domainRestricted': True
        }
    }).execute()
print('result = %s' % pprint.pformat(result))
