from util.database import Database
import urequests
import gc


class InfluxDB(Database):
    def __init__(self, baseURL, dbname, username, password):
        self.__baseURL = baseURL
        self.__writeURL = "{0}/write?db={1}&u={2}&p={3}".format(
            baseURL,
            dbname,
            username,
            password)

    def __generate_post_data(self, metric, tags, **kwargs):
        post_tags = ",".join("{0}={1}".format(t, v) for t, v in tags.items())
        post_values = ",".join("{0}={1}".format(k, v) for k, v in kwargs.items())
        postdata = "{0},{1} {2}".format(metric, post_tags, post_values)
        return postdata

    def write(self, metric, tags, **kwargs):
        post_data = self.__generate_post_data(metric, tags, **kwargs)
        try:
            response = urequests.post(self.__writeURL, data=post_data)
            response.close()
            return response.status_code == 204
        except Exception as e:
            print("Error write to InfluxDB", e)
