// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract IdeaContract is Ownable, ReentrancyGuard {
    struct Idea {
        uint256 id;
        address creator;
        string description;
        uint256 timestamp;
    }

    uint256 public ideaCount;
    mapping(uint256 => Idea) public ideas;

    event IdeaSubmitted(uint256 id, address creator, string description, uint256 timestamp);

    modifier onlyCreator(uint256 ideaId) {
        require(ideas[ideaId].creator == msg.sender, "Not the idea creator");
        _;
    }

    modifier validDescription(string memory description) {
        require(bytes(description).length > 0, "Description cannot be empty");
        _;
    }

    function submitIdea(string memory description) public validDescription(description) nonReentrant {
        ideaCount++;
        ideas[ideaCount] = Idea(ideaCount, msg.sender, description, block.timestamp);
        emit IdeaSubmitted(ideaCount, msg.sender, description, block.timestamp);
    }

    function getIdea(uint256 id) public view returns (Idea memory) {
        require(id > 0 && id <= ideaCount, "Invalid idea ID");
        return ideas[id];
    }
}
