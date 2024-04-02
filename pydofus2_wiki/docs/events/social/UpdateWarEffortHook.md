
# UpdateWarEffortHook Event

## Description

Indicates an update to the war effort, typically with no parameters sent.

## Example Usage

```python
def on_update_war_effort(event):
    print("War effort has been updated.")

KernelEventsManager().on(KernelEvent.UpdateWarEffortHook, on_update_war_effort)
```