# CharacterSelectionSuccess Event

## Description

This event is triggered when a character selection process is completed successfully. It signifies that the player has chosen a character with which to play, and the game client can proceed with loading the character's game session. This event is essential for initializing the game state for the selected character and preparing any necessary game environments or data specific to them.

## Parameters

- `characterBaseInformations`: An object containing base information about the character that has been successfully selected. The object includes:

  - `sex`: A boolean indicating the character's sex.
  - `entityLook`: An `EntityLook` object describing the character's appearance.
  - `breed`: An integer representing the character's breed.
  - `level`: An integer indicating the character's level.
  - `name`: A string containing the character's name.
  - `id`: An integer that serves as the unique identifier for the character.

## Example Usage

```python
def on_character_selected_successfully(event, cbi):
    print(f"Character selected: {cbi.name} (ID: {cbi.id})")
    # Further logic to initialize the character's game session

KernelEventsManager().on(KernelEvent.CharacterSelectionSuccess, on_character_selected_successfully)
```