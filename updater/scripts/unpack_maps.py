import os
from pathlib import Path

from tqdm import tqdm

import pydofus2.com.ankamagames.dofus.Constants as Constants
from pydofus2.dataAdapter.pak2 import PakProtocol2

work_dir = Path(os.path.dirname(__file__))
D2P_MAPS_PATH = Constants.DOFUS_HOME / "content" / "maps"
out_dir = Constants.MAPS_PATH

if not os.path.exists(D2P_MAPS_PATH):
    raise Exception("D2P maps path not found: " + str(D2P_MAPS_PATH))

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
    
def unpackD2pFile(file_p, out_dir):
    file_name = os.path.basename(file_p)
    print("D2P Unpacker for " + file_name)
    d2p_reader = PakProtocol2(Path(file_p))
    for name, stream in tqdm(d2p_reader.iterStreams()):
        mapid_mod_10, mapId = name.split("/")
        file_output_p = out_dir / mapid_mod_10 / mapId
        if not os.path.exists(file_output_p.parent):
            os.makedirs(file_output_p.parent)
        file_output = open(file_output_p, "wb")
        file_output.write(stream)
        file_output.close()


for d2p_file_path in Path(D2P_MAPS_PATH).glob("**/*.d2p"):
    unpackD2pFile(d2p_file_path, out_dir)