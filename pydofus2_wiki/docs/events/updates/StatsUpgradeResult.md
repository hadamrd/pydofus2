# StatsUpgradeResult Event

## Description

This event is fired when a player upgrades their stats.

## Parameters

- `result`: The result of the upgrade.
- `boost`: The new stats boost amount.

## Example Usage

```python
def onStatsUpgradeResult(event, result, boost):
    Logger().info(f"Stats upgrade result: {result}, new boost: {boost}")

KernelEventsManager().on(KernelEvent.StatsUpgradeResult, onStatsUpgradeResult)
```