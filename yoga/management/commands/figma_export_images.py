# -*- coding: utf-8 -*-
"""
Export images from Figma into static/yoga/images/ using the Figma REST API.

Requires: FIGMA_ACCESS_TOKEN in environment.
Get token: Figma → Settings → Security → Personal access tokens.

Usage:
  set FIGMA_ACCESS_TOKEN=your_token
  python manage.py figma_export_images

  For hero background only (no overlay/text):
  python manage.py figma_export_images --hero-background-only
"""
import os
import urllib.error
import urllib.parse
import urllib.request
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings


FIGMA_FILE_KEY = "I8MWlb1THJeTQb81HP9y6R"
HERO_BANNER_NODE = "49:136"
# Use mobile hero for both desktop and mobile (set to mobile frame node ID from Figma)
# Run: python manage.py figma_export_images --list-nodes  to find mobile hero frame ID
HERO_BANNER_MOBILE_NODE = "210:41580"  # HERO BANNER MOBILE – used for hero-banner.png (desktop + mobile)
# Node IDs from Figma (HEADER DESKTOP, LOGO, HERO BANNER – hero uses mobile if HERO_BANNER_MOBILE_NODE set)
def _hero_node():
    return HERO_BANNER_MOBILE_NODE or HERO_BANNER_NODE


def _node_ids():
    return ["49:133", "49:134", _hero_node()]


def _output_names():
    return {
        "49:133": "header.png",
        "49:134": "logo.png",
        _hero_node(): "hero-banner.png",
    }


def _load_token_from_env_file():
    """Load FIGMA_ACCESS_TOKEN from project root .env if present."""
    env_path = Path(settings.BASE_DIR) / ".env"
    if not env_path.exists():
        return None
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("FIGMA_ACCESS_TOKEN="):
                    value = line.split("=", 1)[1].strip().strip("'\"")
                    return value or None
    except OSError:
        pass
    return None


def _request(token, url):
    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Figma-Token", token)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def _find_image_ref_in_node(node):
    """Recursively find first imageRef in node or its children."""
    fills = node.get("fills")
    if fills and isinstance(fills, list):
        for f in fills:
            if isinstance(f, dict) and f.get("imageRef"):
                return f["imageRef"]
    for child in node.get("children") or []:
        ref = _find_image_ref_in_node(child)
        if ref:
            return ref
    return None


def _find_background_child(token, file_key, frame_node_id):
    """Get frame's direct children; return first (bottom layer = usually background)."""
    # GET /v1/files/:key/nodes?ids=...&depth=1 returns direct children only
    url = (
        f"https://api.figma.com/v1/files/{file_key}/nodes"
        f"?ids={urllib.parse.quote(frame_node_id)}&depth=1"
    )
    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Figma-Token", token)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    nodes = data.get("nodes") or {}
    frame_data = nodes.get(frame_node_id)
    if not frame_data:
        return None
    doc_node = frame_data.get("document")
    if not doc_node:
        return None
    children = doc_node.get("children") or []
    if not children:
        return None
    # First child = bottom layer in Figma = usually the background image
    return children[0].get("id")


