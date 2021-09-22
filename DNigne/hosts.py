from django_hosts import host, patterns

host_patterns = patterns(
    '',
    host(r'', 'DNigne.urls', name=' '),


    host(r'business', 'DeliverySystem.urls', name='business'),
)