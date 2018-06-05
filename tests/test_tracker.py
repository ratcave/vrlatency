import natnetclient as natnet
import pytest

@pytest.fixture
def client():
    return natnet.NatClient()


def test_has_LED_body(client):
    assert 'LED' in client.rigid_bodies