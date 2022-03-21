from hkx_file import HKXFile
from glob import glob


probe_len = 16

ps4_files = glob('ps4_c_hkx\\*.*')
for ps4_filename in ps4_files:
    conv_file = HKXFile('conv_c\\' + ps4_filename.split('\\')[1])
    ps4_file = HKXFile(ps4_filename)
    print(ps4_filename)

    for i in range(len(ps4_file.virtual_fixups)):
        src_add_ps4 = ps4_file.virtual_fixups[i]['src'] + ps4_file.absolute_data_start
        src_ps4 = ps4_file.bytes[src_add_ps4: src_add_ps4 + probe_len]

        src_add_conv = conv_file.virtual_fixups[i]['src'] + conv_file.absolute_data_start
        src_conv = conv_file.bytes[src_add_conv: src_add_conv + probe_len]

        if src_ps4.hex() != src_conv.hex():
            print('Diff src: at fixup %d, ps4 value %s; conv value %s' % (i, src_ps4.hex(), src_conv.hex()))

    for i in range(len(ps4_file.global_fixups)):
        src_add_ps4 = ps4_file.global_fixups[i]['src'] + ps4_file.absolute_data_start
        dst_add_ps4 = ps4_file.global_fixups[i]['dst'] + ps4_file.absolute_data_start
        src_ps4 = ps4_file.bytes[src_add_ps4: src_add_ps4 + probe_len]
        dst_ps4 = ps4_file.bytes[dst_add_ps4: dst_add_ps4 + probe_len]

        src_add_conv = conv_file.global_fixups[i]['src'] + conv_file.absolute_data_start
        dst_add_conv = conv_file.global_fixups[i]['dst'] + conv_file.absolute_data_start
        src_conv = conv_file.bytes[src_add_conv: src_add_conv + probe_len]
        dst_conv = conv_file.bytes[dst_add_conv: dst_add_conv + probe_len]

        if src_ps4.hex() != src_conv.hex():
            print('Diff src: at fixup %d, ps4 value %s; conv value %s' % (i, src_ps4.hex(), src_conv.hex()))

        if dst_ps4.hex() != dst_conv.hex():
            print('Diff dst: at fixup %d, ps4 value %s; conv value %s' % (i, dst_ps4.hex(), dst_conv.hex()))

    for i in range(len(ps4_file.local_fixups)):
        src_add_ps4 = ps4_file.local_fixups[i]['src'] + ps4_file.absolute_data_start
        dst_add_ps4 = ps4_file.local_fixups[i]['dst'] + ps4_file.absolute_data_start
        src_ps4 = ps4_file.bytes[src_add_ps4: src_add_ps4 + probe_len]
        dst_ps4 = ps4_file.bytes[dst_add_ps4: dst_add_ps4 + probe_len]

        src_add_conv = conv_file.local_fixups[i]['src'] + conv_file.absolute_data_start
        dst_add_conv = conv_file.local_fixups[i]['dst'] + conv_file.absolute_data_start
        src_conv = conv_file.bytes[src_add_conv: src_add_conv + probe_len]
        dst_conv = conv_file.bytes[dst_add_conv: dst_add_conv + probe_len]

        if src_ps4.hex() != src_conv.hex():
            print('Diff src: at fixup %d, ps4 value %s; conv value %s' % (i, src_ps4.hex(), src_conv.hex()))

        if dst_ps4.hex() != dst_conv.hex():
            print('Diff dst: at fixup %d, ps4 value %s; conv value %s' % (i, dst_ps4.hex(), dst_conv.hex()))
