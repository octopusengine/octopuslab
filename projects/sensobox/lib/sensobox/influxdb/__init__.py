# Example usage
# from utils.database.influxdb import InfluxDB
# testflux = InfluxDB("https://url/to/influxdb", "database", "user", "pass", "measurement_name", namedtag="value")
# testflux.write(field1=value1, field2=value2)
# testflux.write(temperature=24, humidiry=60)

__version__ = "1.1.0"

from urequests import post


class InfluxDB():
    def __init__(self, baseURL, dbname, username, password, measurement=None, **tags):
        if not baseURL.startswith('http'):
            raise ValueError("InfluxDB base URL needs to start with http or https")

        self.__baseURL = baseURL
        self.__writeURL = "{0}/write?db={1}&u={2}&p={3}".format(
            baseURL,
            dbname,
            username,
            password)
        self.__tags = tags
        self.__measurement = measurement

    @classmethod
    def fromconfig(cls, config_name="influxdb"):
        from config import Config
        import binascii
        import machine
        
        config = Config(config_name)

        iurl = config.get("influxdb_url")
        if not iurl:
            raise ValueError("InfluxDB config error: `influxdb_url` is not set. Check configuration file '{}.json'".format(config_name))
        idb = config.get("influxdb_name")
        if not idb:
            raise ValueError("InfluxDB config error: `influxdb_name` is not set. Check configuration file '{}.json'".format(config_name))
        iusr = config.get("influxdb_user")
        if not iusr:
            raise ValueError("InfluxDB config error: `influxdb_user` is not set. Check configuration file '{}.json'".format(config_name))
        ipsw = config.get("influxdb_pass")
        if not ipsw:
            raise ValueError("InfluxDB config error: `influxdb_pass` is not set. Check configuration file '{}.json'".format(config_name))
        imeasurement = config.get("influxdb_measurement")
        if not imeasurement:
            raise ValueError("InfluxDB config error: `influxdb_measurement` is not set. Check configuration file '{}.json'".format(config_name))
        itags = config.get("influxdb_tags") or {
            "id":str(binascii.hexlify(machine.unique_id()).decode())
        }
#         print("Copy device id to find your measurement: " + binascii.hexlify(machine.unique_id()).decode())
        if not isinstance(itags, dict):
            raise ValueError("InfluxDB config error: `influxdb_tags` is object (dict). Check configuration file '{}.json'".format(config_name))
    
        return cls(iurl, idb, iusr, ipsw, imeasurement, **itags)

    def __generate_post_data(self, measurement, **kwargs):
        post_tags = ",".join("{0}={1}".format(t, v) for t, v in self.__tags.items())
        post_values = ",".join("{0}={1}".format(k, v) for k, v in kwargs.items())

        if post_tags == '':
            postdata = "{0} {1}".format(measurement, post_values)
        else:
            postdata = "{0},{1} {2}".format(measurement, post_tags, post_values)

        return postdata

    def set_measurement(self, measurement):
        if measurement is None:
            raise ValueError("Measurement can not be None")

        self.__measurement = measurement

    def set_tags(self, **kwargs):
        self.__tags = kwargs

    def write(self, *args, **kwargs):
        measurement = self.__measurement

        if len(args) > 1:
            raise ValueError("Only measurements optional argument supported in this version.")

        if len(kwargs) == 0:
            raise ValueError("Empty write")

        if len(args) == 1 and len(kwargs) > 0:
            measurement = args[0]

        if measurement is None:
            raise ValueError("Measurement is not defined")

        post_data = self.__generate_post_data(measurement, **kwargs)
        try:
            response = post(self.__writeURL, data=post_data)
            response.close()
            return response.status_code == 204
        except Exception as e:
            print("Error write to InfluxDB", e)
