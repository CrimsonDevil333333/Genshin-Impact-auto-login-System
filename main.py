import os

from modules.settings import log, CONFIG
from modules.sign import Sign
from modules.notify import Notify


if __name__ == '__main__':
    log.info(f'Genshin Impact Check-In Helper v{CONFIG.GIH_VERSION}')
    log.info('If you fail to check in, please try to update!')

    notify = Notify()
    msg_list = []
    ret = success_num = fail_num = 0
  
#################  Add cookie ###########################

    OS_COOKIE = '' # add your cookie here !
    token = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'

#########################################################   

    cookie_list = OS_COOKIE.split('#')
    log.info(f'Number of account cookies read: {len(cookie_list)}')
    for i in range(len(cookie_list)):
        log.info(f'Preparing NO.{i + 1} Account Check-In...')
        try:
            #ltoken = cookie_list[i].split('ltoken=')[1].split(';')[0]
            token = cookie_list[i].split('cookie_token=')[1].split(';')[0]
            msg = f'	NO.{i + 1} Account:{Sign(cookie_list[i]).run()}'
            msg_list.append(msg)
            success_num = success_num + 1
        except Exception as e:
            if not token:
                log.error("Cookie token not found, please try to relog on the check-in page.")

            msg = f'	NO.{i + 1} Account:\n    {e}'
            msg_list.append(msg)
            fail_num = fail_num + 1
            log.error(msg)
            ret = -1
        continue
    notify.send(status=f'\n  -Number of successful sign-ins: {success_num} \n  -Number of failed sign-ins: {fail_num}', msg=msg_list)
    if ret != 0:
        log.error('program terminated with errors')
        exit(ret)
    log.info('exit success')