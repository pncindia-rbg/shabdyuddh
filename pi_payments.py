"""Pi Network entry fee: STUB ONLY. No real payment is wired yet.

Testnet plan (later):
  1. Frontend/Pi Browser calls Pi.createPayment({amount: ENTRY_FEE_PI, memo, metadata}).
  2. Server approval: POST to Pi Platform API /v2/payments/{payment_id}/approve with PI_API_KEY.
  3. Client completes the tx, server verifies via /v2/payments/{payment_id}/complete.
  4. Store payment_id + status in SQLite before pairing the player.
Until then charge_entry() always returns True so the duel flow can be tested for free.
"""
import config


async def charge_entry(user_id: int, amount: float = config.ENTRY_FEE_PI) -> bool:
    # TODO(testnet): replace with real Pi approve/complete flow. Stub: always succeeds.
    return True


async def refund_entry(user_id: int, amount: float = config.ENTRY_FEE_PI) -> bool:
    # TODO(testnet): refund hook for players who leave the queue before pairing.
    return True
