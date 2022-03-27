from apps.modules.device import DeviceProfile, Device
from datetime import datetime
from apps.modules.client import Client
import config as config, secret

if __name__ == "__main__":
    START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    d = Device('L1', dp, client, 'Arvores')
    # print(d.query_all_fields(START ))
    print(d.query_field('tmp', START ))