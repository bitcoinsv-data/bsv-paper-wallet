# Security

## Model

- All key generation happens in the vendored, unmodified
  `vendor/bip39-standalone.html` (iancoleman/bip39). The UI layer added by
  `build.py` performs no cryptography: it fills the upstream form, clicks its
  buttons, and reads its output.
- The built page makes **zero network requests** and writes **nothing** to
  disk, localStorage, or cookies. Keys live only in the memory of the open tab.
- The seed phrase and the BIP38 password are never included in the print
  output. Printing is gated behind an explicit "I have written the seed
  phrase down" confirmation.
- The page detects the browser's connectivity state and shows a red
  ONLINE · NOT SAFE badge and warning whenever a connection is present.

## Intended use

For a wallet that will hold real funds: download the release file, verify its
SHA-256 checksum, copy it to a USB stick, and open it in a browser inside an
offline live session (Ubuntu or Tails live USB with networking off). Print on
a USB-cable printer, then power off. See the README for details.

## Reporting a vulnerability

Please open a GitHub issue for anything that does not reveal a working
exploit, or use GitHub's private vulnerability reporting on this repository
for anything sensitive. Reports affecting the upstream engine should also be
reported to iancoleman/bip39.
