from brownie import UsageTrackingContract, accounts

def main():
    account = accounts[0]
    usage_tracking_contract = UsageTrackingContract.deploy({'from': account})
    print(f"UsageTrackingContract deployed at {usage_tracking_contract.address}")
    print(f"IdeaContract deployed at {usage_tracking_contract.ideaContract()}")
