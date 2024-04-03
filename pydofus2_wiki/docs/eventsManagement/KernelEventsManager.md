
# KernelEventsManager Class Documentation

`KernelEventsManager` is a singleton class that manages events throughout the application, built on top of the `EventsHandler` base class.


Initializes the `KernelEventsManager` instance.

## Core Methods

### onceFramePushed

Registers a callback to be executed once when a specific frame is pushed.

```python
def onceFramePushed(self, frameName, callback, args=[], originator=None):
    # Method implementation
```

### onceFramePulled

Registers a callback to be executed once when a specific frame is pulled.

```python
def onceFramePulled(self, frameName, callback, args=[], originator=None):
    # Method implementation
```

### onceMapProcessed

Registers a callback to be executed once when a map has been processed.

```python
def onceMapProcessed(self, callback, args=[], mapId=None, timeout=None, ontimeout=None, originator=None):
    # Method implementation
```

### send

Sends an event to all registered listeners for the given event ID.

```python
def send(self, event_id: KernelEvent, *args, **kwargs):
    # Method implementation
```

### onceActorShowed

Registers a callback for when an actor is shown, executed only once.

```python
def onceActorShowed(self, actorId, callback, args=[], originator=None):
    # Method implementation
```

### onEntityMoved

Registers a callback for when an entity moves.

```python
def onEntityMoved(self, entityId, callback, timeout=None, ontimeout=None, once=False, originator=None):
    # Method implementation
```

### onceEntityMoved

Registers a callback for when an entity moves, executed only once.

```python
def onceEntityMoved(self, entityId, callback, timeout=None, ontimeout=None, originator=None):
    # Method implementation
```

### onceEntityVanished

Registers a callback for when an entity vanishes.

```python
def onceEntityVanished(self, entityId, callback, args=[], originator=None):
    # Method implementation
```

... (and so on) ...
