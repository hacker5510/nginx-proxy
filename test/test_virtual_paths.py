from time import sleep

import pytest
from docker.errors import NotFound

@pytest.mark.parametrize("stub,expected_port", [
    ("nginx-proxy.test/web1", 81),
    ("nginx-proxy.test/web2", 82),
    ("nginx-proxy.test", 83),
    ("foo.nginx-proxy.test", 42),
])
def test_valid_path(docker_compose, nginxproxy, stub, expected_port):
    r = nginxproxy.get(f"http://{stub}/port")
    assert r.status_code == 200
    assert r.text == f"answer from port {expected_port}\n"

@pytest.mark.parametrize("stub", [
    "nginx-proxy.test/foo",
    "bar.nginx-proxy.test",
])
def test_invalid_path(docker_compose, nginxproxy, stub):
    r = nginxproxy.get(f"http://{stub}/port")
    assert r.status_code in [404, 503]

"""
Test if we can remove a single virtual_path from multiple ones on the same subdomain.

TODO: FIX: This test is currently failing!
"""
def test_container_removal(docker_compose, nginxproxy):
    r = nginxproxy.get(f"http://nginx-proxy.test/web2/port")
    assert r.status_code == 200
    assert r.text == f"answer from port 82\n"
    try:
        docker_compose.containers.get("web2").remove(force=True)
    except NotFound:
        pass
    r = nginxproxy.get(f"http://nginx-proxy.test/web2/port")
    assert r.status_code in [404, 503]

