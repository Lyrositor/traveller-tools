from typing import Optional

import requests

POSTER_API_URL = "https://travellermap.com/api/poster"


def render_sector_poster_svg(data: str, metadata: Optional[str] = None, subsector: Optional[str] = None) -> str:
    form_data = dict(data=data, accept="image/svg+xml", style="mongoose", scale="64", options="25591")
    if metadata:
        form_data["metadata"] = metadata
    if subsector:
        form_data["subsector"] = subsector
    response = requests.post(POSTER_API_URL, data=form_data)
    return response.text
