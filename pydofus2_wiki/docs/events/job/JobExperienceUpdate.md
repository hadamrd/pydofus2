# Job Experience Update Event

## Description

This event is fired in the JobsFrame when a job gains experience.

## Parameters

- `oldJobXp`: The previous job experience value.
- `jobExp`: An instance of `JobExperience` containing the job ID and the gained experience details.

## Example Usage

```python
KernelEventsManager().on(KernelEvent.JobExperienceUpdate, self.onJobExperience)
def onJobExperience(self, event, oldJobXp, jobExp):
    Logger().info(f"Job {jobExp.jobId} has gained {jobExp.jobXP} xp")
```