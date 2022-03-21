from glob import glob
from hkx_file import HKXFile

files = glob('hkx/*.hkx')

for file in files:
    converted = HKXFile(file)
    converted.convert()
    converted.write_converted()

