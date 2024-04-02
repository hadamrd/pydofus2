# ClientCrashed Event

## Description

This event is triggered when the client crashes.

## Parameters

- `message`: A descriptive message about the cause of the crash.

## Example Usage

```python
def on_client_crashed(message):
    print(f"Client crashed due to: {message}")

KernelEventsManager().on(KernelEvent.ClientCrashed, on_client_crashed)
```