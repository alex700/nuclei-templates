# Observed product response differential

Local controls used checksum-verified Apache binary WARs, Tomcat 9, PostgreSQL 15, and an anonymous scanner session. The request is a POST to `/roller-services/xmlrpc` with a benign XML-RPC `<ex:nil/>` value and the extension namespace declared on the root `methodCall` element.

| Apache Roller | XML-RPC setting | HTTP result and relevant fault | Nuclei findings |
| --- | --- | --- | ---: |
| 6.1.4 | Default disabled | 200 XML; `No method matching arguments: null` | 1 |
| 6.1.5 | Default disabled | 200 XML; `No method matching arguments: null` | 1 |
| 6.1.6 | Default disabled | 404; `XML-RPC service is disabled` | 0 |
| 6.1.6 | Explicitly enabled | 200 XML; `The tag {http://ws.apache.org/xmlrpc/namespaces/extensions}nil is invalid, if isEnabledForExtensions() == false.` | 0 |

The 6.1.4 control is the release explicitly covered by CVE-2026-129448. Apache identifies the same bug in 6.1.5 under CVE-2026-82384. An ordinary XML-RPC string value reached method dispatch on both the old and fixed products when the service was enabled; an unknown vendor extension was rejected. These controls distinguish the `ex:nil` result from a generic route or XML parsing failure.

The portable runner completed all four assertions with Nuclei v3.11.0 and the exact template SHA-256 recorded in `results.json`. No serialized object, command, callback, credential, or real-world target was used.
