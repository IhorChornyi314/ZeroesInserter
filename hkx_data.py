class HKXData:
    def __init__(self, hkx_bytes=b''):
        self.bytes = hkx_bytes
        self.endian = 'little'
        self.position = 0
        self.classnames_section_start = 0
        self.section_metadata = {}

    def read_file(self, filename):
        self.__init__(open(filename, 'rb').read())

    def write_file(self, filename):
        open(filename, 'wb').write(self.bytes)

    def get_data(self, size):
        self.position += size
        return self.bytes[self.position - size:self.position]

    def assert_data(self, data):
        if self.bytes[self.position:self.position + len(data)] != data:
            raise Exception('Data assertion failed!')
        self.position += len(data)

