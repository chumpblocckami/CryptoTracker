from elasticsearch import Elasticsearchdef generate_custom_home():    head = """<h1>Select which tracker you want to inspect</h1>          <style>             table, td, th {                border: 1px solid black;                width: 200px;                text-align:center;                align:center;             }          </style>"""    es = Elasticsearch(hosts=["elasticsearch"],                       http_auth=("", ""),                       timeout=40,                       max_retries=10,                       retry_on_timeout=True, )    infos = es.indices.get_alias("*").keys()    head += "<table><tr>"    for n in range(0, len(infos)):        crypto = infos[n].split(",")[0]        head += f"""<td><button class="{crypto}" onclick="location.href='/{crypto}'">{crypto.upper()}</button></td>"""    head += "</tr></table>"    with open('templates/home.html', "w") as f:        f.write(head)