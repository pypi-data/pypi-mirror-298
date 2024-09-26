# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import logging

import click
from pioreactor.background_jobs.base import BackgroundJobContrib
from pioreactor.config import config
from pioreactor.mureq import post
from pioreactor.types import MQTTMessage
from pioreactor.utils import JobManager
from pioreactor.whoami import get_unit_name
from pioreactor.whoami import UNIVERSAL_EXPERIMENT


# since this is a long-running job, we don't want it to be killed by pio kill --all-jobs.
JobManager.LONG_RUNNING_JOBS = JobManager.LONG_RUNNING_JOBS + ("logs2discord",)


class Logs2Discord(BackgroundJobContrib):
    job_name = "logs2discord"

    def __init__(self, unit: str, experiment: str) -> None:
        super(Logs2Discord, self).__init__(
            unit=unit, experiment=experiment, plugin_name="pioreactor_logs2discord"
        )
        self.discord_webhook_url = config.get("logs2discord", "discord_webhook_url")
        if not self.discord_webhook_url:
            self.logger.error("[logs2discord] discord_webhook_url is not defined in your config.ini.")
            raise ValueError("[logs2discord] discord_webhook_url is not defined in your config.ini.")

        self.log_level = config.get("logs2discord", "log_level", fallback="INFO")
        self.start_passive_listeners()

    def publish_to_discord(self, msg: MQTTMessage) -> None:
        payload = json.loads(msg.payload)
        topics = msg.topic.split("/")
        unit = topics[1]

        # check to see if we should allow the logs based on the level.
        if getattr(logging, self.log_level) > getattr(logging, payload["level"]):
            return
        elif payload["task"] == self.job_name:
            # avoid an infinite loop, https://github.com/Pioreactor/pioreactor-logs2discord/issues/2
            return

        discord_msg = f"[{payload['level']}] [{unit}] [{payload['task']}] {payload['message']}"

        r = post(self.discord_webhook_url, json={"content": discord_msg, 'username': unit})

        r.raise_for_status()

    def start_passive_listeners(self) -> None:
        self.subscribe_and_callback(self.publish_to_discord, "pioreactor/+/+/logs/#")


@click.command(name="logs2discord")
def click_logs2discord() -> None:
    """
    turn on logging to Discord
    """

    lg = Logs2Discord(unit=get_unit_name(), experiment=UNIVERSAL_EXPERIMENT)
    lg.block_until_disconnected()
