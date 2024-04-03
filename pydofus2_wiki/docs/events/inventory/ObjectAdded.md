# ObjectAdded Event

## Description

This event is triggered when an object is added to the inventory.

## Parameters

- `iw`: A wrapper of the object added to the inventory.

## Example Usage

```python
def onObjectAdded(event, iw):
    averageKamasWon = (
        Kernel().averagePricesFrame.getItemAveragePrice(iw.objectGID) * iw.quantity
    )
    Logger().debug(f"Average kamas won from item: {averageKamasWon}")

KernelEventsManager().on(KernelEvent.ObjectAdded, onObjectAdded)
```