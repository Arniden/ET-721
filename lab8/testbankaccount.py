import unittest

from bankaccount import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        """Create a default account before each test."""
        self.account = BankAccount("Alice", 100)

    # 2. Initialization
    def test_initial_balance(self):
        self.assertEqual(self.account.get_balance(), 100)
        self.assertEqual(self.account.owner, "Alice")

    def test_default_initial_balance_is_zero(self):
        account = BankAccount("Bob")
        self.assertEqual(account.get_balance(), 0)

    # 3. Deposit
    def test_deposit_adds_to_balance(self):
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_deposit_non_positive_amount_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        with self.assertRaises(ValueError):
            self.account.deposit(-10)
            self.assertEqual(self.account.get_balance(), 100)

    # 4. Withdrawal
    def test_withdraw_subtracts_from_balance(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.get_balance(), 70)

    def test_withdraw_entire_balance(self):
        self.account.withdraw(100)
        self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_non_positive_amount_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-5)
        self.assertEqual(self.account.get_balance(), 100)

    # 5. Overdraw
    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(101)
        self.assertIn("Insufficient funds", str(context.exception))
        # Balance must be unchanged after the failed withdrawal
        self.assertEqual(self.account.get_balance(), 100)

    # 6. Sequence of operations
    def test_sequence_of_deposits_and_withdrawals(self):
        self.account.deposit(50)    # 150
        self.account.withdraw(30)   # 120
        self.account.deposit(200)   # 320
        self.account.withdraw(120)  # 200
        self.account.withdraw(50)   # 150
        self.assertEqual(self.account.get_balance(), 150)

    def test_failed_operation_in_sequence_does_not_change_balance(self):
        self.account.deposit(25)    # 125
        with self.assertRaises(ValueError):
            self.account.withdraw(500)
        self.account.withdraw(25)   # 100
        self.assertEqual(self.account.get_balance(), 100)


if __name__ == "__main__":
    unittest.main()