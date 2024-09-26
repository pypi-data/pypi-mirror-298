
# シンプルなLLMインターフェース [LLM00]
# 【動作確認 / 使用例】

import sys
from relpath import add_import_path
add_import_path("../")
import LLM00

print(LLM00("ずばり簡潔に、タコの足は何本？"))	# AIへの問いかけ [LLM00]
