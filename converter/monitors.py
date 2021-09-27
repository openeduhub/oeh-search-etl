from spidermon import Monitor, MonitorSuite, monitors


@monitors.name('Item count')
class ItemCountMonitor(Monitor):
    # see https://spidermon.readthedocs.io/en/latest/monitors.html#monitors
    @monitors.name('Minimum number of items')
    def test_minimum_number_of_items(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 10

        msg = 'Extracted less than {} items'.format(
            minimum_threshold)
        self.assertTrue(
            item_extracted >= minimum_threshold, msg=msg
        )


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        ItemCountMonitor,
    ]


@monitors.name('Item count is exactly one')
class ItemCountExactlyOneMonitor(Monitor):
    # this Monitor is only useful for debugging a crawler that expects 1 single site to be crawled
    @monitors.name('Minimum number of items_scraped == 1')
    def test_minimum_number_of_items_equals_one(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 1

        msg = f'Expected to extract exactly {minimum_threshold} items, but extracted {item_extracted}'
        self.assertTrue(item_extracted == minimum_threshold, msg=msg)


class SpiderDebugMonitorSuite(MonitorSuite):
    monitors = [
        ItemCountExactlyOneMonitor
    ]
