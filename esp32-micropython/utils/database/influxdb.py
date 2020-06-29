# Example usage
# from util.database.influxdb import InfluxDB
# testflux = InfluxDB("https://url/to/influxdb", "database", "user", "pass", "metrics", namedtag="value")
# testflux.write(field1=value1, field2=value2)
# testflux.write(temperature=24, humidiry=60)

__version__ = "1.0.0"

from util.database import Database
from urequests import post


class InfluxDB(Database):
    def __init__(self, baseURL, dbname, username, password, metric=None, **tags):
        self.__baseURL = baseURL
        self.__writeURL = "{0}/write?db={1}&u={2}&p={3}".format(
            baseURL,
            dbname,
            username,
            password)
        self.__tags = tags
        self.__metric = metric

    def __generate_post_data(self, metric, **kwargs):
        post_tags = ",".join("{0}={1}".format(t, v) for t, v in self.__tags.items())
        post_values = ",".join("{0}={1}".format(k, v) for k, v in kwargs.items())

        if post_tags == '':
            postdata = "{0} {1}".format(metric, post_values)
        else:
            postdata = "{0},{1} {2}".format(metric, post_tags, post_values)

        return postdata

    def set_metric(self, metric):
        if metric is None:
            raise ValueError("Metric can not be None")

        self.__metric = metric

    def set_tags(self, **kwargs):
        self.__tags = kwargs

    def write(self, *args, **kwargs):
        metric = self.__metric

        if len(args) > 1:
            raise ValueError("Only metrics optional argument supported in this version.")

        if len(kwargs) == 0:
            raise ValueError("Empty write")

        if len(args) == 1 and len(kwargs) > 0:
            metric = args[0]

        if metric is None:
            raise ValueError("Metric is not defined")

        post_data = self.__generate_post_data(metric, **kwargs)
        try:
            response = post(self.__writeURL, data=post_data)
            response.close()
            return response.status_code == 204
        except Exception as e:
            print("Error write to InfluxDB", e)
