# PlayerLevelUp Event

## Description

This event is fired when a player levels up.

## Parameters

- `oldLevel`: The previous player level.
- `newLevel`: The new player level.

## Example Usage

```python
def onPlayerLevelUp(event, oldLevel, newLevel):
    Logger().info(f"Player has leveled up from {oldLevel} to {newLevel}")

KernelEventsManager().on(KernelEvent.PlayerLevelUp, onPlayerLevelUp)
```