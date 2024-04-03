
# ReloginToken Event

## Description

This event is sent when a relogin token is generated, often as part of a reauthentication process.

## Parameters

- `validToken`: Indicates whether the token is valid.
- `token`: The relogin token.

## Example Usage

```python
def on_relogin_token(event, validToken, token):
    if validToken:
        print(f"Received valid relogin token: {token}")
    else:
        print("Received invalid relogin token.")

KernelEventsManager().on(KernelEvent.ReloginToken, on_relogin_token)
```