from fastapi  import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from web3 import Web3
from db import SessionLocal, database, Idea
from pydantic import BaseModel
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.../.env')
load_dotenv(dotenv_path)

app = FastAPI()

# Read the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# connect to local ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Contract ABI and Address
idea_contract_abi = [...] # ABI of IdeaContract
idea_contract_address = '0xYourContractAddress'

idea_contract = w3.eth.contract(address=idea_contract_address, abi=idea_contract_abi)

# Dependency to get DB session
def get_db():
    db = SessionLocal(DATABASE_URL=DATABASE_URL)
    try:
        yield db
    finally:
        db.close()

class IdeaBase(BaseModel):
    description: str
    creator: str

class IdeaCreate(IdeaBase):
    private_key: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/submit_idea/")
async def submit_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    nonce = w3.eth.getTransactionCount(idea.creator)
    txn = idea_contract.functions.submitIdea(idea.description).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=idea.private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    new_idea = Idea(description=idea.description, creator=idea.creator, timestamp=w3.eth.getBlock('latest')['timestamp'])
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return new_idea

@app.get("/get_idea/{idea_id}", response_model=IdeaBase)
async def get_idea(idea_id: int, db: Session = Depends(get_db)):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()

    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea