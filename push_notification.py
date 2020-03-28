from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage

# Basic arguments. We can extend this function with the push features I want to
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    PushClient().publish(
        PushMessage(to=token,
                    body=message,
                    data=extra)).validate_response()
