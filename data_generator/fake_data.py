from faker import Faker
import random
import time

class FakeDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.user_ids = set()  # Store user_ids to ensure consistency

    def generate_bank_transactions(self):
        user_id = random.randint(10000, 99999)
        self.user_ids.add(user_id)  # Store the user_id for reuse

        transaction = {
            "transaction_id": self.fake.uuid4(),
            "timestamp": int(time.time()),
            "user_id": user_id,  # Use the generated user_id
            "amount": round(random.uniform(5, 5000), 2),
            "transaction_type": random.choice(["purchase", "transfer", "withdrawal"]),
            "location": self.fake.city(),
            "merchant": self.fake.company(),
            "card_number": self.fake.credit_card_number()
        }
        return transaction

    def generate_account_holder(self, user_id):
        account_holder = {
            "user_id": user_id,  # Use the same user_id from the transaction
            "name": self.fake.name(),
            "address": self.fake.address(),
            "phone_number": self.fake.phone_number(),
            "email": self.fake.email(),
            "date_of_birth": self.fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            "account_number": self.fake.iban(),
            "account_type": random.choice(["savings", "current", "fixed deposit"]),
            "balance": round(random.uniform(100, 100000), 2)
        }
        return account_holder

# Example usage
if __name__ == "__main__":
    generator = FakeDataGenerator()

    # Generate a bank transaction
    transaction = generator.generate_bank_transactions()
    print("Generated Transaction:", transaction)

    # Generate account holder data using the same user_id
    user_id = transaction["user_id"]
    account_holder = generator.generate_account_holder(user_id)
    print("Generated Account Holder:", account_holder)