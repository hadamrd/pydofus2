
# ClientShutdown Event

## Description

Triggered when the client shuts down, usually because of an error while attempting to auto-revive a player.

## Parameters

- `error`: A description of the error that caused the shutdown.

## Example Usage

```python
def on_client_shutdown(event, error):
    print(f"Client shutdown due to: {error}")

KernelEventsManager().on(KernelEvent.ClientShutdown, on_client_shutdown)
```