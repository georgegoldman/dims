// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {IdeaContract} from "./IdeaContract.sol";

contract UsageTrackingContract {
    IdeaContract public ideaContract;
    mapping (uint256=>mapping (address=>uint256)) public ideaUsage;
    mapping (uint256=>uint256) public ideaEquity;

    event IdeaUsed(uint256 ideaId, address user, uint256 equity);

    constructor(address ideaContractAddress) {
        ideaContract = IdeaContract(ideaContractAddress);
    }

    function useIdea(uint256 ideaId, uint256 equity) public {
        require(equity > 0, "Equity must be greater than 0");
        ideaUsage[ideaId][msg.sender] += equity;
        ideaEquity[ideaId] += equity;
        emit IdeaUsed(ideaId, msg.sender, equity);
    }

    function getIdeaEquity(uint256 ideaId) public view returns (uint256) {
        return ideaEquity[ideaId];
    }

}