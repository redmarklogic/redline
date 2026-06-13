"""Generate and trust a local `localhost` HTTPS certificate, Python-only (issue #190).

Adapted from the Masterjx9 Outlook-Addin-TaskPane-python template's
``devcerts/generate.py`` and ``devcerts/install.py`` (see ``README.md``). Unlike
the template we (a) use timezone-aware datetimes (``datetime.utcnow`` is
deprecated and trips ``filterwarnings=error``), (b) write ``cert.pem``/``key.pem``
into ``src/addin/certs/`` rather than ``~/.office-addin-dev-certs/``, and (c) keep
generation a pure function so it is unit-testable against a temp directory.

A self-signed CA signs a ``localhost`` leaf certificate. The leaf (cert.pem) and
its key (key.pem) are what Flask serves; the CA is what gets installed into the
host trust store so browsers accept the leaf without warning.

Run::

    python -m addin.make_cert
"""

import datetime
import subprocess
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

HERE = Path(__file__).resolve().parent
CERTS_DIR = HERE / "certs"

_CA_ORG = "Developer CA for Microsoft Office Add-ins"
_VALID_DAYS = 30


def _private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def _ca_certificate(ca_key: rsa.RSAPrivateKey) -> x509.Certificate:
    """Build a self-signed CA certificate."""
    name = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "WA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Redmond"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, _CA_ORG),
            x509.NameAttribute(NameOID.COMMON_NAME, _CA_ORG),
        ]
    )
    return (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(_now())
        .not_valid_after(_now() + datetime.timedelta(days=_VALID_DAYS))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )


def _localhost_certificate(
    leaf_key: rsa.RSAPrivateKey,
    ca_cert: x509.Certificate,
    ca_key: rsa.RSAPrivateKey,
) -> x509.Certificate:
    """Build a `localhost` leaf certificate signed by the CA, with SAN localhost."""
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "WA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Redmond"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "localhost"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ]
    )
    return (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(leaf_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(_now())
        .not_valid_after(_now() + datetime.timedelta(days=_VALID_DAYS))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )


def _write_pem_cert(cert: x509.Certificate, path: Path) -> None:
    path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


def _write_pem_key(key: rsa.RSAPrivateKey, path: Path) -> None:
    path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )


def generate_localhost_cert(certs_dir: Path) -> tuple[Path, Path]:
    """Generate a CA + `localhost` leaf cert into ``certs_dir``.

    Writes ``cert.pem`` (the leaf Flask serves), ``key.pem`` (its private key) and
    ``ca.pem`` (the CA, which is what gets installed into the trust store).

    Args:
        certs_dir: Directory to write the PEM files into; created if absent.

    Returns:
        The ``(cert_path, key_path)`` of the leaf certificate and its key.
    """
    certs_dir = Path(certs_dir)
    certs_dir.mkdir(parents=True, exist_ok=True)

    ca_key = _private_key()
    ca_cert = _ca_certificate(ca_key)
    leaf_key = _private_key()
    leaf_cert = _localhost_certificate(leaf_key, ca_cert, ca_key)

    cert_path = certs_dir / "cert.pem"
    key_path = certs_dir / "key.pem"
    ca_path = certs_dir / "ca.pem"

    _write_pem_cert(leaf_cert, cert_path)
    _write_pem_key(leaf_key, key_path)
    _write_pem_cert(ca_cert, ca_path)

    return cert_path, key_path


def _install_ca_windows(ca_path: Path) -> bool:
    """Install the CA cert into the Windows CurrentUser Root trust store.

    Uses PowerShell ``Import-Certificate`` — the mechanism the Masterjx9 template
    uses (T002a). Returns True on success, False on a denied/failed write.
    """
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        f"Import-Certificate -FilePath '{ca_path}' "
        "-CertStoreLocation Cert:\\CurrentUser\\Root",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0


def main() -> None:
    """Generate the certificate and install the CA into the trust store.

    On a non-Windows platform or a denied trust-store write, prints an actionable
    message naming the elevated-shell requirement rather than failing silently
    (edge case: trust write denied without an administrator shell).
    """
    cert_path, key_path = generate_localhost_cert(CERTS_DIR)
    ca_path = CERTS_DIR / "ca.pem"
    print(f"Generated certificate:\n  cert: {cert_path}\n  key:  {key_path}")

    if sys.platform != "win32":
        print(
            "Trust-store install is only wired for Windows in this spike. "
            f"Install {ca_path} into your OS trust store manually to clear the "
            "browser warning."
        )
        return

    if _install_ca_windows(ca_path):
        print(
            "Installed CA into Cert:\\CurrentUser\\Root. https://localhost is trusted."
        )
    else:
        print(
            "Could not install the CA certificate into the trust store. "
            "Re-run this command from an elevated (Administrator) PowerShell, "
            f"or import {ca_path} into Cert:\\CurrentUser\\Root manually."
        )


if __name__ == "__main__":
    main()
