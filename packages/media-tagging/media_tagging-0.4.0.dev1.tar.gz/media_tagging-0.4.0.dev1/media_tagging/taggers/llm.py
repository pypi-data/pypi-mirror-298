# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for performing media tagging with LLMs."""

import base64
import dataclasses
import enum
import json
import logging
import tempfile
import time
from typing import Final

import google.generativeai as google_genai
import langchain_google_genai as genai
from langchain_core import (
  language_models,
  output_parsers,
  prompts,
  runnables,
)
from typing_extensions import override

from media_tagging.taggers import base

_MAX_NUMBER_LLM_TAGS: Final[int] = 10


class LLMTaggerTypeEnum(enum.Enum):
  """Enum for selecting of type of LLM tagging."""

  STRUCTURED = 1
  UNSTRUCTURED = 2
  DESCRIPTION = 3


_HUMAN_INSTRUCTIONS = (
  'human',
  [
    {
      'type': 'image_url',
      'image_url': {'url': 'data:image/jpeg;base64,{image_data}'},
    }
  ],
)

_UNSTRUCTURED_PROMPT: Final[prompts.ChatPromptTemplate] = (
  prompts.ChatPromptTemplate.from_messages(
    [
      ('system', 'Generate {n_tags} tags for the image, {format_instructions}'),
      _HUMAN_INSTRUCTIONS,
    ]
  )
)

_UNSTRUCTURED_PROMPT_VIDEO: Final[str] = (
  'Generate {n_tags} tags for the following video.'
)
_STRUCTURED_PROMPT: Final[prompts.ChatPromptTemplate] = (
  prompts.ChatPromptTemplate.from_messages(
    [
      (
        'system',
        'Find whether the following tags can be found in the image: {tags}.'
        ' {format_instructions}',
      ),
      _HUMAN_INSTRUCTIONS,
    ]
  )
)

_STRUCTURED_PROMPT_VIDEO: Final[str] = (
  'Find whether the following tags can be found in the video: {tags}.'
)


_DESCRIPTION_PROMPT: Final[prompts.ChatPromptTemplate] = (
  prompts.ChatPromptTemplate.from_messages(
    [
      (
        'system',
        'Describe the following image.' ' {format_instructions}',
      ),
      _HUMAN_INSTRUCTIONS,
    ]
  )
)

_DESCRIPTION_PROMPT_VIDEO: Final[str] = 'Describe the following video.'

llm_tagger_promps: dict[LLMTaggerTypeEnum, prompts.ChatPromptTemplate] = {
  LLMTaggerTypeEnum.UNSTRUCTURED: _UNSTRUCTURED_PROMPT,
  LLMTaggerTypeEnum.STRUCTURED: _STRUCTURED_PROMPT,
  LLMTaggerTypeEnum.DESCRIPTION: _DESCRIPTION_PROMPT,
}

video_llm_tagger_promps: dict[LLMTaggerTypeEnum, str] = {
  LLMTaggerTypeEnum.UNSTRUCTURED: _UNSTRUCTURED_PROMPT_VIDEO,
  LLMTaggerTypeEnum.STRUCTURED: _STRUCTURED_PROMPT_VIDEO,
  LLMTaggerTypeEnum.DESCRIPTION: _DESCRIPTION_PROMPT_VIDEO,
}


class LLMTagger(base.BaseTagger):
  """Tags media via LLM."""

  def __init__(
    self,
    llm_tagger_type: LLMTaggerTypeEnum,
    llm: language_models.BaseLanguageModel,
  ) -> None:
    """Initializes LLMTagger based on selected LLM."""
    self.llm_tagger_type = llm_tagger_type
    self.llm = llm
    self.output_object = (
      base.Description
      if llm_tagger_type == LLMTaggerTypeEnum.DESCRIPTION
      else base.Tag
    )

  @property
  def prompt(self) -> prompts.ChatPromptTemplate:
    """Builds correct prompt to send to LLM.

    Prompt contains format instructions to get output result.
    """
    return llm_tagger_promps[self.llm_tagger_type]

  @property
  def output_parser(self) -> output_parsers.BaseOutputParser:
    """Defines how LLM response should be formatted."""
    return output_parsers.JsonOutputParser(pydantic_object=self.output_object)

  @property
  def chain(self) -> runnables.base.RunnableSequence:  # noqa: D102
    return self.prompt | self.llm | self.output_parser

  def invocation_parameters(
    self, image_data: str, tagging_options: base.TaggingOptions
  ) -> dict[str, str]:
    """Prepares necessary parameters for chain invocation.

    Args:
      image_data: Base64 encoded image.
      tagging_options: Parameters to refine the tagging results.

    Returns:
      Necessary parameters to be invoke by the chain.
    """
    parameters = {
      'image_data': image_data,
      'format_instructions': self.output_parser.get_format_instructions(),
    }
    if n_tags := tagging_options.n_tags:
      parameters['n_tags'] = n_tags
    if tags := tagging_options.tags:
      parameters['tags'] = ', '.join(tags)
    return parameters

  @override
  def tag(
    self,
    name: str,
    content: bytes,
    tagging_options: base.TaggingOptions = base.TaggingOptions(
      n_tags=_MAX_NUMBER_LLM_TAGS
    ),
  ) -> base.TaggingResult:
    logging.debug('Tagging image "%s" with LLMTagger', name)
    image_data = base64.b64encode(content).decode('utf-8')
    result = self.chain.invoke(
      self.invocation_parameters(image_data, tagging_options)
    )
    if self.llm_tagger_type == LLMTaggerTypeEnum.DESCRIPTION:
      return base.TaggingResult(
        identifier=name,
        type='image',
        content=base.Description(text=result.get('text')),
      )
    tags = [base.Tag(name=r.get('name'), score=r.get('score')) for r in result]
    return base.TaggingResult(identifier=name, type='image', content=tags)


