# ObtainedItem Event

## Description

This event is triggered when an object is obtained.

## Parameters

- `iw`: A wrapper of the object added to the inventory.
- `qty`: The quantity of the object obtained.

## Example Usage

```python
def onObtainedItem(event, iw, qty):
    averageKamasWon = (
        Kernel().averagePricesFrame.getItemAveragePrice(iw.objectGID) * qty
    )
    Logger().debug(f"Average kamas won from item: {averageKamasWon}")

KernelEventsManager().on(KernelEvent.ObtainedItem, onObtainedItem)
```