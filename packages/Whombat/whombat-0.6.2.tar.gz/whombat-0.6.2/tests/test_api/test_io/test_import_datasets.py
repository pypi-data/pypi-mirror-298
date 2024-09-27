from pathlib import Path

from soundevent import data, io
from sqlalchemy.ext.asyncio import AsyncSession

from whombat.api.io.aoef.datasets import import_dataset


async def test_can_import_a_dataset_with_user_without_email(
    audio_dir: Path,
    random_wav_factory,
    session: AsyncSession,
):
    path = random_wav_factory()

    recording = data.Recording.from_file(
        path,
        owners=[data.User(name="Test user")],
    )

    dataset = data.Dataset(
        name="Test dataset",
        description="Test description",
        recordings=[recording],
    )

    aoef_file = "test_dataset.aoef"
    io.save(dataset, audio_dir / aoef_file, audio_dir=audio_dir)

    imported = await import_dataset(
        session,
        audio_dir / aoef_file,
        dataset_dir=audio_dir,
        audio_dir=audio_dir,
    )

    assert imported.name == dataset.name
