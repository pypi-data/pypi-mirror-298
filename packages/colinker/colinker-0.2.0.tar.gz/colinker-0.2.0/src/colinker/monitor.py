from colinker.colinker import Linker
import time
from threading import Thread
from colinker.modbus import modbus_client
import logging
import numpy as np

class Monitor(Linker):

    def __init__(self, cfg_dev, cfg_ctrl):

        name = 'MONITOR'
        super(Monitor, self).__init__(name, cfg_dev, cfg_ctrl)
        self.setup_multiple_device()
        print(self.devices_list)

        self.N_store = 1000

        self.Time = np.zeros((self.N_store,))
        self.Measurements = np.zeros((self.N_store,self.N_measurements))
        self.monitoring = True

    def update(self):
        '''
        Linker_MODBUS - Monitor_var
        '''

        self.modbus_linker_client = modbus_client.Modbus_client(self.modbus_linker_ip,self.modbus_linker_port)
        logging.info(f"Connected to linker at ip = {self.modbus_linker_ip}, port = {self.modbus_linker_port}")
        self.modbus_linker_client.start()   
        self.it = 0     
        measurements = np.zeros((self.N_measurements,))

        while self.monitoring:
            emec_setpoints_dict = {}
            for setpoints_list,measurements_list in self.devices_list:

            #     # Setpoints  ###############################################################################################
                
                

            #     # read setpoints from modbus (real system side)
            #     for setpoint in setpoints_list:

            #         modbus_value = self.modbus_linker_client.read(setpoint['linker_register'], setpoint['type'],format=setpoint['format'])
            #         emec_value = modbus_value*setpoint['emec_scale']
            #         emec_setpoints_dict.update({setpoint['emec_name']:emec_value})
            #         logger.verbose(f"modbus_value@{setpoint['linker_register']} = {modbus_value}  -> {setpoint['emec_name']} = {emec_value}  ")

            #     self.emec_setpoints_dict = emec_setpoints_dict


                # Measurements #####################################################################################

                measurements_dict = self.measurements_dict

                # write measurements in modbus (real system side)
                self.it_meas = 0
                for meas in measurements_list:

                    modbus_value = self.modbus_linker_client.read(meas['linker_register'], meas['type'],format=meas['format'])
                    emec_value = modbus_value*meas['emec_scale']
                    measurements_dict.update({meas['emec_name']:emec_value})
                    measurements[self.it_meas] = emec_value

                    self.it_meas += 1


            self.Time[0:-1] = self.Time[1:]
            self.Measurements[0:-1,:] = self.Measurements[1:,:]

            self.Time[-1] = time.perf_counter()
            self.Measurements[-1,:] = measurements
            
            # Emulator control #####################################################################################

            self.it += 1
            time.sleep(0.05)

    def start(self):

        self.monitor_thread = Thread(target = self.update)
        self.monitor_thread.start()
        print(f'Monitoring started')
                
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg_dev", help="config_devices.json file")
    args = parser.parse_args()
    mon = Monitor(cfg_dev)

    
