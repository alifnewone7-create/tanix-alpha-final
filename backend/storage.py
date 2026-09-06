import json
from config import DATA_DIR, OWNER_TAG

CHANNELS_FILE = DATA_DIR / "channels.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
SIGNALS_FILE = DATA_DIR / "signals.json"


def _load(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


MAX_CHANNELS = 10

BRAND_NAME = "TaNix Alpha 2.0"
BRAND_KEYS = ("image_name", "text_name", "owner_tag")
DEFAULT_BRAND = {
    "image_name": BRAND_NAME,
    "text_name": BRAND_NAME,
    "owner_tag": OWNER_TAG,
}


def get_channels():
    return _load(CHANNELS_FILE, [])


def get_channel(chat_id):
    return next((c for c in get_channels() if c["id"] == chat_id), None)


def add_channel(chat_id, title):
    """Returns 'updated', 'added' or 'limit'."""
    channels = get_channels()
    for ch in channels:
        if ch["id"] == chat_id:
            ch["title"] = title
            _save(CHANNELS_FILE, channels)
            return "updated"
    if len(channels) >= MAX_CHANNELS:
        return "limit"
    channels.append({"id": chat_id, "title": title})
    _save(CHANNELS_FILE, channels)
    return "added"


def get_channel_brand(chat_id):
    """Per-channel branding, falling back to the global defaults."""
    ch = get_channel(chat_id) or {}
    brand = dict(DEFAULT_BRAND)
    for key in BRAND_KEYS:
        val = ch.get(key)
        if val:
            brand[key] = val
    return brand


def set_channel_brand(chat_id, key, value):
    if key not in BRAND_KEYS:
        return False
    channels = get_channels()
    for ch in channels:
        if ch["id"] == chat_id:
            ch[key] = value
            _save(CHANNELS_FILE, channels)
            return True
    return False


def reset_channel_brand(chat_id):
    channels = get_channels()
    for ch in channels:
        if ch["id"] == chat_id:
            for key in BRAND_KEYS:
                ch.pop(key, None)
            _save(CHANNELS_FILE, channels)
            return True
    return False


def remove_channel(chat_id):
    channels = [c for c in get_channels() if c["id"] != chat_id]
    _save(CHANNELS_FILE, channels)


DEFAULT_SETTINGS = {"mtg": "MTG-1", "strategy": "classic", "per_trade_pct": 1.0}


def get_settings():
    s = _load(SETTINGS_FILE, {})
    return {**DEFAULT_SETTINGS, **s}


def save_settings(settings):
    _save(SETTINGS_FILE, settings)


def append_signal(record):
    signals = _load(SIGNALS_FILE, [])
    signals.append(record)
    _save(SIGNALS_FILE, signals)


def get_signals():
    return _load(SIGNALS_FILE, [])
