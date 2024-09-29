import base64
import os
import time
from cartesia import AsyncCartesia # type: ignore
from cartesia.client import OutputFormat, VoiceControls, _AsyncTTSContext # type: ignore
import asyncio
import typing
from dotenv import load_dotenv
from pydantic import BaseModel

from vocalize.queues.queues import  TTSOutputQueueDict

load_dotenv()


class CartesiaAudioOutput(BaseModel):
    audio: bytes
    context_id: str


class CartesiaWordOutput(BaseModel):
    words: list[str]
    start: list[int | float]
    end: list[int | float]
    context_id: str

class CartesiaConfig(BaseModel):
    speed: float
    positivity: typing.Literal['lowest', 'low', 'medium', 'high', 'highest'] 
    curiosity: typing.Literal['lowest', 'low', 'medium', 'high', 'highest']


    def convert_to_voice_controls(self):
        emotions = []
        if self.positivity:
            if self.positivity == 'medium':
                emotions.append("positivity")
            else:
                emotions.append(f"positivity:{self.positivity}")
        if self.curiosity:
            if self.curiosity == 'medium':
                emotions.append("curiosity")
            else:
                emotions.append(f"curiosity:{self.curiosity}")
        return VoiceControls(
            speed=self.speed,
            emotions=emotions
        )

class Cartesia:
    def __init__(
        self,
        api_key: str,
        model_id: str,
        voice_id: str,
        output_format: OutputFormat,
        config: CartesiaConfig | None = None,
        on_finished: typing.Callable[[], typing.Awaitable[None]] | None = None,
    ):
        self.client = AsyncCartesia(api_key=api_key)
        self.ws = None
        self.model_id = model_id
        self.voice_id = voice_id
        self.output_format = output_format
        self.on_finished = on_finished
        self.config = config

    async def connect(self):
        self.ws = await AsyncCartesia(
            api_key=os.environ["CARTESIA_API_KEY"]
        ).tts.websocket()
        return self.ws

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            self.ws = None
        await self.client.close()

    async def create_context(self):
        if not self.ws:
            raise Exception("Not connected to Cartesia")
        context = self.ws.context()
        return CartesiaContext(
            self.client, context, self.model_id, self.voice_id, self.output_format, config=self.config, on_finished=self.on_finished
        )

    async def synthesize(self, text: str):
        if not self.ws:
            raise Exception("Not connected to Cartesia")
        await self.ws.send(
            transcript=text,
            model_id=self.model_id,
            output_format=self.output_format,
            voice_id=self.voice_id,
        )


class CartesiaContext:
    def __init__(
        self,
        client: AsyncCartesia,
        cartesia_context: _AsyncTTSContext,
        model_id: str,
        voice_id: str,
        output_format: OutputFormat,
        config: CartesiaConfig | None = None,
        on_finished: typing.Callable[[], typing.Awaitable[None]] | None = None,
    ):
        self.client = client
        self.cartesia_context = cartesia_context
        self.model_id = model_id
        self.voice_id = voice_id
        self.config = config 
        self.output_format = output_format
        self.on_finished = on_finished
    


    async def add_text(self, text: str):
        await self.cartesia_context.send(
            transcript=text,
            model_id=self.model_id,
            output_format=self.output_format,
            voice_id=self.voice_id,
            continue_=True,
            context_id=self.cartesia_context.context_id,
            add_timestamps=True,
            _experimental_voice_controls=self.config.convert_to_voice_controls() if self.config else None
        )

    async def receive(self):
        async for output in self.cartesia_context.receive():
            # print(output)
            output = self.convert_output(output)
            yield output

    def convert_output(self, output: typing.Dict[str, typing.Any]):
        if "audio" in output:

            # audio data is a mulaw encoded byte string (it started off as base64 encoded but was decoded by the cartesia library)
            # cartesia library gives us latin-1 encoded data --- WTF!! TOOK ME HOURS TO FIGURE THIS OUT
            audio_bytes = base64.b64encode(output['audio'])
            
            return CartesiaAudioOutput(
                audio=audio_bytes, context_id=output["context_id"]
            )
        elif "word_timestamps" in output:
            word_timestamps = output["word_timestamps"]
            return CartesiaWordOutput(
                words=word_timestamps["words"],
                start=word_timestamps["start"],
                end=word_timestamps["end"],
                context_id=output["context_id"],
            )
        else:
            raise Exception("Unknown output type")

    async def finish(self):
        await self.cartesia_context.no_more_inputs()
        if self.on_finished:
            await self.on_finished()

class Interrupted:
    pass

