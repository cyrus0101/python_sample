import usb.core
import usb.util

def hid_set_report(dev, report):
    """ Implements HID SetReport via USB control transfer """
    dev.ctrl_transfer(
      0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
      9,     # SET_REPORT
      0x200, # "Vendor" Descriptor Type + 0 Descriptor Index
      0,     # USB interface № 0
      report # the HID payload as a byte array -- e.g. from struct.pack()
    )

#发现设备
dev = usb.core.find(idVendor=0x248A, idProduct=0x880C)
if dev is None:
    raise ValueError('Our device is not connected')

#获取设备配置
try:
    cfg = dev.get_active_configuration()
except usb.core.USBError:
    cfg = None

if cfg is None:
    dev.set_configuration()

text_report = [0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00]
hid_set_report(dev, text_report)

endpoint = dev[0][(0,0)][0]

try:
    dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 1000)
except Exception as e:
    print(e)


