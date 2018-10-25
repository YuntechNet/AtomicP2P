
class Device(object):

    def __init__(self, device_type):
        self.device_type = device_type

    def __str__(self):
        return 'Device<type={}>'.format(self.device_type)
