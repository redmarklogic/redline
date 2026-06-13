"""Tests for the addin certificate generator (issue #190, Scenario 2).

Asserts only the pure, portable parts: the generated ``cert.pem``/``key.pem``
files exist, are non-empty, and the certificate carries SAN ``localhost`` and is
currently valid. The OS trust-store install is a side effect that cannot be
unit-tested portably; it is human-verified (browser padlock), not asserted here.
"""

import datetime

from cryptography import x509
from cryptography.x509.oid import ExtensionOID

from addin.make_cert import generate_localhost_cert


def test_generate_writes_nonempty_cert_and_key(tmp_path):
    """Generation writes non-empty cert.pem and key.pem into the target dir."""
    cert_path, key_path = generate_localhost_cert(tmp_path)

    assert cert_path.exists()
    assert key_path.exists()
    assert cert_path.stat().st_size > 0
    assert key_path.stat().st_size > 0


def test_generated_cert_has_localhost_san(tmp_path):
    """The leaf certificate lists `localhost` in its Subject Alternative Name."""
    cert_path, _ = generate_localhost_cert(tmp_path)

    cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
    san = cert.extensions.get_extension_for_oid(
        ExtensionOID.SUBJECT_ALTERNATIVE_NAME
    ).value
    assert "localhost" in san.get_values_for_type(x509.DNSName)


def test_generated_cert_is_currently_valid(tmp_path):
    """The leaf certificate's validity window covers the current moment."""
    cert_path, _ = generate_localhost_cert(tmp_path)

    cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
    now = datetime.datetime.now(datetime.UTC)
    assert cert.not_valid_before_utc <= now <= cert.not_valid_after_utc
