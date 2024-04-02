# PlayerLoginSuccess Event

## Description

This event is fired when the player successfully logs in to the game server. It signifies that the player's login attempt was successful and that the game session can now begin. This event is crucial for initiating any post-login processes, such as loading player data or transitioning to the game interface.

## Parameters

- `IdentificationSuccessMessage`: The message received from the server upon successful identification. This message typically contains critical information regarding the player's account, such as privileges, subscription details, and other account-specific data.

## Example Usage

```python
def on_player_login_success(event, ismsg):
    print(f"Login successful for account: {ismsg.login}")
    # Additional logic to handle successful login, such as fetching player data

KernelEventsManager().on(KernelEvent.PlayerLoginSuccess, on_player_login_success)
```