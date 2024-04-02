# ExchangeObjectModified Event

## Description

This event is triggered when an object in the exchange is modified.

## Parameters

- `iwModified`: The modified item wrapper.
- `remote`: Indicates if the modification was made by the remote party.

## Example Usage

```python
def on_exchange_object_modified(event, iwModified, remote):
    if remote:
        print(f"Remote party modified item: {iwModified}")
    else:
        print(f"Local modification detected: {iwModified}")
```
