import tls_client

def get_session():
    sesh = tls_client.Session(
    client_identifier="chrome_107",
    ja3_string="771,4866-4867-4865-49196-49200-49195-49199-52393-52392-49327-49325-49188-49192-49162-49172-163-159-49315-49311-162-158-49314-49310-107-106-103-64-57-56-51-50-157-156-52394-49326-49324-49187-49191-49161-49171-49313-49309-49233-49312-49308-49232-61-192-60-186-53-132-47-65-49239-49235-49238-49234-196-195-190-189-136-135-69-68-255,0-11-10-35-16-22-23-49-13-43-45-51-21,29-23-30-25-24,0-1-2",
    h2_settings={
        "HEADER_TABLE_SIZE": 65536,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_HEADER_LIST_SIZE": 262144,
    },
    h2_settings_order=[
        "HEADER_TABLE_SIZE",
        "MAX_CONCURRENT_STREAMS",
        "INITIAL_WINDOW_SIZE",
        "MAX_HEADER_LIST_SIZE",
    ],
    supported_signature_algorithms=[
        "ECDSAWithP256AndSHA256",
        "PSSWithSHA256",
        "PKCS1WithSHA256",
        "ECDSAWithP384AndSHA384",
        "PSSWithSHA384",
        "PKCS1WithSHA384",
        "PSSWithSHA512",
        "PKCS1WithSHA512",
    ],
    supported_versions=["GREASE", "1.3", "1.2"],
    key_share_curves=["GREASE", "X25519"],
    cert_compression_algo="brotli",
    pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
    connection_flow=15663105,
    header_order=["accept", "user-agent", "accept-encoding", "accept-language"],
    )
    return sesh
