import time
import socket

from hcsr04 import HCSR04
from aws import AWSPublisher


if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Presence detector')
    parser.add_argument('-d', dest='distance', action='store', type=float,
                        help='distance on cms', required=True)

    args = parser.parse_args()
    distance_arg = args.distance

    base_dir = os.path.dirname(os.path.abspath(__file__))
    keys_path = os.path.join(base_dir, 'auth', 'distance_sensor')
    root_cert_file = os.path.join(keys_path, 'root-CA.crt')
    certificate_file = os.path.join(keys_path, 'distance_sensor.cert.pem')
    private_key_file = os.path.join(keys_path, 'distance_sensor.private.key')
    hostname = socket.gethostname()
    log_file = os.path.join(base_dir, 'distance_publisher.log')
    publisher = AWSPublisher(log_file=log_file,
                             topic='$aws/things/distance_sensor/shadow/update',
                             root_cert_file=root_cert_file,
                             certificate_file=certificate_file,
                             private_key_file=private_key_file,
                             client_id=hostname,
                             address='hostname.com.br')  # add aws broker hostname
    distance = HCSR04()
    while True:
        if distance.value < distance_arg:
            publisher.send({'distance': distance.value}, debug=True)
            print(distance.value)
        time.sleep(1)

    distance.clean()

