// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import {BaseStrategy as BentoBaseStrategy} from "./sushiswap/BaseStrategy.sol";
import "./sushiswap/IBentoBoxMinimal.sol";
import "./boringcrypto/boring-solidity/libraries/BoringERC20.sol";
import {VaultAPI} from "@yearnvaults/contracts/BaseStrategy.sol";
import {
    BaseWrapper as YearnBaseWrapper
} from "@yearnvaults/contracts/BaseWrapper.sol";

contract YearnVaultStrategy is YearnBaseWrapper, BentoBaseStrategy {
    using BoringERC20 for IERC20;

    constructor(
        IERC20 _underlying,
        address _yRegistry,
        IBentoBoxMinimal _bentoBox,
        address _strategyExecutor,
        address _factory,
        address[][] memory paths
    )
        public
        YearnBaseWrapper(address(_underlying), _yRegistry)
        BentoBaseStrategy(
            _underlying,
            _bentoBox,
            _strategyExecutor,
            _factory,
            paths
        )
    {}

    function _skim(uint256 amount) internal override {
        super._deposit(address(this), address(this), amount, false);
    }

    function _harvest(uint256 balance)
        internal
        override
        returns (int256 amountAdded)
    {
        return int256(super.totalVaultBalance(address(this))) - int256(balance);
    }

    function _withdraw(uint256 amount) internal override {
        super._withdraw(address(this), address(this), amount, true);
    }

    function _exit() internal override {
        _withdraw(type(uint256).max);
    }

    function migrate(uint256 amount, uint256 maxMigrationLoss)
        external
        onlyOwner
        returns (uint256)
    {
        return super._migrate(address(this), amount, maxMigrationLoss);
    }
}
