def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    source_type = attrs.get('TIPOVIAL')
    source_name = attrs.get('NOMVIAL')

    if source_type:
        if source_type == 'Privada' or source_type == 'Cerrada':
            tags['access'] = 'private'
    tags['highway'] = 'residential'

    if source_name:
        # tags['inegi:nomvial'] = source_name.lower()
        if source_name != 'Ninguno':
            tags['name'] = u'{}{}'.format(
                source_type + ' ' if source_type != 'Otro' else '',
                source_name).title()

    if 'SENTIDO' in attrs:
        source_oneway = attrs.get('SENTIDO')
        # tags['inegi:sentido'] = source_oneway.lower()
        if source_oneway == 'DOS SENTIDOS':
            tags['oneway'] = 'no'
        if source_oneway == 'UN SENTIDO':
            tags['oneway'] = 'yes'

    return tags
