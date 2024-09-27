"""
Return Salt data via Mattermost

.. important::

    Using this module requires the :ref:`general setup <mattermost-setup>`.

Usage
-----
To use the mattermost returner, append ``--return mattermost`` to the Salt command.

.. code-block:: bash

    salt '*' test.ping --return mattermost

To override individual configuration items, append ``--return_kwargs '{'key:': 'value'}'`` to the Salt command.

.. code-block:: bash

    salt '*' test.ping --return mattermost --return_kwargs '{'channel': '#random'}'
"""

import logging

import salt.returners
from salt.utils import json

from saltext.mattermost.utils import mattermost

log = logging.getLogger(__name__)

__virtualname__ = "mattermost"


def __virtual__():
    return __virtualname__


def _get_options(ret=None):
    """
    Get the mattermost options from salt.
    """

    attrs = {
        "channel": "channel",
        "username": "username",
        "hook": "hook",
        "api_url": "api_url",
    }

    _options = salt.returners.get_returner_options(
        __virtualname__, ret, attrs, __salt__=__salt__, __opts__=__opts__
    )
    log.debug("Options: %s", _options)
    return _options


def returner(ret):
    """
    Send an mattermost message with the data
    """

    _options = _get_options(ret)

    api_url = _options.get("api_url")
    channel = _options.get("channel")
    username = _options.get("username")
    hook = _options.get("hook")

    if not hook:
        log.error("mattermost.hook not defined in salt config")
        return None

    returns = ret.get("return")

    message = "id: {}\r\nfunction: {}\r\nfunction args: {}\r\njid: {}\r\nreturn: {}\r\n".format(  # pylint: disable=consider-using-f-string
        ret.get("id"), ret.get("fun"), ret.get("fun_args"), ret.get("jid"), returns
    )

    return post_message(channel, message, username, api_url, hook)


def event_return(events):
    """
    Send the events to a mattermost room.

    :param events:      List of events
    :return:            Boolean if messages were sent successfully.
    """
    _options = _get_options()

    api_url = _options.get("api_url")
    channel = _options.get("channel")
    username = _options.get("username")
    hook = _options.get("hook")

    is_ok = True
    for event in events:
        log.debug("Event: %s", event)
        log.debug("Event data: %s", event["data"])
        message = f"tag: {event['tag']}\r\n"
        for key, value in event["data"].items():
            message += f"{key}: {value}\r\n"
        result = post_message(channel, message, username, api_url, hook)
        if not result:
            is_ok = False

    return is_ok


def post_message(channel, message, username, api_url, hook):
    """
    Send a message to a mattermost room.

    :param channel:     The room name.
    :param message:     The message to send to the mattermost room.
    :param username:    Specify who the message is from.
    :param hook:        The mattermost hook, if not specified in the configuration.
    :return:            Boolean if message was sent successfully.
    """

    parameters = {}
    if channel:
        parameters["channel"] = channel
    if username:
        parameters["username"] = username
    parameters["text"] = "```" + message + "```"  # pre-formatted, fixed-width text
    log.debug("Parameters: %s", parameters)
    result = mattermost.query(
        api_url=api_url,
        hook=hook,
        data=f"payload={json.dumps(parameters)}",
    )

    log.debug("result %s", result)
    return bool(result)
