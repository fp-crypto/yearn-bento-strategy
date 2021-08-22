// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import {BaseStrategy as BentoBaseStrategy} from "./sushiswap/BaseStrategy.sol";
import "./sushiswap/IBentoBoxMinimal.sol";
import "./boringcrypto/boring-solidity/libraries/BoringERC20.sol";

contract YearnVaultStrategy is BentoBaseStrategy {
    using BoringERC20 for IERC20;

    constructor(
        IERC20 _underlying,
        IBentoBoxMinimal _bentoBox,
        address _strategyExecutor,
        address _factory,
        address[][] memory paths
    )
        public
        BentoBaseStrategy(
            _underlying,
            _bentoBox,
            _strategyExecutor,
            _factory,
            paths
        )
    {}

    function _skim(uint256 amount) internal override {}

    function _harvest(uint256 balance)
        internal
        override
        returns (int256 amountAdded)
    {}

    function _withdraw(uint256 amount) internal override {}

    function _exit() internal override {}
}
