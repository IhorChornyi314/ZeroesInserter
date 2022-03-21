from glob import glob
from hkx_file import HKXFile


conv_filenames = glob('conv\\*_c.hkx')
for conv_filename in conv_filenames:
    try:
        conv_file = HKXFile(conv_filename)
        true_file = HKXFile('pc_c_hkx\\' + conv_file.filename)
        c_a = conv_file.absolute_data_start
        t_a = true_file.absolute_data_start
        c_f = conv_file.local_fixups_offset
        t_f = true_file.local_fixups_offset
        a = conv_file.bytes[:10] != true_file.bytes[:10]

        if conv_file.bytes[:c_a] != true_file.bytes[:t_a] or conv_file.bytes[c_f + c_a:] != true_file.bytes[t_f + t_a:]:
            print('Metadata diff:', conv_file.filename)
            if len(conv_file.bytes) == len(true_file.bytes):
                print('Same Length:', conv_file.filename)
    except FileNotFoundError:
        pass

