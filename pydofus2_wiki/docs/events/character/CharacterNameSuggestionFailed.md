# CharacterNameSuggestionFailed Event

## Description

This event occurs when an attempt to suggest a character name fails, typically sent with no parameters.

## Example Usage

```python
def on_character_name_suggestion_failed(event):
    print("Character name suggestion failed.")

KernelEventsManager().on(KernelEvent.CharacterNameSuggestionFailed, on_character_name_suggestion_failed)
```