class CartesiaStep:
    def __init__(
        self,
        input_queue: asyncio.Queue[str | Interrupted |None],
        output_queue: asyncio.Queue[TTSOutputQueueDict | None],
        is_call_connected: asyncio.Event,
        api_key: str,
        model_id: str,
        voice_id: str,
        output_format: OutputFormat,
        config: CartesiaConfig | None = None,
        on_finished: typing.Callable[[], typing.Awaitable[None]] | None = None,
        on_output: typing.Callable[[TTSOutputQueueDict], typing.Awaitable[None]] | None = None,
    ):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.is_call_connected = is_call_connected
        self.api_key = api_key
        self.model_id = model_id
        self.voice_id = voice_id
        self.output_format = output_format
        self.config = config
        self.cartesia = Cartesia(
            api_key=os.environ["CARTESIA_API_KEY"],
            model_id=model_id,
            voice_id=voice_id,
            output_format=self.output_format,
            on_finished=on_finished,
            config=self.config,
        )
        self.context: CartesiaContext | None = None
        self.on_output = on_output
        self.on_finished = on_finished
        self.is_first_word_output = True

        self.loop_task: asyncio.Task[typing.Any] | None = None

    async def sender(self, context: CartesiaContext, first_text: str):
        try:
            await context.add_text(text=first_text)

            while self.is_call_connected.is_set():
                text = await self.input_queue.get()
                print('cartesia step sender text: ', text)

                if isinstance(text, Interrupted):
                    break

                # if text is None, that represents the end of the LLM response
                if text is None:
                    await context.finish()
                    await self.output_queue.put(None)
                    break

                await context.add_text(text=text)
        except Exception as e:
            print('Cartesia step sender error: ', e)

    async def receiver(self, context: CartesiaContext):
        try:
            async for output in context.receive():
                if isinstance(output, CartesiaAudioOutput):
                    output_data = TTSOutputQueueDict({"audio": output.audio, "text": None})
                    await self.output_queue.put(output_data)
                    if self.on_output:
                        await self.on_output(output_data)
                    continue

                # is a word output
                print(f"Carteisa step receiver output.words: {output.words}")
                words = " ".join(output.words)
                if not self.is_first_word_output:
                    # words += " "
                    words = f" {words}"


                self.is_first_word_output = False
                    
                output_data = TTSOutputQueueDict({"audio": None, "text": words})
                await self.output_queue.put(output_data)
                if self.on_output:
                    await self.on_output(output_data)
            if self.on_finished:
                await self.on_finished()
        except Exception as e:
            print('Cartesia step receiver error: ', e)
    
    async def run_task(self):
        self.global_start_time = time.perf_counter()
        await self.cartesia.connect()
        print('cartesia step run_task after connect')
        while self.is_call_connected.is_set():
            print('cartesia step run_task loop')
            text = await self.input_queue.get()
            print('cartesia step start text: ', text)
            if text is None or isinstance(text, Interrupted):
                continue
            self.is_first_word_output = True
            self.start_time = time.perf_counter()
            context = await self.cartesia.create_context()
            self.context = context
            tasks = [self.sender(context, first_text=text), self.receiver(context)]
            await asyncio.gather(*tasks)
        await self.cartesia.disconnect()

    async def start(self):
        while self.is_call_connected.is_set():
            print('cartesia step start --- starting loop')
            try:
                self.loop_task = asyncio.create_task(self.run_task())
                await self.loop_task
            except asyncio.CancelledError as e:
                print('Cartesia step start cancelled error: ', e)
            #     continue
            except Exception as e:
                print('Cartesia step start error: ', e)
                continue

    async def interrupt(self):
        if self.context:
           await self.context.finish()
        if self.loop_task:
            self.loop_task.cancel()
        await self.input_queue.put(Interrupted())
        


async def main():
    output_format = OutputFormat(
        sample_rate=8000, container="raw", encoding="pcm_mulaw"
    )
    input_queue = asyncio.Queue[str | None]()
    is_call_connected = asyncio.Event()
    is_call_connected.set()
    step = CartesiaStep(
        input_queue=input_queue,
        output_queue=asyncio.Queue(),
        is_call_connected=is_call_connected,
        api_key=os.environ["CARTESIA_API_KEY"],
        model_id="sonic-english",
        voice_id="41f3c367-e0a8-4a85-89e0-c27bae9c9b6d",
        output_format=output_format,
    )
    start_task = asyncio.create_task(step.start())

    await asyncio.sleep(3)
    await input_queue.put("What are you doing later?")
    await asyncio.sleep(2)
    await input_queue.put(" Is today going to be a good day?")
    await asyncio.sleep(3)
    await input_queue.put(None)
    is_call_connected.clear()
    await start_task


if __name__ == "__main__":
    asyncio.run(main())
