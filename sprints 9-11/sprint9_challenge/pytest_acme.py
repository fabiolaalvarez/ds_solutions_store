import pytest
from acme_report import generate_products

def test_generate_products():
    """Check that we make 30 products by default."""
    assert len(generate_products()), 30