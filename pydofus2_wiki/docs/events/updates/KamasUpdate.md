# KamasUpdate Event

## Description

This event is triggered when the player started a fight.

## Parameters

- `kamas`: The new amount of kamas.

## Example Usage

```python
def onKamasUpdate(event, kamas):
    pass

KernelEventsManager().on(KernelEvent.KamasUpdate, onKamasUpdate)
```
