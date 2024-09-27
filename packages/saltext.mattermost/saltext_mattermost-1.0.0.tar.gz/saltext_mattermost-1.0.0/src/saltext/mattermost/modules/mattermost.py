"""
Module for sending messages to Mattermost

.. important::

    You can optionally :ref:`add a configuration profile <mattermost-setup>`
    to avoid having to pass `hook` and `api_url` to each invocation.
"""

import logging

from salt.exceptions import SaltInvocationError
from salt.utils import json

from saltext.mattermost.utils import mattermost

log = logging.getLogger(__name__)

__virtualname__ = "mattermost"


def __virtual__():
    return __virtualname__


def _get_hook():
    """
    Retrieves and return the Mattermost's configured hook

    :return:            String: the hook string
    """
    hook = __salt__["config.get"]("mattermost.hook") or __salt__["config.get"]("mattermost:hook")
    if not hook:
        raise SaltInvocationError("No Mattermost Hook found")

    return hook


def _get_api_url():
    """
    Retrieves and return the Mattermost's configured api url

    :return:            String: the api url string
    """
    api_url = __salt__["config.get"]("mattermost.api_url") or __salt__["config.get"](
        "mattermost:api_url"
    )
    if not api_url:
        raise SaltInvocationError("No Mattermost API URL found")

    return api_url


def _get_channel():
    """
    Retrieves the Mattermost's configured channel

    :return:            String: the channel string
    """
    channel = __salt__["config.get"]("mattermost.channel") or __salt__["config.get"](
        "mattermost:channel"
    )

    return channel


def _get_username():
    """
    Retrieves the Mattermost's configured username

    :return:            String: the username string
    """
    username = __salt__["config.get"]("mattermost.username") or __salt__["config.get"](
        "mattermost:username"
    )

    return username


def post_message(message, channel=None, username=None, api_url=None, hook=None):
    """
    Send a message to a Mattermost channel.

    :param channel:     The channel name, either will work.
    :param username:    The username of the poster.
    :param message:     The message to send to the Mattermost channel.
    :param api_url:     The Mattermost api url, if not specified in the configuration.
    :param hook:        The Mattermost hook, if not specified in the configuration.
    :return:            Boolean if message was sent successfully.

    CLI Example:

    .. code-block:: bash

        salt '*' mattermost.post_message message='Build is done'
    """
    if not api_url:
        api_url = _get_api_url()

    if not hook:
        hook = _get_hook()

    if not username:
        username = _get_username()

    if not channel:
        channel = _get_channel()

    if not message:
        log.error("message is a required option.")

    parameters = {}
    if channel:
        parameters["channel"] = channel
    if username:
        parameters["username"] = username
    parameters["text"] = "```" + message + "```"  # pre-formatted, fixed-width text
    log.debug("Parameters: %s", parameters)
    data = f"payload={json.dumps(parameters)}"
    result = mattermost.query(api_url=api_url, hook=hook, data=data)

    return bool(result)
