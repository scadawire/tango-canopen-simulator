import time
from tango import AttrQuality, AttrWriteType, DevState, Attr, CmdArgType, UserDefaultAttrProp
from tango.server import Device, attribute, command, DeviceMeta
from tango.server import class_property, device_property, run
import os
import json
from json import JSONDecodeError
import tempfile
import canopen

class CanopenSimulator(Device, metaclass=DeviceMeta):
    network = None
    node = None
    network_channel = device_property(dtype=str, default_value="can0")
    network_interface = device_property(dtype=str, default_value="socketcan")
    eds_file = device_property(dtype=str, default_value="")
    node_id = device_property(dtype=int, default_value=1)

    @attribute
    def time(self):
        return time.time()

    def init_device(self):

		# note this ds requires the following to be present on the system:
		# modprobe vcan
		# ip link add dev vcan0 type vcan
		# ip link set up vcan0

        self.set_state(DevState.INIT)
        self.get_device_properties(self.get_device_class())
        network = canopen.Network()
        network.connect(channel=self.network_channel, interface=self.network_interface)
        self.info_stream(f"Adding node {self.node_id} with EDS {self.eds_file}")
        temp_eds_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.eds')
        temp_eds_file.write(self.eds_file)
        temp_eds_file.close()
        self.info_stream(f"EDS content written to temporary file: {temp_eds_file.name}")
        self.node = canopen.RemoteNode(int(self.node_id), temp_eds_file.name)
        node = canopen.LocalNode(int(self.node_id), temp_eds_file.name)
        network.add_node(node)
        print("Simulated CANopen server running")
        os.remove(temp_eds_file.name)
        self.set_state(DevState.ON)

if __name__ == "__main__":
    deviceServerName = os.getenv("DEVICE_SERVER_NAME", "CanopenSimulator")
    run({deviceServerName: CanopenSimulator})