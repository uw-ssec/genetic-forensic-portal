"""This package contains clients that retrieve data and authentication/authorization information for the genetic forensic portal.

Right now, of course, these clients are largely simulating these interactions, but the idea is that they would be able to interact with the actual services once they exist.

If the portal needs to call other services in the future, they would be added here.

Current clients:
- `gf_api_client`: A client that interacts with the genetic forensic API (but since one does not currently exist, it simulates these interactions but provides canned data).
- `keycloak_client`: A client that interacts with a local Keycloak instance to make auth decisions.
"""
