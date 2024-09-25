# TLDParse

Split a given domain into its different parts (subdomain, domain, suffix).

It was built in the aim to be very fast. To do so, it starts in reverse, going from the TLD down to any subdomains.

## Installation

```python
pip install tldparse
```

## Basic usage

The following code will show you the basic usage you can have from this library.

```python
from tldparse import DomainResult

parsed = DomainResult('https://example.github.io/with/some/path')
print(parsed.tld) # io
print(parsed.domain) # github
print(parsed.subdomain) # example
```

## Common usage

A common usage is to check whereas the given domain is the fqdn or if it has subdomains

```python
from tldparse import DomainResult

email = 'user@sub.domain.com'
mbox, domain = email.split('@')

parsed = DomainResult(domain)
assert parsed.fqdn == domain, "Please register using a domain with no subdomain parts"
```

## Advanced usage

### Replacing TLDParse with a custom one:

`DomainResult` class use the default `TLDParse` object that relies on the list of suffixes provided by Mozilla.
(The list is freely available at https://publicsuffix.org/list/public_suffix_list.dat)

But you can either pass another parser, such as:

```python

class MyCustomParser:
    def __call__(self, domain, private=True):
        # PLEASE DON'T DO THAT
        return domain.rsplit('.', 2)  # Consider a TLD has only one part. Ignores things such as ".co.uk"

from tldparse import DomainResult

parser = MyCostumParser()

result = DomainResult('example.github.com', parser=parser)
print(result.fqdn)  # github.com

result = DomainResult('bbc.co.uk', parser=parser)
print(result.fqdn)  # co.uk  # Too bad
```

### Using private subdomains:

By default, the library will consider the subdomains as part of the fqdn for certain domain.
But you can change this behavior by setting the `private` parameter to `True`.

```python
from tldparse import DomainResult

result = DomainResult('example.github.io')
print(result.fqdn) # example.github.io

result = DomainResult('example.github.io', private=False)
print(result.fqdn) # github.io
```

### Adding/Removing TLDs entries:

You can add/remove entries to the parser by using the `add`/`remove` methods of the tldparse object:

```python
from .tldparse import TLDParse, DomainResult

# Adding a custom domain
parser.add('weebly.co.uk')  # added in private
result = DomainResult('example.weebly.co.uk', parser=parser, private=False)
print(result.suffix)  # 'co.uk'
print(result.domain)  # 'weebly'
print(result.subdomain)  # 'example'

result = DomainResult('example.weebly.co.uk', parser=parser)
print(result.suffix)  # 'weebly.co.uk'
print(result.domain)  # 'example'

# Removing a domain
TLDParse.remove('github.io')
result = DomainResult('example.github.io')
print(result.suffix)  # 'io'
print(result.domain)  # 'github'
print(result.subdomain)  # 'example'
```

## Support

If you find an issue, please open a support requests, or even better, a Pull Requests :)

Thank you!
