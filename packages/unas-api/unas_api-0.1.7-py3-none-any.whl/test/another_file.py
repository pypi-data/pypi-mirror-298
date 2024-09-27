from ..unas_api.unas import UnasAPIBase, Product

unas_client = UnasAPIBase("cfcdf8a7109a30971415ff7f026becdc50dbebbd")

print(unas_client.get_unas_feed_url())
