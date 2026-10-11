#!/usr/bin/env -S uv run --quiet --with boto3 --script
"""Transfer a domain's registration into Route 53 Domains (brianpfeil.com from Hover, 2026-10-11).

    ./infra/scripts/transfer_domain.py brianpfeil.com          # prompts for the auth code, hidden
    ./infra/scripts/transfer_domain.py brianpfeil.com --check  # transferability + price only

The authorization (EPP) code is a secret: it is read with getpass, sent to Route 53, and never
printed, logged or stored. The registrant contact is copied, at run time, from a domain already
registered in this account (never printed, never written to git) — the same rule as
~/projects/media/scripts/register_domain.py. Nameservers are the Route 53 hosted zone's own, so
the transfer changes nothing about how the domain resolves. 1 year added, auto-renew on, WHOIS
privacy on.

Idempotent: a transfer already in progress for the domain is reported and polled, not resubmitted.
"""

from __future__ import annotations

import argparse
import getpass
import sys
import time

import boto3

REGION = "us-east-1"  # the Route 53 Domains API lives only here
CONTACT_FIELDS = ("FirstName", "LastName", "AddressLine1", "City", "CountryCode", "ZipCode", "PhoneNumber", "Email")


def existing_contact(domains, skip: str) -> tuple[dict, str]:
    for d in domains.list_domains().get("Domains", []):
        name = d["DomainName"]
        if name == skip:
            continue
        c = domains.get_domain_detail(DomainName=name).get("RegistrantContact") or {}
        if all(c.get(f) for f in CONTACT_FIELDS):
            return {k: v for k, v in c.items() if v not in (None, "", [])}, name
    sys.exit("no domain in this account with a complete registrant contact to copy")


def zone_nameservers(route53, domain: str) -> list[dict]:
    zones = route53.list_hosted_zones_by_name(DNSName=domain, MaxItems="1")["HostedZones"]
    if not zones or zones[0]["Name"].rstrip(".") != domain:
        sys.exit(f"no Route 53 hosted zone for {domain}")
    ns = route53.get_hosted_zone(Id=zones[0]["Id"])["DelegationSet"]["NameServers"]
    return [{"Name": n} for n in ns]


def in_progress(domains, domain: str) -> str | None:
    for op in domains.list_operations(MaxItems=50).get("Operations", []):
        if op.get("DomainName") == domain and op.get("Type") == "TRANSFER_IN_DOMAIN" and op["Status"] in ("SUBMITTED", "IN_PROGRESS"):
            return op["OperationId"]
    return None


def poll(domains, op_id: str, minutes: int) -> str:
    end = time.time() + minutes * 60
    status = "?"
    while time.time() < end:
        d = domains.get_operation_detail(OperationId=op_id)
        status = f"{d['Status']}{(' — ' + d['Message']) if d.get('Message') else ''}"
        print(f"  {time.strftime('%H:%M:%S')} {status}", flush=True)
        if d["Status"] in ("SUCCESSFUL", "FAILED", "ERROR"):
            break
        time.sleep(30)
    return status


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--finish", action="store_true",
                    help="after the transfer lands: WHOIS privacy and the transfer lock, which a transfer-in does NOT "
                         "carry over (brianpfeil.com arrived 2026-10-11 with privacy off despite the flags)")
    ap.add_argument("--wait-minutes", type=int, default=3)
    a = ap.parse_args()
    domains = boto3.client("route53domains", region_name=REGION)
    route53 = boto3.client("route53")

    if a.finish:
        domains.update_domain_contact_privacy(DomainName=a.domain, AdminPrivacy=True, RegistrantPrivacy=True, TechPrivacy=True)
        domains.enable_domain_transfer_lock(DomainName=a.domain)
        print(f"{a.domain}: privacy on, transfer lock requested")
        return 0
    if any(d["DomainName"] == a.domain for d in domains.list_domains().get("Domains", [])):
        print(f"{a.domain} is already registered in this account — nothing to transfer")
        return 0
    op = in_progress(domains, a.domain)
    if op:
        print(f"a transfer is already in progress ({op}) — polling it")
        poll(domains, op, a.wait_minutes)
        return 0

    t = domains.check_domain_transferability(DomainName=a.domain)["Transferability"]["Transferable"]
    price = next(p for p in domains.list_prices(Tld=a.domain.rsplit(".", 1)[1])["Prices"])["TransferPrice"]
    print(f"{a.domain}: {t}; transfer price {price['Price']} {price['Currency']} (adds a year)")
    if a.check:
        return 0
    if t not in ("TRANSFERABLE", "PREMIUM_DOMAIN"):
        print("not transferable yet — is the registrar's transfer lock off?")
        return 1

    contact, source = existing_contact(domains, a.domain)
    ns = zone_nameservers(route53, a.domain)
    print(f"registrant contact copied from {source}; nameservers: {', '.join(n['Name'] for n in ns)}")
    code = getpass.getpass(f"Paste the authorization code for {a.domain} from Hover (hidden), then Enter: ").strip()
    if not code:
        print("no code — nothing submitted")
        return 1
    out = domains.transfer_domain(
        DomainName=a.domain, DurationInYears=1, Nameservers=ns, AuthCode=code, AutoRenew=True,
        AdminContact=contact, RegistrantContact=contact, TechContact=contact,
        PrivacyProtectAdminContact=True, PrivacyProtectRegistrantContact=True, PrivacyProtectTechContact=True,
    )
    code = None
    print(f"transfer submitted: operation {out['OperationId']}")
    print(poll(domains, out["OperationId"], a.wait_minutes))
    print("Hover will email a transfer-away notice; approving it there finishes in minutes, otherwise it completes in about 5 days.")
    print(f"When it lands: ./infra/scripts/transfer_domain.py {a.domain} --finish  (privacy + transfer lock)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
