

def generation_headers(auth_token:str):

    return    {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dream.ai/',
    'x-app-version': 'WEB-2.0.0',
    'Authorization': f'bearer {auth_token}',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://dream.ai',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}



class Headers:
    identity_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Firebase-gmpid': '1:181681569359:web:277133b57fecf57af0f43a',
        'Content-Type': 'application/json',
        'Origin': 'https://dream.ai',
        'Connection': 'keep-alive',
    }

