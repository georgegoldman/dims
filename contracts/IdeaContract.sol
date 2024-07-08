// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract IdeaContract {
    struct Idea {
        uint256 id;
        address creator;
        string description;
        uint256 timestamp;
    }

    mapping (uint256 => Idea) public ideas;
    uint256 public ideaCount;

    event IdeaSubmitted(uint256 id, address creator, string description, uint256 timestamp);

    function submitIdea(string memory description) public {
        ideaCount++;
        ideas[ideaCount] = Idea(ideaCount, msg.sender, description, block.timestamp);
        emit IdeaSubmitted(ideaCount, msg.sender, description, block.timestamp);
    }

    function getIdea(uint256 id) public view returns (Idea memory) {
        return ideas[id];
    }
}