import pydofus2.com.ankamagames.jerakine.pools.Pool as pool
from pydofus2.com.ankamagames.jerakine import JerakineConstants


class PoolsManager:
    _linkedListNodePool = None

    @classmethod
    def getLinkedListNodePool(cls) -> pool.Pool:
        if not cls._linkedListNodePool:
            from pydofus2.com.ankamagames.jerakine.pools.PoolableLinkedListNode import \
                PoolableLinkedListNode

            cls._linkedListNodePool = pool.Pool(
                pooledClass=PoolableLinkedListNode,
                initialSize=JerakineConstants.LINKED_LIST_NODE_POOL_INITIAL_SIZE,
                growSize=JerakineConstants.LINKED_LIST_NODE_POOL_GROW_SIZE,
                warnLimit=JerakineConstants.LINKED_LIST_NODE_POOL_WARN_LIMIT,
            )
        return cls._linkedListNodePool
