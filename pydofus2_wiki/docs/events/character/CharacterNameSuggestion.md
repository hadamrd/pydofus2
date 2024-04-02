
# CharacterNameSuggestion Event

## Description

Fired when a character name suggestion is made.

## Parameters

- `suggestion`: The suggested name.

## Example Usage

```python
def on_character_name_suggestion(event, suggestion):
    print(f"Suggested character name: {suggestion}")

KernelEventsManager().on(KernelEvent.CharacterNameSuggestion, on_character_name_suggestion)
```