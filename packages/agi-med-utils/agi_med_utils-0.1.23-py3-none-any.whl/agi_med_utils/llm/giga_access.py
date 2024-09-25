import contextlib
from base64 import b64encode

from gigachat.models import Embedding
from tqdm import tqdm
from gigachat import GigaChat
import typing as t
from itertools import chain
from time import sleep
from tqdm.contrib.concurrent import process_map


class GigaChatEntryPoint:
    __slots__ = ("_creds", "_model", "_DIM", "_ZEROS", "_ERROR_MESSAGE", "_warmed_up")

    def __init__(self, client_id: str, client_secret: str, obligatory_warmup=False):
        self._creds: str = b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
        self._model = GigaChat(
            credentials=self._creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Pro',
            profanity_check=False,
        )
        self._DIM: int = 1024
        self._ZEROS: t.List[int] = [0 for _ in range(self._DIM)]
        self._ERROR_MESSAGE: str = ''
        self._warmed_up: bool = False
        if obligatory_warmup:
            self.warmup()

    def __call__(self) -> GigaChat:
        return self._model

    def get_response(self, sentence: str) -> str:
        with contextlib.suppress(Exception):
            return self._model.chat(sentence).choices[0].message.content
        return self._ERROR_MESSAGE

    def get_embedding(self, sentence: str) -> list:
        with contextlib.suppress(Exception):
            return self._model.embeddings(sentence).data[0].embedding
        return self._ZEROS

    def get_embeddings(self, sentences: t.List[str], request_limit=50) -> t.List[t.List]:
        embeddings: t.List[t.List[float]] | None = None
        counter: int = 0
        while embeddings is None and counter < request_limit:
            with contextlib.suppress(Exception):
                items: t.List[Embedding] = self._model.embeddings(sentences).data
                embeddings = [item.embedding for item in items]
                break
            sleep(0.1)
            counter += 1
        if embeddings is not None:
            return embeddings
        return [self._ZEROS for _ in sentences]

    def get_more_embeddings(
            self,
            sentences: t.List[str],
            batch_size: int = 100,
            hide_progress_bar: bool = False,
            parallel: bool = False,
    ) -> t.List[t.List]:
        batches: t.List[t.List[str]] = self.make_batches(sentences, size=batch_size)
        if not parallel:
            emb_batches = [
                self.get_embeddings(batch)
                for batch in tqdm(batches, disable=hide_progress_bar)
            ]
        else:
            emb_batches = process_map(
                self.get_embeddings,
                batches,
                chunksize=1,
                max_workers=16,
                disable=hide_progress_bar,
            )
        return list(chain.from_iterable(emb_batches))

    @staticmethod
    def make_batches(items: list, size: int = 500) -> t.List[t.List[str]]:
        slices = [
            (i * size, (i + 1) * size) for i in range(len(items) // size + 1)
        ]
        return [items[st:ed] for st, ed in slices]

    def warmup(self) -> None:
        assert (self.get_response('Прогрев') != self._ERROR_MESSAGE), 'Нет доступа к ллм!'
        assert self.get_embedding('Прогрев') != self._ZEROS, 'Нет доступа к ллм!'
        self._warmed_up = True

    def is_warmed_up(self) -> bool:
        return self._warmed_up


class GigaPlusEntryPoint(GigaChatEntryPoint):
    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)
        self.model = GigaChat(
            credentials=self._creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Plus',
            profanity_check=False,
        )
