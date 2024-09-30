import inspect
import os
import subprocess
from threading import Thread
from time import sleep
from types import FunctionType
from typing import Callable, Any

from playwright.sync_api import PageAssertions, LocatorAssertions, APIResponseAssertions, Page, sync_playwright, \
    Playwright

with sync_playwright() as pw: pass  # workaround to run playwright in a new thread. see: https://github.com/microsoft/playwright-python/issues/1685


def main():
    playwright = sync_playwright().start()
    chrome_exe = playwright.chromium.executable_path
    print('chrome_exe =', chrome_exe)
    # start a chrome process with '--remote-debugging-port=9222 '
    # capture stderr

    proc = subprocess.Popen([chrome_exe, '--remote-debugging-port=9223', '--disable-gpu'],
                            stderr=subprocess.PIPE)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stderr_lines = []
        ws = ''
        for line in proc.stderr:
            line = line.decode('utf-8').strip()
            stderr_lines.append(line)
            if line.startswith('DevTools listening on '):
                ws = line.split(' ')[-1]
                print(f'===========chrome started, pid={proc.pid} ws={ws}')
                break
            print(f'   chrome stderr: {line}')
            if len(stderr_lines) > 10:
                print('too many lines, killing the process; no websocket found')
                return

        browser = playwright.chromium.connect_over_cdp(ws)
        print(f'context count = {len(browser.contexts)}')
        if len(browser.contexts) == 0:
            print('no context found, exiting')
            return
        context = browser.contexts[0]
        print(f'c.pages = {len(context.pages)}')
        page = context.new_page()
        page.goto('https://pyodide.org/en/stable/console.html')
        proc.wait(100)
    finally:
        proc.kill()
    return

    url = 'ws://localhost:40119/'
    browser = playwright.chromium.connect(url)
    print(f'context count = {len(browser.contexts)}')
    for c in browser.contexts:
        print(f'c.pages = {c.pages.count()}')

    browser.new_context()
    page = browser.new_page()

    page.goto('https://www.google.com')
    print(page.title())
    print(page.url)
    print(page.content()[0:1000])


if __name__ == '__main__':
    main()


def start_playwright_in_thread(url: str, headless: bool):
    def in_thread():
        start_playwright(url, headless)

    thread = Thread(target=in_thread, daemon=True)
    thread.start()


def start_playwright(url: str, headless: bool):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    playwright_setup_page_logger(page)
    page.goto(url)
    return playwright


def playwright_setup_page_logger(page: Page):
    page.on('console', lambda msg: print(f'console [{msg.type}] ==== {msg.text}'))
    sep = '\n' + ('=' * 60) + '\n'
    page.on('pageerror', lambda exc: print(f'{sep}uncaught exception through pageerror: {sep}{exc}{sep}'))


def playwright_patch_timeout() -> None:
    def PLAYWRIGHT_PATCH_TIMEOUT_MILLIS() -> int:
        timeout = 30000
        try:
            import wwwpy_user_conf
            timeout = wwwpy_user_conf.PLAYWRIGHT_PATCH_TIMEOUT_MILLIS
        except:
            pass
        return int(os.environ.get('PLAYWRIGHT_PATCH_TIMEOUT_MILLIS', f'{timeout}'))

    print(f'Using PLAYWRIGHT_PATCH_TIMEOUT, current value={PLAYWRIGHT_PATCH_TIMEOUT_MILLIS()}')

    # patch playwright assertion timeout to match our configuration
    # this is temporary solution until playwright supports setting custom timeout for assertions
    # github issue: https://github.com/microsoft/playwright-python/issues/1358

    def patch_timeout(_member_obj: FunctionType) -> Callable:
        def patch_timeout_inner(*args, **kwargs) -> Any:
            timeout_millis = PLAYWRIGHT_PATCH_TIMEOUT_MILLIS()
            parameters = inspect.signature(_member_obj).parameters
            timeout_arg_index = list(parameters.keys()).index("timeout")
            if timeout_arg_index >= 0:
                if len(args) > timeout_arg_index:
                    args = list(args)  # type: ignore
                    args[timeout_arg_index] = timeout_millis  # type: ignore
                elif 'timeout' not in kwargs:
                    kwargs["timeout"] = timeout_millis
            return _member_obj(*args, **kwargs)

        return patch_timeout_inner

    for assertion_cls in [PageAssertions, LocatorAssertions, APIResponseAssertions]:
        for member_name, member_obj in inspect.getmembers(assertion_cls):
            if isinstance(member_obj, FunctionType):
                if "timeout" in inspect.signature(member_obj).parameters:
                    setattr(assertion_cls, member_name, patch_timeout(member_obj))
