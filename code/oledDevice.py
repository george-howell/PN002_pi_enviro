import sys

from luma.core import cmdline, error

def display_settings(args):

    iface = ''
    display_types = cmdline.get_display_types()
    if args.display not in display_types['emulator']:
        iface = 'Interface  : {}'.format(args.interface)

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = 'unknown'

    import luma.core

    print('\tLuma Oled  : luma.{} {}'.format(lib_name, lib_version))
    print('\tLuma Core  : luma.core {}'.format(luma.core.__version__))
    print('\tDisplay    : {}'.format(args.display))       
    print('\t{}'.format(iface))
    print('\tDimensions : {} x {}'.format(args.width, args.height))
    print('-' * 50)

def get_device(actual_args=None):

    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    display_settings(args)

    # create device
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)

    return device
