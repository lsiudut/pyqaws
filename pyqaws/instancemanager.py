#!/usr/bin/env python2.7

class InstanceManager:
    changes = {}

    def __init__(self, instance, ro = True):
        self.manager = {
                        'name': {
                            'get': lambda(x): x.tags['Name'],
                            'set': None,
                        },
                        'id': {
                            'get': lambda(x): x.id,
                            'set': None,
                        },
                        'state': {
                            'get': lambda(x): x.state,
                            'set': self._setState,
                        },
                        'groups': {
                            'get': lambda(x): ','.join([ str(y.name) for y in x.groups]),
                            'set': None,
                        },
                        'launch_time': {
                            'get': lambda(x): x.launch_time,
                            'set': None,
                        },
                        'kernel': {
                            'get': lambda(x): x.kernel,
                            'set': self._setKernel
                        },
                        'public_dns_name': {
                            'get': lambda(x): x.public_dns_name,
                            'set': None
                        },
                        'private_dns_name': {
                            'get': lambda(x): x.private_dns_name,
                            'set': None
                        },
                        'key_name': {
                            'get': lambda(x): x.key_name,
                            'set': None,
                        },
                        'instance_type': {
                            'get': lambda(x): x.instance_type,
                            'set': self._setInstanceType
                        },
                        'image_id': {
                            'get': lambda(x): x.image_id,
                            'set': None,
                        },
                        'placement': {
                            'get': lambda(x): x.placement,
                            'set': None,
                        },
                        'ramdisk': {
                            'get': lambda(x): x.ramdisk,
                            'set': None,
                        },
                        'architecture': {
                            'get': lambda(x): x.architecture,
                            'set': None,
                        },
                        'monitored': {
                            'get': lambda(x): x.monitored,
                            'set': None,
                        },
                        'private_ip_address': {
                            'get': lambda(x): x.private_ip_address,
                            'set': None,
                        },
                        'root_device_name': {
                            'get': lambda(x): x.root_device_name,
                            'set': None,
                        },
                        'root_device_type': {
                            'get': lambda(x): x.root_device_type,
                            'set': None,
                        },
                        'interfaces': {
                            'get': lambda(x): x.interfaces,
                            'set': None,
                        },
                        'ebs_optimized': {
                            'get': lambda(x): x.ebs_optimized,
                            'set': None,
                        },
                   }
        
        if ro:
            for (k, v) in self.manager.items():
                self.manager[k]['set'] = None

        self.instance = instance

    def get(self, name):
        if not name in self.manager:
            raise Exception('Bad instance attribute value name')

        return self.manager[name]['get'](self.instance)

    def set(self, name, value):
        self.changes[name] = value

    def commit(self):
        pass

    def getAttributes(self):
        return self.manager.keys()

    def isEditable(self, name):
        return False if self.manager[name]['set'] == None else True

    def _setState(self, state):
        pass

    def _setKernel(self, kernel):
        pass

    def _setInstanceType(self, instance_type):
        pass
