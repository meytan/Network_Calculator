import sys
import socket
from ip import Ip
from pythonping import ping


if len(sys.argv) == 1:
    ip_address = Ip(socket.gethostbyname(socket.gethostname()), 24)
else:
    try:
        if not Ip.check_ip(str(sys.argv[1]).split("/")[0]):
            raise ValueError("This not ip address")

        ip_address = Ip(str(sys.argv[1]).split("/")[0], int(str(sys.argv[1]).split("/")[1]))

    except IndexError:
        print("Wrong ip format!")
        exit()
    except ValueError as e:
        print(e)
        exit()

ip_address.print()
ip_address.write_to_file("plik.txt")

if ip_address.check_if_host():
    print("Do you want to ping that address?[Y/N]")
    if input() == "Y":
        ping(ip_address.ip_address, verbose=True)