class GeminiImageTagger(LLMTagger):
  """Tags image based on Gemini."""

  def __init__(
    self,
    tagger_type: LLMTaggerTypeEnum,
    model_name: str = 'models/gemini-1.5-flash',
  ) -> None:
    """Initializes GeminiImageTagger.

    Args:
      tagger_type: Type of LLM tagger.
      model_name: Name of the model to perform the tagging.
    """
    super().__init__(
      llm_tagger_type=tagger_type,
      llm=genai.ChatGoogleGenerativeAI(model=model_name),
    )


class GeminiVideoTagger(LLMTagger):
  """Tags video based on Gemini."""

  def __init__(
    self,
    tagger_type: LLMTaggerTypeEnum,
    model_name: str = 'models/gemini-1.5-flash',
  ) -> None:
    """Initializes GeminiVideoTagger.

    Args:
      tagger_type: Type of LLM tagger.
      model_name: Name of the model to perform the tagging.
    """
    self.llm_tagger_type = tagger_type
    self.model_name = model_name

  @property
  def model(self) -> google_genai.GenerativeModel:
    """Initializes GenerativeModel."""
    return google_genai.GenerativeModel(model_name=self.model_name)

  @override
  def tag(
    self,
    name: str,
    content: bytes,
    tagging_options: base.TaggingOptions = base.TaggingOptions(),
  ):
    logging.debug('Tagging video "%s" with GeminiVideoTagger', name)
    with tempfile.NamedTemporaryFile(suffix='.mp4') as f:
      f.write(content)
      try:
        video_file = google_genai.upload_file(f.name)
        while video_file.state.name == 'PROCESSING':
          print('.', end=' ')
          time.sleep(5)
          video_file = google_genai.get_file(video_file.name)

        result = self.model.generate_content(
          [
            video_file,
            '\n\n',
            f'{self.format_prompt(tagging_options)} ',
          ],
          generation_config=google_genai.GenerationConfig(
            response_mime_type='application/json',
            response_schema=self.response_schema,
          ),
        )
      finally:
        video_file.delete()

      if self.llm_tagger_type == LLMTaggerTypeEnum.DESCRIPTION:
        return base.TaggingResult(
          identifier=name,
          type='video',
          content=base.Description(text=json.loads(result.text).get('text')),
        )
      tags = [
        base.Tag(name=r.get('name'), score=r.get('score'))
        for r in json.loads(result.text)
      ]
      return base.TaggingResult(identifier=name, type='video', content=tags)

  def format_prompt(self, tagging_options: base.TaggingOptions) -> str:
    """Builds correct prompt to send to LLM.

    Prompt contains format instructions to get output result.

    Args:
      tagging_options: Parameters to refine the prompt.

    Returns:
      Formatted prompt.
    """
    base_prompt = video_llm_tagger_promps[self.llm_tagger_type]
    formatting_instructions = (
      ' For each tag provide name and a score from 0 to 1 '
      'where 0 is tag absence and 1 complete tag presence.'
    )
    prompt = base_prompt.format(**dataclasses.asdict(tagging_options))
    if self.llm_tagger_type == LLMTaggerTypeEnum.DESCRIPTION:
      return prompt
    return prompt + formatting_instructions

  @property
  def response_schema(self) -> list[base.Tag] | base.Description:
    """Generates correct response schema based on type of LLM tagger."""
    return (
      base.Description
      if self.llm_tagger_type == LLMTaggerTypeEnum.DESCRIPTION
      else list[base.Tag]
    )
