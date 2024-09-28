# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from mysql.connector import connect
from lxml import etree


def getDatabase(db):
    connection = _connect(db)
    with connection.cursor() as cursor:
        hera = _create_tree(db.entities, cursor)
    connection.close()
    return hera


def _connect(db):
    url = urlparse(db.url)
    # due to urlparse, url.path is something like '/dbname'
    # but mysql.connector.connect wants database = 'dbname'
    connection = connect(database=url.path.split('/')[1],
                         user=url.username, password=url.password,
                         host=url.hostname, port=url.port)
    if connection.is_connected():
        return connection
    return None


def _create_tree(tables, cursor):
    url_xmlschema = "http://www.w3.org/2001/XMLSchema-instance"
    url_hera = "https://gitlab.huma-num.fr/datasphere/hera/schema/schema.xsd"
    qname = etree.QName(url_xmlschema, "schemaLocation")
    root = etree.Element('hera', {qname: url_hera})
    properties = etree.SubElement(root, 'properties')
    entities = etree.SubElement(root, 'entities')
    items = etree.SubElement(root, 'items')
    for table in tables:
        # create entity for this table
        entity, properties_used_by_entity = _create_entity(table, cursor)
        entities.append(entity)
        # create properties for this entity
        for p in properties_used_by_entity:
            properties.append(p)
        # create items for this entity
        eid = entity.get('id')
        result = cursor.execute(f'SELECT * FROM {table}')
        for row in cursor.fetchall():
            items.append(_create_item(eid, row, properties_used_by_entity))
    return root


def _create_item(eid, row, properties):
    item = etree.Element('item', {'eid': eid, })
    for index, p in enumerate(properties):
        value = row[index]
        if not value:
            continue
        item.append(_create_metadata(p.get('id'), value))
    return item


def _create_metadata(pid, value):
    metadata = etree.Element('metadata', {'pid': pid, })
    metadata.text = str(value)
    return metadata


def _create_entity(table, cursor):
    cursor.execute(f'SHOW CREATE TABLE {table}')
    create_table_query = cursor.fetchall()[0][1]
    entity = etree.Element('entity', {'id': table, })
    etree.SubElement(entity, 'name').text = table
    comment = _get_table_comment(create_table_query)
    if comment:
        etree.SubElement(entity, 'description').text = comment

    properties = []
    cursor.execute(f'SHOW FULL COLUMNS FROM {table}')
    for row in cursor.fetchall():
        entity.append(_create_attribute(table, row))
        properties.append(_create_property(table, row))
    return entity, properties


def _get_table_comment(create_table_query):
    import re
    pattern = re.compile(r"COMMENT='(?P<res>[\w\s]*)'")
    m = pattern.search(create_table_query)
    return m.group('res') if m is not None else None


def _create_attribute(table, row):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    collation = row[2]
    nullability = row[3]  # YES|NO
    indexed = row[4]  # PRI|UNI|MUL
    default_value = row[5]
    extra = row[6]
    privileges = row[7]
    comment = row[8]
    root = etree.Element('attribute', {
        'id': f'{table}.{name}_attr', 'pid': f'{table}.{name}',
        'min': str(0) if nullability == 'YES' else str(1),
        'max': str(1),  # TODO hera allows repeatability, sql does not (as is)
        })
    etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment:
        etree.SubElement(root, 'description').text = comment
    return root


def _create_property(table, row):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    comment = row[8]
    root = etree.Element('property', id=f'{table}.{name}')
    etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment:
        etree.SubElement(root, 'description').text = comment
    return root


def _type_sql2hera(sqltype):
    if sqltype == 'date':
        return 'datetime'
    if sqltype.startswith('varchar') or sqltype.startswith('char'):
        return 'text'
    if sqltype.startswith('int'):
        return 'number'
    raise ValueError(f"Unknown type '{sqltype}'")