class Command(BaseCommand):
    help = "Export Figma nodes as PNG to yoga/static/yoga/images/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--token",
            type=str,
            default=os.environ.get("FIGMA_ACCESS_TOKEN"),
            help="Figma personal access token (or set FIGMA_ACCESS_TOKEN)",
        )
        parser.add_argument(
            "--hero-background-only",
            action="store_true",
            help="Export only hero background layer (no overlay; still rendered by Figma)",
        )
        parser.add_argument(
            "--hero-raw-image",
            action="store_true",
            help="Download hero background as raw image file (no Figma effects/filters)",
        )
        parser.add_argument(
            "--list-nodes",
            action="store_true",
            help="List all frame nodes (id + name) in the Figma file to find mobile hero node ID",
        )

    def handle(self, *args, **options):
        token = options["token"] or os.environ.get("FIGMA_ACCESS_TOKEN") or _load_token_from_env_file()
        if not token:
            self.stderr.write(
                "Error: No Figma token. Set FIGMA_ACCESS_TOKEN, use --token=..., or add it to .env"
            )
            return

        static_dir = Path(settings.BASE_DIR) / "yoga" / "static" / "yoga" / "images"
        static_dir.mkdir(parents=True, exist_ok=True)

        if options.get("list_nodes"):
            self._list_nodes(token)
            return
        if options["hero_raw_image"]:
            self._export_hero_raw_image(token, static_dir)
            return
        if options["hero_background_only"]:
            self._export_hero_background_only(token, static_dir)
            return

        node_ids = _node_ids()
        output_names = _output_names()
        ids_param = ",".join(node_ids)
        url = (
            f"https://api.figma.com/v1/images/{FIGMA_FILE_KEY}"
            f"?ids={ids_param}&format=png"
        )
        req = urllib.request.Request(url, method="GET")
        req.add_header("X-Figma-Token", token)

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            self.stderr.write(f"Figma API error: {e.code} {e.reason}")
            if e.code == 403:
                self.stderr.write("Check that your token is valid and has file read scope.")
            return
        except Exception as e:
            self.stderr.write(f"Request error: {e}")
            return

        images = data.get("images") or {}
        err = data.get("err")
        if err:
            self.stderr.write(f"Figma API err: {err}")

        saved = 0
        for node_id, download_url in images.items():
            if not download_url:
                self.stdout.write(f"Skip (no URL): {node_id}")
                continue
            name = output_names.get(node_id, node_id.replace(":", "-") + ".png")
            path = static_dir / name
            try:
                urllib.request.urlretrieve(download_url, path)
                self.stdout.write(f"Saved: {path}")
                saved += 1
            except Exception as e:
                self.stderr.write(f"Download failed {name}: {e}")

        self.stdout.write(f"Done. {saved} image(s) saved to {static_dir}")

    def _walk_frames(self, node, depth=0):
        """Recursively yield (id, name) for every FRAME node."""
        if node.get("type") == "FRAME":
            yield (node.get("id", ""), node.get("name", ""))
        for child in node.get("children") or []:
            yield from self._walk_frames(child, depth + 1)

    def _list_nodes(self, token):
        """List all FRAME nodes in the file so user can find mobile hero node ID."""
        url = f"https://api.figma.com/v1/files/{FIGMA_FILE_KEY}?depth=6"
        try:
            data = _request(token, url)
        except Exception as e:
            self.stderr.write(f"Failed to get file: {e}")
            return
        doc = data.get("document") or {}
        self.stdout.write("Frame nodes (id, name) – use id for HERO_BANNER_MOBILE_NODE:\n")
        for page in doc.get("children") or []:
            for nid, name in self._walk_frames(page):
                self.stdout.write(f"  {nid}  {name}")
        self.stdout.write("\nCurrent hero node for export: " + _hero_node())

    def _export_hero_background_only(self, token, static_dir):
        """Export only the bottom layer of HERO BANNER (background image, no overlay)."""
        hero_node = _hero_node()
        try:
            bg_id = _find_background_child(token, FIGMA_FILE_KEY, hero_node)
        except urllib.error.HTTPError as e:
            self.stderr.write(f"Figma API error: {e.code} {e.reason}")
            return
        except Exception as e:
            self.stderr.write(f"Failed to get file structure: {e}")
            return

        if not bg_id:
            self.stderr.write(
                "Could not find background layer under HERO BANNER. "
                "Check node structure in Figma. Run --list-nodes to see frame IDs."
            )
            return

        self.stdout.write(f"Exporting hero background node: {bg_id} (from frame {hero_node})")
        url = (
            f"https://api.figma.com/v1/images/{FIGMA_FILE_KEY}"
            f"?ids={urllib.parse.quote(bg_id)}&format=png"
        )
        req = urllib.request.Request(url, method="GET")
        req.add_header("X-Figma-Token", token)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            self.stderr.write(f"Export error: {e}")
            return

        images = data.get("images") or {}
        download_url = images.get(bg_id)
        if not download_url:
            self.stderr.write(f"No image URL for node {bg_id}. Node may not be renderable.")
            return

        path = static_dir / "hero-banner.png"
        try:
            urllib.request.urlretrieve(download_url, path)
            self.stdout.write(f"Saved: {path} (hero background only, no overlay)")
        except Exception as e:
            self.stderr.write(f"Download failed: {e}")

    def _export_hero_raw_image(self, token, static_dir):
        """Download the raw image used in hero (image fill), no Figma effects."""
        hero_node = _hero_node()
        # 1) Get hero subtree to find imageRef
        url_nodes = (
            f"https://api.figma.com/v1/files/{FIGMA_FILE_KEY}/nodes"
            f"?ids={urllib.parse.quote(hero_node)}&depth=4"
        )
        req = urllib.request.Request(url_nodes, method="GET")
        req.add_header("X-Figma-Token", token)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            self.stderr.write(f"Failed to get file nodes: {e}")
            return
        nodes = data.get("nodes") or {}
        frame_data = nodes.get(hero_node)
        if not frame_data:
            self.stderr.write("Hero banner node not found.")
            return
        doc_node = frame_data.get("document")
        if not doc_node:
            self.stderr.write("Hero banner document not found.")
            return
        image_ref = _find_image_ref_in_node(doc_node)
        if not image_ref:
            self.stderr.write(
                "No image fill found in hero banner. Use --hero-background-only for rendered layer."
            )
            return
        # 2) Get all image fill URLs
        url_fills = f"https://api.figma.com/v1/files/{FIGMA_FILE_KEY}/images"
        req = urllib.request.Request(url_fills, method="GET")
        req.add_header("X-Figma-Token", token)
        try:
            with urllib.request.urlopen(req) as resp:
                fills_data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            self.stderr.write(f"Image fills API error: {e.code} {e.reason}")
            return
        except Exception as e:
            self.stderr.write(f"Failed to get image fills: {e}")
            return
        # API returns {"images": {"imageRef": "https://..."}}
        images = fills_data.get("images")
        if images is None:
            images = fills_data
        if not isinstance(images, dict):
            images = {}
        download_url = images.get(image_ref)
        if not download_url and images:
            for key, url in images.items():
                if key and (key == image_ref or image_ref.startswith(key) or key.startswith(image_ref)):
                    download_url = url
                    break
        if not download_url and len(images) == 1:
            download_url = next(iter(images.values()), None)
        if not download_url:
            self.stdout.write(
                "Raw image fills not available for this file; saving rendered layer without overlay instead."
            )
            self._export_hero_background_only(token, static_dir)
            return
        path = static_dir / "hero-banner.png"
        try:
            urllib.request.urlretrieve(download_url, path)
            self.stdout.write(f"Saved: {path} (raw image, no effects)")
        except Exception as e:
            self.stderr.write(f"Download failed: {e}")
