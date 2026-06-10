from supabase import Client, create_client
from supabase._sync.client import SyncMemoryStorage
from supabase.lib.client_options import ClientOptions

from config import SUPABASE_URL, SUPABASE_ANON_KEY


# PKCE is the default flow_type in supabase-py 2.30.0 but we set it explicitly
# so the choice is visible at the call site. PKCE is required for Streamlit's
# server-side OAuth callback handling — implicit flow puts the access_token in
# the URL fragment (#) which Python can't read; PKCE puts a code in the query
# string (?) which st.query_params CAN read. See app.py:70-149 for the
# corresponding exchange_code_for_session() handler.
#
# Note: Current supabase-py releases may omit auth storage/httpx_client fields
# from ClientOptions, yet the sync client still expects them. Attach the
# missing attributes manually here.
def get_supabase_client() -> Client:
    options = ClientOptions(
        flow_type="pkce",
        persist_session=True,
        auto_refresh_token=True,
    )
    options.storage = SyncMemoryStorage()
    options.httpx_client = None

    return create_client(
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
        options=options,
    )


supabase: Client = get_supabase_client()
