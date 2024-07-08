from brownie import accounts, Contract, IdeaContract

def main():
    account = accounts[0]
    contract_address = "0xd8F2819AaE2ac39b903400D9ee3966c757233Dcb"  # Replace with your contract address

    # Load the contract from the specified address
    idea_contract = Contract.from_abi("IdeaContract", contract_address, IdeaContract.abi)

    # Submit an idea
    tx = idea_contract.submitIdea("My first idea", {'from': account})
    tx.wait(1)
    print("Idea submitted!")

    # Get the idea
    idea = idea_contract.getIdea(1)
    print(f"Idea ID: {idea[0]}, Creator: {idea[1]}, Description: {idea[2]}, Timestamp: {idea[3]}")
