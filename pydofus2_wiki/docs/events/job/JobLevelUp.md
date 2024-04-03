# JobLevelUp Event

## Description

This event is fired in the JobsFrame when a job levels up.

## Parameters

- `jobId`: The job ID that leveled up.
- `jobName`: The name of the job that leveled up.
- `lastLevel`: The previous level of the job.
- `newLevel`: The new level of the job.
- `podsBonus`: The pods bonus gained from leveling up.

## Example Usage

```python
KernelEventsManager().on(KernelEvent.JobLevelUp, self.onJobLevelUp)

def onJobLevelUp(self, event, jobId, jobName, lastLevel, newLevel, podsBonus):
    Logger().info(f"Job {jobName} has leveled up from level {lastLevel} to {newLevel}")
    Logger().info(f"Pods bonus gained: {podsBonus}")
```