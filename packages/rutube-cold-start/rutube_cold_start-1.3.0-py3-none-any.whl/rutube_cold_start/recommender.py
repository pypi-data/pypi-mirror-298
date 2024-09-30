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
    similarity = cosine_similarity([person_vector],
                                   video_df["vector"].to_list())[0]

    M = N * 10
    most_similarity = np.random.choice(np.argpartition(similarity, -M)[-M:], size=N, replace=False)

    return video_df.loc[most_similarity]


def get_popular_video(video_df, viewed_ids, bad_categories=None, N=100, popularity_criterion="v_week_views"):
    M = N * 10
    mask = video_df["video_id"].isin(viewed_ids)
    no_rp_df = video_df[~mask]
    if bad_categories is not None:
        no_rp_df = no_rp_df[~(no_rp_df["category_id"].isin(bad_categories))]
    popular_video = no_rp_df.nlargest(M, popularity_criterion)
    return [row[1] for row in popular_video.sample(N).iterrows()]


def get_recommend_in_cat(df, iters_, N=10):
    # берёт N * 10 самых схожих и берёт случайные N

    viewed_ids = [iter[0] for iter in iters_]
    viewed_mask = df["video_id"].isin(viewed_ids)
    viewed_video = df[viewed_mask]
    vector_size = 312
    person_vector = np.zeros(vector_size)
    for k, (index, v) in enumerate(viewed_video.iterrows()):
        person_vector = person_vector + v["vector"] * iters_[k][1]

    person_vector = person_vector / len(iters_)

    no_rp_df = df[~viewed_mask].reset_index(drop=True)


    similarity = cosine_similarity([person_vector],
                                   no_rp_df["vector"].to_list())[0]

    M = N * 5
    most_similarity = np.random.choice(np.argpartition(similarity, -M)[-M:], size=N, replace=False)

    # indexes = no_rp_df.loc[most_similarity.index]["video_id"].index
    return no_rp_df.loc[most_similarity]


def get_all_interests(
        video, iter_, count
):  # dataframe_videos,[video_id, inter] n-size_patch
    pool = {}
    view = {}
    gen = []
    if not iter_:
        return get_popular_video(video, [], N=count, bad_categories=[])

    for iteraction in iter_:
        id_ = iteraction[0]
        it  = iteraction[1]
        meta_v = video[video["video_id"] == id_][
            ["title", "description", "category_id"]
        ].iloc[0]
        cat = meta_v["category_id"]
        pool[cat] = pool.get(cat, 0) + it
        view[cat] = view.get(cat, list())
        view[cat].append(id_)

    sort_pool = sorted(pool.items(), key=lambda x: x[1])
    bad_categories = [cat[0] for cat in sort_pool if cat[1] < 0]
    metrics = {}
    pool["trash"] = 1
    categs = list(view.keys())

    for categ in categs:
        metrics[categ] = metrics.get(categ, list())
        metrics[categ].append(
            [pool[categ] / len(iter_), pool[categ] / len(view[categ])]
        )

    for el_sort_pool in sort_pool:
        if el_sort_pool[1] < 1:
            continue
        gen.extend(
            get_recommend_in_cat(
                video[video["category_id"] == el_sort_pool[0]], iter_
            ).iterrows()
        )

    rec_based_count = round(0.7 * count)

    viewed_ids = [iter_[0]] * len(iter_)
    if len(gen) > rec_based_count:
        rec_based = random.choices(gen, k=rec_based_count)
    else:
        rec_based = gen
    rec_based = [i[1] for i in rec_based]
    rec_based_ids = [i["video_id"] for i in rec_based]

    random_recs = get_popular_video(
        video, viewed_ids + rec_based_ids, N=count - len(rec_based), bad_categories=bad_categories
    )

    return rec_based + random_recs
