
# AlignmentRankUpdate Event

## Description

Fired when there's an update to a character's alignment rank.

## Parameters

- `alignmentRank`: The new alignment rank.

## Example Usage

```python
def on_alignment_rank_update(event, alignmentRank):
    print(f"Alignment rank updated to: {alignmentRank}")

KernelEventsManager().on(KernelEvent.AlignmentRankUpdate, on_alignment_rank_update)
```