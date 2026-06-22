import requests
from typing import Optional

class Supabase:
    @staticmethod
    def IsValidConfig(projectId: str, apiKey: str, token: str) -> str:
        url = f"https://{projectId}.supabase.co/auth/v1/token"
        headers = {
            "ApiKey": apiKey,
            "Authorization": f"Bearer {token.strip()}" if not token.startswith("Bearer ") else token
        }
        return requests.get(url, headers=headers, timeout=3).status_code == 405

    @staticmethod
    def TryExtractContent(session: requests.Session, tableName: str) -> Optional[list]:
        allRows = []
        offset = 0
        limit = 1000

        headers = {
            "ApiKey": session.headers.get("ApiKey", ""),
            "Authorization": session.headers.get("Authorization", ""),
            "Range-Unit": "items",
        }

        while True:
            rangeHeader = f"{offset}-{offset + limit - 1}"
            headers["Range"] = rangeHeader

            resp = session.get(
                f"https://{session.ProjectId}.supabase.co/rest/v1/{tableName}?select=*",
                headers=headers
            )

            if resp.status_code not in (200, 206):
                break

            try:
                rows = resp.json()
            except Exception:
                break

            if not rows:
                break

            allRows.extend(rows)
            offset += limit

            if len(rows) < limit:
                break

        return allRows if allRows else None