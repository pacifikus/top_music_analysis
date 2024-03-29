import luigi
import pandas as pd

import top_music_analysis.clustering as clustering
import top_music_analysis.config as config
import top_music_analysis.spotify as spotify


class GetSpotifyDataTask(luigi.Task):
    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(config.DATA_PATH)

    def run(self):
        data = spotify.get_data()
        df = spotify.to_dataframe(data)
        df.to_csv(self.output().path)


class ClusteringTask(luigi.Task):
    def requires(self):
        return GetSpotifyDataTask()

    def output(self):
        return luigi.LocalTarget(config.CLUSTERED_DATA_PATH)

    def run(self):
        with self.input().open("r") as in_file:
            df = pd.read_csv(in_file, index_col="Unnamed: 0")
            optimal_k = clustering.silhouette(df, 10)
            df["label"] = clustering.get_labels(df, optimal_k)
            df.to_csv(self.output().path)


if __name__ == "__main__":
    # luigi.run()
    luigi.build([GetSpotifyDataTask(), ClusteringTask()], local_scheduler=True)
