from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea


for sa in SubArea.getAllSubArea():
    print(f"SubareaId:", sa.id)
    print(f"SubAreaName:", sa.name)
    print(f"mapIds:", sa.mapIds)
