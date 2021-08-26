import brownie
import pytest


def test_operation(
    dai,
    dai_whale,
    bento_box,
    bento_strategy,
    bento_owner,
    strategist,
    RELATIVE_APPROX,
):
    # start with 0 balance
    strategyData = bento_box.strategyData(dai).dict()
    assert strategyData["balance"] == 0

    # Set target to 50% and harvest 1M dai
    bento_box.setStrategyTargetPercentage(dai, 50, {"from": bento_owner})
    bento_box.harvest(dai, True, 1_000_000e18, {"from": bento_owner})

    balance = bento_strategy.totalVaultBalance(bento_strategy) / 1e18
    strategyDataBalance = bento_box.strategyData(dai).dict()["balance"] / 1e18

    assert balance > 0
    assert pytest.approx(strategyDataBalance, rel=RELATIVE_APPROX) == balance

    best_vault = bento_strategy.bestVault()

    # make profit on yearn vault
    dai.transfer(best_vault, 100_000e18, {"from": dai_whale})
    assert (bento_strategy.totalVaultBalance(bento_strategy) / 1e18) > balance

    # harvest profit on bentobox
    total_elastic_before = bento_box.totals(dai).dict()["elastic"]
    tx = bento_strategy.safeHarvest(2**256-1, False, 0, False, {"from": strategist})
    total_elastic_after = bento_box.totals(dai).dict()["elastic"]
    profit_amount = tx.events['LogStrategyProfit']['amount']
    assert profit_amount > 0
    assert total_elastic_after == total_elastic_before + profit_amount
