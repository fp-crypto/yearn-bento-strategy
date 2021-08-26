import pytest
from brownie import config
from brownie import Contract


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def ygov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@pytest.fixture(scope="session")
def user(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def strategist(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def yregistry():
    token_address = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"  # dai
    yield Contract(token_address)


@pytest.fixture(scope="session")
def dai():
    token_address = "0x6b175474e89094c44da98b954eedeac495271d0f"  # dai
    yield Contract(token_address)


@pytest.fixture(scope="session")
def dai_whale(accounts):
    yield accounts.at("0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643", force=True)


@pytest.fixture(scope="session")
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)


@pytest.fixture(scope="session")
def bento_box():
    yield Contract("0xF5BCE5077908a1b7370B9ae04AdC565EBd643966")


@pytest.fixture(scope="session")
def bento_owner(accounts, bento_box):
    owner = bento_box.owner()
    yield accounts.at(owner, force=True)


@pytest.fixture(scope="function")
def bento_strategy(
    chain, YearnVaultStrategy, dai, yregistry, bento_box, strategist, bento_owner
):
    strategy = strategist.deploy(
        YearnVaultStrategy, dai, yregistry, bento_box, strategist
    )

    bento_box.setStrategy(dai, strategy, {"from": bento_owner})
    chain.sleep(2 * 7 * 24 * 3600 + 1)  # 2 week activation delay
    chain.mine()
    bento_box.setStrategy(dai, strategy, {"from": bento_owner})
    assert bento_box.strategy(dai) == strategy

    yield strategy


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
