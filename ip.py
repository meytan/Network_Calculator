import re


class Ip:

    def __init__(self, ip_address, mask):
        self.ip_address = ip_address
        self.mask = mask
        self.octet_ip = str(ip_address).split(".")
        self.octet_ip = [int(x) for x in self.octet_ip]
        self.bin_octet_ip = [bin(x)[2:].zfill(8) for x in self.octet_ip]
        self.octet_mask = self.__get_octet_mask()
        self.bin_octet_mask = [bin(x)[2:].zfill(8) for x in self.octet_mask]
        self.network_address = self.__get_network_address()
        self.broadcast_address = [(x | (255 - y)) for x, y in zip(self.octet_ip, self.octet_mask)]
        self.bin_broadcast_address = [bin(x)[2:].zfill(8) for x in self.broadcast_address]
        self.first_host = self.network_address[:]
        self.first_host[3] += 1
        self.bin_first_host = [bin(x)[2:].zfill(8) for x in self.first_host]
        self.last_host = self.broadcast_address[:]
        self.last_host[3] -= 1
        self.bin_last_host = [bin(x)[2:].zfill(8) for x in self.last_host]
        self.max_host_count = 2**(32-self.mask) - 2 if self.mask<30 else "None"
        self.type = "private" if self.is_private() else "public"

    @staticmethod
    def check_ip(ip):
        return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)

    def __get_octet_mask(self):
        mask = self.mask
        octet_mask = []
        for i in range(0, 4):
            if mask > 0:
                if mask >= 8:
                    octet_mask.append(2**8-1)
                else:
                    octet_mask.append(2**8-2**(8-mask))
                mask -= 8
            else:
                octet_mask.append(0)
        return octet_mask

    def __get_network_address(self):
        network_address = []
        for x, y in zip(self.octet_ip, self.octet_mask):
            network_address.append(x & y)
        return network_address

    def get_network_class(self):
        if self.octet_ip[0] < 128:
            return "A"
        elif self.octet_ip[0] < 192:
            return "B"
        elif self.octet_ip[0] < 224:
            return "C"
        elif self.octet_ip[0] < 240:
            return "D"
        else:
            return "E"

    def is_private(self):
        if self.octet_ip[0] == 10 or (self.octet_ip[0] == 172 and 16 <= self.octet_ip[1] <= 31) or (self.octet_ip[0] == 192 and self.octet_ip[1] == 168):
            return True
        return False

    def print(self):

        print("Ip Address: \t\t" + self.ip_address + "/", self.mask)
        print("Binary Ip Address: \t" + self.make_printable(self.bin_octet_ip) + "/"+ self.make_printable(self.bin_octet_mask))
        print("Network Address: \t" + self.make_printable(self.network_address))
        print("Type: \t\t\t\t"+self.type)
        print("Broadcast Address: \t" + self.make_printable(self.broadcast_address))
        print("Binary Broadcast Address: " + self.make_printable(self.bin_broadcast_address))
        if self.mask < 30:
            print("First host: \t\t" + self.make_printable(self.first_host))
            print("Last host: \t\t\t" + self.make_printable(self.last_host))
            print("Binary First host: \t" + self.make_printable(self.bin_first_host))
            print("Binary Last host: \t" + self.make_printable(self.bin_last_host))
            print("Max Host Number:\t", self.max_host_count)
        else:
            print("There is no host addresses")

    @staticmethod
    def make_printable(val):
        tmp_str=""
        for s in val:
            tmp_str += str(s) + "."
        return tmp_str[:-1]

    def check_if_host(self):
        if self.ip_address == self.network_address:
            return False
        return True

    def write_to_file(self, fname):
        f = open(fname, "w+")
        f.write("Ip Address: \t\t" + self.ip_address + "/" +  str(self.mask) + "\n")
        f.write("Binary Ip Address: \t" + self.make_printable(self.bin_octet_ip) + "/" + self.make_printable(
            self.bin_octet_mask) + "\n")
        f.write("Network Address: \t" + self.make_printable(self.network_address) + "\n")
        f.write("Type: \t\t\t\t" + self.type + "\n")
        f.write("Broadcast Address: \t" + self.make_printable(self.broadcast_address) + "\n")
        f.write("Binary Broadcast Address: " + self.make_printable(self.bin_broadcast_address) + "\n")
        if self.mask < 30:
            f.write("First host: \t\t" + self.make_printable(self.first_host) + "\n")
            f.write("Last host: \t\t\t" + self.make_printable(self.last_host) + "\n")
            f.write("Binary First host: \t" + self.make_printable(self.bin_first_host) + "\n")
            f.write("Binary Last host: \t" + self.make_printable(self.bin_last_host) + "\n")
            f.write("Max Host Number:\t" + str(self.max_host_count) + "\n")
        else:
            f.write("There is no host addresses" + "\n")
        f.close()
