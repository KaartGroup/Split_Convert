def filterTags(attrs):
    if not attrs:
        return
    tags = {}

#    source_type = attrs.get('TIPOVIAL')
    source_name = attrs.get('TEXTO')

#    if source_type:
#        if source_type == 'Privada' or source_type == 'Cerrada':
#           tags['access'] = 'private'
    tags['highway'] = 'residential'

    if source_name:
        # tags['inegi:nomvial'] = source_name.lower()
        if source_name != 'SN':
            # if the road has a useful road type or the road name doesn't already have a type create the new road name with both
            tags['name'] = u'{}'.format(source_name).title()

    if 'SENTIDO' in attrs:
        source_oneway = attrs.get('SENTIDO').lower()
        # tags['inegi:sentido'] = source_oneway.lower()
        if source_oneway == 'dos sentidos':
            tags['oneway'] = 'no'
        if source_oneway == 'un sentido':
            tags['oneway'] = 'yes'

    return tags
