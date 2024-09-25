from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import httpx
from typing import Dict, Any
import os
import json

from optimodel_server.OptimodelError import OptimodelError
from optimodel_server.Routes import LytixProxyResponse
import logging
from optimodel_server.Config import config
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

openaiRouter = APIRouter()

OPENAI_API_URL = "https://api.openai.com/v1"


@openaiRouter.api_route("/{path:path}", methods=["POST"])
async def openai_chat_proxy(request: Request, path: str):
    # Get the request body as JSON
    body = await request.json()

    # Extract necessary parameters from the request body
    model = body.get("model")
    stream = body.get("stream", False)
    messages = []

    try:
        # Parse user and system messages
        for message in body.get("messages", []):
            role = message.get("role")
            content = message.get("content")

            if isinstance(content, list):
                # If content is a list, extract text content
                text_content = next(
                    (item["content"] for item in content if item["type"] == "text"),
                    None,
                )
                if text_content:
                    messages.append({"role": role, "text": text_content})
            elif isinstance(content, str):
                # If content is a string, add it directly
                messages.append({"role": role, "text": content})
    except Exception as e:
        logger.error(f"Error attempting to extract messages", e)

    if model is None:
        raise OptimodelError("model is required")

    # Prepare the headers for the Anthropic API call
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {request.headers.get('openaikey')}",
        **{
            k: v
            for k, v in request.headers.items()
            if k
            not in [
                "Content-Type",
                "authorization",
                "content-length",
                "host",
            ]
        },
    }

    # Remove any headers with None values
    headers = {k: str(v) for k, v in headers.items() if v is not None}

    # Construct the full path for the Anthropic API request
    full_url = f"{OPENAI_API_URL}/{path.lstrip('openai/')}"

    async def event_stream():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", full_url, json=body, headers=headers
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk

    if stream:
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(full_url, json=body, headers=headers)

        response_data = response.json()

        lytixProxyPayload = None
        try:
            # Extract model messages
            if "choices" in response_data:
                for choice in response_data["choices"]:
                    if "message" in choice:
                        message = choice["message"]
                        if "content" in message:
                            try:
                                # Attempt to parse the content as JSON
                                content_json = json.loads(message["content"])
                                if "response" in content_json:
                                    messages.append(
                                        {
                                            "role": message["role"],
                                            "text": content_json["response"],
                                        }
                                    )
                            except json.JSONDecodeError:
                                # If parsing fails, treat the content as plain text
                                messages.append(
                                    {
                                        "role": message["role"],
                                        "text": message["content"],
                                    }
                                )

            # Extract token usage
            usage = response_data.get("usage", {})
            input_tokens = usage.get("prompt_tokens")
            output_tokens = usage.get("completion_tokens")

            # Now attempt to calculate cost based on the model
            modelData = config.modelToProvider.get(
                model.lower().replace("-", "_"), None
            )

            # Get the first openai provider
            modelData = next((x for x in modelData if x["provider"] == "openai"), None)

            cost = None
            if modelData is not None:
                cost = modelData["pricePer1MInput"] * (
                    input_tokens / 1_000_000
                ) + modelData["pricePer1MOutput"] * (output_tokens / 1_000_000)
            lytixProxyPayload = LytixProxyResponse(
                messages=messages,
                inputTokens=input_tokens,
                outputTokens=output_tokens,
                cost=cost,
            ).dict()
        except Exception as e:
            logger.error(f"Error attempting to extract usage tokens", e)

        return Response(
            content=json.dumps(
                {
                    "lytix-proxy-payload": lytixProxyPayload,
                    **response_data,
                }
            ),
            status_code=response.status_code,
            media_type="application/json",
        )


@openaiRouter.api_route("/{path:path}", methods=["GET"])
async def openai_get_proxy(request: Request, path: str):
    """
    Blindly forward and get requests, dont intercept anything just proxy
    """
    # Construct the full URL for the Anthropic API request
    full_url = f"{OPENAI_API_URL}/{path}"

    # Prepare the headers for the Anthropic API call
    headers = {
        "X-API-Key": request.headers.get("openaiApiKey"),
        "anthropic-version": "2023-06-01",
        **{
            k: v
            for k, v in request.headers.items()
            if k.lower() not in ["host", "content-length"]
        },
    }

    # Remove any headers with None values
    headers = {k: v for k, v in headers.items() if v is not None}

    # Get query parameters
    params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        response = await client.get(full_url, headers=headers, params=params)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
