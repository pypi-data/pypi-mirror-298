import logging
from typing import Generator, cast

import pytest
import torch
from PIL import Image

from colpali_engine.models import ColPali, ColPaliProcessor
from colpali_engine.utils.torch_utils import get_torch_device, tear_down_torch

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def colpali_model_name() -> str:
    return "vidore/colpali-v1.2"


@pytest.fixture(scope="module")
def colpali_from_pretrained(colpali_model_name: str) -> Generator[ColPali, None, None]:
    device = get_torch_device("auto")
    logger.info(f"Device used: {device}")

    yield cast(
        ColPali,
        ColPali.from_pretrained(
            colpali_model_name,
            torch_dtype=torch.bfloat16,
            device_map=device,
        ),
    )
    tear_down_torch()


@pytest.fixture(scope="module")
def processor(colpali_model_name: str) -> Generator[ColPaliProcessor, None, None]:
    yield cast(ColPaliProcessor, ColPaliProcessor.from_pretrained(colpali_model_name))


@pytest.mark.slow
def test_load_colpali_from_pretrained(colpali_from_pretrained: ColPali):
    assert isinstance(colpali_from_pretrained, ColPali)


@pytest.mark.slow
def test_colpali_forward_images(
    colpali_from_pretrained: ColPali,
    processor: ColPaliProcessor,
):
    # Create a batch of dummy images
    images = [
        Image.new("RGB", (32, 32), color="white"),
        Image.new("RGB", (16, 16), color="black"),
    ]

    # Process the image
    batch_images = processor.process_images(images).to(colpali_from_pretrained.device)

    # Forward pass
    with torch.no_grad():
        outputs = colpali_from_pretrained(**batch_images)

    # Assertions
    assert isinstance(outputs, torch.Tensor)
    assert outputs.dim() == 3
    batch_size, n_visual_tokens, emb_dim = outputs.shape
    assert batch_size == len(images)
    assert emb_dim == colpali_from_pretrained.dim


@pytest.mark.slow
def test_colpali_forward_queries(
    colpali_from_pretrained: ColPali,
    processor: ColPaliProcessor,
):
    queries = [
        "Is attention really all you need?",
        "Are Benjamin, Antoine, Merve, and Jo best friends?",
    ]

    # Process the queries
    batch_queries = processor.process_queries(queries).to(colpali_from_pretrained.device)

    # Forward pass
    with torch.no_grad():
        outputs = colpali_from_pretrained(**batch_queries).to(colpali_from_pretrained.device)

    # Assertions
    assert isinstance(outputs, torch.Tensor)
    assert outputs.dim() == 3
    batch_size, n_query_tokens, emb_dim = outputs.shape
    assert batch_size == len(queries)
    assert emb_dim == colpali_from_pretrained.dim
