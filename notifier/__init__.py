import subprocess
from datetime import datetime, timedelta
from time import sleep

from fmpclient import Client, Review

DEFAULT_CHECK_INTERVAL = 60 * 5


class Notifier:

    def __init__(
            self,
            fmp_client: Client,
            exec_command: str,
            check_interval: int = DEFAULT_CHECK_INTERVAL,
    ):
        self.fmp_client = fmp_client
        self.check_interval = check_interval
        self.exec_command = exec_command
        self.last_update = datetime.now() - timedelta(seconds=check_interval)

    def monitor(self):

        while True:
            update_time = datetime.now()

            try:
                self.check()
            except Exception as e:
                print(f'Unable to get flaps: {e}')

            else:
                self.last_update = update_time

            sleep(self.check_interval)

    def _replace_template(self, info: dict):
        cmd_parts = []
        for cmd_part in self.exec_command.split():
            cmd_part = cmd_part.replace('$up_ports', str(info['up_ports']))
            cmd_part = cmd_part.replace('$full_text', info['full_text'])
            cmd_part = cmd_part.replace('$short_text', info['short_text'])
            cmd_part = cmd_part.replace('$down_ports', str(info['down_ports']))
            cmd_part = cmd_part.replace('$flap_count', str(info['flap_count']))
            cmd_part = cmd_part.replace('$affected_devices', str(info['affected_devices']))
            cmd_parts.append(cmd_part)

        return cmd_parts

    def prepare_info(self, review: Review):
        up_ports = len([x for x in review.events if x.ifOperStatus == 'up'])
        down_ports = len([x for x in review.events if x.ifOperStatus == 'down'])

        affected_devices = {x.hostname for x in review.events}
        short_text = 'All ok!'
        full_text = ''

        flapCount = 0

        if not review.events:
            short_text = 'All ok!'

        elif len(review.events) == 1:
            e = review.events[0]
            short_text = f'{e.hostname}: {e.ifName} {e.ifOperStatus} [{e.flapCount}]'

        else:
            short_text = f'{down_ports} ports down, {up_ports} up on {len(affected_devices)} hosts'

        for e in review.events:
            flapCount += e.flapCount
            full_text += f'{e.hostname} {e.ifName} ({e.ifAlias}): {e.ifOperStatus} [{e.flapCount}]\n'

        return {
            'up_ports': up_ports,
            'down_ports': down_ports,
            'full_text': full_text,
            'short_text': short_text,
            'flap_count': flapCount,
            'affected_devices': len(affected_devices),
        }

    def check(self):
        delta = datetime.now() - self.last_update
        interval = int(delta.total_seconds())
        review = self.fmp_client.review(interval=interval)
        if review:
            info = self.prepare_info(review)
            cmd = self._replace_template(info)
            subprocess.run(cmd)
