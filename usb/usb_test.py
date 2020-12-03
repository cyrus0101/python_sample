import usb
import usb.core
import usb.util


#发现设备
dev = usb.core.find(idVendor=0x248A, idProduct=0x880C)
if dev is None:
    raise ValueError('Our device is not connected')
#print(dev)

#获取设备配置
try:
    cfg = dev.get_active_configuration()
except usb.core.USBError:
    cfg = None

if cfg is None:
    dev.set_configuration()
#print(cfg)

# get an endpoint instance
intf = cfg[(0,0)]
#print(intf)
ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)
if ep is None:
    print("ep is none!")
    raise ValueError('There are not endpoint in')


def USB_read_data(ep_in_addr, data_len, Timeout=1000):
    """data_len:应该为最大包长，不然会发生无效端点的警告
    e.g. :
        ep_in_addr = endpoint.bEndpointAddress
        data_len = endpoint.wMaxPacketSize
    """
    try:
        data_r = dev.read(ep_in_addr, data_len, Timeout)
        print(data_r)
    except Exception as e:
        print(e)

def USB_write_data(ep_out_addr, data, Timeout=1000):
    """参数应该与协议对应，不应该超过或者小于，这样容易导致接收方接收不到数据"""
    try:
        data_w = dev.write(ep_out_addr, data, Timeout)
        print(data_w)
    except Exception as e:
        print(e)

def hid_set_report(dev, report):
    """ Implements HID SetReport via USB control transfer """
    dev.ctrl_transfer(
      0x21,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
      9,     # SET_REPORT
      0x200, # "Vendor" Descriptor Type + 0 Descriptor Index
      0,     # USB interface № 0
      report # the HID payload as a byte array -- e.g. from struct.pack()
    )

def hid_get_report(dev):
    """ Implements HID GetReport via USB control transfer """
    return dev.ctrl_transfer(
      0xA1,  # REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
      1,     # GET_REPORT
      0x200, # "Vendor" Descriptor Type + 0 Descriptor Index
      0,     # USB interface № 0
      8     # max reply size
    )
text_report = [0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00]
hid_set_report(dev, text_report)

endpoint = dev[0][(0,0)][0]
print(endpoint.bEndpointAddress)

try:
    dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 1000)
except Exception as e:
    print(e)

