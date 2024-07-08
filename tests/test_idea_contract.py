import pytest
from brownie import accounts, UsageTrackingContract

@pytest.fixture
def idea_contract():
    account = accounts[0]
    contract = UsageTrackingContract.deploy({'from': account})
    return contract

def test_submit_and_get_idea(idea_contract):
    account = accounts[0]
    idea_description = "My first idea"
    
    # Submit an idea
    tx = idea_contract.submitIdea(idea_description, {'from': account})
    tx.wait(1)
    
    # Get the idea
    idea_id, creator, description, timestamp = idea_contract.getIdea(1)
    
    assert idea_id == 1
    assert creator == account.address
    assert description == idea_description
    assert timestamp > 0

def test_idea_count(idea_contract):
    account = accounts[0]
    
    # Initially, the idea count should be 0
    assert idea_contract.ideaCount() == 0
    
    # Submit an idea
    idea_contract.submitIdea("First idea", {'from': account})
    
    # The idea count should now be 1
    assert idea_contract.ideaCount() == 1

def test_multiple_ideas(idea_contract):
    account = accounts[0]
    
    # Submit multiple ideas
    idea_contract.submitIdea("Idea 1", {'from': account})
    idea_contract.submitIdea("Idea 2", {'from': account})
    
    # Get the ideas
    idea1 = idea_contract.getIdea(1)
    idea2 = idea_contract.getIdea(2)
    
    assert idea1[2] == "Idea 1"
    assert idea2[2] == "Idea 2"
