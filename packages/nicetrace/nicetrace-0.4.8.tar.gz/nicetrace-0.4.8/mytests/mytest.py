# /// script
# dependencies = [
#   "python-dotenv"
# ]
# ///
import dotenv
import json

dotenv.load_dotenv()
from nicetrace import trace, DirWriter
from nicetrace.ext.langchain import Tracer
import langchain_openai
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic

# class MyCallback(BaseCallbackHandler):
#     def __init__(self):
#         self.running_nodes = {}
#
#     def on_llm_start(
#         self,
#         serialized: Dict[str, Any],
#         prompts: list[str],
#         *,
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         tags: Optional[list[str]] = None,
#         metadata: Optional[Dict[str, Any]] = None,
#         **kwargs: Any,
#     ) -> Any:
#         kwargs = serialized["kwargs"]
#         inputs = {}
#         if len(prompts) == 1:
#             inputs["prompt"] = prompts[0]
#         else:
#             inputs["prompts"] = prompts
#         inputs["config"] = (
#             metadata  # {"name": serialized["name"], "model_name": kwargs["model_name"], "temperature": kwargs["temperature"]}
#         )
#         pair = start_trace_block(
#             f"Query {kwargs['model_name']}", kind="query", inputs=inputs
#         )
#         self.running_nodes[run_id] = pair
#
#     def on_llm_end(
#         self,
#         response,
#         *,
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         tags: Optional[list[str]] = None,
#         **kwargs: Any,
#     ) -> None:
#         node, token = self.running_nodes.pop(run_id)
#         print(response)
#         print(response.generations)
#         generations = [g.text for gg in response.generations for g in gg]
#         if len(generations) == 1:
#             node.set_output(generations[0])
#         else:
#             node.set_output(generations)
#         end_trace_block(node, token, None)
#
#     def on_llm_error(
#         self,
#         error: BaseException,
#         *,
#         run_id: UUID,
#         parent_run_id: Optional[UUID] = None,
#         tags: Optional[list[str]] = None,
#         **kwargs: Any,
#     ) -> None:
#         node, token = self.running_nodes.pop(run_id)
#         end_trace_block(node, token, None)
#
tracer = Tracer()
try:
    with DirWriter("traces"):
        with trace("Experiment") as tt:
            # model = langchain_openai.chat_models.ChatOpenAI(
            #     model="gpt-3.5-turbo", callbacks=[Tracer()]
            # )
            # print(model.invoke("Name two colors"))
            # print(model.invoke("Name one color"))
            # model = ChatTogether(
            #     model="mistralai/Mistral-7B-Instruct-v0.3", callbacks=[tracer]
            # )
            # model = ChatTogether(
            #     model="mistralai/Mistral-7B-Instruct-v0.3", callbacks=[tracer]
            # )
            model = ChatAnthropic(model="claude-3-5-sonnet-20240620", callbacks=[tracer])

            model.invoke("Write 20 lines long poem")
            with trace("Subnode 0"):
                pass
except Exception:
    pass
print(json.dumps(tt.to_dict(), indent=2))
