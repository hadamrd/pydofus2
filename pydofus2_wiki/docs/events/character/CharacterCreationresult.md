# CharacterCreationResult Event

## Description

Triggered after a character creation attempt, conveying the result.

## Parameters

- `result`: The result of the character creation attempt (`True` for success, `False` for failure).
- `reason`: Reason for failure, if applicable.
- `error_text`: Additional error text providing more context on the failure.

## Example Usage

```python
def on_character_creation_result(event, result, reason, error_text):
    if result:
        print("Character created successfully.")
    else:
        print(f"Character creation failed: {reason} - {error_text}")

KernelEventsManager().on(KernelEvent.CharacterCreationResult, on_character_creation_result)
```
