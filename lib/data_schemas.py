from voluptuous import Schema, Optional, Required, Any


LIST_SCHEMA = Schema({
    Required('sort_key', default='created_at'): str,
    Required('sort_order', default='desc'): Any('desc', 'asc'),
    Required('page', default=1): int,
    'limit': int
})