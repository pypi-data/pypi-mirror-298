import base64
import io
import os
import asyncio
from vocalize.conversation.built_in import Llama3Conversation
from vocalize.conversation.role import Role, Roles
from vocalize.flow.flow import Flow
from vocalize.llm.config import LLMConfig
from vocalize.llm.llm import LocalLLM
from vocalize.queues.queues import TTSOutputQueueDict
from vocalize.tts.cartesia_custom import CartesiaStep, OutputFormat
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()


class AgentFinished:
    def __init__(self) -> None:
        pass

    
    
def handle_interrupt():
    pass

audio = b""
async def handle_tts_output(output: TTSOutputQueueDict):
    # print('tts output', output)
    global audio
    if output['audio']:
        audio += output['audio']
    pass

async def test_flow():
    is_call_connected = asyncio.Event()
    is_call_connected.set()
    input_queue: asyncio.Queue[str | None] = asyncio.Queue()

    llm_config = LLMConfig(
        generation_max_tokens=20,
        turn_max_tokens=200,
        stopping_tokens=["<|eot_id|>"],
    )
    llm_port = os.environ.get("LLM_PORT", None)
    user_role = Role(name="user")
    assistant_role = Role(name="assistant")
    system_role = Role(name="system")
    roles = Roles(assistant=assistant_role, system=system_role, user=user_role)
    conversation = Llama3Conversation(roles=roles)

    llm = LocalLLM(
        protocol=os.environ["LLM_PROTOCOL"],
        config=llm_config,
        host=os.environ["LLM_HOST"],
        port=int(llm_port) if llm_port else None,
        conversation=conversation,
        slug=None,
        is_call_connected=is_call_connected,
        debug=True,
        on_finished=None
    )

    output_format = OutputFormat(container='raw', encoding='pcm_mulaw', sample_rate=8000)    

    tts_output_queue = asyncio.Queue[
            TTSOutputQueueDict | None
        ]()
    tts_input_queue: asyncio.Queue[str | None] = asyncio.Queue()
    tts_output_queue: asyncio.Queue[TTSOutputQueueDict | None] = asyncio.Queue()
    tts = CartesiaStep(
        input_queue=tts_input_queue,
        output_queue=tts_output_queue,
        is_call_connected=is_call_connected,
        api_key=os.environ["TTS_API_KEY"],
        model_id="sonic-english",
        voice_id="41f3c367-e0a8-4a85-89e0-c27bae9c9b6d",
        output_format=output_format,
        on_finished=None,
        on_output=handle_tts_output,
    )

    flow = Flow(
        input=None,
        stt=None,
        llm=llm,
        tts=tts,
        roles=conversation.roles,
        output=None,
        llm_tts_queue_max_size=2,
        tts_output_queue_max_size=1,
    )


    flow.tts.output_queue = tts_output_queue  # type: ignore
    flow.interrupter.queues.append(tts_output_queue)
    flow.interrupter.on_interrupt = handle_interrupt
    flow.llm.input_queue = input_queue

    start_task = asyncio.create_task(flow.start())

    await input_queue.put('Hey how are you doing today?')
    # await conversation.add_message(user_role, 'Hey how are you doing today?', metadata=None)
    await input_queue.put(None)

    await asyncio.sleep(1)

    await input_queue.put('I am doing great, how about you?')
    # await conversation.add_message(user_role, 'I am doing great, how about you?', metadata=None)
    await input_queue.put(None)

    await asyncio.sleep(1)
    is_call_connected.clear()
    await start_task
    # print(f'audio: {audio}')
    audio_segment = AudioSegment(data=base64.b64decode(audio), sample_width=1, frame_rate=8000, channels=1)
    # audio_segment = AudioSegment(data=audio.encode('latin-1'), sample_width=1, frame_rate=8000, channels=1)
    # audio_segment = AudioSegment.from_file(io.BytesIO(base64.b64decode(audio.decode('latin-1').encode('utf-8'))), format='mulaw')
    # audio_segment.frame_rate = 8000
    audio_segment.export('test.wav', format='wav')
    # assert False
    
    

