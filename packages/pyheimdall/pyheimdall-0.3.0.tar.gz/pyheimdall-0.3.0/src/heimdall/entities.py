# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit entities in a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from .util import _get_node, _get_nodes


def getEntity(tree, filter=None):
    """Retrieves a single entity.

    This function works exactly like ``heimdall.getEntities``, but raises an
    ``IndexError`` if ``filter`` returns more than one result.

    :param tree: HERA elements tree
    :param filter: (optional) Filtering function
    :return: Item element
    :rtype: lxml.Element
    """
    return _get_node(tree, 'entity', filter)


def getEntities(tree, filter=None):
    """Retrieves a collection of entities.

    :param tree: HERA elements tree
    :param filter: (optional) Filtering function
    :return: List of Entity elements
    :rtype: list

    This function can be used to retrieve all entities in a database: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> entities = heimdall.getEntities(tree)  # retrieve all entities

    To retrieve only *some* entities, you can use a filter.
    A filter is a function which takes only an item as a parameter, and
    returns either ``True`` (we want this entity to be part of the list
    returned by ``getEntities``) or ``False`` (we don't want it). ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>>
      >>> def by_attribute_property(attribute):  # attribute filter
      >>>     return attribute.get('pid', '101010')
      >>>
      >>> def by_property(entity):  # entity filter
      >>>     attribute = getAttribute(entity, by_attribute_property)
      >>>     return attribute is not None
      >>>
      >>> # retrieve only entities reusing a property of id '101010'
      >>> entities = heimdall.getEntities(tree, by_property)

    For simple filters, anonymous functions can of course be used: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # retrieve only entities of a specific id
      >>> heimdall.getEntities(tree, lambda e: e.getValue('id') == '42')
    """
    return _get_nodes(tree, 'entity', filter)


def createEntity(tree, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def replaceEntity(entity, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateEntity(entity, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def deleteEntity(tree, filter):
    """Deletes a single entity.

    This method doesn't delete any item documented by the deleted entity.
    All items referencing this entity, if any, will become invalid.
    One can either delete these items afterwards, or change their ``eid``, or
    recreate a new entity and update these items accordingly.

    This function raises an ``IndexError`` if the filtering method ``filter``
    returns more than one result.
    If ``filter`` returns no result, this function does nothing,
    and does not raise any error.

    This function performs the entity deletion "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param filter: Filtering function

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete a property using its unique id
      >>> heimdall.deleteEntity(tree, lambda e: e.get('id') == '42')
    """
    node = _get_node(tree, 'entity', filter)
    if node:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getEntity', 'getEntities',
    'createEntity', 'deleteEntity',
    'replaceEntity', 'updateEntity',
    '__copyright__', '__license__',
    ]
