import pytest
import importlib
import pkg_resources

def get_required_packages():
    with open('requirements.in', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

REQUIRED_PACKAGES = get_required_packages()

@pytest.mark.parametrize("package", REQUIRED_PACKAGES)
def test_required_packages_installed(package):
    try:
        pkg_resources.get_distribution(package)
    except pkg_resources.DistributionNotFound:
        pytest.fail(f"Required package '{package}' is not installed.")