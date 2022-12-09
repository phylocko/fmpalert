from datetime import datetime
from typing import Optional

import requests as r


class Client:

    def __init__(self, api_url: str):
        if not api_url.endswith('/'):
            api_url += '/'
        self.api_url = api_url

    def __repr__(self):
        return f'FMPClient for {self.api_url}'

    def review(
            self,
            interval: int = None,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None
    ):

        if interval:
            ext = f'&interval={interval}'
        else:
            if not start:
                raise ValueError('`start` or `interval` are required')
            ext = f'&start={start.isoformat()}'
            if end:
                ext += f'&end={end.isoformat()}'

        url = f'{self.api_url}?review{ext}'
        data = r.get(url).json()
        return Review(data)


class Review:
    def __init__(self, data: dict):
        self.hosts = [Host(x) for x in data['hosts']]
        self.params = ReviewParams(data['params'])
        self.events = []

        for host in self.hosts:
            for port in host.ports:
                self.events.append(Event(host, port))

    def __repr__(self):
        return f'Review [{len(self.events)} events]'

    def __bool__(self):
        return bool(self.events)


class ReviewParams:
    def __init__(self, data: dict):
        for k, v in data.items():
            setattr(self, k, v)


class Host:

    def __init__(self, data: dict):
        self.attrs = []

        for k, v in data.items():
            self.attrs.append(k)

            if k == 'ports':
                self.ports = [Port(x) for x in v]
            else:
                setattr(self, k, v)

    def __repr__(self) -> str:
        return f'Host {self.name}'


class Port:

    def __init__(self, data: dict):
        self.attrs = []

        for k, v in data.items():

            self.attrs.append(k)

            if k == 'flapCount':
                v = int(v)
            setattr(self, k, v)

    def __repr__(self) -> str:
        return f'Port {self.ifName} [{self.ifOperStatus}]'


class Event:

    def __init__(self, host, port):
        for attr_name in host.attrs:
            value = getattr(host, attr_name)
            if attr_name == 'name':
                attr_name = 'hostname'
            setattr(self, attr_name, value)

        for attr_name in port.attrs:
            value = getattr(port, attr_name)
            setattr(self, attr_name, value)

    def __repr__(self):
        return f'Event {self.hostname}, {self.ifOperStatus}'
