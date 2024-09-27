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
"""Provides HTTP endpoint for media tagging."""

import logging

import fastapi
from typing_extensions import TypedDict

from media_tagging import tagger, utils
from media_tagging.tagger import base as base_tagger

taggers: dict[str, base_tagger.BaseTagger] = {}
app = fastapi.FastAPI()


class MediaPostRequest(TypedDict):
  """Specifies structure of request for tagging media.

  Attributes:
    tagger_type: Type of tagger.
    media_url: Local or remote URL of media.
  """

  media_url: str
  tagger_type: str
  tagging_parameters: dict[str, int | list[str]]


@app.post('/tagger/llm')
async def tag_with_llm(
  data: MediaPostRequest = fastapi.Body(embed=True),
) -> dict[str, str]:
  """Performs media tagging via LLMs.

  Args:
    data: Post request for media tagging.

  Returns:
    Json results of tagging.
  """
  return process_post_request(data)


@app.post('/tagger/api')
async def tag_with_api(
  data: MediaPostRequest = fastapi.Body(embed=True),
) -> dict[str, str]:
  """Performs media tagging via Google Cloud APIs.

  Args:
    data: Post request for media tagging.

  Returns:
    Json results of tagging.
  """
  return process_post_request(data)


def process_post_request(
  data: MediaPostRequest,
) -> fastapi.responses.JSONResponse:
  """Helper method for performing tagging.

  Args:
    data: Post request for media tagging.

  Returns:
    Json results of tagging.
  """
  tagger_type = data.get('tagger_type')
  if not (concrete_tagger := taggers.get(tagger_type)):
    concrete_tagger = tagger.create_tagger(tagger_type)
    taggers[tagger_type] = concrete_tagger
  if media_url := data.get('media_url'):
    media_name = utils.convert_path_to_media_name(media_url)
    media_bytes = utils.read_media_as_bytes(media_url)
    logging.info('Processing media: %s', media_url)
    tagging_options = base_tagger.TaggingOptions(
      **data.get('tagging_parameters')
    )
    tagging_result = concrete_tagger.tag(
      name=media_name, content=media_bytes, tagging_options=tagging_options
    )
    return fastapi.responses.JSONResponse(
      content=fastapi.encoders.jsonable_encoder(tagging_result.dict())
    )
  raise ValueError('No path to media is provided.')
