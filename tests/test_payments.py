import pytest
from app.services.payments import create_invoice


@pytest.mark.asyncio
async def test_create_invoice():
    payment_id = await create_invoice(123456, 1, 100.0)
    assert payment_id > 0