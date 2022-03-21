from utilities import *
from json import load


class HKXFile:
    def __init__(self, filename):
        self.header_start = 0
        self.classnames_section_start = 0
        self.absolute_data_start = 0
        self.local_fixups_offset = 0
        self.global_fixups_offset = 0
        self.virtual_fixups_offset = 0
        self.exports_offset = 0
        self.imports_offset = 0
        self.end_offset = 0
        self.classnames = {}
        self.local_fixups = []
        self.global_fixups = []
        self.address_locations = []
        self.virtual_fixups = []
        self.object_addresses = []
        self.zero_insert_points = []
        self.filename = filename.split('\\')[-1]
        self.bytes = open(filename, 'rb').read()
        self.manifest = load(open('insertion_points.json'))
        self.read_header()
        self.read_classnames()
        self.read_data_header()
        self.read_fixups()

    def read_header(self):
        self.header_start = self.bytes[62] + 64
        self.classnames_section_start = read_int(self.bytes, self.header_start + 20, 4)
        self.absolute_data_start = read_int(self.bytes, self.header_start + 84, 4)

    def read_classnames(self):
        position = self.classnames_section_start
        while position < self.absolute_data_start:
            position += 5
            offset = position - self.classnames_section_start
            if self.bytes[position] == 255:
                break
            self.classnames[offset] = read_string(self.bytes, position)
            position += len(self.classnames[offset]) + 1

    def read_data_header(self):
        self.local_fixups_offset = read_int(self.bytes, self.header_start + 152, 4)
        self.address_locations.append({
            'address': self.header_start + 152,
            'value': read_int(self.bytes, self.header_start + 152, 4)
        })

        self.global_fixups_offset = read_int(self.bytes, self.header_start + 156, 4)
        self.address_locations.append({
            'address': self.header_start + 156,
            'value': read_int(self.bytes, self.header_start + 156, 4)
        })

        self.virtual_fixups_offset = read_int(self.bytes, self.header_start + 160, 4)
        self.address_locations.append({
            'address': self.header_start + 160,
            'value': read_int(self.bytes, self.header_start + 160, 4)
        })

        self.exports_offset = read_int(self.bytes, self.header_start + 164, 4)
        self.address_locations.append({
            'address': self.header_start + 164,
            'value': read_int(self.bytes, self.header_start + 164, 4)
        })

        self.imports_offset = read_int(self.bytes, self.header_start + 168, 4)
        self.address_locations.append({
            'address': self.header_start + 168,
            'value': read_int(self.bytes, self.header_start + 168, 4)
        })

        self.end_offset = read_int(self.bytes, self.header_start + 172, 4)
        self.address_locations.append({
            'address': self.header_start + 172,
            'value': read_int(self.bytes, self.header_start + 172, 4)
        })

    def read_fixups(self):
        for i in range(self.local_fixups_offset, self.global_fixups_offset, 8):
            index = i + self.absolute_data_start
            if self.bytes[index:index + 4] == b'\xff\xff\xff\xff':
                continue
            self.address_locations.append({
                'address': index,
                'value': read_int(self.bytes, index, 4)
            })
            self.address_locations.append({
                'address': index + 4,
                'value': read_int(self.bytes, index + 4, 4)
            })
            self.local_fixups.append({'src': read_int(self.bytes, index, 4),
                                      'dst': read_int(self.bytes, index + 4, 4),
                                      'address': index})

        for i in range(self.global_fixups_offset, self.virtual_fixups_offset, 12):
            index = i + self.absolute_data_start
            if self.bytes[index:index + 4] == b'\xff\xff\xff\xff':
                continue
            self.address_locations.append({
                'address': index,
                'value': read_int(self.bytes, index, 4)
            })
            self.address_locations.append({
                'address': index + 8,
                'value': read_int(self.bytes, index + 8, 4)
            })
            self.global_fixups.append({'src': read_int(self.bytes, index, 4),
                                      'dst': read_int(self.bytes, index + 8, 4),
                                      'address': index})

        for i in range(self.virtual_fixups_offset, self.exports_offset, 12):
            index = i + self.absolute_data_start
            if self.bytes[index:index + 4] == b'\xff\xff\xff\xff':
                continue
            self.address_locations.append({
                'address': index,
                'value': read_int(self.bytes, index, 4)
            })
            self.virtual_fixups.append({
                'src': read_int(self.bytes, index, 4),
                'section_index': read_int(self.bytes, index + 4, 4),
                'name_offset': read_int(self.bytes, index + 8, 4)
            })

    def get_zero_insert_points(self):
        for virtual_fixup in self.virtual_fixups:
            object_name = self.classnames[virtual_fixup['name_offset']]
            # print(object_name)
            if object_name in self.manifest:
                for insert_point in self.manifest[object_name]:
                    self.zero_insert_points.append(
                        {
                            'address': virtual_fixup['src'] + insert_point['point'],
                            'count': insert_point['count']
                        })

    def insert_zeroes(self):
        for address_location in self.address_locations:
            value = address_location['value']
            address = address_location['address']
            for zero_insert_point in self.zero_insert_points:
                if zero_insert_point['address'] + self.absolute_data_start <= address:
                    address_location['address'] += zero_insert_point['count']
                if zero_insert_point['address'] <= value:
                    address_location['value'] += zero_insert_point['count']

        for zero_insert_point in self.zero_insert_points:
            add = zero_insert_point['address'] + self.absolute_data_start
            if zero_insert_point['count'] > 0:
                self.bytes = self.bytes[:add] + b'\x00' * zero_insert_point['count'] + self.bytes[add:]
            else:
                if self.bytes[add + 1:add - zero_insert_point['count'] - 1] != b'\x00' * zero_insert_point['count']:
                    print('\nWarning! Deleting non-zero bytes!\n')
                self.bytes = self.bytes[:add] + self.bytes[add - zero_insert_point['count']:]

            for i in range(len(self.zero_insert_points)):
                if self.zero_insert_points[i]['address'] > zero_insert_point['address']:
                    self.zero_insert_points[i]['address'] += zero_insert_point['count']

        for address_location in self.address_locations:
            location = address_location['address']
            value = address_location['value']
            self.bytes = self.bytes[:location] + value.to_bytes(4, 'little') + self.bytes[location + 4:]

    def write_converted(self):
        self.bytes = self.bytes[:18] + b'\x00' + self.bytes[19:]
        open(f'conv/{self.filename}', 'wb').write(self.bytes)

    def convert(self):
        self.get_zero_insert_points()
        self.insert_zeroes()
        self.write_converted()
        return self.bytes





