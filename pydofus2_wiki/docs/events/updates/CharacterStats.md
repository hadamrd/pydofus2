# CharacterStats Event

## Description

This event is fired when a player receives its stats list from the server.

## Parameters

- `stats`: The player's stats in a `CharacterCharacteristicsInformations` object.

the `CharacterCharacteristicsInformations` object contains the following fields:

- `experience`: int
- `experienceLevelFloor`: int
- `experienceNextLevelFloor`: int
- `experienceBonusLimit`: int
- `kamas`: int
- `alignmentInfos`: "ActorExtendedAlignmentInformations"
- `criticalHitWeapon`: int
- `characteristics`: list["CharacterCharacteristic"]
- `spellModifiers`: list["SpellModifierMessage"]
- `probationTime`: int

## Example Usage

```python
def onCharacterStats(event, stats):
    Logger().info(f"Character stats: {stats}")

KernelEventsManager().on(KernelEvent.CharacterStats, onCharacterStats)
```