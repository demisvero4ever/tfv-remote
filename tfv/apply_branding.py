"""Applies Tampa FL VoIP Remote branding on top of a clean RustDesk checkout.

Usage: python3 -I apply_branding.py <path-to-rustdesk-checkout>
Re-runnable: every edit checks for the original text first.
"""
import base64
import io
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ICON = Image.open(HERE / "branding" / "tfv-remote-icon-1024.png").convert("RGBA")
ICON_OPAQUE = Image.open(HERE / "branding" / "tfv-remote-icon-1024-opaque.png").convert("RGB")

SERVER = "remote.tampaflvoip.com"
PUB_KEY = "M5TDNq39SIxWChHR0P5YuRJ9bsxaYlHsDNYRK+Im1bg="
APP_NAME = "TFVRemote"              # internal: config dirs, service names (no spaces on purpose)
LONG_NAME = "Tampa FL VoIP Remote"  # desktop display name
SHORT_NAME = "TFV Remote"           # phone launcher label
BUNDLE_ID = "com.tampaflvoip.remote"

root = pathlib.Path(sys.argv[1]).resolve()
changes = []


def edit(rel, old, new, count=1):
    p = root / rel
    s = p.read_text()
    if new in s and old not in s:
        return  # already applied
    if s.count(old) < count:
        sys.exit(f"ERROR: expected text not found in {rel}: {old!r}")
    p.write_text(s.replace(old, new))
    changes.append(rel)


def png(rel, opaque=False, pad=0.0):
    p = root / rel
    w, h = Image.open(p).size
    src = ICON_OPAQUE if opaque else ICON
    if pad:
        inner = int(w * (1 - 2 * pad))
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        img.alpha_composite(ICON.resize((inner, inner), Image.LANCZOS), ((w - inner) // 2, (h - inner) // 2))
    else:
        img = src.resize((w, h), Image.LANCZOS)
    img.save(p)
    changes.append(rel)


# 1. Our own server and its public key
edit("libs/hbb_common/src/config.rs",
     'RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"]',
     f'RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"]')
edit("libs/hbb_common/src/config.rs",
     'RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="',
     f'RS_PUB_KEY: &str = "{PUB_KEY}"')
edit("libs/hbb_common/src/config.rs",
     'APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned())',
     f'APP_NAME: RwLock<String> = RwLock::new("{APP_NAME}".to_owned())')

# 2. Display names
edit("flutter/android/app/src/main/AndroidManifest.xml", 'android:label="RustDesk"', f'android:label="{SHORT_NAME}"')
edit("flutter/android/app/src/main/AndroidManifest.xml", 'android:label="RustDesk Input"', f'android:label="{SHORT_NAME} Input"')
edit("flutter/ios/Runner/Info.plist", "<string>RustDesk</string>", f"<string>{SHORT_NAME}</string>", count=2)
edit("flutter/windows/runner/Runner.rc", '"RustDesk Remote Desktop"', f'"{LONG_NAME}"')
edit("flutter/windows/runner/Runner.rc", 'VALUE "ProductName", "RustDesk"', f'VALUE "ProductName", "{LONG_NAME}"')

# 3. Store identities (needed to sign with the Tampa FL VoIP Apple/Google accounts)
edit("flutter/android/app/build.gradle", 'applicationId "com.carriez.flutter_hbb"', f'applicationId "{BUNDLE_ID}"')
edit("flutter/ios/Runner.xcodeproj/project.pbxproj",
     "PRODUCT_BUNDLE_IDENTIFIER = com.carriez.flutterHbb;", f"PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID};", count=3)

# 4. Icons: every existing file is replaced at its own size
for rel in ["res/icon.png", "res/mac-icon.png", "res/32x32.png", "res/64x64.png", "res/128x128.png", "res/128x128@2x.png"]:
    png(rel)
for ico in ["res/icon.ico", "res/tray-icon.ico"]:
    ICON.save(root / ico, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    changes.append(ico)
for p in sorted((root / "flutter/android/app/src/main/res").glob("mipmap-*/ic_launcher*.png")):
    rel = p.relative_to(root).as_posix()
    png(rel, pad=0.2 if "foreground" in rel else 0.0)  # adaptive icons crop the outer ring
for p in sorted((root / "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset").glob("*.png")):
    png(p.relative_to(root).as_posix(), opaque=True)  # App Store rejects transparency

# In-app logo: SVG wrapper around the PNG so the UI picks it up without code changes
buf = io.BytesIO()
ICON.resize((256, 256), Image.LANCZOS).save(buf, "PNG")
data = base64.b64encode(buf.getvalue()).decode()
svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="256" height="256" viewBox="0 0 256 256"><image width="256" height="256" '
       f'xlink:href="data:image/png;base64,{data}"/></svg>\n')
for rel in ["flutter/assets/icon.svg", "res/logo.svg"]:
    (root / rel).write_text(svg)
    changes.append(rel)

print(f"{len(changes)} files branded")
