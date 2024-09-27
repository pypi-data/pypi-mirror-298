import statistics

import pytest

from telliot_feeds.feeds.steth_btc_feed import steth_btc_median_feed


@pytest.mark.asyncio
async def test_steth_btc_median_feed(caplog):
    """Retrieve median STETH/BTC price."""
    v, _ = await steth_btc_median_feed.source.fetch_new_datapoint()

    assert v is not None
    assert v > 0
    assert "sources used in aggregate: 3" in caplog.text.lower()
    print(f"STETH/BTC Price: {v}")

    # Get list of data sources from sources dict
    source_prices = [source.latest[0] for source in steth_btc_median_feed.source.sources if source.latest[0]]

    # Make sure error is less than decimal tolerance
    assert (v - statistics.median(source_prices)) < 10**-6
