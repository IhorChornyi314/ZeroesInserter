from glob import glob
from json import load


def insert_zeroes(class_bytes, insertion_points):
    new_bytes = b''
    old_bytes = b'' + class_bytes
    for address, count in insertion_points:
        if count > 0:
            new_bytes += old_bytes[:address] + b'\x00' * count
            old_bytes = old_bytes[address:]
        else:
            new_bytes += old_bytes[:address]
            old_bytes = old_bytes[address - count:]
    return new_bytes


def test_class(classname, classes_dir):
    insertion_points = load(open('insertion_points.json', 'r'))
    class_files = glob('%s/%s/*_pc.hkc' % (classes_dir, classname))
    for class_file in class_files:
        class_bytes = open(class_file, 'rb').read()
        guess = insert_zeroes(class_bytes, insertion_points[classname])
        truth = open(class_file.replace('_pc', '_ps4'), 'rb').read()
        if guess != truth:
            print('Discrepancy detected in class %s - %s' % (classname, class_file))


test_class('hclObjectSpaceMeshMeshDeformPNTBOperator', 'C:\\Project BloodSouls\\hkx_converter\\output')



