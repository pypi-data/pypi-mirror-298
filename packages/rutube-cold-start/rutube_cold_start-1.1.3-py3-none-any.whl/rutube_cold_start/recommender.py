import random

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .config import minimum_video_path


full_video_df = pd.read_parquet(
    minimum_video_path,
    engine="pyarrow",
    columns=[
        "title",
        "video_id",
        "description",
        "v_week_views",
        "category_id",
        "vector",
    ],
)


def get_most_similarity_videos(person_vector, video_df, N=100):
    similarity = video_df["vector"].apply(
        lambda s: cosine_similarity([person_vector], [s])
    )
    M = N * 10
    most_similarity = (
        similarity.sort_values(ascending=False)
        .head(M)
        .sample(N, random_state=42)
        .index
    )
    videos = video_df.loc[most_similarity]
    return videos


def get_popular_video(video_df, viewed_ids, N=100, popularity_criterion="v_week_views"):
    M = N * 10
    mask = video_df["video_id"].isin(viewed_ids)
    no_rp_df = video_df[~mask]
    popular_video = no_rp_df.nlargest(M, popularity_criterion)
    return popular_video.sample(N, random_state=42)


def get_recommend_in_cat(df, iters_, N=10):
    # берёт N * 10 самых схожих и берёт случайные N

    viewed_ids = [iters_[i][0] for i in range(len(iters_))]
    viewed_video = df[df["video_id"].isin(viewed_ids)]
    vector_size = 312
    person_vector = np.zeros(vector_size)
    for k, (index, v) in enumerate(viewed_video.iterrows()):
        person_vector = person_vector + v["vector"] * iters_[k][1]

    person_vector = person_vector / len(iters_)

    mask = df["video_id"].isin(viewed_ids)
    no_rp_df = df[~mask]
    similarity = no_rp_df["vector"].apply(
        lambda s: cosine_similarity([person_vector], [s])
    )

    M = N * 5
    most_similarity = (
        similarity.sort_values(ascending=False).head(M).sample(N, random_state=42)
    )
    # indexes = no_rp_df.loc[most_similarity.index]["video_id"].index
    return no_rp_df.loc[most_similarity.index]


def get_all_interests(
        video, iter_, count
):  # dataframe_videos,[video_id, inter] n-size_patch
    pool = {}
    view = {}
    gen = []
    if not iter_:
        return get_popular_video(video, [], N=count)

    for i in range(len(iter_)):
        id_ = iter_[i][0]
        it = iter_[i][1]
        meta_v = video[video["video_id"] == id_][
            ["title", "description", "category_id"]
        ].iloc[0]
        cat = meta_v["category_id"]
        pool[cat] = pool.get(cat, 0) + it
        view[cat] = view.get(cat, list())
        view[cat].append(id_)

    sort_pool = sorted(pool.items(), key=lambda x: x[1])
    metrics = {}
    pool["trash"] = 1
    categs = list(view.keys())

    for i in range(len(categs)):
        metrics[categs[i]] = metrics.get(categs[i], list())
        metrics[categs[i]].append(
            [pool[categs[i]] / len(iter_), pool[categs[i]] / len(view[categs[i]])]
        )
    for i in range(len(sort_pool)):
        if sort_pool[i][1] < 1:
            continue
        gen.extend(
            get_recommend_in_cat(
                video[video["category_id"] == sort_pool[i][0]], iter_
            ).iterrows()
        )

    rec_based_count = round(0.7 * count)

    viewed_ids = [iter_[0] for _ in range(len(iter_))]
    if len(gen) > rec_based_count:
        rec_based = random.choices(gen, k=rec_based_count)
    else:
        rec_based = gen
    rec_based = [rec_based[i][1] for i in range(len(rec_based))]
    rec_based_ids = [rec_based[i]["video_id"] for i in range(len(rec_based))]

    random_recs = get_popular_video(
        video, viewed_ids + rec_based_ids, N=count - len(rec_based)
    )

    return rec_based + [rr[1] for rr in random_recs.iterrows()]
