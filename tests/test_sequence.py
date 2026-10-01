from organelle_evo.sequence import isoelectric_point, proteome_stats


def test_isoelectric_point_orders_acidic_and_basic():
    assert isoelectric_point("DDDDEEEE") < 4 < 7 < 11 < isoelectric_point("KKKKRRRR")


def test_proteome_stats_shares_sum_and_signals():
    acidic = proteome_stats(["M" + "DEAL" * 20] * 5)
    basic = proteome_stats(["M" + "KRAL" * 20] * 5)
    assert abs(sum(acidic["composition"].values()) - 1) < 1e-4
    assert acidic["acidic_excess"] > 0 > basic["acidic_excess"]
    assert acidic["median_pi"] < basic["median_pi"]
    assert basic["n_side"] > acidic["n_side"]  # arginine and lysine carry side-chain nitrogen
    assert proteome_stats(["M" + "A" * 10])["n_proteins"] == 0  # shorter than 30 residues
