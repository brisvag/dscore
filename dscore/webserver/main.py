#!/usr/bin/env python3

import asyncio
import threading
from queue import Queue
from collections import defaultdict

import justpy as jp
import pandas as pd

from ..servers import sequence_disorder
from ..dscore import prepare_threads
from ..utils import pre_format_result, as_csv, as_dscore


session_data = defaultdict(dict)

button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2 block'


class SeqForm(jp.Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        seq_label = jp.Label(text='Input Sequence (fasta format):',
                             classes='block tracking-wide text-gray-700 text-xs font-bold mb-2',
                             a=self)

        jp.Textarea(placeholder='Your sequence', a=seq_label, classes='block border m-2 p-2', id='sequence')

        jp.Label(text='Servers:', classes='text-sm block', a=self)

        for server in sequence_disorder:
            label = jp.Label(text=server, a=self, classes='ml-2 mr-6 block')
            jp.Input(type='checkbox', a=label, classes='form-checkbox text-blue-500 border m-1', id=server, checked=True)

        jp.Input(value='Get DScore', type='submit', a=self, classes=button_classes, id='submit_button')

        self.on('submit', submit)


class MainPage(jp.WebPage):
    def __init__(self, request, **kwargs):
        super().__init__(classes='p-2', **kwargs)
        self.form = SeqForm(a=self)

        self.session_id = request.session_id
        # post-form stuff
        self.loading = jp.Div(a=self, show=False, classes='p-2')

        self.df = pd.DataFrame()


async def main_page(request):
    wp = MainPage(request)
    return wp


async def submit(form, msg):
    breakpoint()
    wp = msg.page

    # extract sequence and server list from form
    server_list = []
    for field in msg.form_data:
        if field.id == 'sequence':
            seq = field.value
        elif field.id in sequence_disorder and field.checked:
            server_list.append(field.id)

    # disable form and show rest
    form.show = False
    wp.loading.show = True

    session_data[msg.session_id] = {
        'seq': seq,
        'server_list': server_list,
    }
    queue.put(msg.session_id)

    results = (wp.seq, server_list, wp.df)
    jp.run_task(update_page(wp,))


async def update_page(wp, threads):
    while not_done := [thread.name for thread in threads if thread.is_alive()]:
        wp.loading.text = f'Loading... Do not close this page! Servers left: {", ".join(not_done)}.'
        await wp.update()
        await asyncio.sleep(2)

    # Done, add text and download to page
    wp.loading.text = 'Done!'

    result = pre_format_result(wp.df, wp.seq)
    session_data[wp.session_id] = result
    jp.A(a=wp, text='Download CSV', href='/make_csv', download=f'dscore.csv', classes=button_classes)
    jp.A(a=wp, text='Download DScore', href='/make_dscore', download=f'dscore.dscore', classes=button_classes)

    await wp.update()


@jp.SetRoute('/make_csv')
def make_csv(request):
    wp = jp.WebPage()
    wp.html = as_csv(session_data[request.session_id])
    return wp


@jp.SetRoute('/make_dscore')
def make_dscore(request):
    wp = jp.WebPage()
    wp.html = as_dscore(session_data[request.session_id])
    return wp


class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
async def run_queue():
    while True:
        if not queue.empty():
            sid = queue.get_nowait()
        await asyncio.sleep(2)
        worker.start


if __name__ == '__main__':
    jp.justpy(main_page)
