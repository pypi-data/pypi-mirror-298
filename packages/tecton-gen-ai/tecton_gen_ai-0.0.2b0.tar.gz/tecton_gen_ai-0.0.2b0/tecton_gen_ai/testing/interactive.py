import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, Iterator, Optional

import ipywidgets as widgets
from IPython.display import HTML, Markdown, display

from tecton_gen_ai.agent import AgentClient
from tecton_gen_ai.utils.log import NOOP_LOGGER
import re

_WIDGET_LOGGER = ContextVar("widget_logger", default=NOOP_LOGGER)


def qna(
    client: AgentClient,
    llm: Any = None,
    system_prompt: Any = None,
    context: Any = None,
    debug: bool = True,
) -> Any:
    def _run(message: str) -> str:
        logger = get_widget_logger()
        logger.setLevel(logging.DEBUG)
        with client.set_logger(logger):
            return client.invoke_agent(
                message, llm=llm, system_prompt=system_prompt, context=context
            )

    return single_turn(_run, realtime=False, markdown=True, debug=debug)


def auto_complete(
    client: AgentClient,
    search_name: str,
    handle: Any,
    top_k: int = 5,
    debug: bool = False,
) -> Any:
    if isinstance(handle, str):

        def _handle(x):
            return x[handle]

    elif handle is None:

        def _handle(x):
            return str(x)

    else:
        _handle = handle
    return single_turn(
        lambda x: "\n".join(_handle(x) for x in client.search(search_name, x, top_k)),
        realtime=True,
        markdown=False,
        debug=debug,
    )


def chat(
    client: AgentClient, llm: Any = None, system_prompt: Any = None, debug: bool = True
) -> Any:
    chat = _Chat(client, llm, system_prompt)
    chat.display()


def single_turn(
    on_compute: Callable[[str], str],
    realtime: bool = False,
    markdown: bool = False,
    debug: bool = True,
) -> Any:
    # Create a text input widget
    text_input = widgets.Text(
        value="",
        placeholder="Type something",
        disabled=False,
        continuous_update=realtime,
        layout=widgets.Layout(
            width="90%",
            border_radius="10px",
        ),
    )

    output = widgets.Output()
    debugo = widgets.Output()

    def on_event(change):
        with output:
            if not realtime:
                output.clear_output()
                display(Markdown("Generating response..."))
        with set_widget_logger(debugo if debug else None):
            res = on_compute(change["new"])
        with output:
            output.clear_output()
            if markdown:
                display(Markdown(res))
            else:
                print(res)

    text_input.observe(on_event, names="value")

    items = [text_input, output]
    if debug:
        accordion = widgets.Accordion(children=[debugo], titles=("Debug",))
        items.append(accordion)

    vbox = widgets.VBox(items)

    # Display the text input widget
    display(vbox)


@contextmanager
def set_widget_logger(output: Optional[widgets.Output]) -> Iterator[logging.Logger]:
    if output is None:
        logger = NOOP_LOGGER
    else:
        logger = logging.getLogger("widget")
        logger.handlers.clear()
        logger.addHandler(_WidgetLogHandler(output))
        logger.propagate = False
        output.clear_output()
    token = _WIDGET_LOGGER.set(logger)
    try:
        yield logger
    finally:
        _WIDGET_LOGGER.reset(token)


def get_widget_logger() -> logging.Logger:
    return _WIDGET_LOGGER.get()


class _WidgetLogHandler(logging.Handler):
    def __init__(self, output: widgets.Output):
        super().__init__()
        self.output = output

    def emit(self, record: Any) -> None:
        with self.output:
            print(self.format(record))


class _Chat:
    def __init__(self, client: AgentClient, llm: Any = None, system_prompt: Any = None):
        self.box = widgets.Output()
        self.input = widgets.Textarea(
            value="",
            placeholder="Chat with AI",
            disabled=False,
            continuous_update=False,
            layout=widgets.Layout(width="90%"),
        )
        self.submit = widgets.Button(
            description="Submit", layout=widgets.Layout(width="100px")
        )
        hbox = widgets.HBox([self.submit, self.input])
        self.vbox = widgets.VBox([self.box, hbox])
        self.history = []
        self.llm = llm
        self.client = client
        self.system_prompt = system_prompt

    def display(self):
        display(_CSS)
        self.submit.on_click(self.on_submit)
        display(self.vbox)

    def append(self, role: str, text: str):
        import markdown

        self.history.append((role, text))
        rs = "chat_user" if role == "user" else "chat_agent"
        _text = markdown.markdown(text, extensions=["fenced_code"])
        _text = re.sub("(^<P>|</P>$)", "", _text, flags=re.IGNORECASE)
        q = (
            f'<div class="chat_outer"><div class="chat_role">{role}:'
            f'</div><div class="chat_text {rs}">{_text}</div></div>'
        )
        self.box.append_display_data(HTML(q))

    def on_submit(self, change):
        question = self.input.value
        self.input.disabled = True
        self.input.value = "Generating response ..."
        self.submit.disabled = True
        try:
            self.ask(question)
        finally:
            self.input.value = ""
            self.input.disabled = False
            self.submit.disabled = False

    def ask(self, message: str, context: Any = None):
        self.append("user", message)
        response = self.client.invoke_agent(
            message,
            llm=self.llm,
            system_prompt=self.system_prompt,
            chat_history=self.history,
            context=context,
        )
        self.append("ai", response)
        return response


_CSS = HTML(
    """<style>
.chat_outer {
  overflow: hidden;
}

.chat_role {
  width: 100px;
  float: left;
  text-align: right;
  font-weight: bold;
  padding-right: 10px;
}

.chat_text {
  overflow: auto;
}

.chat_agent {
  background-color: #f0fff0;
}

.chat_user {
  background-color: #f0f0ff;
}
</style>"""
)
