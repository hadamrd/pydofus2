# ClientRestart Event

## Description

This event is triggered when the client restarts, typically due to a follow transition failure.

## Parameters

- `reason`: The reason for the client's restart.

## Example Usage

```python
def on_client_restart(reason):
    print(f"Client restart due to: {reason}")

KernelEventsManager().on(KernelEvent.ClientRestart, on_client_restart)
```