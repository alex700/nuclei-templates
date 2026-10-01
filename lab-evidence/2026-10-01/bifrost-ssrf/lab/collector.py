import http.server,json,os,time
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/health':
            row={'path':self.path,'time':time.time(),'remote':self.client_address[0]}
            with open('/data/requests.jsonl','a') as f:f.write(json.dumps(row)+'\n')
            print(json.dumps(row),flush=True)
        payload=b'inert-non-plugin-content\n'
        self.send_response(200)
        self.send_header('Content-Type','text/plain')
        self.send_header('Content-Length',str(len(payload)))
        self.end_headers();self.wfile.write(payload)
    def log_message(self,*args):pass
http.server.ThreadingHTTPServer(('0.0.0.0',8081),Handler).serve_forever()
