# Germany: automatic tracking from GLS e-mail

The German GLS tracking hub already supports parcel numbers and postcodes, but
does not yet support consumer-account sign-in. This optional automation is a
local workaround for automatic discovery from incoming GLS notification mail.
It is not an account integration and does not read the GLS app's parcel list.

## Setup

1. Install GLS and configure **Tracking codes → Germany**, using your five-digit
   delivery postcode. Use one unambiguous tracking hub for this postcode.
2. Create a dedicated mail folder for GLS notifications and a server-side
   filtering rule limited to verified GLS senders. Configure Home Assistant's
   [IMAP integration](https://www.home-assistant.io/integrations/imap/) for that
   folder. In its options, include `text` in the event data. Start with the
   default event size and increase only if the relevant lines are truncated.
3. Import the [blueprint](../blueprints/gls_de_mail_tracking.yaml) into Home
   Assistant (Settings → Automations & scenes → Blueprints → Import blueprint),
   using the raw GitHub URL for the desired revision, or place it under
   `config/blueprints/automation/gls/`. Create an automation from it.
4. Enter the exact IMAP username and folder, the exact sender values observed
   in trusted GLS messages (one per line), and the delivery postcode. The sender
   allowlist is not an authentication mechanism: enforce your mail provider's
   anti-spoofing checks and dedicated filtering at the source.
5. Verify with a real new GLS notification to the configured mailbox and
   confirm the new parcel appears in the GLS incoming sensor and optional
   Parcel Aggregator. Do not use live parcel identifiers in public issues.

The blueprint accepts labeled 11–12-digit parcel numbers and mixed
eight-character Track IDs, plus the `match` parameter of recognized GLS tracking
page URLs. It never follows e-mail links. It ignores unqualified number runs,
unknown senders and non-initial events; repeated identical codes are deduplicated.
The existing GLS service handles already-tracked codes. A short Track ID and
long parcel number may identify the same parcel but are distinct input codes.
Only supported mail layouts are recognized, not arbitrary HTML or attachments;
the tests use synthetic messages, not verified live German notification samples.
The automation does not scan historical mail or discover packages for which no
matching notification arrives. The configured postcode is used for every code.

## Privacy and operational limitations

No AI task or cloud e-mail processing is required. The IMAP integration still
has access to the configured mailbox and publishes message text on HA's event
bus. Keep the IMAP scope narrow; if appropriate, exclude `imap_content` from
Recorder's event recording and review other event consumers. The blueprint
disables its stored automation traces. Do not use mailbox passwords or real
tracking numbers in the repo. Other mailbox integrations are unchanged.

GLS is queried only by its existing tracking component; this automation does
not access a GLS consumer account or change delivery preferences. It can be
disabled or removed independently of the GLS integration.

## Native account mode

GLS's [official German app](https://apps.apple.com/de/app/gls-pakete/id1614461687)
supports automatic discovery of packages associated with an account. A German
consumer-account sign-in and read-only feed are not yet verified for this
component. Native support requires a verified user-authorized authentication
and refresh flow, a complete account-scoped feed, redacted test fixtures, and
end-to-end acceptance with a real account. No unsupported login is exposed.
