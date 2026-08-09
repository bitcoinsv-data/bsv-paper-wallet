# BSV Paper Wallet

A free, open-source **Bitcoin SV ($BSV) paper wallet generator** in a single HTML file.
Download it, go offline, open it in any browser: no installation, no account, no server.

Built on the audited, widely-used [iancoleman/bip39](https://github.com/iancoleman/bip39)
engine (vendored untouched in this repository), with a guided interface designed so that a
first-time user cannot skip the steps that keep their coins safe.

## Download

**[⬇ Download bsv-paper-wallet.html](https://github.com/bitcoinsv-data/bsv-paper-wallet/releases/latest/download/bsv-paper-wallet.html)**
— that single file is the whole tool.

Open it with a real browser (Chrome, Firefox, Safari, Edge). Some "HTML viewer" apps block
JavaScript, and the generator needs it: the keys are made inside the browser, which is why
nothing is ever sent anywhere.

All versions and checksums: [releases](../../releases).

## How to use it safely

The file works in any modern browser. How safe your wallet is depends on **where you open it**:

| | Setup | Good for |
|---|---|---|
| 🥇 **Best** | Copy the file to a USB stick. Boot the computer from an Ubuntu or Tails **live USB**, without network. Open the file, generate, print, power off. Nothing ever touches a hard drive. | Any amount |
| 🥈 **Good** | Your everyday computer with **Wi-Fi switched off** (the badge in the top corner turns green by itself). Print on a USB-cable printer. Close the browser and reboot afterwards. | Modest amounts |
| 🔴 **Never** | Online. The tool shows a red **ONLINE · NOT SAFE** badge and a warning. Use this mode only to explore with throwaway wallets. | Nothing real |

The interface walks you through the rest: write down the seed phrase by hand (it is never
printed and never sent to the printer), optionally protect the printed keys with a BIP38
password, and printing stays locked until you confirm the seed phrase is written down.

## What it generates

- A standard **BIP39 seed phrase** (12 or 24 words) — restorable in any wallet that lets you
  set the derivation path, using `m/44'/236'/0'`. On BSV that is
  [ElectrumSVP](https://electrumsv.io), the maintained fork of the old ElectrumSV client.
- **1 to 20 paper wallets** derived from that one seed, printed as cut-out strips: green
  SHARE half (deposit address + QR) and SECRET half (private key + QR), plus a printed
  usage guide on the same sheet.
- Optional **BIP38 encryption** of the printed private keys: a stolen printout is useless
  without your password, and your handwritten seed phrase still restores everything if the
  password is lost.

## Why you can trust it

- **It cannot phone home.** The page makes zero network requests: no fonts, no analytics,
  no APIs. Verify it yourself: open the browser dev tools (F12) → Network tab.
- **Nothing is stored.** Keys exist only in the memory of the open tab. Close it and they
  are gone. Nothing is written to disk, localStorage, or cookies.
- **The cryptography is not ours.** All key generation is performed by the vendored,
  byte-for-byte unmodified `bip39-standalone.html` from iancoleman/bip39 (a tool used and
  reviewed by the crypto community since 2014). Our code only drives its interface and
  reads its results. You can diff `vendor/bip39-standalone.html` against the official
  release yourself.
- **The build is reproducible.** `python build.py` regenerates `bsv-paper-wallet.html`
  from the vendored engine + the UI layer in this repository. Compare checksums with
  `SHA256SUMS.txt`.

### Verify your download

Open a terminal in the folder where you saved the file and run the command for your system:

**Windows** (right-click the folder → "Open in Terminal", or type `powershell` in the
Explorer address bar):

```powershell
Get-FileHash bsv-paper-wallet.html
```

**macOS:**

```bash
shasum -a 256 bsv-paper-wallet.html
```

**Linux:**

```bash
sha256sum bsv-paper-wallet.html
```

Compare the result with the checksum published on the release page (upper or lower case does
not matter). If the first and last few characters match, your copy is genuine.

## Build from source

Requires Python 3 (no dependencies):

```bash
python build.py
# -> bsv-paper-wallet.html
```

## Credits

- Key generation engine: [iancoleman/bip39](https://github.com/iancoleman/bip39) (MIT),
  which itself bundles bitcoinjs-lib, kjua and others — see the in-file notices.
- QR rendering: [kjua](https://github.com/lrsjng/kjua) (MIT), bundled by the upstream file.
- Bitcoin SV logo: trademark of its respective owners, used to identify the coin.

## License

MIT — see [LICENSE](LICENSE). The vendored upstream file keeps its own MIT license and
copyright notices.

## Disclaimer

This software is provided "as is", without warranty of any kind. Paper wallets put you in
sole charge of your keys: a lost seed phrase or a leaked private key means lost coins, and
nobody can reverse that. Test with a small amount first. Use at your own risk.
