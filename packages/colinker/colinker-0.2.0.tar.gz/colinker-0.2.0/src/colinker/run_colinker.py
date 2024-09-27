from colinker.colinker import linker_run
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="id name of the device")
    parser.add_argument("mode", help="working mode")
    parser.add_argument("-cfg_dev", help="config_devices.json file")
    parser.add_argument("-cfg_ctrl", help="config_controller.json file")
    args = parser.parse_args()
    name = args.id    
    mode = args.mode

    linker_run(name, mode, args.cfg_dev, args.cfg_ctrl)
