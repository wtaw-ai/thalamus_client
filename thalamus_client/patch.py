def patch_requests(api_key: str):
    import requests
    original_get = requests.get

    def new_get(*args, **kwargs):
        if args[0].startswith("https://api.openai.com/v1/chat/completions"):
            args = ("https://api.wheretheresawill.app/answer_question",) + args[1:]
        return original_get(*args, **kwargs)

    requests.get = new_get

def patch_httpx(api_key: str):
    import httpx
    original_request = httpx.Client.request

    def new_request(self, method, url, *args, **kwargs):
        if url.startswith("https://api.openai.com/v1/chat/completions"):
            url = "https://api.wheretheresawill.app/answer_question"
        return original_request(self, method, url, *args, **kwargs)

    httpx.Client.request = new_request

def apply_patches(api_key: str):
    patch_requests(api_key)
    patch_httpx(api_key)