def test_dickson():
    import seawater_crm as swcrm
    import pandas as pd

    crms = swcrm.dickson.get_crm_batches()
    assert isinstance(crms, pd.DataFrame)
