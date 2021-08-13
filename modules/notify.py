import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from modules.settings import log, req


class Notify(object):


    def __init__(self):
        # Custom Push Config
        self.PUSH_CONFIG = ''
        if 'PUSH_CONFIG' in os.environ:
            self.PUSH_CONFIG = os.environ['PUSH_CONFIG']
        # Discord Webhook
        self.DISCORD_WEBHOOK = ''
        if 'DISCORD_WEBHOOK' in os.environ:
            self.DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']

    def pushTemplate(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        name = kwargs.get('name')
        # needs = kwargs.get('needs')
        token = kwargs.get('token')
        text = kwargs.get('text')
        code = kwargs.get('code')
        if not token:
            log.info(f'{name} SKIPPED')
            return False
        try:
            response = req.to_python(req.request(
                method, url, 2, params, data, json, headers).text)
            rspcode = response[text]
        except Exception as e:
            log.error(f'{name} FAILED\n{e}')
        else:
            if rspcode == code:
                log.info(f'{name} SUCCESS')
            else:
                log.error(f'{name} FAILED\n{response}')
        return True

    def custPush(self, text, status, desp):
        PUSH_CONFIG = self.PUSH_CONFIG

        if not PUSH_CONFIG:
            log.info(f'Custom Notifications SKIPPED')
            return False
        cust = req.to_python(PUSH_CONFIG)
        title = f'{text} {status}'
        if cust['show_title_and_desp']:
            title = f'{text} {status}\n\n{desp}'
        if cust['set_data_title'] and cust['set_data_sub_title']:
            cust['data'][cust['set_data_title']] = {
                cust['set_data_sub_title']: title
            }
        elif cust['set_data_title'] and cust['set_data_desp']:
            cust['data'][cust['set_data_title']] = title
            cust['data'][cust['set_data_desp']] = desp
        elif cust['set_data_title']:
            cust['data'][cust['set_data_title']] = title
        conf = [cust['url'], cust['data'], 'Custom Notifications', cust['text'], cust['code']]
        url, data, name, text, code = conf

        if cust['method'].upper() == 'GET':
            return self.pushTemplate('get', url, params=data, name=name, token='token', text=text, code=code)
        elif cust['method'].upper() == 'POST' and cust['data_type'].lower() == 'json':
            return self.pushTemplate('post', url, json=data, name=name, token='token', text=text, code=code)
        else:
            return self.pushTemplate('post', url, data=data, name=name, token='token', text=text, code=code)

    def discordWebhook(self, text, status, desp):
        DISCORD_WEBHOOK = self.DISCORD_WEBHOOK

        if not DISCORD_WEBHOOK:
            log.info(f'Discord SKIPPED')
            return False

        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=f'{text} {status}', description=desp, color='03b2f8')
        webhook.add_embed(embed)
        response = webhook.execute()
        if (response.status_code == 200):
            log.info(f'Discord SUCCESS')
        else:
            log.error(f'Discord FAILED\n{response}')
        return True

    def send(self, app='Genshin Daily Sign-In', status='', msg='', **kwargs):
        hide = kwargs.get('hide', '')
        if isinstance(msg, list) or isinstance(msg, dict):
            # msg = self.to_json(msg)
            msg = '\n\n'.join(msg)
        if not hide:
            log.info(f'Sign-In result: {status}\n\n{msg}')

        if self.PUSH_CONFIG or self.DISCORD_WEBHOOK:
            log.info('Sending push notifications...')
            self.custPush(app, status, msg)
            self.discordWebhook(app, status, msg)
        else:
            log.info('No social media notifications configured to be sent.')


if __name__ == '__main__':
    Notify().send(app='Genshin Impact Check-In Helper', status='Test Run', msg='Testing integration with social media APIs')