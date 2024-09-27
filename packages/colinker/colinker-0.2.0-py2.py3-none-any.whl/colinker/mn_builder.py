# -*- coding: utf-8 -*-
"""

"""

import json
import os
import hjson
import requests
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time 
import json
import argparse

# todo:
    # 
    
class builder:
    '''
    

    Parameters
    ----------

        # #WAN1 = {'bw':1000,'delay':'20ms','loss':1,'jitter':'10ms'} 
        # #GBPS = {'delay':'18ms'} 
        # #MBPS = {'bw':10} 
        

    '''

    def __init__(self,data_input='',testing=False):

        self.load_data(data_input)

    def load_data(self, data_input=''):

        if type(data_input) == str:
            if 'http' in data_input:
                url = data_input
                resp = requests.get(url)
                data = hjson.loads(resp.text)
            else:
                if os.path.splitext(data_input)[1] == '.json':
                    with open(data_input,'r') as fobj:
                        data = json.loads(fobj.read().replace("'",'"'))
                if os.path.splitext(data_input)[1] == '.hjson':
                    with open(data_input,'r') as fobj:
                        data = hjson.loads(fobj.read().replace("'",'"'))
        elif type(data_input) == dict:
            data = data_input
            
        self.data = data

        if not 'hosts' in self.data:
            self.data['hosts'] = []
        if not 'switches' in self.data:
            self.data['switches'] = []
        if not 'links' in self.data:
            self.data['links'] = []


    def interSecureModelNetwork(self):

        net = Mininet( topo=None,
                    build=False,
                    ipBase='1.0.0.0/8')
        
        info( '*** Adding controller\n' )
        c0=net.addController(name='c0',
                        controller=OVSController,
                        protocol='tcp',
                        port=6633)

        switchType = OVSKernelSwitch; 

        self.dpid = 1

        nodes = {}

        ## Add switches
        for switch in self.data['switches']:
            self.dpid += 1
            name = switch['name']
            if 'interface' in switch: 
                interface = switch['interface']
                sw = net.addSwitch(name, cls=switchType, dpid=f'{self.dpid}',failMode='standalone')
                Intf(interface, node=sw )    
            else:
                sw = net.addSwitch(name, cls=switchType, dpid=f'{self.dpid}',failMode='standalone')
            switch.update({'instance':sw})
            nodes.update({name:sw})

        ## Add hosts
        for host in self.data['hosts']:
            name = host['name']
            ip = host['ip']
            mac = host['mac']
            h = net.addHost(  name, cls=Host, ip=ip, defaultRoute='10.0.0.1',mac=mac)  
            host.update({'instance':h})
            nodes.update({name:h})

        # Create links
        for link in self.data['links']:
            node_j = link['node_j']
            node_k = link['node_k']
            bw = 1000
            delay = 0
            loss = 0
            jitter = 0
            if 'bw' in link: delay = link['bw']
            if 'delay' in link: delay = link['delay']
            if 'loss' in link: loss = link['loss']
            if 'jitter' in link: jitter = link['jitter']

            net.addLink(nodes[node_j], nodes[node_k], cls =TCLink, 
                                                      bw = bw,  
                                                      delay = delay,
                                                      loss = loss,
                                                      jitter = jitter
                                                      )

        self.net = net


    def setup(self):
        '''
        Setup devices
        '''
        hosts_pids_dict = {}
        for host in self.data['hosts']:
            name = host['name']
            if 'ip_2' in host: 
                ip_2, mask = host['ip_2'].split('/')
                self.net.get(name).cmd(f"ifconfig {name}-eth1 {ip_2} netmask 255.255.0.0")
            if 'run_linker' in host:
                if host['run_linker']:
                    pid_raw = self.net.get(name).cmd(f"pgrep -f '{name}'")
                    pid_raws = pid_raw.split('\r\n')
                    hosts_pids_dict.update({name:{'pid':int(pid_raws[-2])}})
        
        hosts_pids_json = json.dumps(hosts_pids_dict, indent=4) # Convert dictionary to JSON
        # Write JSON data to a file
        with open("hosts_pids.json", "w") as json_file:
            json_file.write(hosts_pids_json)
          

    def start(self):
        '''
        Build and starts the netowork
        '''

        info( '*** Starting network\n')
        self.net.build()
        info( '*** Starting controllers\n')
        for controller in self.net.controllers:
            controller.start()

        info( '*** Starting networking devices \n')
        
        for switch in self.data['switches']:
            name = switch['name']
            self.net.get(name).start([])

        CLI(self.net)
        self.net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    mn = builder('mn_pv_1_2_bess.json')
    mn.interSecureModelNetwork()
    mn.setup()
    mn.start()

        # sEEMU = net.addSwitch('sEEMU', cls=switchType, dpid=f'{dpid}',failMode='standalone')  # switch for the electrical emulator
        # 
        # info( '*** Starting real networking devices\n')
        # dpid = 1
        # sPOI =     

        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         dpid += 1
        #         name = f"{i_m}".zfill(2) + f"{i_n}".zfill(2)
        #         net.addSwitch(f's{name}', cls=switchType, dpid=f'{dpid}',failMode='standalone')    

        # info( '*** Adding hosts \n')


        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         dpid += 1
        #         m_str,n_str =  f"{i_m}".zfill(2),f"{i_n}".zfill(2)
        #         name = m_str + n_str 
        #         net.addHost(f'LV{name}', cls=Host, ip=f'10.10.{i_m}.{i_n}/8', defaultRoute='10.10.0.1',mac=f'00:00:00:00:{m_str}:{n_str}')   

        # info( '*** Adding real network links\n')



        # for i_m in range(1,M+1):
        #     name_j = "sPOI"
        #     for i_n in range(1,N+1):
        #         name = f"{i_m}".zfill(2) + f"{i_n}".zfill(2)
        #         name_k = 's' + name

        #         net.addLink(name_j, name_k)
        #         net.addLink(f"LV{name}", name_k, cls=TCLink, delay='20ms')
        #         name_j = name_k
        
        # ## Emulation network  ########################################################################################

        # info( '*** Starting external connection\n')  
        # dpid += 1
        # sEXT =  net.addSwitch( 'sEXT', cls=switchType, dpid=f'{dpid}',failMode='standalone')     
        # dpid += 1 
        # sEEMU = net.addSwitch('sEEMU', cls=switchType, dpid=f'{dpid}',failMode='standalone')  # switch for the electrical emulator
        # Intf(  sEEMU_if, node=sEEMU )  # EDIT the interface name here! 
        # #Intf(  'eth1', node=sEEMU )  # EDIT the interface name here! 

        # Intf(  sEXT_if, node=sEXT )  # EDIT the interface name here! 
        # #Intf( 'enp0s10', node=sPOI )  # EDIT the interface name here! 



        # info( '*** Setting link parameters\n')
        # #WAN1 = {'bw':1000,'delay':'20ms','loss':1,'jitter':'10ms'} 
        # #GBPS = {'delay':'18ms'} 
        # #MBPS = {'bw':10} 

        # net.addLink(  POI, sEEMU)
        # net.addLink(  PPC, sEXT)

        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         name = f"{i_m}".zfill(2) + f"{i_n}".zfill(2)
        #         net.addLink(f"LV{name}", sEEMU)

        # #net.addLink(WANR1, DSS1GW, cls=TCLink , **MBPS)
        # info( '\n')

        # info( '*** Starting network\n')
        # net.build()
        # info( '*** Starting controllers\n')
        # for controller in net.controllers:
        #     controller.start()

        # info( '*** Starting networking devices \n')
        # net.get( 'sPOI').start([])

        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         dpid += 1
        #         m_str,n_str =  f"{i_m}".zfill(2),f"{i_n}".zfill(2)
        #         name = m_str + n_str 
        #         net.get(f's{name}').start([])

        # net.get('sEEMU').start([])
        # net.get('sEXT').start([])

        # info( '\n')

        # info( '*** Preparing custom sgsim scripts \n')
        # #CLI.do_webserver = webserver    
        # net.get(  'POI').cmd('ifconfig POI-eth1 10.20.0.3 netmask 255.255.0.0')
        # net.get(  'PPC').cmd('ifconfig PPC-eth1 172.20.0.4 netmask 255.255.0.0')
        # net.get('Probe').cmd('ifconfig Probe-eth1 10.10.0.5 netmask 255.255.0.0')


        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         dpid += 1
        #         m_str,n_str =  f"{i_m}".zfill(2),f"{i_n}".zfill(2)
        #         name = m_str + n_str 
        #         net.get(f's{name}').start([])

        #         net.get(f'LV{name}').cmd(f'ifconfig LV{name}-eth1 10.20.{m_str}.{n_str} netmask 255.255.0.0')

        # hosts_dict = {}
        # for item in ['POI']:
        #     #pid = net.get(item).cmd(f"pgrep -f '{item}'| head -n 1")
        #     pid_raw = net.get(item).cmd(f"pgrep -f '{item}'")
        #     pid_raws = pid_raw.split('\r\n')
        #     print(pid_raws)
        #     hosts_dict.update({item:{'pid':int(pid_raws[-2])}})

        # for i_m in range(1,M+1):
        #     for i_n in range(1,N+1):
        #         m_str,n_str =  f"{i_m}".zfill(2),f"{i_n}".zfill(2)
        #         name = m_str + n_str 
        #         #pid = net.get(item).cmd(f"pgrep -f '{item}'| head -n 1")
        #         pid_raw = net.get(f'LV{name}').cmd(f"pgrep -f 'LV{name}'")
        #         pid_raws = pid_raw.split('\r\n')
        #         print('LV',pid_raws)
        #         hosts_dict.update({f'LV{name}':{'pid':int(pid_raws[-2])}})

        # print(hosts_dict)
        # # Convert dictionary to JSON
        # hosts_json = json.dumps(hosts_dict, indent=4)

        # # Write JSON data to a file
        # with open("hosts.json", "w") as json_file:
        #     json_file.write(hosts_json)


        # info( '*** Model Started *** \n' )
        # CLI(net)
        # net.stop()

   



    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", help="number of feeders")
    # parser.add_argument("-n", help="number of generators per feeder")
    # parser.add_argument("-sEEMU_if", help="Emulator interface")
    # parser.add_argument("-sEXT_if", help="PPC External interface")

    # args = parser.parse_args()
    # print(args)
    # m = int(args.m)
    # n = int(args.n)
    # sEEMU_if = args.sEEMU_if
    # sEXT_if = args.sEXT_if

    # if sEEMU_if == None: sEEMU_if = 'enp0s8' 
    # if sEXT_if == None: sEXT_if = 'enp0s9' 
        
    # interSecureModelNetwork(m,n,sEEMU_if,sEXT_if)