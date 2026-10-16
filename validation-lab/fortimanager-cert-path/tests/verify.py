import pathlib,subprocess,os,ast,json,tempfile
import sys
repo=pathlib.Path(sys.argv[1]).resolve();pkg=pathlib.Path(__file__).resolve().parents[1]
(pkg/'evidence').mkdir(exist_ok=True)
s=(repo/'code/cves/2024/CVE-2024-47575.yaml').read_text();source=s.split('    source: |\n')[1].split('\n    matchers:')[0];source='\n'.join(line[6:] for line in source.splitlines());tree=ast.parse(source);nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name=='create_ssl_context'];isolated=ast.unparse(ast.Module(body=nodes,type_ignores=[]))
isolated+='''
loaded = []
original_load = ssl.SSLContext.load_cert_chain
def record_load(self, *args, **kwargs):
    result = original_load(self, *args, **kwargs)
    loaded.append(kwargs.get("certfile", args[0] if args else None))
    return result
ssl.SSLContext.load_cert_chain = record_load
context = create_ssl_context()
print("CERT_LOADED=" + str(bool(loaded)))
print("KEYSDIR=" + str(os.getenv("keysDir")))
'''
(pkg/'tests/loader.py').write_text(isolated)
with tempfile.TemporaryDirectory(prefix='ig-sign-') as t:
 t=pathlib.Path(t);subprocess.run(['openssl','ecparam','-name','prime256v1','-genkey','-noout','-out',str(t/'key.pem')],check=True);subprocess.run(['openssl','req','-new','-x509','-key',str(t/'key.pem'),'-subj','/CN=local-loader-test','-days','1','-out',str(t/'cert.pem')],check=True)
 env=os.environ.copy();env.update(NUCLEI_USER_PRIVATE_KEY=str(t/'key.pem'),NUCLEI_USER_CERTIFICATE=str(t/'cert.pem'));results=[]
 for label,folder,expected in [('before','cve-2024-475759-keys','False'),('after','cve-2024-47575-keys','True')]:
  template=t/(label+'.yaml');template.write_text('id: loader-'+label+'\ninfo:\n  name: Certificate loader regression\n  author: local-test\n  severity: info\nvariables:\n  keysDir: helpers/payloads/'+folder+'\ncode:\n  - engine:\n      - python3\n    source: |\n'+''.join('      '+line+'\n' for line in isolated.splitlines())+'    matchers:\n      - type: word\n        words:\n          - "CERT_LOADED='+expected+'"\n')
  sign=subprocess.run(['nuclei','-t',str(template),'-sign','-duc','-no-stdin'],cwd=repo,env=env,capture_output=True,text=True,timeout=30)
  run=subprocess.run(['nuclei','-t',str(template),'-code','-u','localhost','-duc','-ni','-no-stdin','-debug','-nc','-jsonl'],cwd=repo,env=env,capture_output=True,text=True,timeout=30)
  log=sign.stdout+sign.stderr+run.stdout+run.stderr;(pkg/'evidence'/('engine-'+label+'.log')).write_text(log);findings=[json.loads(line) for line in run.stdout.splitlines() if line.startswith('{')];assert run.returncode==0 and len(findings)==1 and findings[0]['template-id']=='loader-'+label,log
  results.append({'case':label,'expected':expected,'matched':True,'returncode':run.returncode})
 (pkg/'evidence/loader-results.json').write_text(json.dumps(results,indent=2));print(results)
