import asyncio
from uuid import UUID

from .recommender import full_video_df, get_all_interests


def recommend(
    interaction_history: list[tuple[UUID, int]],
    count: int = 10,
) -> list[UUID]:
    """
        Synchronously predict the best recommendations for given ``interaction_history``

        Args:
            interaction_history: list of ``(UUID, int)`` pairs, where ``UUID`` is the video id,
                and ``int`` is the reaction (``1`` - like, ``-1`` - dislike, ``0`` - neutral)
            count: number of recommended videos

        Returns:
            UUIDs of recommended videos
    """
    interaction_history = [(str(pair[0]), pair[1]) for pair in interaction_history]

    recommendations = get_all_interests(full_video_df, interaction_history, count)

    recommended_ids = [rec["video_id"] for rec in recommendations]

    return [UUID(recommendation) for recommendation in recommended_ids]


async def recommend_async(
    interaction_history: list[tuple[UUID, int]],
    count: int = 10,
) -> list[UUID]:
    """
        Asynchronous wrapper around the ``recommend`` function

        Args:
            interaction_history: list of ``(UUID, int)`` pairs, where ``UUID`` is the video id,
                and ``int`` is the reaction (``1`` - like, ``-1`` - dislike, ``0`` - neutral)
            count: number of recommended videos

        Returns:
            UUIDs of recommended videos
    """
    return await asyncio.to_thread(recommend, interaction_history, count)
