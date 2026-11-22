import json

async def fetch_player_matches(page, steamid64: str, matches: int = 50) -> dict:
    """
    Fetches player's chat logs through the existing Chrome session using Playwright.
    Returns the decoded API response.
    """

    result = await page.evaluate(
        """
        async ({ steamid, matches }) => {
            const params = new URLSearchParams({
                steamid,
                scope: "all",
                matches: String(matches)
            });

            const response = await fetch(
                `/api/player/chat-log?${params}`,
                { credentials: "same-origin" }
            );

            return {
                status: response.status,
                body: await response.text()
            };
        }
        """,
        {"steamid": steamid64, "matches": matches}
    )

    if result["status"] != 200:
        raise RuntimeError(
            f"CS2Tracker returned HTTP {result['status']}: "
            f"{result['body'][:300]}"
        )

    data = json.loads(result["body"])

    if not data.get("ok"):
        raise RuntimeError(f"API returned an unsuccessful response: {data}")

    return data

    pass