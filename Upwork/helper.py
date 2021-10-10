def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d


def run():

    cookies = 'Host: www.upwork.com\
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\
Accept-Language: en-US,en;q=0.5\
Accept-Encoding: gzip, deflate, br\
Referer: https://www.upwork.com/ab/jobs/search/?q=web%20scrape&sort=recency\
Alt-Used: www.upwork.com\
Connection: keep-alive\
Cookie: _pxhd=p6VJOR7w6DkgaA2c0iulUdZYXf3qDFN8TMiDu-3RRRn7bOQtaVtSPF/MSR5-ACYf23ZW7kw5CQGUXncNLeWLQQ==:S7j0g4JiUOQWd/6-6UL8Sh9RsKM1iGlomZYUSAUtCKcVuxPlpXfaezS26W3Yh6l/RasQM75ibH/mQEhxOf1/YcV0nBJipSbOSRMT1yuQpyw=; visitor_id=124.106.133.72.1622962730119000; G_ENABLED_IDPS=google; bmuid=1622962735653-4698BB01-84E2-4F54-B9D9-AD0BC0A2A8A0; cdSNum=1633770596674-sjc0000890-e0935d66-08e7-414b-94e9-bc0f758a7596; recognized=6367fd3b; DA[6367fd3b]=8875644e795ad6bade6c16fa0ebc80b5%2C0%2Cv8%2C1641401156; g_state={"i_l":0}; spt=92af21b9-d9fd-4cce-8e67-0c91ef459746; company_last_accessed=d1000802843; current_organization_uid=1368214272048214017; forterToken=2febba1b9de648af9148178bc6c42514_1633076406120_291_UAL9_9ck; _pxvid=33676fd1-0198-11ec-819f-54526d4b446e; acced1000802843=39644121; dash_company_last_accessed=1368214272048214017; device_view=full; lang=en; idv_oauth=oauth2v2_3888eb42fc7dc01985fa0fb5091ed80f; __zlcmid=16HkMZyqCe4CeS2; undefined=oauth2v2_3bde7757912eec3461f501971d7f3341; fe.app.proposals.1368214272048214016.successMessage=%22Your%20proposal%20was%20submitted.%22; enabled_ff=CI11132Air2Dot75,CI9570Air2Dot5,!CI10270Air2Dot5QTAllocations,!CI10857Air3Dot0; visitor_gql_token=oauth2v2_ec01dc84feffcd36c0167f00a4eed644; survey_allowed=true; cookie_prefix=; cookie_domain=.upwork.com; __cfruid=369b7286f204e2d88b8fa9f542cc038b70b98d05-1633756181; XSRF-TOKEN=fe16d469ed61452478ab4b5acbb027e0; odesk_signup.referer.raw=https%3A%2F%2Fwww.upwork.com%2Fab%2Fjobs%2Fsearch%2F%3Fq%3Dweb%2520scrape%26sort%3Drecency; restriction_verified=1; cdContextId=14; console_user=6367fd3b; user_uid=1368214272048214016; master_access_token=b4909198.oauth2v2_881e78ecf95e06aacba777c5499dcbd0; oauth2_global_js_token=oauth2v2_341dca3e9a14ebe905993cda159e4860; user_oauth2_slave_access_token=b4909198.oauth2v2_881e78ecf95e06aacba777c5499dcbd0:1368214272048214016.oauth2v2_5fb9a6fce994aacc889a219fc15f4951; channel=other; __cf_bm=TEJeWAu_.VvqhInHbMCmQAzObcDp9JMHN8AsVQUOLKU-1633770892-0-AShDvgxbaZ3+DVofsw325xvEJRrycdH3sF3hiDS0fd+MVUm7ssFRQt8AXhW+6lgQ5fMrDdCEeeF7+N8hwTMLK1A=; upwork_bc=1633770596516_124.106.133.72.1622962730119000\
Upgrade-Insecure-Requests: 1\
Sec-Fetch-Dest: document\
Sec-Fetch-Mode: navigate\
Sec-Fetch-Site: same-origin\
Sec-Fetch-User: ?1'

    print(get_headers(cookies))

    