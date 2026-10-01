#!/usr/bin/env python3
"""Run a package's isolated Compose lab and preserve assertion evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import uuid


def assert_findings(output, template_id, minimum, maximum):
    findings = [json.loads(line) for line in output.splitlines() if line.strip()]
    if any(not isinstance(row, dict) or row.get('template-id') != template_id for row in findings):
        raise ValueError('Unexpected finding or template ID')
    if not 0 <= minimum <= maximum or not minimum <= len(findings) <= maximum:
        raise ValueError(f'Expected {minimum}..{maximum} findings; observed {len(findings)}')
    return findings


def run(package):
    package = package.resolve()
    config = json.loads((package / 'tests/lab.json').read_text())
    template = (package / config['template_path']).resolve()
    compose = (package / config['compose_file']).resolve()
    for path in (template, compose):
        if not path.is_relative_to(package) or not path.is_file():
            raise ValueError(f'Expected file within package: {path}')
    tests = config['tests']
    if not tests or not config['target_services']:
        raise ValueError('Tests and target services are required')
    names = [test['name'] for test in tests]
    if len(set(names)) != len(names) or any(not re.fullmatch(r'[a-zA-Z0-9_-]+', name) for name in names):
        raise ValueError('Test names must be unique simple identifiers')
    run_id = uuid.uuid4().hex[:12]
    evidence = package / 'evidence' / run_id
    evidence.mkdir(parents=True, exist_ok=False)
    prefix = ['docker', 'compose', '-p', 'nuclei-lab-' + run_id, '-f', str(compose)]
    timeout = int(config.get('timeout_seconds', 180))
    summary = {'template_sha256': hashlib.sha256(template.read_bytes()).hexdigest(),
               'tests': [], 'commands': [], 'assertions_passed': False}

    def command(label, arguments):
        args = prefix + arguments
        record = {'label': label, 'argv': args}
        summary['commands'].append(record)
        try:
            result = subprocess.run(args, cwd=package, capture_output=True, text=True, timeout=timeout)
            stdout, stderr = result.stdout, result.stderr
            record['exit_code'] = result.returncode
        except subprocess.TimeoutExpired as error:
            stdout, stderr = error.stdout or b'', error.stderr or b''
            stdout = stdout.decode(errors='replace') if isinstance(stdout, bytes) else stdout
            stderr = stderr.decode(errors='replace') if isinstance(stderr, bytes) else stderr
            record['exit_code'] = None
            record['error'] = 'timeout'
        (evidence / (label + '.stdout.log')).write_text(stdout)
        (evidence / (label + '.stderr.log')).write_text(stderr)
        if record['exit_code'] != 0:
            raise RuntimeError(f'{label} failed: see {evidence}')
        return stdout

    started = False
    try:
        rendered = json.loads(command('compose-config', ['config', '--format', 'json']))
        services = rendered['services']
        scanner_config = services[config['scanner_service']]
        if '@sha256:' not in scanner_config.get('image', ''):
            raise ValueError('Pin the scanner image by digest')
        for name in config['target_services']:
            health = services[name].get('healthcheck', {})
            if not health.get('test') or health.get('disable') or health['test'] == ['NONE']:
                raise ValueError(f'Target {name} requires a readiness healthcheck')
        started = True
        command('startup', ['up', '-d', '--wait', '--wait-timeout', str(max(1, timeout - 10)),
                            *config['target_services']])
        scanner = ['run', '--rm', '--no-deps', '-T', config['scanner_service']]
        command('version', scanner + ['-version'])
        common = ['-t', config['container_template'], '-duc', '-nc']
        command('validate', scanner + common + ['-validate'])
        for test in tests:
            output = command('test-' + test['name'], scanner + common +
                             ['-u', test['target'], '-jsonl', '-silent', '-debug'] + test.get('extra_args', []))
            findings = assert_findings(output, config['template_id'], test['min_matches'], test['max_matches'])
            (evidence / (test['name'] + '.jsonl')).write_text(output)
            summary['tests'].append({'name': test['name'], 'observed_matches': len(findings),
                                     'expected_min': test['min_matches'], 'expected_max': test['max_matches']})
        summary['assertions_passed'] = True
    except Exception as error:
        summary['error'] = str(error)
    finally:
        if started:
            try:
                command('application-logs', ['logs', '--no-color', *config['target_services']])
            except Exception as error:
                summary['logs_error'] = str(error)
            try:
                command('cleanup', ['down', '--remove-orphans'])
                summary['cleanup_passed'] = True
            except Exception as error:
                summary['cleanup_passed'] = False
                summary['cleanup_error'] = str(error)
        (evidence / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'evidence': str(evidence), **summary}, indent=2))
    return 0 if summary['assertions_passed'] and summary.get('cleanup_passed') else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    raise SystemExit(run(parser.parse_args().package))
