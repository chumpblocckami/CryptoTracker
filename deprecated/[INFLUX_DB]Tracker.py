import datetime as dtimport osimport requestsfrom apscheduler.schedulers.background import BackgroundSchedulerfrom bs4 import BeautifulSoup as bsimport influxdb_clientfrom influxdb_client.client.write_api import SYNCHRONOUSclass CurrencyTracker():    def __init__(self,                 currency="bitcoin",                 download_time=10):        """        Download information about cryptocurrency price from Coinmarketcap.        :param currency: State the currency to be tracked        :param download_time: Rate of price's download (in seconds)        """        self.currency = currency        self.URL = f"https://coinmarketcap.com/currencies/{currency}/"        self.download_time = download_time  # time is in seconds        self.scheduler = self.init_scheduler()        self.bucket = os.getenv("INFLUX_BUCKET")        self.org = os.getenv("INFLUX_ORG")        self.influx_client = influxdb_client.InfluxDBClient(url=os.getenv("INFLUX_URL"),                                                            token=os.getenv("INFLUX_TOKEN"),                                                            org=self.org)        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)    def init_scheduler(self):        scheduler = BackgroundScheduler()        scheduler.add_job(self.job,                          'interval',                          seconds=self.download_time,                          name=f"{self.currency}_tracker")        return scheduler    def job(self):        r = requests.get(self.URL)        soup = bs(r.content, 'html.parser')        price = soup.find("div", {"class": "priceValue"}).select_one("span").text        price = float(price.replace(",", "").replace("$", "").strip())        datapoint = influxdb_client.Point("self.currency").tag("datetime", dt.datetime.now()).field("price", price)        self.write_api.write(bucket=self.bucket, org=self.org, record=datapoint)        with open(f"{self.currency}_price.csv", 'a') as fd:            fd.write(f"\t{dt.datetime.now()}\t{price}\n")        del r, soup, price    def start(self):        self.scheduler.start()        print(f"{self.currency} tracker started")